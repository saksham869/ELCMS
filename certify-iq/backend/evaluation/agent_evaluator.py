import re


class AgentEvaluator:
    def score(
        self,
        agent_name: str,
        response: str,
        query: str,
        citations: list,
        latency_ms: int = 9999,
        grounding_verified: bool = False,
    ) -> float:
        total = 0.0
        if citations:
            total += 0.25
        if 100 <= len(response) <= 800:
            total += 0.20
        if re.search(r"\d+", response):
            total += 0.20
        if grounding_verified:
            total += 0.20
        if latency_ms < 5000:
            total += 0.15
        return round(min(total, 1.0), 2)

    def grade(self, score: float) -> str:
        if score >= 0.85:
            return "EXCELLENT"
        elif score >= 0.70:
            return "GOOD"
        elif score >= 0.50:
            return "ACCEPTABLE"
        return "NEEDS_REVIEW"

    def get_pipeline_score(self, all_scores: dict) -> dict:
        if not all_scores:
            return {"average_score": 0.0, "grade": "NEEDS_REVIEW", "weakest_agent": "", "strongest_agent": "", "all_scores": {}}
        avg = round(sum(all_scores.values()) / len(all_scores), 2)
        weakest = min(all_scores, key=all_scores.get)
        strongest = max(all_scores, key=all_scores.get)
        return {
            "average_score": avg,
            "grade": self.grade(avg),
            "weakest_agent": weakest,
            "strongest_agent": strongest,
            "all_scores": all_scores,
        }


evaluator = AgentEvaluator()