import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from data.synthetic_employees import get_employee, get_all_employees
from foundry.knowledge_retriever import retriever
from orchestrator.certify_orchestrator import run_pipeline

app = FastAPI(title="CertifyIQ API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    foundry_health = retriever.health_check()
    return {
        "status": "healthy",
        "version": "3.0.0",
        "agents": 10,
        "certifications": 15,
        "guardrails": 25,
        "fallback_tiers": 4,
        "mock_mode": os.getenv("MOCK_MODE", "false").lower() == "true",
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