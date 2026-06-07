import json
from .base_agent import BaseAgent


class LearningPathCurator(BaseAgent):
    name = "Learning Path Curator"

    def __init__(self):
        super().__init__()

    def _get_queries(self, certification: str, role: str) -> list:
        return [
            (f"{certification} certification guide", "certification-guide"),
            (f"{role} skills matrix", "skills-matrix"),
        ]

    def run(self, input_data: dict, docs: list) -> dict:
        cert = input_data.get("certification_target", "AZ-204")
        role = input_data.get("role", "Software Engineer")
        self.foundry_queries = self._get_queries(cert, role)

        context = "\n\n".join(f"**{d['title']}**\n{d['content']}" for d in docs)
        citations = [d["citation"] for d in docs]

        system_prompt = f"""You are the Learning Path Curator agent for CertifyIQ,
an enterprise certification management system.

Your role: Recommend a precise, actionable learning path
using ONLY the grounded knowledge sources provided below.

Rules:
- Every recommendation MUST cite its source as [Source: title]
- Never invent statistics, pass rates, or time estimates
- Be specific: name exact topics, exact hours, exact milestones
- If sources don't cover a topic, say so explicitly
- Output must be actionable by a busy professional

Employee context: {json.dumps(input_data)}

Knowledge sources:
{context}

Respond with a JSON object with fields: summary, learning_path (array of objects with topic/hours/priority), total_hours, prerequisites."""

        gpt_response = self._call_gpt(
            system_prompt=system_prompt,
            user_prompt=f"Create a learning path for {cert} certification for a {role}.",
        )

        learning_path = self._default_path(cert)
        try:
            parsed = json.loads(gpt_response) if gpt_response.startswith("{") else {}
            if parsed.get("learning_path"):
                learning_path = parsed["learning_path"]
        except Exception:
            pass

        total_hours = sum(t.get("hours", 0) for t in learning_path)
        for item in learning_path:
            if "[Source:" not in item.get("topic", ""):
                item["citation"] = citations[0] if citations else "[Source: Engineering Certification Guide]"

        return {
            "certification": cert,
            "learning_path": learning_path,
            "total_hours": total_hours,
            "prerequisites": self._prerequisites(cert),
            "citations": citations,
            "summary": f"{len(learning_path)}-topic learning path, {total_hours}hrs total",
        }

    def _default_path(self, cert: str) -> list:
        paths = {
            "AZ-204": [
                {"topic": "Azure App Service & Compute", "hours": 8, "priority": "HIGH"},
                {"topic": "Azure Storage Solutions", "hours": 6, "priority": "HIGH"},
                {"topic": "Azure Security & Key Vault", "hours": 7, "priority": "HIGH"},
                {"topic": "Azure Functions & Serverless", "hours": 5, "priority": "MED"},
                {"topic": "Azure API Management", "hours": 4, "priority": "MED"},
                {"topic": "Practice Exams & Gap Review", "hours": 6, "priority": "HIGH"},
            ],
            "AZ-400": [
                {"topic": "Azure Pipelines & CI/CD", "hours": 10, "priority": "HIGH"},
                {"topic": "Infrastructure as Code (Bicep/Terraform)", "hours": 8, "priority": "HIGH"},
                {"topic": "Azure Monitor & Observability", "hours": 6, "priority": "MED"},
                {"topic": "GitHub Actions & Source Control", "hours": 5, "priority": "MED"},
                {"topic": "Release Management & Gates", "hours": 6, "priority": "HIGH"},
                {"topic": "Practice Exams & Gap Review", "hours": 8, "priority": "HIGH"},
            ],
            "DP-900": [
                {"topic": "Core Data Concepts", "hours": 5, "priority": "HIGH"},
                {"topic": "Azure Relational Data Services", "hours": 5, "priority": "HIGH"},
                {"topic": "Azure Non-Relational Data", "hours": 4, "priority": "MED"},
                {"topic": "Azure Analytics Workloads", "hours": 5, "priority": "MED"},
                {"topic": "Practice Exams", "hours": 4, "priority": "HIGH"},
            ],
        }
        return paths.get(cert, paths["AZ-204"])

    def _prerequisites(self, cert: str) -> list:
        prereqs = {
            "AZ-204": ["AZ-900 (recommended)", "Basic Python or C# knowledge", "REST API familiarity"],
            "AZ-400": ["AZ-204 or equivalent", "Git proficiency", "CI/CD pipeline experience"],
            "DP-900": ["Basic data concepts", "Excel/SQL familiarity"],
        }
        return prereqs.get(cert, ["AZ-900 (recommended)"])
