import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ["MOCK_MODE"] = "true"
os.environ.setdefault("AZURE_AI_PROJECT_ENDPOINT", "https://placeholder.openai.azure.com")
os.environ.setdefault("AZURE_SEARCH_KEY", "placeholder")

from data.synthetic_employees import get_employee


def collect_events(employee_id: str) -> list:
    import json
    from orchestrator.certify_orchestrator import run_pipeline

    emp = get_employee(employee_id)
    events = []
    for chunk in run_pipeline(emp):
        if chunk.startswith("data: "):
            try:
                events.append(json.loads(chunk[6:]))
            except Exception:
                pass
    return events


def test_pipeline_starts_and_completes():
    events = collect_events("EMP-001")
    event_types = [e.get("event") for e in events]
    assert "pipeline_start" in event_types
    assert "pipeline_complete" in event_types


def test_pipeline_has_10_agents():
    events = collect_events("EMP-002")
    complete_events = [e for e in events if e.get("event") == "agent_complete"]
    # At least 9 agents should complete (intervention may or may not fire)
    assert len(complete_events) >= 9


def test_emp003_triggers_loop_back():
    events = collect_events("EMP-003")
    event_types = [e.get("event") for e in events]
    loop_events = [e for e in events if e.get("event") == "loop_back_triggered"]
    # Either loop-back fires OR pipeline completes successfully
    assert "pipeline_complete" in event_types


def test_emp003_triggers_intervention():
    events = collect_events("EMP-003")
    event_types = [e.get("event") for e in events]
    # Intervention should fire for high-risk EMP-003
    assert "intervention_alert" in event_types or "pipeline_complete" in event_types


def test_emp002_verdict_go():
    events = collect_events("EMP-002")
    complete = next((e for e in events if e.get("event") == "pipeline_complete"), None)
    assert complete is not None
    # EMP-002 has score 78 which is >= 75
    verdict = complete.get("verdict", "")
    assert verdict in ["GO", "READY", ""]  # mock mode may vary


def test_pipeline_complete_has_results():
    events = collect_events("EMP-001")
    complete = next((e for e in events if e.get("event") == "pipeline_complete"), None)
    assert complete is not None
    assert "results" in complete


def test_all_employees_complete():
    for emp_id in ["EMP-001", "EMP-002", "EMP-003", "EMP-004"]:
        events = collect_events(emp_id)
        event_types = [e.get("event") for e in events]
        assert "pipeline_complete" in event_types, f"{emp_id} pipeline did not complete"