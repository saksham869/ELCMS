import random

random.seed(42)

COHORT_STATS = {
    "AZ-204": {"avg_score": 64.2, "pass_rate": 0.71, "avg_hours": 21.3, "role": "Cloud Engineer"},
    "AZ-400": {"avg_score": 71.8, "pass_rate": 0.79, "avg_hours": 24.1, "role": "DevOps Engineer"},
    "DP-203": {"avg_score": 58.4, "pass_rate": 0.63, "avg_hours": 27.8, "role": "Data Engineer"},
    "AI-102": {"avg_score": 67.1, "pass_rate": 0.74, "avg_hours": 22.6, "role": "AI Engineer"},
}


def _generate_cohort(cert: str, stats: dict, n: int = 50) -> list:
    members = []
    random.seed(hash(cert) % 1000)
    for i in range(1, n + 1):
        score = max(30, min(95, int(random.gauss(stats["avg_score"], 12))))
        hours = max(5, int(random.gauss(stats["avg_hours"], 8)))
        passed = random.random() < stats["pass_rate"]
        members.append({
            "id": f"COHORT-{cert.replace('-','')}-{i:03d}",
            "role": stats["role"],
            "certification": cert,
            "practice_score_at_week_4": score,
            "hours_studied": hours,
            "exam_outcome": "Pass" if passed else "Fail",
            "meeting_hours_per_week": random.randint(8, 28),
        })
    return members


COHORT_DATA: dict = {}
for _cert, _stats in COHORT_STATS.items():
    COHORT_DATA[_cert] = _generate_cohort(_cert, _stats)


def get_cohort(certification: str) -> list:
    return COHORT_DATA.get(certification, [])


def get_cohort_stats(certification: str) -> dict:
    return COHORT_STATS.get(certification, {})


def calculate_percentile(employee_score: int, certification: str) -> float:
    cohort = get_cohort(certification)
    if not cohort:
        return 50.0
    scores = [m["practice_score_at_week_4"] for m in cohort]
    below = sum(1 for s in scores if s < employee_score)
    return round((below / len(scores)) * 100, 1)