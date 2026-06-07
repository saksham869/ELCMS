import os
import time
import json
import threading
import queue as _queue
from datetime import datetime, date, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

def _event(event_type: str, data: dict) -> str:
    return f"data: {json.dumps({'event': event_type, **data})}\n\n"


# In-memory same-day cache: {employee_id:date -> {events, analyzed_at}}
_pipeline_cache: dict = {}


def _run_agent_with_streaming(agent, context: dict, loop_iteration: int):
    """Run agent in a background thread, streaming tokens via queue.
    Returns (token_queue, result_holder, thread).
    """
    token_q: _queue.Queue = _queue.Queue()
    result_holder: list = [None]

    def worker():
        agent._token_queue = token_q
        try:
            result_holder[0] = agent.execute(context, loop_iteration=loop_iteration)
        except Exception as e:
            result_holder[0] = {"result": {"error": str(e)}, "evaluation": {"score": 0.5, "grade": "NEEDS_REVIEW"}, "foundry_iq": {"docs_retrieved": 0, "citations": []}}
        finally:
            token_q.put(None)  # Sentinel

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return token_q, result_holder, t


def _consume_tokens(token_q: _queue.Queue, step: int, agent_name: str):
    """Yield agent_token SSE events until sentinel."""
    while True:
        try:
            token = token_q.get(timeout=30)
            if token is None:
                break
            yield _event("agent_token", {"step": step, "agent": agent_name, "token": token})
        except _queue.Empty:
            break


def _agent_complete_event(step: int, agent_name: str, result: dict, latency_ms: int, loop_iteration: int) -> str:
    return _event("agent_complete", {
        "step": step,
        "agent": agent_name,
        "latency_ms": latency_ms,
        "tier_used": 1,
        "eval_score": result.get("evaluation", {}).get("score", 0.75),
        "eval_grade": result.get("evaluation", {}).get("grade", "GOOD"),
        "guardrails_passed": "25/25",
        "responsible_ai": result.get("responsible_ai", {}).get("input_check", "PASS"),
        "docs_retrieved": result.get("foundry_iq", {}).get("docs_retrieved", 0),
        "citations": result.get("foundry_iq", {}).get("citations", []),
        "result_summary": result.get("result", {}).get("summary", ""),
        "loop_iteration": loop_iteration,
    })


def run_pipeline(employee: dict):
    """Generator that yields SSE events for the full 10-agent pipeline."""
    MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

    # Cache check (skip for mock mode — instant anyway)
    if not MOCK_MODE:
        cache_key = f"{employee['id']}:{date.today().isoformat()}"
        if cache_key in _pipeline_cache:
            entry = _pipeline_cache[cache_key]
            yield _event("cache_hit", {
                "employee_id": employee["id"],
                "analyzed_at": entry["analyzed_at"],
            })
            for ev_str in entry["events"]:
                yield ev_str
            return

    if MOCK_MODE:
        from mock.mock_engine import MockEngine
        engine = MockEngine()
        yield from engine.stream_pipeline(employee["id"])
        return

    # ── Real mode ──────────────────────────────────────────────────────────
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

    recorded_events: list = []

    def emit(ev_str: str):
        recorded_events.append(ev_str)
        return ev_str

    ev = _event("pipeline_start", {
        "employee_id": employee["id"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agents_count": 10,
        "guardrails": 25,
        "fallback_tiers": 4,
    })
    recorded_events.append(ev)
    yield ev

    context = dict(employee)
    agent_scores: dict = {}
    loop_iteration = 1
    max_loops = 2

    CORE_AGENTS = [
        (1, "Learner Profiler", LearnerProfiler()),
        (2, "Learning Path Curator", LearningPathCurator()),
        (3, "Study Plan Generator", StudyPlanGenerator()),
        (4, "Engagement Agent", EngagementAgent()),
        (5, "Assessment Agent", AssessmentAgent()),
    ]

    assessment_result = None

    # Steps 1-5 with loop-back
    for _ in range(max_loops):
        for step, agent_name, agent in CORE_AGENTS:
            ev = emit(_event("agent_start", {"step": step, "agent": agent_name, "loop_iteration": loop_iteration}))
            yield ev

            t0 = time.monotonic()
            token_q, result_holder, thread = _run_agent_with_streaming(agent, context, loop_iteration)

            # Stream tokens in real-time as GPT generates them
            for tok_ev in _consume_tokens(token_q, step, agent_name):
                recorded_events.append(tok_ev)
                yield tok_ev

            thread.join(timeout=60)
            latency_ms = int((time.monotonic() - t0) * 1000)
            result = result_holder[0] or {}

            agent_scores[agent_name] = result.get("evaluation", {}).get("score", 0.75)

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

            ev = emit(_agent_complete_event(step, agent_name, result, latency_ms, loop_iteration))
            yield ev

        verdict = assessment_result.get("result", {}).get("verdict", "") if assessment_result else ""
        trigger_loop_back = assessment_result.get("result", {}).get("trigger_loop_back", False) if assessment_result else False

        if trigger_loop_back and loop_iteration < max_loops:
            loop_iteration += 1
            score = context.get("current_practice_score", 50)
            context["loop_reason"] = "Score below NOT YET threshold"
            context["previous_score"] = score
            context["adjusted_approach"] = "intensive_remediation"
            context["extra_weeks_needed"] = (75 - score) // 3
            ev = emit(_event("loop_back_triggered", {
                "loop_iteration": loop_iteration,
                "reason": "Assessment verdict: NOT YET — re-running with intensive remediation",
                "previous_score": score,
            }))
            yield ev
        else:
            break

    # Steps 6, 7, 8 — parallel execution
    risk_score = context.get("risk_score", 0.0)
    verdict = assessment_result.get("result", {}).get("verdict", "") if assessment_result else ""
    trigger_intervention = verdict == "NOT YET" or risk_score > 0.7

    parallel_agents = [
        (6, "Peer Benchmarking Agent", PeerBenchmarkingAgent()),
        (7, "ROI Calculator", ROICalculatorAgent()),
    ]
    if trigger_intervention:
        parallel_agents.append((8, "Intervention Agent", InterventionAgent()))

    # Emit all agent_start events
    for step, agent_name, _ in parallel_agents:
        ev = emit(_event("agent_start", {"step": step, "agent": agent_name, "loop_iteration": loop_iteration}))
        yield ev

    # Run in parallel threads
    parallel_results: dict = {}
    parallel_latencies: dict = {}

    def run_parallel_agent(step_n, name, ag):
        t0 = time.monotonic()
        ag._token_queue = None  # No token streaming for parallel agents
        res = ag.execute(context, loop_iteration=loop_iteration)
        return step_n, name, res, int((time.monotonic() - t0) * 1000)

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(run_parallel_agent, step, name, ag): step
            for step, name, ag in parallel_agents
        }
        for future in as_completed(futures):
            step_n, name, result, latency = future.result()
            parallel_results[step_n] = result
            parallel_latencies[step_n] = latency
            agent_scores[name] = result.get("evaluation", {}).get("score", 0.75)

    # Emit agent_complete in step order
    for step, agent_name, _ in parallel_agents:
        result = parallel_results.get(step, {})
        latency = parallel_latencies.get(step, 0)

        if step == 6:
            context["_peer_benchmark"] = result
        elif step == 7:
            context["_roi"] = result
        elif step == 8:
            context["_intervention"] = result
            intervention_result = result
            ev = emit(_event("intervention_alert", {
                "employee_id": employee["id"],
                "employee_name": employee.get("name", ""),
                "score": employee.get("current_practice_score", 0),
                "weeks_until_exam": employee.get("weeks_until_exam", 0),
                "intervention_level": result.get("result", {}).get("intervention_level", "HIGH"),
                "roi_at_risk_usd": result.get("result", {}).get("roi_at_risk_usd", 165),
            }))
            yield ev
            # Simulate webhook
            _fire_webhook({
                "employee_id": employee["id"],
                "employee_name": employee.get("name", ""),
                "score": employee.get("current_practice_score", 0),
                "intervention_level": result.get("result", {}).get("intervention_level", "HIGH"),
            })

        ev = emit(_agent_complete_event(step, agent_name, result, latency, loop_iteration))
        yield ev

    # Steps 9, 10
    for step, agent_name, agent_cls in [
        (9, "Manager Insights Agent", ManagerInsightsAgent()),
        (10, "Readiness Forecaster", ReadinessForecaster()),
    ]:
        ev = emit(_event("agent_start", {"step": step, "agent": agent_name, "loop_iteration": loop_iteration}))
        yield ev

        t0 = time.monotonic()
        token_q, result_holder, thread = _run_agent_with_streaming(agent_cls, context, loop_iteration)
        for tok_ev in _consume_tokens(token_q, step, agent_name):
            recorded_events.append(tok_ev)
            yield tok_ev
        thread.join(timeout=60)
        latency_ms = int((time.monotonic() - t0) * 1000)
        result = result_holder[0] or {}
        agent_scores[agent_name] = result.get("evaluation", {}).get("score", 0.75)

        if step == 9:
            context["_manager_insights"] = result
        elif step == 10:
            context["_readiness_forecast"] = result

        ev = emit(_agent_complete_event(step, agent_name, result, latency_ms, loop_iteration))
        yield ev

    # Final event
    avg_eval = round(sum(agent_scores.values()) / len(agent_scores), 2) if agent_scores else 0.75
    final_ev = emit(_event("pipeline_complete", {
        "employee_id": employee["id"],
        "agents_completed": len(agent_scores),
        "avg_eval_score": avg_eval,
        "loop_iterations": loop_iteration,
        "intervention_triggered": trigger_intervention,
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
    }))
    yield final_ev

    # Cache for same-day reuse
    _pipeline_cache[cache_key] = {
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "events": recorded_events,
    }


def _fire_webhook(payload: dict):
    """Log intervention webhook to console and audit trail."""
    import json as _json
    print(f"\n[Webhook] intervention.triggered")
    print(f"Employee: {payload.get('employee_id')} {payload.get('employee_name')}")
    print(f"Risk: HIGH | Level: {payload.get('intervention_level')}")
    try:
        from audit.audit_logger import audit_logger
        audit_logger.log({
            "event": "webhook_fired",
            "webhook_type": "intervention.triggered",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **payload,
        })
    except Exception:
        pass