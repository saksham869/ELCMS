import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("AZURE_AI_PROJECT_ENDPOINT", "https://placeholder.openai.azure.com")
os.environ.setdefault("AZURE_SEARCH_KEY", "placeholder")
os.environ.setdefault("AZURE_SEARCH_INDEX", "learning-knowledge")
os.environ.setdefault("AZURE_AI_MODEL_DEPLOYMENT", "gpt-4o")
os.environ.setdefault("OPENAI_API_VERSION", "2024-02-01")
os.environ.setdefault("MOCK_MODE", "true")

from data.synthetic_employees import get_employee

SAMPLE_DOCS = [
    {
        "id": "doc-001",
        "title": "Engineering Certification Guide",
        "content": "AZ-204 requires 40-60 hours of study. [Source: Engineering Certification Guide]",
        "category": "certification-guide",
        "citation": "[Source: Engineering Certification Guide]",
    },
    {
        "id": "doc-006",
        "title": "Role Skills Matrix",
        "content": "Cloud Engineers need Azure SDK skills. [Source: Role Skills Matrix]",
        "category": "skills-matrix",
        "citation": "[Source: Role Skills Matrix]",
    },
]

EMP001 = get_employee("EMP-001")
EMP003 = get_employee("EMP-003")


# Agent 1: Learner Profiler
def test_learner_profiler_schema():
    from agents.learner_profiler import LearnerProfiler
    agent = LearnerProfiler()
    result = agent.run(EMP001, SAMPLE_DOCS)
    assert "learner_type" in result
    assert "skill_gap" in result
    assert "experience_score" in result
    assert "risk_score" in result
    assert "recommended_approach" in result
    assert "citations" in result


def test_learner_profiler_emp003_struggling():
    from agents.learner_profiler import LearnerProfiler
    agent = LearnerProfiler()
    result = agent.run(EMP003, SAMPLE_DOCS)
    assert result["learner_type"] in ["STRUGGLING", "CAPACITY_LIMITED"]


def test_learner_profiler_citations_nonempty():
    from agents.learner_profiler import LearnerProfiler
    agent = LearnerProfiler()
    result = agent.run(EMP001, SAMPLE_DOCS)
    assert len(result["citations"]) > 0


# Agent 2: Learning Path Curator
def test_learning_path_curator_schema():
    from agents.learning_path_curator import LearningPathCurator
    agent = LearningPathCurator()
    result = agent.run(EMP001, SAMPLE_DOCS)
    assert "certification" in result
    assert "learning_path" in result
    assert "total_hours" in result
    assert isinstance(result["learning_path"], list)


def test_learning_path_curator_topics_nonempty():
    from agents.learning_path_curator import LearningPathCurator
    agent = LearningPathCurator()
    result = agent.run(EMP001, SAMPLE_DOCS)
    assert len(result["learning_path"]) > 0


# Agent 3: Study Plan Generator
def test_study_plan_generator_schema():
    from agents.study_plan_generator import StudyPlanGenerator
    agent = StudyPlanGenerator()
    emp = dict(EMP001)
    emp["_learning_path"] = {
        "total_hours": 36,
        "learning_path": [{"topic": "Azure Fundamentals", "hours": 6, "priority": "HIGH"}],
    }
    result = agent.run(emp, SAMPLE_DOCS)
    assert "weekly_plan" in result
    assert "total_weeks" in result
    assert result["total_weeks"] > 0


# Agent 4: Engagement Agent
def test_engagement_agent_schema():
    from agents.engagement_agent import EngagementAgent
    agent = EngagementAgent()
    result = agent.run(EMP001, SAMPLE_DOCS)
    assert "study_slots" in result
    assert "capacity_flag" in result
    assert "reminder_messages" in result
    assert len(result["reminder_messages"]) == 3


# Agent 5: Assessment Agent
def test_assessment_agent_verdicts():
    from agents.assessment_agent import AssessmentAgent
    agent = AssessmentAgent()
    # EMP-002: score 78 → GO
    emp2 = get_employee("EMP-002")
    result = agent.run(emp2, SAMPLE_DOCS)
    assert result["verdict"] == "GO"


def test_assessment_agent_not_yet():
    from agents.assessment_agent import AssessmentAgent
    agent = AssessmentAgent()
    result = agent.run(EMP003, SAMPLE_DOCS)
    assert result["verdict"] == "NOT YET"
    assert result["trigger_loop_back"] == True


def test_assessment_agent_conditional_go():
    from agents.assessment_agent import AssessmentAgent
    agent = AssessmentAgent()
    emp = dict(EMP001)
    emp["current_practice_score"] = 68
    result = agent.run(emp, SAMPLE_DOCS)
    assert result["verdict"] == "CONDITIONAL GO"


def test_assessment_agent_schema():
    from agents.assessment_agent import AssessmentAgent
    agent = AssessmentAgent()
    result = agent.run(EMP001, SAMPLE_DOCS)
    assert "verdict" in result
    assert "practice_score" in result
    assert "trigger_loop_back" in result
    assert "weak_areas" in result


# Agent 6: Peer Benchmarking
def test_peer_benchmarking_schema():
    from agents.peer_benchmarking_agent import PeerBenchmarkingAgent
    agent = PeerBenchmarkingAgent()
    result = agent.run(EMP001, SAMPLE_DOCS)
    assert "percentile" in result
    assert "cohort_avg_score" in result
    assert "benchmark_insight" in result
    assert "motivation_message" in result


def test_peer_benchmarking_percentile_range():
    from agents.peer_benchmarking_agent import PeerBenchmarkingAgent
    agent = PeerBenchmarkingAgent()
    result = agent.run(EMP001, SAMPLE_DOCS)
    assert 0 <= result["percentile"] <= 100


# Agent 7: ROI Calculator
def test_roi_calculator_schema():
    from agents.roi_calculator_agent import ROICalculatorAgent
    agent = ROICalculatorAgent()
    emp = dict(EMP001)
    emp["_study_plan"] = {"total_weeks": 6}
    result = agent.run(emp, SAMPLE_DOCS)
    assert "total_roi_usd" in result
    assert "cost_savings_usd" in result
    assert "roi_message" in result
    assert result["total_roi_usd"] > 0


# Agent 8: Intervention
def test_intervention_agent_schema():
    from agents.intervention_agent import InterventionAgent
    agent = InterventionAgent()
    result = agent.run(EMP003, SAMPLE_DOCS)
    assert "intervention_level" in result
    assert "manager_email_draft" in result
    assert "employee_message" in result
    assert "escalation_triggered" in result
    assert result["escalation_triggered"] == True


def test_intervention_email_contains_name():
    from agents.intervention_agent import InterventionAgent
    agent = InterventionAgent()
    result = agent.run(EMP003, SAMPLE_DOCS)
    assert "Morgan Lee" in result["manager_email_draft"]


# Agent 9: Manager Insights
def test_manager_insights_schema():
    from agents.manager_insights_agent import ManagerInsightsAgent
    agent = ManagerInsightsAgent()
    result = agent.run({"team_id": "TEAM-A"}, SAMPLE_DOCS)
    assert "team_readiness_score" in result
    assert "member_status" in result


# Agent 10: Readiness Forecaster
def test_readiness_forecaster_schema():
    from agents.readiness_forecaster import ReadinessForecaster
    agent = ReadinessForecaster()
    result = agent.run(EMP001, SAMPLE_DOCS)
    assert "weeks_to_ready" in result
    assert "score_velocity" in result
    assert "confidence" in result
    assert "trend" in result
    assert result["trend"] in ["ACCELERATING", "STEADY", "DECELERATING"]


def test_readiness_forecaster_emp002_ready():
    from agents.readiness_forecaster import ReadinessForecaster
    agent = ReadinessForecaster()
    result = agent.run(get_employee("EMP-002"), SAMPLE_DOCS)
    assert result["weeks_to_ready"] == 0.0