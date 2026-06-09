# 🚀 NexusAI — Multi-Agent Startup Validator

> Drop your startup idea. Get a full business plan, tech architecture, MVP roadmap, and starter code in under 60 seconds.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nexusai.streamlit.app)

## What It Does

NexusAI runs **8 specialist AI agents** that collaborate to validate your startup idea:

| Agent | Output |
|-------|--------|
| 👔 CEO Agent | Strategy, verdict, task assignment |
| 📊 Market Research Agent | Market size, growth rate, competitor analysis |
| 💬 Sentiment Agent | Reddit/HN pain points, customer personas |
| 📈 Business Analyst Agent | Business model, unit economics, risk register |
| 🏗️ Technical Architect Agent | Tech stack, system design, API endpoints |
| 📋 Product Manager Agent | PRD, MVP features, 90-day roadmap |
| 💻 Software Engineer Agent | Starter code, repo structure |
| 📄 Documentation Agent | README, deployment guide, investor pitch |

## Quick Start

```bash
git clone https://github.com/Gagan0916/NexusAI
cd NexusAI
pip install -r requirements.txt
streamlit run app.py
```

## LLM Support (Optional)

The app works fully offline with a built-in knowledge base.  
Add API keys to unlock AI-generated analysis:

```toml
# .streamlit/secrets.toml (local) or Streamlit Cloud Secrets
GROQ_API_KEY = "your_key"      # Free at console.groq.com
GEMINI_API_KEY = "your_key"    # Free at aistudio.google.com
```

## Pages

- **Dashboard** — Validation scores, MVP features, competitor cards, roadmap
- **Agent Logs** — Real-time per-agent status and detailed output
- **Reports** — Download Business Plan, PRD, Architecture Doc, README, Pitch

## Tech Stack

- **Frontend**: Streamlit
- **Agents**: Custom multi-agent orchestrator (no heavy frameworks)
- **LLM**: Groq (LLaMA 3.3) / Gemini 1.5 Flash / Smart offline fallback
- **Reports**: Markdown export

## Deploy to Streamlit Cloud

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. New app → select this repo → `main` → `app.py`
4. Add secrets in Advanced Settings (optional)
5. Deploy 🚀
