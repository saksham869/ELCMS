from .base_agent import BaseAgent

EXAM_COST_USD = 165
FAILED_ATTEMPT_COST = 165
MANAGER_TIME_COST_PER_HOUR = 75
PRODUCTIVITY_LOSS_PER_WEEK = 200

UNGUIDED_PASS_RATE = 0.58
GUIDED_PASS_RATE = 0.89


class ROICalculatorAgent(BaseAgent):
    name = "ROI Calculator"

    def __init__(self):
        super().__init__()
        self.foundry_queries = [("certification ROI enterprise cost", "manager-guide")]

    def run(self, input_data: dict, docs: list) -> dict:
        total_weeks = input_data.get("_study_plan", {}).get("total_weeks", 6)
        citations = [d["citation"] for d in docs]

        expected_attempts_unguided = round(1 / UNGUIDED_PASS_RATE, 2)
        expected_attempts_guided = round(1 / GUIDED_PASS_RATE, 2)

        unguided_total_cost = round(expected_attempts_unguided * EXAM_COST_USD, 2)
        guided_total_cost = round(expected_attempts_guided * EXAM_COST_USD, 2)

        cost_savings = round(unguided_total_cost - guided_total_cost, 2)
        productivity_savings = round(total_weeks * PRODUCTIVITY_LOSS_PER_WEEK * 0.3, 2)
        total_roi = round(cost_savings + productivity_savings, 2)

        roi_message = (
            f"CertifyIQ saves ${total_roi:.0f} per employee vs unguided exam prep. "
            f"This includes ${cost_savings:.0f} in reduced retake costs "
            f"(guided pass rate: {GUIDED_PASS_RATE*100:.0f}% vs unguided: {UNGUIDED_PASS_RATE*100:.0f}%) "
            f"and ${productivity_savings:.0f} in productivity recovery. "
            f"[Source: Certification ROI & Cost Analysis]"
        )

        return {
            "exam_cost_usd": EXAM_COST_USD,
            "unguided_pass_rate": UNGUIDED_PASS_RATE,
            "guided_pass_rate": GUIDED_PASS_RATE,
            "unguided_expected_attempts": expected_attempts_unguided,
            "guided_expected_attempts": expected_attempts_guided,
            "unguided_total_cost_usd": unguided_total_cost,
            "guided_total_cost_usd": guided_total_cost,
            "cost_savings_usd": cost_savings,
            "productivity_savings_usd": productivity_savings,
            "total_roi_usd": total_roi,
            "roi_message": roi_message,
            "citations": citations,
            "summary": f"ROI: ${total_roi:.0f} savings | {GUIDED_PASS_RATE*100:.0f}% guided pass rate",
        }