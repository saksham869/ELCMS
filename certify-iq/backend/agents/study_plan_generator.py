import math
from datetime import date, timedelta
from .base_agent import BaseAgent


class StudyPlanGenerator(BaseAgent):
    name = "Study Plan Generator"

    def __init__(self):
        super().__init__()
        self.foundry_queries = [
            ("certification study schedule template", "study-template"),
            ("workload learning correlation", "workload-insights"),
        ]

    def run(self, input_data: dict, docs: list) -> dict:
        focus_hours = input_data.get("focus_hours_per_week", 8)
        available_hours = max(2, focus_hours - 6)
        learning_path = input_data.get("_learning_path", {})
        total_hours = learning_path.get("total_hours", 36)
        topics = learning_path.get("learning_path", [])
        citations = [d["citation"] for d in docs]

        total_weeks = math.ceil(total_hours / available_hours)
        exam_ready_date = date.today() + timedelta(weeks=total_weeks)

        weekly_plan = self._build_weekly_plan(topics, total_weeks, available_hours)

        return {
            "weekly_plan": weekly_plan,
            "total_weeks": total_weeks,
            "available_hours_per_week": available_hours,
            "exam_ready_date": exam_ready_date.isoformat(),
            "citations": citations,
            "summary": f"{total_weeks}-week plan, {available_hours}hrs/week available",
        }

    def _build_weekly_plan(self, topics: list, total_weeks: int, hours_per_week: int) -> list:
        plan = []
        topic_idx = 0
        for week in range(1, total_weeks + 1):
            week_topics = []
            remaining = hours_per_week
            while remaining > 0 and topic_idx < len(topics):
                t = topics[topic_idx]
                week_topics.append(t.get("topic", f"Topic {topic_idx + 1}"))
                remaining -= t.get("hours", hours_per_week)
                topic_idx += 1
            if week == total_weeks:
                week_topics = week_topics or ["Practice Exam & Gap Review"]
                milestone = "Final practice exam — target 80%+ score"
                target_score = 80
            elif week == 1:
                milestone = "Complete foundational concepts"
                target_score = 60
            else:
                milestone = f"Complete {', '.join(week_topics[:1])} module"
                target_score = 65 + (week * 3)
            plan.append({
                "week": week,
                "topics": week_topics or ["Review & consolidation"],
                "hours": hours_per_week,
                "milestone": milestone,
                "target_score": min(target_score, 80),
            })
        return plan
