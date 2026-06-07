from .base_agent import BaseAgent

SLOTS = {
    "Morning": [
        {"day": "Monday", "time": "6:30 AM", "duration_minutes": 90},
        {"day": "Wednesday", "time": "6:30 AM", "duration_minutes": 90},
        {"day": "Friday", "time": "6:30 AM", "duration_minutes": 90},
    ],
    "Afternoon": [
        {"day": "Tuesday", "time": "12:00 PM", "duration_minutes": 60},
        {"day": "Thursday", "time": "12:00 PM", "duration_minutes": 60},
        {"day": "Saturday", "time": "10:00 AM", "duration_minutes": 120},
    ],
    "Evening": [
        {"day": "Monday", "time": "7:00 PM", "duration_minutes": 90},
        {"day": "Wednesday", "time": "7:00 PM", "duration_minutes": 90},
        {"day": "Friday", "time": "7:00 PM", "duration_minutes": 90},
    ],
}


class EngagementAgent(BaseAgent):
    name = "Engagement Agent"

    def __init__(self):
        super().__init__()
        self.foundry_queries = [
            ("workload insights reminders engagement", "workload-insights"),
            ("learning engagement best practices", "responsible-ai"),
        ]

    def run(self, input_data: dict, docs: list) -> dict:
        meeting_hours = input_data.get("meeting_hours_per_week", 14)
        preferred = input_data.get("preferred_study_time", "Morning")
        name = input_data.get("name", "Learner")
        cert = input_data.get("certification_target", "certification")
        citations = [d["citation"] for d in docs]

        if meeting_hours > 22:
            capacity_flag = "HIGH_CAPACITY_RISK"
            capacity_message = "Recommend blocking 2hrs/week from calendar for study"
        elif meeting_hours > 16:
            capacity_flag = "MODERATE_CAPACITY"
            capacity_message = "Monitor workload weekly — at risk of study drop-off"
        else:
            capacity_flag = "HEALTHY_CAPACITY"
            capacity_message = "Good conditions for consistent study"

        slots = SLOTS.get(preferred, SLOTS["Morning"])
        weekly_minutes = sum(s["duration_minutes"] for s in slots)
        weekly_hours = round(weekly_minutes / 60, 1)

        reminders = [
            f"🌅 {name}, your {preferred.lower()} study block starts soon — 25 mins to go. Topic: {cert} core concepts. [Source: Workload Insights Report]",
            f"📊 Weekly check-in: You've completed {int(weekly_hours * 0.6)}/{int(weekly_hours)} planned study hours this week. Keep it up! [Source: Workload Insights Report]",
            f"🎯 Exam milestone reminder: {cert} practice exam target is 80%+. Schedule a mock exam this weekend. [Source: Study Schedule Templates]",
        ]

        return {
            "study_slots": slots,
            "weekly_study_hours": weekly_hours,
            "capacity_flag": capacity_flag,
            "capacity_message": capacity_message,
            "reminder_messages": reminders,
            "citations": citations,
            "summary": f"{len(slots)} study slots/week · {weekly_hours}hrs · {capacity_flag}",
        }
