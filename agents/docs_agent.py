from __future__ import annotations

from tools.llm_client import call_llm, has_llm
from agents.base_agent import BaseAgent


class DocumentationAgent(BaseAgent):
    name = "Documentation Agent"
    role = "Creates README, deployment guide, and investor pitch summary"
    emoji = "📄"

    def run(self, context: dict) -> dict:
        self._set_running("Writing README, deployment guide, and pitch summary...")
        idea = context["startup_idea"]
        industry = context["ceo"]["industry"]
        tech_stack = context.get("architect", {}).get("tech_stack", industry["tech_stack"])
        mvp_features = context.get("pm", {}).get("mvp_features", [])
        value_prop = context.get("pm", {}).get("value_proposition", "")
        ceo_output = context.get("ceo", {})

        app_name = " ".join(w.capitalize() for w in idea.split()[:4])
        feature_list = "\n".join(f"- {f['feature']}" for f in mvp_features[:5]) if mvp_features else "- Core AI features"

        readme = f"""# {app_name}

> {value_prop or idea}

## Overview
{ceo_output.get('strategic_overview', idea)}

## Features
{feature_list}

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | {tech_stack.get('frontend', 'React')} |
| Backend | {tech_stack.get('backend', 'FastAPI')} |
| Database | {tech_stack.get('database', 'PostgreSQL')} |
| AI Layer | {tech_stack.get('ai_layer', 'OpenAI API')} |
| Deployment | {tech_stack.get('infra', 'Railway')} |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/{idea.split()[0].lower()}-app

# Install dependencies
cd {idea.split()[0].lower()}-app
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys

# Run the app
streamlit run app.py
```

## Environment Variables
```env
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your_secret_key
GROQ_API_KEY=optional_cheaper_alternative
```

## Project Structure
```
{idea.split()[0].lower()}-app/
├── app.py              # Streamlit UI
├── main.py             # FastAPI backend
├── agents/             # AI agent modules
├── api/                # API routes & models
├── services/           # Business logic
├── db/                 # Database models
├── tests/              # Test suite
└── requirements.txt
```

## Deployment (Railway)
1. Push code to GitHub
2. Connect repo at railway.app
3. Add environment variables in Railway dashboard
4. Deploy — Railway auto-detects Streamlit

## Contributing
Pull requests welcome. Please read CONTRIBUTING.md first.

## License
MIT
"""

        deployment_guide = f"""# Deployment Guide — {app_name}

## Option 1: Railway (Recommended — Free Tier Available)
1. Create account at railway.app
2. New Project → Deploy from GitHub repo
3. Add environment variables in Settings → Variables
4. Railway detects Python/Streamlit automatically
5. Custom domain: Settings → Networking → Generate Domain

## Option 2: Render
1. Create account at render.com
2. New → Web Service → Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run app.py --server.port $PORT`
5. Add env vars in Environment tab

## Option 3: Streamlit Cloud (Easiest)
1. Push code to GitHub (public or private)
2. Go to share.streamlit.io
3. Connect GitHub → select repo → branch → app.py
4. Add secrets in Advanced Settings
5. Deploy — free hosting for Streamlit apps

## Production Checklist
- [ ] All API keys in environment variables (NOT in code)
- [ ] .env file in .gitignore
- [ ] Error handling on all API calls
- [ ] Rate limiting on API endpoints
- [ ] Database backups configured
- [ ] Monitoring set up (Sentry / LogRocket)
"""

        pitch_summary = f"""# Pitch Summary — {app_name}

## One-Liner
{value_prop or idea}

## Problem
{context.get('pm', {}).get('problem_statement', f'Current {industry["name"]} solutions are manual, expensive, and lack AI.')}

## Solution
An AI-native platform that automates {industry['name'].lower()} workflows, giving users
instant results that previously required hours of manual work.

## Market
- **TAM:** {context.get('research', {}).get('tam_sam_som', {}).get('TAM', industry['market_size'])}
- **Growth:** {industry['growth_rate']}% CAGR
- **Competition score:** {context.get('research', {}).get('competition_score', industry['competition_score'])}/10

## Business Model
{industry['business_model']}
Revenue streams: {', '.join(industry['revenue_models'][:2])}

## Traction Potential
- Target: 100 beta users in 30 days
- Goal: $10k MRR by month 6

## Why Now
AI costs dropped 90% in 2 years. The time to build AI-native {industry['name'].lower()} products is today.

## The Ask
[Your raise amount] to hire 1 engineer + 6 months runway to reach $10k MRR.
"""

        if has_llm():
            prompt = f"""Improve this pitch summary for "{idea}" in {industry['name']}.
Make it more compelling, specific, and investor-ready. Keep it under 300 words.
Add 3 specific traction metrics as bullet points.
Return only the improved pitch text, no explanation."""
            raw = call_llm(prompt)
            if raw and len(raw) > 100:
                pitch_summary = raw

        result = {
            "readme": readme,
            "deployment_guide": deployment_guide,
            "pitch_summary": pitch_summary,
        }

        self.status.output = result
        self._set_done("README, deployment guide, and pitch summary created.")
        return result
