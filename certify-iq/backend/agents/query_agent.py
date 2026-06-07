import json
from .base_agent import BaseAgent


class QueryAgent(BaseAgent):
    name = "Natural Language Query"
    foundry_queries = [
        ("certification requirements learning path", "certification-guide"),
        ("employee performance skills assessment", "skills-matrix"),
        ("intervention risk certification", "intervention"),
    ]

    def run(self, input_data: dict, docs: list) -> dict:
        question = input_data.get("question", "")
        all_employees = input_data.get("all_employees", [])

        context = "\n\n".join(f"**{d['title']}**\n{d['content']}" for d in docs)
        citations = [d["citation"] for d in docs]

        emp_summary = json.dumps([
            {
                "id": e.get("id"),
                "name": e.get("name"),
                "role": e.get("role"),
                "cert": e.get("certification_target"),
                "score": e.get("current_practice_score"),
                "weeks": e.get("weeks_until_exam"),
                "meetings": e.get("meeting_hours_per_week"),
                "hours_studied": e.get("hours_studied"),
            }
            for e in all_employees
        ], indent=2)

        system_prompt = f"""You are CertifyIQ's natural language intelligence layer.
You answer questions about workforce certification readiness based on real employee data
and knowledge from Azure AI Foundry IQ.

Rules:
- Be specific: reference actual employee names, scores, and percentages
- Every recommendation must cite its source as [Source: title]
- If asking about risk: identify the specific highest-risk employee with evidence
- If asking about budget/cost: calculate actual dollar amounts
- Keep answers concise (2-4 sentences) and actionable
- End with a specific recommended action

Employee data:
{emp_summary}

Knowledge sources:
{context}

Respond with a JSON object with fields:
- answer: string (concise, specific, data-backed)
- relevant_employees: array of employee IDs mentioned
- action: string (specific next step)
- confidence: float 0-1"""

        gpt_response = self._call_gpt(
            system_prompt=system_prompt,
            user_prompt=f"Question: {question}",
        )

        # Parse GPT response
        answer = gpt_response
        relevant_employees: list = []
        action = "Run analysis on the relevant employee to get detailed recommendations."
        confidence = 0.8

        try:
            if "{" in gpt_response:
                start = gpt_response.index("{")
                end = gpt_response.rindex("}") + 1
                parsed = json.loads(gpt_response[start:end])
                answer = parsed.get("answer", gpt_response)
                relevant_employees = parsed.get("relevant_employees", [])
                action = parsed.get("action", action)
                confidence = float(parsed.get("confidence", 0.8))
        except Exception:
            # Use raw response as answer
            pass

        # Fallback rule-based answers for common questions
        if not answer or "[GPT unavailable" in answer or (answer == gpt_response and len(gpt_response) > 500):
            answer = self._rule_based_answer(question, all_employees)
            relevant_employees = self._extract_relevant(question, all_employees)
            confidence = 0.75

        return {
            "question": question,
            "answer": answer,
            "relevant_employees": relevant_employees,
            "action": action,
            "citations": citations,
            "confidence": confidence,
            "summary": f"Query answered · {len(relevant_employees)} employees referenced · {confidence:.0%} confidence",
        }

    def _rule_based_answer(self, question: str, employees: list) -> str:
        q = question.lower()

        # Sort by risk: lowest score + highest meeting load
        ranked = sorted(
            employees,
            key=lambda e: (e.get("current_practice_score", 100), -e.get("meeting_hours_per_week", 0))
        )

        if "risk" in q or "at risk" in q:
            emp = ranked[0] if ranked else None
            if emp:
                return (
                    f"{emp.get('name')} ({emp.get('id')}) is at highest risk. "
                    f"{emp.get('current_practice_score')}% practice score, "
                    f"{emp.get('meeting_hours_per_week')}h/week meeting load, "
                    f"exam in {emp.get('weeks_until_exam')} weeks. "
                    f"Immediate intervention recommended. [Source: Intervention Best Practices]"
                )

        if "budget" in q or "cost" in q or "exposure" in q:
            not_yet = [e for e in employees if e.get("current_practice_score", 100) < 55]
            total_risk = len(not_yet) * (165 + 2400)
            return (
                f"With {len(not_yet)} employee(s) below 55% readiness, your team faces "
                f"${total_risk:,} in exam + productivity costs without intervention. "
                f"CertifyIQ estimates ${len(not_yet) * 940:,} savings with guided preparation. "
                f"[Source: Certification ROI & Cost Analysis]"
            )

        if "soonest" in q or "exam" in q and "schedule" in q:
            sorted_by_exam = sorted(employees, key=lambda e: e.get("weeks_until_exam", 99))
            emp = sorted_by_exam[0] if sorted_by_exam else None
            if emp:
                return (
                    f"{emp.get('name')} has the nearest exam: {emp.get('weeks_until_exam')} weeks, "
                    f"{emp.get('certification_target')} certification, "
                    f"current score {emp.get('current_practice_score')}%. "
                    f"{'Ready — maintain pace.' if emp.get('current_practice_score', 0) >= 75 else 'Needs 2-week focused sprint before exam.'} "
                    f"[Source: Study Schedule Templates]"
                )

        return (
            "Based on current team data, I can provide specific readiness analysis. "
            "Try asking: 'Who is most at risk?' or 'What is our budget exposure?' "
            "[Source: CertifyIQ Knowledge Base]"
        )

    def _extract_relevant(self, question: str, employees: list) -> list:
        ids = []
        for emp in employees:
            if emp.get("name", "").lower() in question.lower():
                ids.append(emp["id"])
        return ids