from .base_agent import BaseAgent
from data.synthetic_employees import get_all_employees, get_team


class ManagerInsightsAgent(BaseAgent):
    name = "Manager Insights Agent"

    def __init__(self):
        super().__init__()
        self.foundry_queries = [
            ("manager team readiness certification", "manager-guide"),
            ("team performance quarterly summary", "performance-report"),
        ]

    def run(self, input_data: dict, docs: list) -> dict:
        team_id = input_data.get("team_id", "TEAM-A")
        team = get_team(team_id) or {"team_id": team_id, "name": "Team", "members": []}
        member_ids = team.get("members", [])
        all_employees = {e["id"]: e for e in get_all_employees()}
        members = [all_employees[mid] for mid in member_ids if mid in all_employees]
        citations = [d["citation"] for d in docs]

        member_status = []
        ready_count = 0
        for emp in members:
            score = emp.get("current_practice_score", 0)
            hours = emp.get("hours_studied", 0)
            meetings = emp.get("meeting_hours_per_week", 0)
            weeks = emp.get("weeks_until_exam", 4)

            if score >= 75:
                ready_count += 1

            risk_level, concern, action = self._assess_risk(score, hours, meetings, weeks)
            member_status.append({
                "employee_id": emp["id"],
                "name": emp["name"],
                "certification": emp.get("certification_target", ""),
                "practice_score": score,
                "hours_studied": hours,
                "risk_level": risk_level,
                "concern": concern,
                "recommended_action": action,
            })

        total = len(members) or 1
        team_score = round((ready_count / total) * 100, 1)

        top_recs = [
            f"Block calendar time for the {len([m for m in member_status if m['risk_level'] == 'HIGH_RISK'])} high-risk member(s) immediately. [Source: Manager Readiness Guide]",
            f"Team readiness is {team_score}% — target is 80% before end of quarter. [Source: Team Learning Report]",
            "Schedule weekly 15-min check-ins to review practice scores and study hours. [Source: Manager Readiness Guide]",
            "Recognise exam passes publicly in team meetings to drive motivation. [Source: Team Learning Report]",
        ]

        return {
            "team_id": team_id,
            "team_name": team.get("name", ""),
            "total_members": total,
            "ready_count": ready_count,
            "team_readiness_score": team_score,
            "executive_summary": (
                f"Team {team_id} has {ready_count}/{total} members exam-ready ({team_score}% readiness). "
                f"{len([m for m in member_status if m['risk_level'] == 'HIGH_RISK'])} members are HIGH RISK. "
                "Immediate manager action required for at-risk members. [Source: Manager Readiness Guide]"
            ),
            "member_status": member_status,
            "top_recommendations": top_recs,
            "citations": citations,
            "summary": f"Team score: {team_score}% | {ready_count}/{total} ready",
        }

    def _assess_risk(self, score: int, hours: int, meetings: int, weeks: int) -> tuple:
        if hours < 10 and weeks <= 3:
            return "HIGH_RISK", f"Only {hours}hrs studied with {weeks} weeks to exam", "Urgent 1:1 — consider deferring exam date"
        if meetings > 22:
            return "CAPACITY_CONCERN", f"{meetings} meeting hrs/week limiting study time", "Block 2hrs/week study time on calendar"
        if 60 <= score < 75:
            return "APPROACHING_READY", f"Score {score}% — {75 - score} points below pass threshold", "Focus on weak areas for 1-2 weeks"
        if score >= 70 and hours >= 15:
            return "ON_TRACK", "Strong study progress and score trajectory", "Maintain current pace — on track for pass"
        return "MONITOR", f"Score {score}% — monitoring required", "Weekly check-in recommended"
