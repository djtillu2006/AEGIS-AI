# Aegis AI
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg)](backend/requirements.txt)
[![React + Vite](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg)](frontend/package.json)

**Human-in-the-loop supply-chain intelligence for maritime route and disruption review.**

Aegis AI helps operators inspect disruption signals, compare maritime route options, review compliance documents, and keep a **human accountable** for every consequential recommendation. It is built as a transparent research and demonstration system, not as an autonomous execution engine.

> Default demos use mock and synthetic data. Outputs must be independently reviewed before they inform operational, compliance, or financial decisions.

## Features

- Multi-agent workflow for market, digital twin, logistics, carbon compliance, and trust audit analysis
- Interactive 2D and 3D maritime route maps
- Risk-based route colors with Red Sea crisis overlays
- Route comparison and alternate-corridor planning
- Compliance, audit, and human approval workflows
- Mock-data fallbacks for local development without paid provider keys

## Stack

- Backend: Python 3.11+, FastAPI, SQLite
- Frontend: React 18, TypeScript/JavaScript, Vite, Deck.gl
- Package manager: pnpm

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- [pnpm](https://pnpm.io/)

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
Copy-Item .env.example .env
python start_server.py
```

API: `http://localhost:8000`

### API Pipeline

The backend pipeline is organized into agents under `backend/agents`, typed models under `backend/models`, API routes under `backend/api`, persistence under `backend/db`, and provider adapters under `backend/services`.

The starter pipeline uses deterministic mock fallbacks and does not require paid provider keys:

```text
POST /api/risk/{port_name}
POST /api/simulate
POST /api/orchestrate
POST /api/compliance
POST /api/audit
POST /api/pipeline/run
POST /api/pipeline/approve/{audit_log_id}
```

The pipeline does not automatically execute a route plan. Approval remains a human decision.

### Frontend

```bash
cd frontend
pnpm install --frozen-lockfile
Copy-Item .env.example .env
pnpm dev
```

UI: `http://localhost:5173`

### Demo flow

1. Open `/pay` and choose **Watch Demo**.
2. Select an origin and destination, such as Netherlands to Shanghai.
3. Start the simulation and compare the available routes.
4. Activate the Red Sea crisis to see the affected route turn red and the safer alternative turn green.

## Configuration

Use `backend/.env.example` and `frontend/.env.example` as templates. Do not commit API keys, Clerk credentials, private allowlists, uploads, or production data.

| File | Purpose |
| --- | --- |
| `backend/.env.example` | API, optional LLM providers, Clerk issuer, allowlist |
| `frontend/.env.example` | Vite public Clerk key stub and API base URL |

The Vite development proxy sends `/api` requests to `http://127.0.0.1:8000`. A deployed frontend requires a publicly reachable backend API URL and matching production environment variables.

## Deployment

The frontend is deployed on Netlify:

https://aegis-ai-frontend.netlify.app

The backend must be deployed separately for API-backed features to work outside the local development environment.

Local checks before review:

```powershell
python -m compileall -q backend
cd frontend
pnpm build
```

## Safety Notice

Aegis AI is not a substitute for professional maritime, legal, compliance, financial, or operational advice. Verify all data, route conditions, regulations, and recommendations independently before use.

## License

This repository is currently a demonstration project. Add the project license and contribution policy before accepting external contributions.
