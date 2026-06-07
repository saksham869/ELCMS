from .base_agent import BaseAgent

LEARNER_TYPES = {
    "FAST_TRACKER": "Practice score >70 and hours <15 — aggressive learner",
    "ON_SCHEDULE": "Score improving week-over-week at steady pace",
    "STRUGGLING": "Score <55 and less than 4 weeks to exam",
    "CAPACITY_LIMITED": "Meeting hours >22 — time-constrained learner",
}

CERT_REQUIRED_SKILLS = {
    "AZ-204": ["Azure App Service", "Azure Functions", "Azure Storage", "Azure Security", "Azure SDK", "REST APIs"],
    "AZ-400": ["CI/CD Pipelines", "Infrastructure as Code", "Azure Monitor", "GitHub Actions", "Release Management", "DORA Metrics"],
    "DP-203": ["Azure Data Factory", "Azure Synapse", "Azure Stream Analytics", "Data Lake", "Spark", "SQL"],
    "AI-102": ["Azure AI Services", "Azure OpenAI", "Computer Vision", "NLP", "Bot Framework", "Azure Cognitive Search"],
    "AZ-104": ["Virtual Machines", "Virtual Networks", "Azure AD", "Storage Accounts", "Azure Monitor", "ARM Templates"],
    "AZ-305": ["Solution Architecture", "Identity Management", "Data Storage", "Business Continuity", "Migration", "Security"],
    "AZ-500": ["Azure AD Security", "Platform Security", "Security Operations", "Data Security", "Network Security", "RBAC"],
    "MS-700": ["Teams Administration", "Teams Meetings", "Teams Calling", "Teams Apps", "Security Compliance", "Governance"],
    "PL-300": ["Power BI Desktop", "DAX", "Power Query", "Data Modeling", "Visualizations", "Power BI Service"],
    "SC-900": ["Security Concepts", "Compliance Concepts", "Azure AD Basics", "Microsoft Security Solutions", "Microsoft Compliance"],
    "AZ-900": ["Cloud Concepts", "Azure Architecture", "Azure Services", "Azure Management", "Azure Security", "Pricing"],
    "DP-900": ["Core Data Concepts", "Relational Data", "Non-Relational Data", "Analytics", "Azure Data Services"],
    "AI-900": ["AI Concepts", "Machine Learning", "Computer Vision", "NLP", "Conversational AI", "Azure AI Services"],
    "MS-900": ["Microsoft 365 Services", "Security Compliance", "Pricing", "Support", "Teams", "SharePoint"],
    "DP-300": ["Azure SQL", "SQL Server", "High Availability", "Performance", "Security", "Monitoring"],
}


class LearnerProfiler(BaseAgent):
    name = "Learner Profiler"

    def __init__(self):
        super().__init__()

    def _get_queries(self, role: str, cert: str) -> list:
        return [
            (f"{role} certification requirements", "skills-matrix"),
            (f"{cert} prerequisites", "certification-guide"),
        ]

    def run(self, input_data: dict, docs: list) -> dict:
        role = input_data.get("role", "Software Engineer")
        cert = input_data.get("certification_target", "AZ-204")
        self.foundry_queries = self._get_queries(role, cert)

        score = input_data.get("current_practice_score", 50)
        hours = input_data.get("hours_studied", 0)
        weeks = input_data.get("weeks_until_exam", 4)
        meeting_hours = input_data.get("meeting_hours_per_week", 14)
        focus_hours = input_data.get("focus_hours_per_week", 10)
        starting_score = input_data.get("starting_score", max(0, score - 10))
        citations = [d["citation"] for d in docs]

        required_skills = CERT_REQUIRED_SKILLS.get(cert, CERT_REQUIRED_SKILLS["AZ-204"])
        # Estimate current skills based on score
        skills_known_count = int(len(required_skills) * (score / 100))
        skill_gap = required_skills[skills_known_count:]

        recommended_hours = 40  # standard
        experience_score = round(min(1.0, hours / recommended_hours), 2)

        gap_to_threshold = max(0, 75 - score)
        risk_score = round(min(1.0, (gap_to_threshold * weeks) / 100), 2)

        # Classify learner type
        if score > 70 and hours < 15:
            learner_type = "FAST_TRACKER"
            recommended_approach = "Compressed 2-week sprint — you're efficient. Go aggressive."
        elif meeting_hours > 22:
            learner_type = "CAPACITY_LIMITED"
            recommended_approach = "Micro-sessions of 30 min. Block calendar. Consistency over volume."
        elif score < 55 and weeks < 4:
            learner_type = "STRUGGLING"
            recommended_approach = "Extended plan with weekly checkpoints. Small consistent steps."
        else:
            learner_type = "ON_SCHEDULE"
            recommended_approach = "Maintain steady pace. Weekly practice exams. Focus on weak areas."

        weeks_studied = max(1, (hours / max(1, focus_hours - 6)))
        score_velocity = round((score - starting_score) / max(1, weeks_studied), 2)

        return {
            "learner_type": learner_type,
            "learner_type_description": LEARNER_TYPES.get(learner_type, ""),
            "skill_gap": skill_gap,
            "skills_known": required_skills[:skills_known_count],
            "experience_score": experience_score,
            "risk_score": risk_score,
            "score_velocity": score_velocity,
            "recommended_approach": recommended_approach,
            "citations": citations,
            "summary": f"Learner type: {learner_type} | Risk: {risk_score:.0%} | Gap: {len(skill_gap)} skills",
        }