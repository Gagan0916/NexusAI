<div align="center">

# NexusAI — Multi-Agent Startup Validator & Builder

**Drop your startup idea. Get a full business plan, tech architecture, MVP roadmap, and investor pitch in under 60 seconds.**

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nexusai-nksewvez2pefaeg5gh69uv.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?logo=streamlit&logoColor=white)
![LLM](https://img.shields.io/badge/LLM-Groq%20%7C%20Gemini-00C896)
![License](https://img.shields.io/badge/License-MIT-green)

### [Try NexusAI Live →](https://nexusai-nksewvez2pefaeg5gh69uv.streamlit.app/)

</div>

---

## What Is NexusAI?

NexusAI is a **Multi-Agent Startup Validator** built with Streamlit and Python. It takes a plain-English startup idea and runs it through a sequential pipeline of **8 specialist AI agents** that collaborate to produce a complete, investor-ready startup analysis — including market research, competitor intelligence, business model, tech architecture, PRD, MVP roadmap, starter code, and downloadable reports.

No setup required. Works fully offline with a built-in industry knowledge base. Add a free API key to unlock AI-generated, idea-specific analysis.

---

## Two Modes

| Mode | How It Works | API Key Needed? |
|------|-------------|-----------------|
| **Smart Offline Mode** | Uses a built-in knowledge base of 7 industries to produce structured, realistic outputs | No |
| **LLM Mode** | Every agent calls Groq (LLaMA 3.3 70B) or Gemini 1.5 Flash for AI-generated, idea-specific analysis | Free key from Groq or Google |

---

## The 8-Agent Pipeline

```
Your Startup Idea
       │
       ▼
 NexusOrchestrator (sequential pipeline)
       │
       ├─► 👔 CEO Agent              → Strategy, verdict, confidence score
       ├─► 📊 Market Research Agent  → Market size, growth, competitors, TAM/SAM/SOM
       ├─► 💬 Sentiment Agent        → Reddit/HN pain points, personas, willingness to pay
       ├─► 📈 Business Analyst Agent → Business model, unit economics, risks, GTM
       ├─► 🏗️ Technical Architect   → Tech stack, system design, DB schema, API endpoints
       ├─► 📋 Product Manager Agent  → PRD, MVP features (P0/P1/P2), 90-day roadmap
       ├─► 💻 Software Engineer      → Starter FastAPI code, repo structure, setup steps
       └─► 📄 Documentation Agent    → README, deployment guide, investor pitch
```

Each agent reads from a shared `context` dict and adds its output — so every downstream agent has the full picture from all agents before it.

---

## Features

### Analysis & Scoring
- **CEO Verdict** — Strong / Promising / Risky with a 1–10 confidence score
- **4 Score Cards** — Market Score, Competition Score, Feasibility Score, Sentiment Score
- **TAM / SAM / SOM** breakdown
- **Competitor cards** — 4 real competitors with stage and weakness analysis
- **Unit Economics** — CAC, LTV, LTV/CAC ratio, payback period, gross margin
- **Risk Register** — severity-rated risks with mitigations
- **90-Day MVP Roadmap** — 4 phases with deliverables

### 7 Downloadable Reports
| # | Report | Contents |
|---|--------|---------|
| 1 | Business Plan | Market analysis + competitors + unit economics + risks + GTM |
| 2 | PRD | Problem statement, MVP features, success metrics |
| 3 | Technical Architecture | Stack, components, DB schema, API endpoints, scaling plan |
| 4 | README.md | Ready-to-use GitHub README for your idea |
| 5 | Deployment Guide | Step-by-step deploy to Railway / Render / Streamlit Cloud |
| 6 | Investor Pitch | 1-page pitch (problem → solution → market → ask) |
| 7 | Starter Code | Production-ready FastAPI + Python code |

### UI
- **3 pages**: Dashboard · Agent Logs · Reports
- **Dark cyberpunk theme** (navy + neon green + purple)
- **Real-time updates** — watch each agent complete live
- Per-agent expandable detail views with full output

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Gagan0916/NexusAI.git
cd NexusAI

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run (works without API keys)
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Enable LLM Mode (Optional — Free)

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Getting free API keys:**

- **Groq** (recommended — fastest): [console.groq.com](https://console.groq.com) — free, no credit card, 14,400 req/day
- **Gemini** (backup): [aistudio.google.com](https://aistudio.google.com) — free, 1,500 req/day

The app tries Groq first, falls back to Gemini, then falls back to offline mode automatically.

---

## Folder Structure

```
nexusai/
├── app.py                    ← Main Streamlit app (entry point)
├── agents/
│   ├── base_agent.py         ← Abstract base class for all agents
│   ├── ceo_agent.py
│   ├── research_agent.py
│   ├── sentiment_agent.py
│   ├── analyst_agent.py
│   ├── architect_agent.py
│   ├── pm_agent.py
│   ├── engineer_agent.py
│   └── docs_agent.py
├── core/
│   └── orchestrator.py       ← Sequential agent pipeline manager
├── tools/
│   ├── llm_client.py         ← Groq + Gemini client with fallback logic
│   ├── industry_data.py      ← Knowledge base for 7 industries
│   └── report_generator.py   ← Builds downloadable report text
├── .streamlit/
│   └── config.toml           ← Dark theme + server config
├── .env.example
├── requirements.txt
└── DOCUMENTATION.md          ← Full technical documentation
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit 1.35+ |
| Language | Python 3.12 |
| LLM Provider 1 | Groq — LLaMA 3.3 70B Versatile |
| LLM Provider 2 | Google Gemini 1.5 Flash |
| HTTP Client | requests |
| Environment | python-dotenv |
| Offline Fallback | Custom industry knowledge base (7 industries) |
| Styling | Custom CSS — dark cyberpunk theme |
| Deployment | Streamlit Cloud / Railway / Render |

---

## Supported Industries (Offline Mode)

| Industry | Trigger Keywords |
|----------|-----------------|
| HR Tech / CareerTech | interview, resume, job, career, hiring |
| EdTech | education, learn, student, teacher, course |
| HealthTech | health, medical, doctor, patient, wellness |
| FinTech | finance, payment, bank, invest, crypto, wallet |
| E-Commerce | shop, store, marketplace, buy, sell, retail |
| B2B SaaS | saas, platform, tool, automation, workflow |
| AI-Native Product | ai, machine learning, gpt, llm, chatbot |

Any idea outside these categories uses the general tech startup template.

---

## Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **Create app** → select this repo → branch: `main` → main file: `app.py`
4. Click **Advanced settings** and add secrets:
   ```toml
   GROQ_API_KEY = "gsk_xxxxxxxxxxxx"
   GEMINI_API_KEY = "AIzaxxxxxxxxxxxxxxx"
   ```
5. Click **Deploy**

### Other Deployment Options

<details>
<summary>Railway</summary>

1. New Project → Deploy from GitHub → connect `Gagan0916/NexusAI`
2. Add env vars: `GROQ_API_KEY`, `GEMINI_API_KEY`
3. Start command: `streamlit run app.py --server.port $PORT --server.headless true`

</details>

<details>
<summary>Render</summary>

1. New Web Service → connect GitHub repo
2. Build command: `pip install -r requirements.txt`
3. Start command: `streamlit run app.py --server.port $PORT --server.headless true`
4. Add env vars in the Environment tab

</details>

---

## Roadmap

### v1.1
- [ ] PDF export for all reports
- [ ] Save and reload previous analyses
- [ ] Side-by-side comparison of two ideas
- [ ] Share analysis via public link

### v1.2
- [ ] 5 more industries (GovTech, LegalTech, CleanTech, PropTech, GameTech)
- [ ] Voice input via Whisper API
- [ ] Real-time web search agent (Tavily / Serper)
- [ ] User authentication and idea history

### v2.0
- [ ] Multi-user workspace
- [ ] Agent debate mode (agents argue for and against the idea)
- [ ] Y Combinator application format integration
- [ ] Automatic slide deck generation
- [ ] Dynamic financial projections chart

---

## Troubleshooting

**App won't start**
```bash
pip install -r requirements.txt          # fix missing modules
streamlit run app.py --server.port 8502  # fix port conflict
```

**LLM not activating**
```bash
python -c "from tools.llm_client import has_llm; print(has_llm())"
```

**Groq API errors**
- `401` — wrong or expired key → get a new one at console.groq.com
- `429` — rate limit hit → wait 60 seconds or the app auto-switches to Gemini
- `503` — Groq is down → app auto-falls back to Gemini, then offline mode

**Streamlit Cloud deploy fails**
- Check `requirements.txt` has all packages
- Confirm `app.py` is at the repo root on the `main` branch
- Add secrets in App Settings → Secrets

---

## Author

**Gagan0916** — [github.com/Gagan0916](https://github.com/Gagan0916)

---

*NexusAI v1.0.0 · Built with Streamlit · Powered by Groq & Gemini*
