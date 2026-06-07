from .base_agent import BaseAgent
from data.synthetic_cohort import get_cohort, get_cohort_stats, calculate_percentile
import statistics


class PeerBenchmarkingAgent(BaseAgent):
    name = "Peer Benchmarking Agent"

    def __init__(self):
        super().__init__()

    def _get_queries(self, cert: str) -> list:
        return [(f"{cert} cohort benchmarks", "performance-report")]

    def run(self, input_data: dict, docs: list) -> dict:
        cert = input_data.get("certification_target", "AZ-204")
        role = input_data.get("role", "Cloud Engineer")
        score = input_data.get("current_practice_score", 50)
        hours = input_data.get("hours_studied", 0)
        self.foundry_queries = self._get_queries(cert)
        citations = [d["citation"] for d in docs]

        cohort = get_cohort(cert)
        cohort_stats = get_cohort_stats(cert)

        if not cohort:
            percentile = 50.0
            cohort_size = 0
            cohort_avg_score = 65.0
            cohort_avg_hours = 20.0
        else:
            scores = [m["practice_score_at_week_4"] for m in cohort]
            hours_list = [m["hours_studied"] for m in cohort]
            percentile = calculate_percentile(score, cert)
            cohort_size = len(cohort)
            cohort_avg_score = round(statistics.mean(scores), 1)
            cohort_avg_hours = round(statistics.mean(hours_list), 1)

        scores_below = int(percentile * cohort_size / 100)

        if hours > cohort_avg_hours:
            pace_pct = round(((hours - cohort_avg_hours) / cohort_avg_hours) * 100, 0)
            pace_comparison = f"Your study pace is {int(pace_pct)}% faster than the cohort average"
        elif hours < cohort_avg_hours:
            pace_pct = round(((cohort_avg_hours - hours) / cohort_avg_hours) * 100, 0)
            pace_comparison = f"Your study pace is {int(pace_pct)}% slower than the cohort average — consider increasing study hours"
        else:
            pace_comparison = "Your study pace matches the cohort average exactly"

        benchmark_insight = (
            f"You're scoring higher than {percentile:.0f}% of {role}s "
            f"attempting {cert} at the same stage of preparation. "
            f"{pace_comparison}. [Source: Peer Cohort Benchmarks]"
        )

        if percentile >= 75:
            motivation_message = f"Outstanding! You're in the top 25% of your peer cohort. Keep this momentum to the exam. [Source: Peer Cohort Benchmarks]"
        elif percentile >= 50:
            motivation_message = f"You're above average in your cohort. A focused final push will put you in the top quarter. [Source: Peer Cohort Benchmarks]"
        elif percentile >= 25:
            motivation_message = f"You're below the cohort median — but {cohort_size - scores_below} peers scored lower. Targeted practice on weak areas will move you up quickly. [Source: Peer Cohort Benchmarks]"
        else:
            motivation_message = f"You're in the bottom quartile of your cohort right now — this is your signal to intensify. The cohort average ({cohort_avg_score:.0f}%) is within reach with 2-3 focused weeks. [Source: Peer Cohort Benchmarks]"

        return {
            "percentile": percentile,
            "cohort_size": cohort_size,
            "cohort_avg_score": cohort_avg_score,
            "cohort_avg_hours": cohort_avg_hours,
            "employee_score": score,
            "employee_hours": hours,
            "pace_comparison": pace_comparison,
            "benchmark_insight": benchmark_insight,
            "motivation_message": motivation_message,
            "citations": citations,
            "summary": f"Percentile: {percentile:.0f}% | Cohort avg: {cohort_avg_score}% | Cohort size: {cohort_size}",
        }