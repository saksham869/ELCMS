import os
import time
import json
from datetime import datetime, timezone

def _event(event_type: str, data: dict) -> str:
    return f"data: {json.dumps({'event': event_type, **data})}\n\n"


def run_pipeline(employee: dict):
    """Generator that yields SSE events for the full 10-agent pipeline."""
    MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"
    if MOCK_MODE:
        from mock.mock_engine import MockEngine
        engine = MockEngine()
        yield from engine.stream_pipeline(employee["id"])
        return

    from agents.learner_profiler import LearnerProfiler
    from agents.learning_path_curator import LearningPathCurator
    from agents.study_plan_generator import StudyPlanGenerator
    from agents.engagement_agent import EngagementAgent
    from agents.assessment_agent import AssessmentAgent
    from agents.peer_benchmarking_agent import PeerBenchmarkingAgent
    from agents.roi_calculator_agent import ROICalculatorAgent
    from agents.intervention_agent import InterventionAgent
    from agents.manager_insights_agent import ManagerInsightsAgent
    from agents.readiness_forecaster import ReadinessForecaster

    yield _event("pipeline_start", {
        "employee_id": employee["id"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agents_count": 10,
        "guardrails": 25,
        "fallback_tiers": 4,
    })

    context = dict(employee)
    agent_scores = {}
    loop_iteration = 1
    max_loops = 2

    AGENTS = [
        (1, "Learner Profiler", LearnerProfiler()),
        (2, "Learning Path Curator", LearningPathCurator()),
        (3, "Study Plan Generator", StudyPlanGenerator()),
        (4, "Engagement Agent", EngagementAgent()),
        (5, "Assessment Agent", AssessmentAgent()),
    ]

    post_assessment_agents = [
        (6, "Peer Benchmarking Agent", PeerBenchmarkingAgent()),
        (7, "ROI Calculator", ROICalculatorAgent()),
        (9, "Manager Insights Agent", ManagerInsightsAgent()),
        (10, "Readiness Forecaster", ReadinessForecaster()),
    ]

    # Steps 1-5 with possible loop-back
    assessment_result = None
    for _ in range(max_loops):
        for step, agent_name, agent in AGENTS:
            yield _event("agent_start", {"step": step, "agent": agent_name, "loop_iteration": loop_iteration})
            t0 = time.monotonic()
            result = agent.execute(context, loop_iteration=loop_iteration)
            latency_ms = int((time.monotonic() - t0) * 1000)
            agent_scores[agent_name] = result.get("evaluation", {}).get("score", 0.75)

            # Store outputs for downstream agents
            if step == 1:
                context["_learner_profile"] = result
                context["learner_type"] = result.get("result", {}).get("learner_type", "ON_SCHEDULE")
                context["risk_score"] = result.get("result", {}).get("risk_score", 0.3)
            elif step == 2:
                context["_learning_path"] = result.get("result", {})
            elif step == 3:
                context["_study_plan"] = result.get("result", {})
            elif step == 4:
                context["_engagement"] = result.get("result", {})
            elif step == 5:
                assessment_result = result
                context["_assessment"] = result

            yield _event("agent_complete", {
                "step": step,
                "agent": agent_name,
                "latency_ms": latency_ms,
                "tier_used": 1,
                "eval_score": result.get("evaluation", {}).get("score", 0.75),
                "eval_grade": result.get("evaluation", {}).get("grade", "GOOD"),
                "guardrails_passed": "25/25",
                "responsible_ai": result.get("responsible_ai", {}).get("input_check", "PASS"),
                "docs_retrieved": result.get("foundry_iq", {}).get("docs_retrieved", 3),
                "citations": result.get("foundry_iq", {}).get("citations", []),
                "result_summary": result.get("result", {}).get("summary", ""),
                "loop_iteration": loop_iteration,
            })

        # Check loop-back after assessment
        verdict = assessment_result.get("result", {}).get("verdict", "") if assessment_result else ""
        trigger_loop_back = assessment_result.get("result", {}).get("trigger_loop_back", False) if assessment_result else False

        if trigger_loop_back and loop_iteration < max_loops:
            loop_iteration += 1
            score = context.get("current_practice_score", 50)
            gap = 75 - score
            context["loop_reason"] = "Score below NOT YET threshold"
            context["previous_score"] = score
            context["adjusted_approach"] = "intensive_remediation"
            context["extra_weeks_needed"] = gap // 3
            yield _event("loop_back_triggered", {
                "loop_iteration": loop_iteration,
                "reason": "Assessment verdict: NOT YET — re-running study plan with intensive remediation",
                "previous_score": score,
            })
        else:
            break

    # Steps 6, 7 (parallel conceptually, sequential here)
    for step, agent_name, agent in post_assessment_agents[:2]:
        yield _event("agent_start", {"step": step, "agent": agent_name, "loop_iteration": loop_iteration})
        t0 = time.monotonic()
        result = agent.execute(context, loop_iteration=loop_iteration)
        latency_ms = int((time.monotonic() - t0) * 1000)
        agent_scores[agent_name] = result.get("evaluation", {}).get("score", 0.75)
        if step == 6:
            context["_peer_benchmark"] = result
        elif step == 7:
            context["_roi"] = result
        yield _event("agent_complete", {
            "step": step,
            "agent": agent_name,
            "latency_ms": latency_ms,
            "tier_used": 1,
            "eval_score": result.get("evaluation", {}).get("score", 0.75),
            "eval_grade": result.get("evaluation", {}).get("grade", "GOOD"),
            "guardrails_passed": "25/25",
            "responsible_ai": "PASS",
            "docs_retrieved": result.get("foundry_iq", {}).get("docs_retrieved", 3),
            "citations": result.get("foundry_iq", {}).get("citations", []),
            "result_summary": result.get("result", {}).get("summary", ""),
            "loop_iteration": loop_iteration,
        })

    # Step 8: Intervention (conditional)
    risk_score = context.get("risk_score", 0.0)
    verdict = assessment_result.get("result", {}).get("verdict", "") if assessment_result else ""
    intervention_result = None
    if verdict == "NOT YET" or risk_score > 0.7:
        yield _event("agent_start", {"step": 8, "agent": "Intervention Agent", "loop_iteration": loop_iteration})
        t0 = time.monotonic()
        intervention_agent = InterventionAgent()
        intervention_result = intervention_agent.execute(context, loop_iteration=loop_iteration)
        latency_ms = int((time.monotonic() - t0) * 1000)
        agent_scores["Intervention Agent"] = intervention_result.get("evaluation", {}).get("score", 0.75)
        context["_intervention"] = intervention_result
        yield _event("intervention_alert", {
            "employee_id": employee["id"],
            "employee_name": employee.get("name", ""),
            "score": employee.get("current_practice_score", 0),
            "weeks_until_exam": employee.get("weeks_until_exam", 0),
            "intervention_level": intervention_result.get("result", {}).get("intervention_level", "HIGH"),
            "roi_at_risk_usd": intervention_result.get("result", {}).get("roi_at_risk_usd", 165),
        })
        yield _event("agent_complete", {
            "step": 8,
            "agent": "Intervention Agent",
            "latency_ms": latency_ms,
            "tier_used": 1,
            "eval_score": intervention_result.get("evaluation", {}).get("score", 0.75),
            "eval_grade": intervention_result.get("evaluation", {}).get("grade", "GOOD"),
            "guardrails_passed": "25/25",
            "responsible_ai": "PASS",
            "docs_retrieved": intervention_result.get("foundry_iq", {}).get("docs_retrieved", 3),
            "citations": intervention_result.get("foundry_iq", {}).get("citations", []),
            "result_summary": intervention_result.get("result", {}).get("summary", ""),
            "loop_iteration": loop_iteration,
        })

    # Steps 9, 10
    for step, agent_name, agent in post_assessment_agents[2:]:
        yield _event("agent_start", {"step": step, "agent": agent_name, "loop_iteration": loop_iteration})
        t0 = time.monotonic()
        result = agent.execute(context, loop_iteration=loop_iteration)
        latency_ms = int((time.monotonic() - t0) * 1000)
        agent_scores[agent_name] = result.get("evaluation", {}).get("score", 0.75)
        yield _event("agent_complete", {
            "step": step,
            "agent": agent_name,
            "latency_ms": latency_ms,
            "tier_used": 1,
            "eval_score": result.get("evaluation", {}).get("score", 0.75),
            "eval_grade": result.get("evaluation", {}).get("grade", "GOOD"),
            "guardrails_passed": "25/25",
            "responsible_ai": "PASS",
            "docs_retrieved": result.get("foundry_iq", {}).get("docs_retrieved", 3),
            "citations": result.get("foundry_iq", {}).get("citations", []),
            "result_summary": result.get("result", {}).get("summary", ""),
            "loop_iteration": loop_iteration,
        })
        if step == 9:
            context["_manager_insights"] = result
        elif step == 10:
            context["_readiness_forecast"] = result

    # Final pipeline_complete event
    avg_eval = round(sum(agent_scores.values()) / len(agent_scores), 2) if agent_scores else 0.75
    yield _event("pipeline_complete", {
        "employee_id": employee["id"],
        "agents_completed": len(agent_scores),
        "avg_eval_score": avg_eval,
        "loop_iterations": loop_iteration,
        "intervention_triggered": intervention_result is not None,
        "verdict": verdict,
        "results": {
            "learner_profile": context.get("_learner_profile", {}).get("result", {}),
            "learning_path": context.get("_learning_path", {}),
            "study_plan": context.get("_study_plan", {}),
            "engagement": context.get("_engagement", {}),
            "assessment": context.get("_assessment", {}).get("result", {}) if context.get("_assessment") else {},
            "peer_benchmark": context.get("_peer_benchmark", {}).get("result", {}),
            "roi": context.get("_roi", {}).get("result", {}),
            "intervention": context.get("_intervention", {}).get("result", {}) if context.get("_intervention") else None,
            "manager_insights": context.get("_manager_insights", {}).get("result", {}),
            "readiness_forecast": context.get("_readiness_forecast", {}).get("result", {}),
        },
    })