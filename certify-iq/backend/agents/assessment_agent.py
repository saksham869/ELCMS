from .base_agent import BaseAgent

PASS_THRESHOLD = 75

SAMPLE_QUESTIONS = {
    "AZ-204": [
        {"question": "Which Azure service enables serverless event-driven compute?", "answer": "Azure Functions", "topic": "Compute"},
        {"question": "What authentication protocol does Azure AD use for modern apps?", "answer": "OAuth 2.0 / OpenID Connect", "topic": "Security"},
        {"question": "Which tier of Azure App Service supports autoscaling?", "answer": "Standard or Premium tier", "topic": "App Service"},
    ],
    "AZ-400": [
        {"question": "What does a deployment gate in Azure Pipelines do?", "answer": "Validates pre/post-deployment conditions before proceeding", "topic": "Release Management"},
        {"question": "What DORA metric measures how quickly you recover from failure?", "answer": "Mean Time to Restore (MTTR)", "topic": "DevOps Metrics"},
        {"question": "Which tool in Azure DevOps stores NuGet and npm packages?", "answer": "Azure Artifacts", "topic": "Package Management"},
    ],
    "DP-203": [
        {"question": "Which Azure service is used for orchestrating data pipelines?", "answer": "Azure Data Factory", "topic": "Data Integration"},
        {"question": "What is the purpose of Azure Synapse Analytics?", "answer": "Unified analytics combining data warehousing and big data", "topic": "Analytics"},
        {"question": "Which format is best for streaming analytics in Azure?", "answer": "Azure Stream Analytics with Event Hubs", "topic": "Streaming"},
    ],
    "AI-102": [
        {"question": "Which Azure service provides pre-built AI models via REST API?", "answer": "Azure AI Services (Cognitive Services)", "topic": "AI Services"},
        {"question": "What is grounding in Azure OpenAI?", "answer": "Connecting LLM outputs to verified knowledge sources", "topic": "Azure OpenAI"},
        {"question": "Which service enables custom NLP model training on Azure?", "answer": "Azure Language Service (Custom Text Classification)", "topic": "NLP"},
    ],
    "DP-900": [
        {"question": "What type of data structure does Azure Cosmos DB primarily use?", "answer": "Non-relational / NoSQL (document, key-value, graph)", "topic": "Non-Relational Data"},
        {"question": "What is the purpose of Azure Synapse Analytics?", "answer": "Unified analytics platform combining data warehousing and big data analytics", "topic": "Analytics"},
        {"question": "Which Azure service provides managed relational database hosting?", "answer": "Azure SQL Database", "topic": "Relational Data"},
    ],
}

WEAK_AREAS = {
    "AZ-204": ["Azure Key Vault integration", "Azure Service Bus vs Event Hubs", "RBAC role assignments"],
    "AZ-400": ["Release gates configuration", "Infrastructure as Code (Bicep)", "DORA metrics interpretation"],
    "DP-203": ["Synapse vs Databricks distinction", "Partition strategies in Data Lake", "Stream Analytics windowing functions"],
    "AI-102": ["Azure OpenAI deployment configuration", "Responsible AI principles in practice", "Custom vision model training"],
    "DP-900": ["Synapse vs Databricks distinction", "Consistency levels in Cosmos DB", "Streaming vs batch analytics"],
}


class AssessmentAgent(BaseAgent):
    name = "Assessment Agent"

    def __init__(self):
        super().__init__()

    def _get_queries(self, cert: str) -> list:
        return [
            (f"{cert} practice questions readiness", "assessment"),
            (f"{cert} pass threshold readiness", "certification-guide"),
        ]

    def run(self, input_data: dict, docs: list) -> dict:
        cert = input_data.get("certification_target", "AZ-204")
        self.foundry_queries = self._get_queries(cert)
        score = input_data.get("current_practice_score", 50)
        citations = [d["citation"] for d in docs]

        gap = max(0, PASS_THRESHOLD - score)
        days_to_ready = max(7, gap * 2)
        trigger_loop_back = False

        if score >= 75:
            verdict = "GO"
            colour = "GREEN"
            action = "Schedule exam within 14 days"
        elif score >= 65:
            verdict = "CONDITIONAL GO"
            colour = "AMBER"
            action = "2 more weeks on weak areas"
        elif score >= 55:
            verdict = "APPROACHING"
            colour = "YELLOW"
            action = "3-4 week focused sprint needed"
        else:
            verdict = "NOT YET"
            colour = "RED"
            action = f"Intensive remediation required — {gap} point gap to threshold"
            trigger_loop_back = True

        return {
            "practice_score": score,
            "pass_threshold": PASS_THRESHOLD,
            "gap": gap,
            "verdict": verdict,
            "colour": colour,
            "recommended_action": action,
            "days_to_exam_ready": days_to_ready,
            "sample_questions": SAMPLE_QUESTIONS.get(cert, SAMPLE_QUESTIONS["AZ-204"]),
            "weak_areas": WEAK_AREAS.get(cert, WEAK_AREAS["AZ-204"]),
            "trigger_loop_back": trigger_loop_back,
            "citations": citations,
            "summary": f"Score: {score}% | Threshold: {PASS_THRESHOLD}% | Verdict: {verdict}",
        }