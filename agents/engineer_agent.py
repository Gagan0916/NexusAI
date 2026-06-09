from __future__ import annotations

from tools.llm_client import call_llm, has_llm
from agents.base_agent import BaseAgent


_STARTER_CODE_TEMPLATE = '''"""
{app_name} — AI-powered {industry_name} platform.
Auto-generated starter code by NexusAI.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI(title="{app_name} API", version="0.1.0")
security = HTTPBearer()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an expert AI assistant for {industry_name}.
Your role is to provide accurate, helpful, and actionable guidance."""


class ProcessRequest(BaseModel):
    user_input: str
    context: dict = {{}}


class ProcessResponse(BaseModel):
    result: str
    confidence: float
    suggestions: list[str]


@app.post("/api/process", response_model=ProcessResponse)
async def process_request(request: ProcessRequest):
    """Core AI processing endpoint."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {{"role": "system", "content": SYSTEM_PROMPT}},
                {{"role": "user", "content": request.user_input}},
            ],
            temperature=0.7,
        )
        result_text = response.choices[0].message.content
        return ProcessResponse(
            result=result_text,
            confidence=0.87,
            suggestions=["Review the output", "Iterate based on feedback"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    return {{"status": "healthy", "version": "0.1.0"}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''


class SoftwareEngineerAgent(BaseAgent):
    name = "Software Engineer Agent"
    role = "Generates starter code, repo structure, and implementation blueprint"
    emoji = "💻"

    def run(self, context: dict) -> dict:
        self._set_running("Generating starter code and repository structure...")
        idea = context["startup_idea"]
        industry = context["ceo"]["industry"]
        tech_stack = context.get("architect", {}).get("tech_stack", industry["tech_stack"])
        mvp_features = context.get("pm", {}).get("mvp_features", [])

        app_name = idea.split()[:3]
        app_name = "".join(w.capitalize() for w in app_name if w.isalpha())

        if has_llm():
            features_str = "\n".join(f"- {f['feature']}" for f in mvp_features[:4]) if mvp_features else "Core AI feature"
            prompt = f"""You are a senior software engineer generating starter code.

Startup idea: "{idea}"
Industry: {industry['name']}
Tech stack: {tech_stack}
MVP features:
{features_str}

Generate a production-ready FastAPI + Python starter code snippet for the core AI feature.
Write clean, working Python code (not pseudocode). Include:
- FastAPI endpoint
- Pydantic models
- OpenAI integration
- Basic error handling

Return ONLY the Python code, no explanation, no markdown fences."""
            raw = call_llm(prompt)
            starter_code = raw.strip() if raw else None
        else:
            starter_code = None

        if not starter_code:
            starter_code = _STARTER_CODE_TEMPLATE.format(
                app_name=app_name or "MyApp",
                industry_name=industry["name"],
            )

        folder = app_name.lower() or "myapp"
        repo_structure = {
            "root": f"{folder}/",
            "files": [
                f"{folder}/",
                f"{folder}/app.py                  # Streamlit frontend",
                f"{folder}/main.py                 # FastAPI backend entry point",
                f"{folder}/requirements.txt        # Python dependencies",
                f"{folder}/.env.example            # Environment variable template",
                f"{folder}/README.md               # Project documentation",
                f"{folder}/",
                f"{folder}/api/",
                f"{folder}/api/__init__.py",
                f"{folder}/api/routes.py           # All API endpoint definitions",
                f"{folder}/api/models.py           # Pydantic request/response models",
                f"{folder}/api/auth.py             # JWT authentication middleware",
                f"{folder}/",
                f"{folder}/services/",
                f"{folder}/services/__init__.py",
                f"{folder}/services/ai_service.py # LLM calls and prompt management",
                f"{folder}/services/user_service.py",
                f"{folder}/",
                f"{folder}/db/",
                f"{folder}/db/__init__.py",
                f"{folder}/db/models.py            # SQLAlchemy ORM models",
                f"{folder}/db/migrations/          # Alembic migration scripts",
                f"{folder}/",
                f"{folder}/tests/",
                f"{folder}/tests/test_api.py",
                f"{folder}/tests/test_services.py",
            ],
        }

        implementation_steps = [
            "Step 1 — Set up repo: git init, create venv, install requirements.txt",
            f"Step 2 — Configure .env: add OPENAI_API_KEY and DATABASE_URL",
            f"Step 3 — Run DB migrations: alembic upgrade head",
            f"Step 4 — Start backend: uvicorn main:app --reload",
            f"Step 5 — Start frontend: streamlit run app.py",
            f"Step 6 — Deploy: push to GitHub → connect to Railway/Render",
        ]

        packages = [
            "fastapi>=0.111.0",
            "uvicorn[standard]>=0.29.0",
            f"openai>=1.30.0",
            "pydantic>=2.7.0",
            "sqlalchemy>=2.0.0",
            "alembic>=1.13.0",
            "psycopg2-binary>=2.9.9",
            "python-jose[cryptography]>=3.3.0",
            "passlib[bcrypt]>=1.7.4",
            "python-multipart>=0.0.9",
            "python-dotenv>=1.0.0",
            "streamlit>=1.35.0",
        ]

        result = {
            "starter_code": starter_code,
            "repo_structure": repo_structure,
            "implementation_steps": implementation_steps,
            "packages": packages,
            "github_actions_hint": (
                "Add .github/workflows/deploy.yml to auto-deploy on push to main. "
                "Use Railway's GitHub integration for zero-config deployment."
            ),
            "env_vars_needed": [
                "OPENAI_API_KEY — from platform.openai.com",
                "DATABASE_URL — PostgreSQL connection string",
                "SECRET_KEY — random 32-char string for JWT signing",
                "GROQ_API_KEY — optional cheaper alternative to OpenAI",
            ],
        }

        self.status.output = result
        self._set_done("Starter code and repo structure generated.")
        return result
