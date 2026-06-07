from .base_agent import BaseAgent
from datetime import date, timedelta


class ReadinessForecaster(BaseAgent):
    name = "Readiness Forecaster"

    def __init__(self):
        super().__init__()
        self.foundry_queries = [("certification readiness forecast", "performance-report")]

    def run(self, input_data: dict, docs: list) -> dict:
        score = input_data.get("current_practice_score", 50)
        starting_score = input_data.get("starting_score", max(0, score - 10))
        hours = input_data.get("hours_studied", 0)
        focus_hours = input_data.get("focus_hours_per_week", 10)
        cert = input_data.get("certification_target", "AZ-204")
        citations = [d["citation"] for d in docs]

        weeks_studied = max(1, hours / max(1, focus_hours - 4))
        score_velocity = round((score - starting_score) / weeks_studied, 2)

        THRESHOLD = 75
        if score >= THRESHOLD:
            weeks_to_ready = 0.0
            trend = "ACCELERATING"
        else:
            weeks_to_ready = round((THRESHOLD - score) / max(0.1, score_velocity), 1)
            if weeks_to_ready < 0:
                weeks_to_ready = 0.0

            if score_velocity > 3:
                trend = "ACCELERATING"
            elif score_velocity >= 1:
                trend = "STEADY"
            else:
                trend = "DECELERATING"

        forecast_date = (date.today() + timedelta(weeks=weeks_to_ready)).strftime("%B %d, %Y")

        if score_velocity > 3:
            confidence = "HIGH"
        elif score_velocity >= 1:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        if score >= THRESHOLD:
            forecast_message = (
                f"You are exam-ready NOW. Score {score}% exceeds the {THRESHOLD}% threshold. "
                f"Schedule your {cert} exam immediately. [Source: Team Learning Report]"
            )
        elif weeks_to_ready <= 2:
            forecast_message = (
                f"At your current velocity of +{score_velocity:.1f} pts/week, you'll be exam-ready by {forecast_date}. "
                f"Keep this pace — the finish line is close. [Source: Team Learning Report]"
            )
        elif weeks_to_ready <= 6:
            forecast_message = (
                f"Forecast: exam-ready by {forecast_date} ({weeks_to_ready:.0f} weeks). "
                f"Velocity: +{score_velocity:.1f} pts/week. Confidence: {confidence}. "
                f"[Source: Team Learning Report]"
            )
        else:
            forecast_message = (
                f"At current pace, you won't reach {THRESHOLD}% threshold before your exam. "
                f"Score velocity is only +{score_velocity:.1f} pts/week. "
                f"Intervention recommended to accelerate progress. [Source: Team Learning Report]"
            )

        return {
            "current_score": score,
            "score_velocity": score_velocity,
            "weeks_to_ready": weeks_to_ready,
            "forecast_date": forecast_date,
            "confidence": confidence,
            "trend": trend,
            "forecast_message": forecast_message,
            "citations": citations,
            "summary": f"Ready in {weeks_to_ready:.0f} weeks | Velocity: +{score_velocity:.1f} pts/wk | {confidence} confidence",
        }