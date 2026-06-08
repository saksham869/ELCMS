import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from data.synthetic_employees import get_employee, get_all_employees
from foundry.knowledge_retriever import retriever
from orchestrator.certify_orchestrator import run_pipeline

app = FastAPI(title="CertifyIQ API", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/api/health")
def health():
    foundry_health = retriever.health_check()
    return {
        "status": "healthy",
        "version": "5.0.0",
        "agents": 11,
        "certifications": 15,
        "guardrails": 25,
        "fallback_tiers": 4,
        "mock_mode": os.getenv("MOCK_MODE", "false").lower() == "true",
        "features": ["token_streaming", "parallel_agents", "result_caching", "nl_query", "webhook_simulation"],
        "foundry_iq": {
            "document_count": 12,
            "index": os.getenv("AZURE_SEARCH_INDEX", "learning-knowledge"),
            "connected": foundry_health.get("connected", False),
        },
    }


@app.get("/api/employees")
def list_employees():
    return {"employees": get_all_employees()}


@app.get("/api/employees/{employee_id}")
def get_emp(employee_id: str):
    emp = get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@app.get("/api/certify/{employee_id}/stream")
def certify_stream(employee_id: str):
    emp = get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return StreamingResponse(
        run_pipeline(emp),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/team/{team_id}/dashboard")
def team_dashboard(team_id: str):
    from data.synthetic_employees import get_team
    team = get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


class QueryRequest(BaseModel):
    question: str


@app.post("/api/query")
def natural_language_query(req: QueryRequest):
    """Natural language query against employee data + Foundry IQ knowledge."""
    try:
        from agents.query_agent import QueryAgent
        agent = QueryAgent()
        all_employees = get_all_employees()
        result = agent.execute({
            "question": req.question,
            "all_employees": all_employees,
        })
        return result.get("result", {
            "question": req.question,
            "answer": "Unable to process query at this time.",
            "relevant_employees": [],
            "action": "Try again or check backend logs.",
            "citations": [],
            "confidence": 0,
        })
    except Exception as e:
        return {
            "question": req.question,
            "answer": f"Query processing failed: {str(e)[:120]}",
            "relevant_employees": [],
            "action": "Ensure MOCK_MODE=false and GITHUB_TOKEN is set.",
            "citations": [],
            "confidence": 0,
        }


class WebhookPayload(BaseModel):
    employee_id: str = ""
    employee_name: str = ""
    score: int = 0
    intervention_level: str = "HIGH"
    roi_at_risk_usd: int = 165


@app.post("/api/webhooks/simulate")
def simulate_webhook(payload: WebhookPayload):
    """Simulate an intervention webhook — demonstrates production architecture."""
    import json
    from datetime import datetime, timezone
    from audit.audit_logger import audit_logger

    data = payload.dict()
    print(f"\n[Webhook] intervention.triggered")
    print(f"Employee: {payload.employee_id} {payload.employee_name}")
    print(f"Score: {payload.score}% | Level: {payload.intervention_level} | ROI at risk: ${payload.roi_at_risk_usd}")
    print(f"Payload: {json.dumps(data, indent=2)}")

    try:
        audit_logger.log({
            "event": "webhook_fired",
            "webhook_type": "intervention.triggered",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data,
        })
    except Exception:
        pass

    return {
        "webhook_fired": True,
        "event": "intervention.triggered",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": data,
    }