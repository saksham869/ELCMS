# CertifyIQ — Workforce AI Readiness Intelligence

> **Microsoft Agents League Hackathon 2026 · Reasoning Agents Track**

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%205.0-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Azure AI](https://img.shields.io/badge/AI-Azure%20AI%20Foundry-0078D4?logo=microsoft-azure)](https://azure.microsoft.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python)](https://python.org)

---

## The Problem

Companies invest millions in Azure — then lose the return because their teams aren't certified to use it.

| Statistic | Source |
|-----------|--------|
| $5.5T global skills gap cost by 2026 | IDC |
| 90%+ enterprises face critical skills shortages | World Economic Forum |
| Only 17.7% of organisations qualify as AI readiness leaders | Microsoft AI Readiness Survey |
| $165 per Microsoft exam attempt, 42% unguided fail rate | Microsoft exam data |
| $20.4B certification management market, 14.95% CAGR | Market Research |

**CertifyIQ predicts certification failure 6 weeks before it happens — and automatically generates the intervention.**

---

## How It Works

```
Predict → Prevent → Prove
```

- **Predict** — Readiness Forecaster calculates exam-ready date with confidence level, 6 weeks out
- **Prevent** — Intervention Agent generates manager escalation with a specific action plan before failure becomes inevitable
- **Prove** — ROI Calculator quantifies the cost of doing nothing vs guided preparation, per employee and per team

---

## 10-Agent Pipeline

| # | Agent | Role |
|---|-------|------|
| 1 | Learner Profiler | Builds employee cognitive + schedule profile |
| 2 | Learning Path Curator | Maps optimal certification path from Foundry IQ |
| 3 | Study Plan Generator | Creates week-by-week study schedule |
| 4 | Engagement Agent | Scores study consistency and momentum |
| 5 | Assessment Agent | Evaluates current readiness vs passing threshold |
| 6 | Peer Benchmarking | Compares against 50-member synthetic cohort |
| 7 | ROI Calculator | Quantifies cost of failure vs guided prep |
| 8 | Intervention Agent | Generates manager email + action plan |
| 9 | Manager Insights | Surfaces team-level patterns |
| 10 | Readiness Forecaster | Delivers GO / CONDITIONAL GO / APPROACHING / NOT YET verdict |
| + | Query Agent | Natural language: "Who is most at risk this month?" |

Agents 6, 7, and 8 run in parallel. If verdict is NOT YET, the pipeline loops back automatically (max 2×).

---

## Features

- **Real-time token streaming** — GPT-4o tokens streamed via SSE as agents reason
- **Azure AI Foundry IQ** — 12-document knowledge base grounding every agent decision
- **25-rule Responsible AI pipeline** — every output validated before reaching the UI
- **4-tier LLM fallback** — GitHub Models GPT-4o → OpenAI → Anthropic → Mock (demo always works)
- **Natural language query** — "Who is most at risk?" answered from live employee data
- **Audit trail** — append-only, tamper-evident log of every agent decision with RAI pass/fail
- **ROI Calculator** — live financial impact (guided vs unguided), 1/3/5-year projections, PDF export
- **Webhook simulation** — `intervention.triggered` event architecture
- **44 tests passing** — pytest coverage across agents and orchestrator

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Framer Motion, Recharts |
| Backend | Python FastAPI, Uvicorn |
| AI Runtime | GitHub Models GPT-4o (Tier 1), Azure OpenAI (Tier 2) |
| Knowledge | Azure AI Search — Foundry IQ index (12 docs) |
| Streaming | Server-Sent Events (SSE) |
| Auth | Cookie-based demo auth |

---

## Quick Start

### Frontend
```bash
cd certify-iq/frontend
npm install
npm run dev
# → http://localhost:3000  (password: certifyiq2026)
```

### Backend
```bash
cd certify-iq/backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
# → http://localhost:8000/docs
```

### Environment Variables (backend)
```env
GITHUB_TOKEN=your_github_token          # Tier 1: GitHub Models GPT-4o
AZURE_SEARCH_ENDPOINT=your_endpoint     # Foundry IQ knowledge retrieval
AZURE_SEARCH_KEY=your_key
AZURE_SEARCH_INDEX=learning-knowledge
MOCK_MODE=false                         # true = demo without API keys
```

---

## Project Structure

```
ELCMS/
└── certify-iq/
    ├── frontend/           # Next.js app
    │   └── app/
    │       ├── page.tsx            # Overview + employee cards
    │       ├── certify/[id]/       # 10-agent analysis per employee
    │       ├── dashboard/          # Team certification intelligence
    │       ├── roi/                # ROI calculator
    │       ├── business/           # Business case & pricing
    │       └── audit/              # Agent decision log
    └── backend/            # FastAPI server
        ├── agents/                 # 11 reasoning agents
        ├── orchestrator/           # Pipeline coordinator
        ├── foundry/                # Azure AI Search retrieval
        ├── responsible_ai/         # 25-rule guardrail pipeline
        ├── fallback/               # 4-tier LLM fallback
        ├── audit/                  # Append-only audit logger
        └── data/                   # Synthetic employee data
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | System status, Foundry IQ connection |
| GET | `/api/employees` | List all employees |
| GET | `/api/employees/{id}` | Single employee profile |
| GET | `/api/certify/{id}/stream` | Run 10-agent pipeline (SSE stream) |
| GET | `/api/team/{id}/dashboard` | Team-level readiness summary |
| POST | `/api/query` | Natural language query |
| POST | `/api/webhooks/simulate` | Simulate intervention webhook |

---

## Readiness Verdicts

| Verdict | Meaning |
|---------|---------|
| **GO** | Ready — pass probability high, proceed to exam |
| **CONDITIONAL GO** | Ready with conditions — address flagged gaps first |
| **APPROACHING** | On track but needs focused effort |
| **NOT YET** | Significant gaps — pipeline loops back, intervention triggered |

---

## Built By

**Satyam Mishra** — [github.com/saksham869](https://github.com/saksham869)

Microsoft Agents League Hackathon 2026