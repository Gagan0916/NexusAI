# NexusAI — Complete Project Documentation

**Version:** 1.0.0  
**Author:** Gagan0916  
**GitHub:** https://github.com/Gagan0916/NexusAI  
**Stack:** Python 3.12 · Streamlit · Multi-Agent Architecture · Groq / Gemini LLM

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Folder Structure](#3-folder-structure)
4. [Architecture & Data Flow](#4-architecture--data-flow)
5. [Agent Reference](#5-agent-reference)
6. [Tools Reference](#6-tools-reference)
7. [UI Pages Reference](#7-ui-pages-reference)
8. [Installation & Local Setup](#8-installation--local-setup)
9. [Environment Variables & API Keys](#9-environment-variables--api-keys)
10. [Running the App](#10-running-the-app)
11. [Deployment Guide](#11-deployment-guide)
12. [GitHub Repository](#12-github-repository)
13. [How Each File Works](#13-how-each-file-works)
14. [Customisation Guide](#14-customisation-guide)
15. [Troubleshooting](#15-troubleshooting)
16. [Tech Stack Summary](#16-tech-stack-summary)
17. [Future Roadmap](#17-future-roadmap)

---

## 1. Project Overview

NexusAI is a **Multi-Agent Startup Validator and Builder** built entirely with
Streamlit. It accepts a plain-English startup idea and runs it through a
pipeline of 8 specialist AI agents that collaborate to produce:

- Market analysis with scoring
- Competitor intelligence
- Customer pain point research
- Business model and unit economics
- Technical architecture design
- Product Requirements Document (PRD)
- MVP feature roadmap
- Starter code
- README, deployment guide, and investor pitch

The app works in two modes:

| Mode | Description |
|------|-------------|
| **Smart Offline Mode** | No API key required. Uses a built-in knowledge base of 7 industries to produce realistic, structured outputs. |
| **LLM Mode** | Adds a free Groq or Gemini API key. Every agent calls the LLM for AI-generated, idea-specific analysis. |

---

## 2. Features

### Core Features
- Single text input → full startup validation in under 60 seconds
- 8 specialist agents running sequentially in a pipeline
- Real-time agent status updates in the UI
- Market scoring: Market Score, Competition Score, Feasibility Score, Sentiment Score
- CEO verdict (Strong / Promising / Risky) with confidence rating
- Competitor cards with stage and weakness analysis
- Customer pain points from Reddit / Hacker News signals
- 90-day MVP roadmap with phases and deliverables
- Unit economics: CAC, LTV, LTV/CAC ratio, payback period, gross margin
- Tech stack recommendation with 6 layers
- Starter FastAPI + Python code ready to use
- 7 downloadable reports (Markdown format)

### Report Downloads
1. Business Plan (market + competitors + unit economics + risks + GTM)
2. Product Requirements Document (PRD)
3. Technical Architecture Document
4. README.md
5. Deployment Guide
6. Investor Pitch Summary
7. Starter Code (.py file)

### UI
- 3-page Streamlit app: Dashboard · Agent Logs · Reports
- Dark cyberpunk theme (navy + neon green + purple)
- Fully responsive layout
- Agent activity log with expandable per-agent detail views

---

## 3. Folder Structure

```
nexusai/
│
├── app.py                        ← Main Streamlit application (entry point)
│
├── agents/                       ← All 8 AI agents
│   ├── __init__.py
│   ├── base_agent.py             ← Abstract base class for all agents
│   ├── ceo_agent.py              ← CEO Agent: strategy + task assignment
│   ├── research_agent.py         ← Market Research Agent
│   ├── sentiment_agent.py        ← Sentiment Agent: pain points + personas
│   ├── analyst_agent.py          ← Business Analyst Agent
│   ├── architect_agent.py        ← Technical Architect Agent
│   ├── pm_agent.py               ← Product Manager Agent
│   ├── engineer_agent.py         ← Software Engineer Agent
│   └── docs_agent.py             ← Documentation Agent
│
├── core/                         ← Orchestration engine
│   ├── __init__.py
│   └── orchestrator.py           ← NexusOrchestrator: runs the agent pipeline
│
├── tools/                        ← Shared utilities
│   ├── __init__.py
│   ├── llm_client.py             ← Groq + Gemini API client with fallback
│   ├── industry_data.py          ← Knowledge base for 7 industries
│   └── report_generator.py       ← Builds downloadable report text
│
├── reports/                      ← Output directory (auto-created, gitignored)
│
├── .streamlit/
│   └── config.toml               ← Streamlit theme and server config
│
├── .env.example                  ← Template for API key configuration
├── .gitignore                    ← Excludes .env, __pycache__, reports/
├── requirements.txt              ← Python dependencies
├── README.md                     ← GitHub repository readme
└── DOCUMENTATION.md              ← This file
```

---

## 4. Architecture & Data Flow

### Pipeline Overview

```
User Input (startup idea)
        │
        ▼
┌─────────────────────┐
│   NexusOrchestrator │  ← core/orchestrator.py
│  (sequential pipeline)
└─────────────────────┘
        │
        ▼ passes context dict between agents
┌──────────────────────────────────────────────┐
│  1. CEO Agent          → context["ceo"]       │
│  2. Market Research    → context["research"]  │
│  3. Sentiment Agent    → context["sentiment"] │
│  4. Business Analyst   → context["analyst"]   │
│  5. Technical Architect→ context["architect"] │
│  6. Product Manager    → context["pm"]        │
│  7. Software Engineer  → context["engineer"]  │
│  8. Documentation      → context["docs"]      │
└──────────────────────────────────────────────┘
        │
        ▼
  Final context dict → Streamlit UI renders results
```

### Context Object

Every agent receives the same growing `context` dictionary and adds its own key:

```python
context = {
    "startup_idea": "AI-powered Interview Preparation Platform",

    # Added by CEO Agent:
    "ceo": {
        "strategic_overview": "...",
        "verdict": "Strong",
        "confidence_score": 8.7,
        "top_risks": [...],
        "key_success_factor": "...",
        "task_plan": [...],
        "industry": { ... }   # full industry KB entry
    },

    # Added by Market Research Agent:
    "research": {
        "market_size": "$28.5B",
        "growth_rate": 14.3,
        "market_demand_score": 8.5,
        "competition_score": 6.2,
        "competitors": [...],
        "key_trends": [...],
        "market_gap": "...",
        "tam_sam_som": { "TAM": "...", "SAM": "...", "SOM": "..." }
    },

    # Added by Sentiment Agent:
    "sentiment": {
        "sentiment_score": 7.8,
        "overall_sentiment": "Positive",
        "pain_points": [...],
        "reddit_signals": [...],
        "willingness_to_pay": "High",
        "customer_quotes": [...],
        "target_personas": [...]
    },

    # Added by Business Analyst Agent:
    "analyst": {
        "feasibility_score": 8.8,
        "business_model": "B2C SaaS subscription",
        "revenue_streams": [...],
        "unit_economics": { "cac": "...", "ltv": "...", ... },
        "risks": [...],
        "go_to_market": [...],
        "break_even_months": 12
    },

    # Added by Technical Architect Agent:
    "architect": {
        "tech_stack": { "frontend": "...", "backend": "...", ... },
        "architecture_style": "...",
        "system_components": [...],
        "database_schema": [...],
        "api_endpoints": [...],
        "scalability_notes": "...",
        "estimated_monthly_infra_cost": "..."
    },

    # Added by Product Manager Agent:
    "pm": {
        "problem_statement": "...",
        "target_user": "...",
        "value_proposition": "...",
        "mvp_features": [...],
        "roadmap": [...],
        "success_metrics": [...],
        "out_of_scope_v1": [...]
    },

    # Added by Software Engineer Agent:
    "engineer": {
        "starter_code": "...",
        "repo_structure": { ... },
        "implementation_steps": [...],
        "packages": [...],
        "env_vars_needed": [...]
    },

    # Added by Documentation Agent:
    "docs": {
        "readme": "...",
        "deployment_guide": "...",
        "pitch_summary": "..."
    }
}
```

### LLM Decision Logic

Each agent uses this decision tree:

```
has_llm()?
   YES → Build a structured JSON prompt → call Groq → if fails, call Gemini
          → parse JSON from response → use as output
   NO  → Use industry knowledge base (industry_data.py) to build output
          → Apply heuristics and templates → return structured dict
```

This ensures the app **always produces output** regardless of API key availability.

---

## 5. Agent Reference

### Agent 1 — CEO Agent (`agents/ceo_agent.py`)

**Role:** Controls the workflow, sets strategy, assigns tasks to all other agents.

**Input:** `startup_idea` string  
**Output key:** `context["ceo"]`

**What it produces:**
- `strategic_overview` — 2-sentence strategy for the idea
- `verdict` — Strong / Promising / Needs Refinement / Risky
- `confidence_score` — 1–10 rating for $1M ARR in 24 months
- `key_success_factor` — single most important thing to get right
- `top_risks` — list of 3 biggest risks
- `task_plan` — list of tasks dispatched to each subsequent agent
- `industry` — detected industry object from knowledge base

**Industry Detection:**  
Uses regex matching on the startup idea text against 7 industry keyword patterns.
Falls back to `general` industry if no match found.

---

### Agent 2 — Market Research Agent (`agents/research_agent.py`)

**Role:** Analyses market size, demand, growth trends, and competitive landscape.

**Input:** reads `context["ceo"]["industry"]`  
**Output key:** `context["research"]`

**What it produces:**
- `market_size` — total market in USD (e.g. "$28.5B")
- `growth_rate` — annual CAGR percentage
- `market_demand_score` — 1–10 score
- `competition_score` — 1–10 (lower = harder market to enter)
- `key_trends` — 3 major market trends
- `competitors` — list of 4 competitors with name, stage, and weakness
- `market_gap` — one-sentence gap this startup can exploit
- `tam_sam_som` — TAM / SAM / SOM breakdown

---

### Agent 3 — Sentiment Agent (`agents/sentiment_agent.py`)

**Role:** Mines Reddit and Hacker News for customer pain points and community sentiment.

**Input:** reads `context["ceo"]["industry"]`  
**Output key:** `context["sentiment"]`

**What it produces:**
- `sentiment_score` — 1–10 community sentiment rating
- `overall_sentiment` — Positive / Mixed / Negative
- `pain_points` — 4 specific customer frustrations
- `reddit_signals` — 3 representative community posts
- `willingness_to_pay` — High / Medium / Low
- `customer_quotes` — 2 example customer statements
- `target_personas` — 2 buyer persona descriptions

---

### Agent 4 — Business Analyst Agent (`agents/analyst_agent.py`)

**Role:** Models business viability, revenue streams, unit economics, and risk register.

**Input:** reads `context["ceo"]` and `context["research"]`  
**Output key:** `context["analyst"]`

**What it produces:**
- `feasibility_score` — 1–10 technical + business feasibility
- `business_model` — e.g. "B2C SaaS subscription"
- `revenue_streams` — list of streams with price and type
- `unit_economics` — CAC, LTV, LTV/CAC ratio, payback period, gross margin
- `risks` — list of risks with severity (High/Medium/Low) and mitigation
- `go_to_market` — 4-step GTM strategy
- `break_even_months` — estimated months to break even

---

### Agent 5 — Technical Architect Agent (`agents/architect_agent.py`)

**Role:** Designs tech stack, system architecture, database schema, and scalability plan.

**Input:** reads `context["ceo"]["industry"]`  
**Output key:** `context["architect"]`

**What it produces:**
- `tech_stack` — 8-layer stack (frontend, backend, database, AI, auth, storage, deployment, CI/CD)
- `architecture_style` — Modular Monolith / Microservices / Monolith
- `system_components` — list of components with purpose
- `database_schema` — key tables with field names
- `api_endpoints` — list of REST endpoints with method and description
- `scalability_notes` — 3-stage scaling plan (100 → 50k → 100k users)
- `estimated_monthly_infra_cost` — launch cost estimate

---

### Agent 6 — Product Manager Agent (`agents/pm_agent.py`)

**Role:** Writes the PRD, defines MVP scope, and builds the 90-day roadmap.

**Input:** reads `context["ceo"]` and `context["sentiment"]["pain_points"]`  
**Output key:** `context["pm"]`

**What it produces:**
- `problem_statement` — one-sentence problem definition
- `target_user` — specific user description
- `value_proposition` — one-sentence value prop
- `mvp_features` — list of 5 features with priority (P0/P1/P2), description, and effort
- `roadmap` — 4 phases (Week 1–2, Week 3–4, Month 2, Month 3) with deliverables
- `success_metrics` — 4 KPIs with targets
- `out_of_scope_v1` — features intentionally deferred

---

### Agent 7 — Software Engineer Agent (`agents/engineer_agent.py`)

**Role:** Generates starter code and the complete repository structure.

**Input:** reads `context["architect"]["tech_stack"]` and `context["pm"]["mvp_features"]`  
**Output key:** `context["engineer"]`

**What it produces:**
- `starter_code` — production-ready FastAPI + Python code with OpenAI integration
- `repo_structure` — complete folder and file tree with descriptions
- `implementation_steps` — 6-step setup guide (clone → run)
- `packages` — full `requirements.txt` package list with versions
- `env_vars_needed` — list of required environment variables with sources
- `github_actions_hint` — CI/CD deployment tip

**When LLM is active:** generates custom code specifically tailored to the startup idea.  
**Offline:** uses a FastAPI template with OpenAI chat completions integration.

---

### Agent 8 — Documentation Agent (`agents/docs_agent.py`)

**Role:** Creates README, deployment guide, and investor pitch summary.

**Input:** reads `context["ceo"]`, `context["architect"]`, `context["pm"]`  
**Output key:** `context["docs"]`

**What it produces:**
- `readme` — full GitHub README with overview, features, quick start, env vars, structure, deployment
- `deployment_guide` — step-by-step guides for Railway, Render, and Streamlit Cloud
- `pitch_summary` — 1-page investor pitch (problem, solution, market, business model, ask)

**When LLM is active:** the pitch summary is enhanced by the LLM for investor-ready language.

---

## 6. Tools Reference

### `tools/llm_client.py` — LLM API Client

Handles all communication with language model APIs.

**Functions:**

| Function | Description |
|----------|-------------|
| `_get_secret(key)` | Reads from `st.secrets` first (Streamlit Cloud), then `os.environ` |
| `call_groq(prompt, temperature)` | Calls Groq API with `llama-3.3-70b-versatile` model |
| `call_gemini(prompt)` | Calls Google Gemini 1.5 Flash API |
| `call_llm(prompt)` | Tries Groq first, falls back to Gemini, returns `None` if both fail |
| `parse_json(text)` | Extracts JSON from LLM response (handles markdown fences and raw JSON) |
| `has_llm()` | Returns `True` if any valid API key is configured |

**Model used:** `llama-3.3-70b-versatile` (Groq) — fastest, highest quality free model.

---

### `tools/industry_data.py` — Industry Knowledge Base

Provides structured startup data for 7 industries used in offline fallback mode.

**Supported Industries:**

| Key | Industry | Trigger Keywords |
|-----|----------|-----------------|
| `hr_tech` | HR Tech / CareerTech | interview, resume, job, career, hiring, recruit |
| `edtech` | EdTech / Learning Platform | education, learn, student, teacher, tutor, course |
| `healthtech` | HealthTech / Digital Health | health, medical, doctor, patient, hospital, wellness |
| `fintech` | FinTech / Financial Technology | finance, payment, bank, invest, crypto, wallet, money |
| `ecommerce` | E-Commerce / Marketplace | shop, store, marketplace, buy, sell, retail |
| `saas` | B2B SaaS / Productivity Tool | saas, software, platform, tool, automation, workflow |
| `ai_product` | AI-Native Product | ai, machine learning, gpt, llm, generative, chatbot |
| `general` | Tech Startup (fallback) | catches all other ideas |

**Each industry entry contains:**
- Market size, growth rate, market demand score, competition score, feasibility score
- 4 real competitors with stage and weakness
- 4 customer pain points
- 3 Reddit/HN community signals
- Revenue models, tech stack, MVP features
- Risk register with mitigations
- Target users, business model, and moat description

**Function:**
```python
detect_industry(idea: str) -> dict
# Runs regex matching on idea text, returns matching industry dict
```

---

### `tools/report_generator.py` — Report Builder

Builds formatted plain-text reports from the final context dictionary.

**Functions:**

| Function | Output |
|----------|--------|
| `build_business_plan(ctx)` | Full business plan (market, competitors, unit economics, risks, GTM, CEO verdict) |
| `build_prd(ctx)` | Product Requirements Document (problem, features, roadmap, metrics) |
| `build_architecture_doc(ctx)` | Technical architecture (stack, components, schema, endpoints, scaling) |
| `save_report(content, filename, dir)` | Saves report to `reports/` directory |

All reports are returned as strings so Streamlit's `st.download_button` can serve them directly without writing to disk.

---

### `core/orchestrator.py` — Agent Pipeline Manager

Manages the sequential execution of all 8 agents.

**Class: `NexusOrchestrator`**

```python
orchestrator = NexusOrchestrator()

# Streaming mode (used in UI for real-time updates):
for agent_name, context in orchestrator.run_streaming("My startup idea"):
    # update UI after each agent completes
    pass

# One-shot mode (used in testing):
final_context = orchestrator.run("My startup idea")
```

**Key method: `run_streaming(startup_idea)`**
- Initialises `context = {"startup_idea": idea}`
- Iterates through all 8 agents in order
- Calls `agent.run(context)`, adds output to context under the agent's key
- Yields `(agent_name, context)` after each agent so the UI can update in real time
- Catches per-agent exceptions without crashing the whole pipeline

---

## 7. UI Pages Reference

### Page 1 — Dashboard (`page_dashboard()` in `app.py`)

**What it shows:**
- Hero banner with app title and subtitle
- LLM status indicator (Active / Offline Mode)
- Startup idea text input + "Validate Idea" button
- During analysis: progress bar + agent status grid (updates live)
- After analysis:
  - CEO Verdict badge
  - 4 score cards: Market Score, Competition, Feasibility, Sentiment
  - Strategic overview panel
  - MVP feature chips
  - Customer pain points list
  - Market snapshot card (industry, size, growth, business model)
  - Competitor cards (4 competitors)
  - Unit economics table
  - 90-day roadmap (4 phase columns)
  - Tech stack cards (6 layers)

---

### Page 2 — Agent Logs (`page_agent_logs()` in `app.py`)

**What it shows:**
- One card per agent showing:
  - Status icon: ⬜ waiting · 🟡 running · ✅ done · ❌ error
  - Agent name, emoji, and role description
  - Completion message with elapsed time
- Each card is expandable to show the full agent output:
  - CEO → strategic overview, verdict, task plan
  - Market Research → metrics, TAM/SAM/SOM, trends
  - Sentiment → pain points, community signals, personas
  - Business Analyst → revenue streams, unit economics, risks, GTM
  - Technical Architect → tech stack, components, schema, endpoints
  - Product Manager → PRD, features, roadmap
  - Software Engineer → starter code, repo structure, setup steps
  - Documentation → README, deployment guide, pitch summary

---

### Page 3 — Reports (`page_reports()` in `app.py`)

**What it shows:**
- 7 individual report cards, each with:
  - Title and description
  - "⬇ Download" button (serves file directly to browser)
  - Expandable preview of the first 1,200 characters
- "Download All Reports" button — single bundled Markdown file
- All filenames include a sanitised version of the startup idea

---

## 8. Installation & Local Setup

### Prerequisites

| Requirement | Version | Check |
|-------------|---------|-------|
| Python | 3.10+ | `python --version` |
| pip | latest | `pip --version` |
| Git | any | `git --version` |

### Step-by-step Setup

**Step 1 — Clone the repository**
```bash
git clone https://github.com/Gagan0916/NexusAI.git
cd NexusAI
```

**Step 2 — Create a virtual environment (recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

**Step 3 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 — Configure API keys (optional)**
```bash
cp .env.example .env
# Open .env and add your keys
```

**Step 5 — Run the app**
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

---

## 9. Environment Variables & API Keys

### `.env` file format
```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Getting Free API Keys

**Groq (Recommended — Fastest)**
1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Click "API Keys" → "Create API Key"
4. Copy key → paste into `.env` as `GROQ_API_KEY`
- Free tier: 14,400 requests/day, 30 requests/minute
- Model used: `llama-3.3-70b-versatile`

**Gemini (Backup)**
1. Go to https://aistudio.google.com
2. Sign in with Google
3. Click "Get API Key" → "Create API key"
4. Copy key → paste into `.env` as `GEMINI_API_KEY`
- Free tier: 1,500 requests/day
- Model used: `gemini-1.5-flash`

### Streamlit Cloud Secrets
When deployed on Streamlit Cloud, add keys in the **Secrets** section:
```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxx"
GEMINI_API_KEY = "AIzaxxxxxxxxxxxxxxx"
```

The app reads `st.secrets` first, then falls back to `os.environ`, so both
local `.env` and Streamlit Cloud secrets work transparently.

---

## 10. Running the App

### Basic run
```bash
streamlit run app.py
```

### Custom port
```bash
streamlit run app.py --server.port 8080
```

### Headless mode (server / CI)
```bash
streamlit run app.py --server.headless true
```

### Public URL via tunnel (for sharing locally)
```bash
pip install pyngrok
# Add your ngrok token from dashboard.ngrok.com
python -c "
from pyngrok import ngrok, conf
conf.get_default().auth_token = 'YOUR_NGROK_TOKEN'
tunnel = ngrok.connect(8501, 'http')
print('Live URL:', tunnel.public_url)
import time; time.sleep(86400)
"
```

---

## 11. Deployment Guide

### Option A — Streamlit Cloud (Free, Recommended)

1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"Create app"**
4. Fill in:
   - Repository: `Gagan0916/NexusAI`
   - Branch: `main`
   - Main file path: `app.py`
5. Click **"Advanced settings"** → add secrets:
   ```toml
   GROQ_API_KEY = "your_key"
   ```
6. Click **Deploy**

Live URL: `https://nexusai.streamlit.app` (or similar)

---

### Option B — Railway

1. Create account at https://railway.app
2. New Project → Deploy from GitHub
3. Connect `Gagan0916/NexusAI`
4. Add environment variables: `GROQ_API_KEY`, `GEMINI_API_KEY`
5. Start command: `streamlit run app.py --server.port $PORT --server.headless true`
6. Deploy

---

### Option C — Render

1. Create account at https://render.com
2. New → Web Service → Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run app.py --server.port $PORT --server.headless true`
5. Add env vars in Environment tab
6. Deploy

---

### Option D — Local + Public Tunnel (Instant)

```bash
# Start app
streamlit run app.py --server.port 8501 &

# Open SSH tunnel (no account needed)
ssh -i ~/.ssh/id_ed25519 -R 80:localhost:8501 localhost.run
# Returns: https://xxxxxxxxxxxxxxxx.lhr.life
```

---

## 12. GitHub Repository

**URL:** https://github.com/Gagan0916/NexusAI

**Branches:**
| Branch | Purpose |
|--------|---------|
| `main` | Production branch — Streamlit Cloud deploys from here |
| `master` | Original development branch |

**Commits:**
1. `Initial commit: NexusAI Multi-Agent Startup Validator` — all 20 core files
2. `Add Streamlit Cloud deployment config and README` — config.toml, README, secrets support

**What is gitignored:**
- `.env` — API keys never committed
- `__pycache__/` — Python bytecode
- `reports/*.md` — generated output files
- `venv/` — virtual environment

---

## 13. How Each File Works

### `app.py` (Main Entry Point)

The entire Streamlit UI lives here. Key sections:

```
CUSTOM_CSS          → dark theme CSS injected via st.markdown
page_dashboard()    → Page 1: input + scores + results
page_agent_logs()   → Page 2: per-agent status cards
page_reports()      → Page 3: download buttons
_render_agent_detail() → expandable agent output view
main()              → session state init + sidebar navigation
```

Session state keys used:
- `st.session_state["results"]` — final context dict after pipeline runs
- `st.session_state["idea"]` — the startup idea string
- `st.session_state["logs"]` — list of completed agent log entries
- `st.session_state["orchestrator"]` — the NexusOrchestrator instance (for agent statuses)

---

### `agents/base_agent.py`

Defines the `BaseAgent` abstract class and `AgentStatus` dataclass.

```python
class BaseAgent(ABC):
    name: str           # Display name
    role: str           # One-line description
    emoji: str          # UI emoji

    def run(self, context: dict) -> dict:
        # Must be implemented by each agent
        # Reads from context, returns output dict

    def _set_running(msg)  # Sets status to "running"
    def _set_done(msg)     # Sets status to "done"
    def _set_error(msg)    # Sets status to "error"
```

`AgentStatus` holds: `name`, `role`, `emoji`, `status`, `message`, `output`

---

### `core/orchestrator.py`

```python
class NexusOrchestrator:
    agents = [CEO, Research, Sentiment, Analyst, Architect, PM, Engineer, Docs]

    key_map = {
        "CEO Agent": "ceo",
        "Market Research Agent": "research",
        ...
    }

    run_streaming(idea) → Generator[tuple[agent_name, context]]
    run(idea)           → dict  (final context)
```

The `key_map` maps agent display names to context dictionary keys so each
agent's output lands at the right key for downstream agents to read.

---

### `.streamlit/config.toml`

```toml
[theme]
base = "dark"
primaryColor = "#00ffb4"        # Neon green — buttons, highlights
backgroundColor = "#070d1a"     # Deep navy background
secondaryBackgroundColor = "#0c182d"
textColor = "#e8f0ff"

[server]
headless = true                 # Required for cloud deployment
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false        # Disables telemetry
```

---

## 14. Customisation Guide

### Adding a New Industry

Open `tools/industry_data.py` and add a new entry to `INDUSTRY_KB`:

```python
"your_key": {
    "name": "Your Industry Name",
    "keywords": r"keyword1|keyword2|keyword3",
    "market_size": "$X.XB",
    "growth_rate": 12.5,
    "market_demand_score": 8.0,
    "competition_score": 6.0,
    "feasibility_score": 8.0,
    "competitors": [
        {"name": "CompA", "stage": "Series B", "weakness": "No AI"},
        ...
    ],
    "pain_points": ["Pain 1", "Pain 2", "Pain 3", "Pain 4"],
    "reddit_signals": ["r/subreddit — 'quote'", ...],
    "sentiment_score": 7.5,
    "revenue_models": ["SaaS subscription", "Enterprise license"],
    "tech_stack": {
        "frontend": "React",
        "backend": "FastAPI",
        "database": "PostgreSQL",
        "ai_layer": "OpenAI API",
        "infra": "Railway",
    },
    "mvp_features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
    "risks": [
        {"risk": "Risk desc", "mitigation": "How to handle"},
    ],
    "target_users": "Description of target users",
    "business_model": "B2C SaaS",
    "moat": "What makes this defensible",
},
```

### Adding a New Agent

1. Create `agents/my_agent.py`:
```python
from agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    name = "My Agent"
    role = "What it does"
    emoji = "🔧"

    def run(self, context: dict) -> dict:
        self._set_running("Working...")
        # your logic here
        result = {"key": "value"}
        self.status.output = result
        self._set_done("Done.")
        return result
```

2. Add to `core/orchestrator.py`:
```python
from agents.my_agent import MyAgent

class NexusOrchestrator:
    def __init__(self):
        self.agents = [
            ...existing agents...,
            MyAgent(),   # Add here
        ]
        # Add to key_map:
        key_map = {
            ...
            "My Agent": "my_agent",
        }
```

### Changing the LLM Model

In `tools/llm_client.py`:
```python
GROQ_MODEL = "llama-3.3-70b-versatile"   # Change this

# Other Groq models:
# "llama-3.1-70b-versatile"   — slightly older, same quality
# "mixtral-8x7b-32768"         — longer context window
# "llama-3.1-8b-instant"       — faster, less capable
```

---

## 15. Troubleshooting

### App won't start

```bash
# Error: ModuleNotFoundError
pip install -r requirements.txt

# Error: Port already in use
streamlit run app.py --server.port 8502
```

### No results appearing after "Validate Idea"

- Check the browser console for JavaScript errors
- Ensure `streamlit >= 1.28.0`: `pip install --upgrade streamlit`
- Try a different browser

### LLM not activating

```bash
# Check your .env file exists and has valid keys
cat .env

# Test the key manually
python -c "
from tools.llm_client import has_llm, call_llm
print('LLM available:', has_llm())
result = call_llm('Say hello in one word')
print('Response:', result)
"
```

### Groq API errors

- **401 Unauthorized** — API key is wrong or expired. Get a new one at console.groq.com
- **429 Too Many Requests** — Hit rate limit. Wait 60 seconds or switch to Gemini
- **503 Service Unavailable** — Groq is down. The app auto-falls back to Gemini then offline mode

### Streamlit Cloud deployment fails

Common causes:
1. `requirements.txt` missing a package → add it and push
2. `app.py` not in repo root → check branch is `main` and file is at root level
3. Secrets not set → go to App Settings → Secrets and add your keys
4. Python version mismatch → add `runtime.txt` with content `python-3.11`

---

## 16. Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit 1.35+ | UI framework |
| Language | Python 3.12 | All backend logic |
| LLM Provider 1 | Groq (LLaMA 3.3 70B) | Primary AI inference |
| LLM Provider 2 | Google Gemini 1.5 Flash | Backup AI inference |
| HTTP Client | requests | API calls to LLM providers |
| Environment | python-dotenv | Local `.env` file loading |
| Secrets (Cloud) | st.secrets | Streamlit Cloud secrets management |
| Charts | Streamlit native | Score cards and metrics |
| Styling | Custom CSS | Dark cyberpunk theme |
| Version Control | Git + GitHub | Source code management |
| Deployment | Streamlit Cloud / Railway | Hosting |

---

## 17. Future Roadmap

### Version 1.1 (Near-term)
- [ ] PDF export for all reports (using `reportlab` or `weasyprint`)
- [ ] Save and reload previous analyses
- [ ] Comparison mode: validate two ideas side-by-side
- [ ] Share analysis via public link

### Version 1.2 (Mid-term)
- [ ] Add 5 more industries (GovTech, LegalTech, CleanTech, PropTech, GameTech)
- [ ] Voice input for startup idea (Whisper API)
- [ ] Real-time web search agent (Tavily / Serper API)
- [ ] User authentication and idea history

### Version 2.0 (Long-term)
- [ ] Multi-user workspace
- [ ] Agent debate mode (agents argue for and against the idea)
- [ ] Integration with Y Combinator application format
- [ ] Automatic slide deck generation (Google Slides API)
- [ ] Financial model with dynamic projections chart

---

*Documentation generated: 2026-06-09*  
*Project: NexusAI v1.0.0*  
*GitHub: https://github.com/Gagan0916/NexusAI*
