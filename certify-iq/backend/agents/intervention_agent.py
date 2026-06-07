from .base_agent import BaseAgent
from datetime import date


class InterventionAgent(BaseAgent):
    name = "Intervention Agent"

    def __init__(self):
        super().__init__()
        self.foundry_queries = [("manager intervention high risk", "manager-guide")]

    def run(self, input_data: dict, docs: list) -> dict:
        name = input_data.get("name", "Employee")
        role = input_data.get("role", "Professional")
        cert = input_data.get("certification_target", "AZ-204")
        score = input_data.get("current_practice_score", 45)
        weeks = input_data.get("weeks_until_exam", 5)
        meeting_hours = input_data.get("meeting_hours_per_week", 24)
        weak_areas = input_data.get("_assessment", {}).get("result", {}).get("weak_areas", ["core concepts"])
        total_roi = input_data.get("_roi", {}).get("result", {}).get("total_roi_usd", 165)
        citations = [d["citation"] for d in docs]

        # Determine intervention level
        if weeks <= 2 and score < 55:
            intervention_level = "URGENT"
        elif weeks <= 3 and score < 65:
            intervention_level = "HIGH"
        elif meeting_hours > 22 and score < 70:
            intervention_level = "MEDIUM"
        else:
            intervention_level = "LOW"

        weak_areas_str = ", ".join(weak_areas[:3]) if weak_areas else "core exam topics"
        exam_date_est = date.today().strftime("%B %Y")

        manager_email_draft = f"""Subject: [CertifyIQ Alert] {name} needs support — {cert} exam in {weeks} weeks

Hi,

CertifyIQ's AI pipeline has flagged {name} as requiring immediate support for their upcoming {cert} certification exam.

Current Status:
• Practice Score: {score}% (threshold: 75%)
• Weeks Until Exam: {weeks}
• Meeting Load: {meeting_hours}hrs/week (above recommended 16hrs)
• Key Weak Areas: {weak_areas_str}

Recommended Actions:
1. Schedule a 30-minute 1:1 with {name} this week to discuss study challenges
2. Block 2hrs on {name}'s calendar every Tuesday and Thursday for the next {weeks} weeks
3. Consider whether any meetings can be delegated to reduce {name}'s {meeting_hours}hr/week meeting load

Financial Context:
Without intervention, this represents ${total_roi:.0f} at risk (exam fee + productivity cost).
With CertifyIQ-guided prep, pass rates increase from 58% to 89%.

This is an automated alert from CertifyIQ. Human review required before any action.
[Source: Intervention Best Practices]"""

        employee_message = (
            f"Hi {name}, we've noticed you're working hard on {cert} with {weeks} weeks to go. "
            f"Your current score of {score}% shows real progress, but we want to make sure you have everything you need. "
            f"Let's focus on {weak_areas_str} — these are your biggest opportunities for score improvement. "
            f"Small, consistent 30-minute sessions will move the needle more than sporadic long study blocks. "
            f"Your manager has been notified to help clear some calendar space. You've got this. "
            f"[Source: Intervention Best Practices]"
        )

        calendar_recommendation = (
            f"Block Tuesday 2-4 PM and Thursday 12-2 PM for the next {weeks} weeks. "
            f"Mark as 'Study — {cert} Prep' and set as 'Busy'. "
            f"This creates {weeks * 4} protected study hours before exam date. "
            f"[Source: Intervention Best Practices]"
        )

        return {
            "intervention_level": intervention_level,
            "manager_email_draft": manager_email_draft,
            "employee_message": employee_message,
            "calendar_recommendation": calendar_recommendation,
            "escalation_triggered": True,
            "roi_at_risk_usd": round(total_roi, 2),
            "citations": citations,
            "summary": f"Intervention: {intervention_level} | ROI at risk: ${total_roi:.0f}",
        }