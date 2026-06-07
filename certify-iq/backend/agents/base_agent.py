import os
import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from openai import OpenAI
from audit.audit_logger import audit_logger
from responsible_ai.guardrails import guardrails, TRANSPARENCY_NOTE
from evaluation.agent_evaluator import evaluator
from foundry.knowledge_retriever import retriever


class BaseAgent(ABC):
    name: str = "Base Agent"
    foundry_queries: list = []

    def __init__(self):
        self._client = None  # Lazy-initialized — only created when _call_gpt is used
        self._model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-4o")

    def _get_client(self):
        if self._client is None:
            github_token = os.getenv("GITHUB_TOKEN", "")
            if github_token:
                self._client = OpenAI(
                    base_url="https://models.inference.ai.azure.com",
                    api_key=github_token,
                )
            else:
                self._client = OpenAI(
                    base_url="https://models.inference.ai.azure.com",
                    api_key="no-token",
                )
        return self._client

    @abstractmethod
    def run(self, input_data: dict, docs: list) -> dict:
        """Core agent logic. Receives employee data + retrieved docs. Returns result dict."""

    def execute(self, input_data: dict, loop_iteration: int = 1) -> dict:
        audit_id = str(uuid.uuid4())
        t_start = datetime.now(timezone.utc)
        ms_start = time.monotonic()
        employee_id = input_data.get("id", "unknown")

        # Validate only core employee fields (not accumulated pipeline context)
        # to avoid Rule 4 (max 2000 chars) false positives as context grows.
        CORE_FIELDS = {"id", "name", "role", "certification_target", "current_practice_score",
                       "hours_studied", "weeks_until_exam", "focus_hours_per_week",
                       "meeting_hours_per_week", "starting_score", "team_id"}
        core_data = {k: v for k, v in input_data.items() if k in CORE_FIELDS}
        rai_input = guardrails.validate_input(str(core_data))
        if not rai_input["safe"]:
            return self._blocked_response(rai_input["reason"], loop_iteration)

        all_docs = []
        citations = []
        query_sent = ""
        for query, category in self.foundry_queries:
            query_sent = query if not query_sent else query_sent
            docs = retriever.retrieve(query, category=category, top_k=3)
            all_docs.extend(docs)
            citations.extend(d["citation"] for d in docs)
        citations = list(dict.fromkeys(citations))

        result = self.run(input_data, all_docs)

        t_end = datetime.now(timezone.utc)
        latency_ms = int((time.monotonic() - ms_start) * 1000)

        response_text = str(result)
        rai_output = guardrails.validate_output(response_text)
        bias = guardrails.check_bias(result.get("citations", citations))

        eval_score = evaluator.score(
            agent_name=self.name,
            response=response_text,
            query=query_sent,
            citations=citations,
            latency_ms=latency_ms,
            grounding_verified=rai_output.get("grounding_verified", False),
        )
        eval_grade = evaluator.grade(eval_score)

        audit_entry = {
            "audit_id": audit_id,
            "timestamp_start": t_start.isoformat(),
            "timestamp_end": t_end.isoformat(),
            "agent_name": self.name,
            "employee_id": employee_id,
            "query_sent_to_foundry": query_sent,
            "docs_retrieved": len(all_docs),
            "doc_titles": [d["title"] for d in all_docs],
            "prompt_length_chars": len(str(input_data)),
            "response_length_chars": len(response_text),
            "latency_ms": latency_ms,
            "eval_score": eval_score,
            "responsible_ai_check": "PASS" if rai_output["safe"] else "FAIL",
            "citations": citations,
            "loop_iteration": loop_iteration,
        }
        audit_logger.log(audit_entry)

        return {
            "agent_name": self.name,
            "status": "success",
            "timestamp": t_end.isoformat(),
            "latency_ms": latency_ms,
            "foundry_iq": {
                "docs_retrieved": len(all_docs),
                "citations": citations,
                "grounded_by": "Azure AI Foundry IQ",
                "index": os.getenv("AZURE_SEARCH_INDEX", "learning-knowledge"),
            },
            "evaluation": {
                "score": eval_score,
                "grade": eval_grade,
            },
            "responsible_ai": {
                "input_check": "PASS" if rai_input["safe"] else "FAIL",
                "output_check": "PASS" if rai_output["safe"] else "FAIL",
                "bias_check": "PASS" if not bias["bias_detected"] else "FAIL",
                "transparency_note": TRANSPARENCY_NOTE,
            },
            "result": result,
            "loop_iteration": loop_iteration,
        }

    def _blocked_response(self, reason: str, loop_iteration: int) -> dict:
        return {
            "agent_name": self.name,
            "status": "guardrail_blocked",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency_ms": 0,
            "foundry_iq": {"docs_retrieved": 0, "citations": [], "grounded_by": "Azure AI Foundry IQ", "index": "learning-knowledge"},
            "evaluation": {"score": 0.0, "grade": "NEEDS_REVIEW"},
            "responsible_ai": {"input_check": "FAIL", "output_check": "N/A", "bias_check": "N/A", "transparency_note": TRANSPARENCY_NOTE},
            "result": {"error": f"Guardrail blocked: {reason}"},
            "loop_iteration": loop_iteration,
        }

    def _call_gpt(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self._get_client().chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=1000,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[GPT unavailable — using structured fallback. Error: {str(e)[:80]}]"
