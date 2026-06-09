from __future__ import annotations

from tools.llm_client import call_llm, has_llm, parse_json
from agents.base_agent import BaseAgent


class TechnicalArchitectAgent(BaseAgent):
    name = "Technical Architect Agent"
    role = "Designs tech stack, system architecture, and scalability plan"
    emoji = "🏗️"

    def run(self, context: dict) -> dict:
        self._set_running("Designing system architecture and selecting tech stack...")
        idea = context["startup_idea"]
        industry = context["ceo"]["industry"]

        if has_llm():
            prompt = f"""You are a senior software architect and CTO advisor.

Startup idea: "{idea}"
Industry: {industry['name']}

Design the technical architecture. Return ONLY valid JSON:
{{
  "tech_stack": {{
    "frontend": "React + TypeScript",
    "backend": "FastAPI (Python)",
    "database": "PostgreSQL + Redis",
    "ai_layer": "OpenAI GPT-4o + LangChain",
    "auth": "Supabase Auth / Auth0",
    "file_storage": "AWS S3 / Cloudflare R2",
    "deployment": "Railway / Render",
    "ci_cd": "GitHub Actions"
  }},
  "architecture_style": "Microservices | Monolith | Modular Monolith",
  "system_components": [
    {{"component": "API Gateway", "purpose": "Route and authenticate requests"}},
    {{"component": "AI Service", "purpose": "Handle all LLM calls and prompt management"}},
    {{"component": "User Service", "purpose": "Manage user accounts and billing"}},
    {{"component": "Data Pipeline", "purpose": "Process and store user data"}}
  ],
  "database_schema": [
    {{"table": "users", "key_fields": ["id", "email", "plan", "created_at"]}},
    {{"table": "sessions", "key_fields": ["id", "user_id", "data", "timestamp"]}},
    {{"table": "analytics", "key_fields": ["id", "user_id", "event", "metadata"]}}
  ],
  "api_endpoints": [
    "POST /api/auth/register",
    "POST /api/auth/login",
    "POST /api/core/process",
    "GET /api/user/dashboard",
    "GET /api/reports/export"
  ],
  "scalability_notes": "How to scale from 100 to 100k users",
  "estimated_monthly_infra_cost": "$25–$80/mo at launch"
}}"""
            raw = call_llm(prompt)
            parsed = parse_json(raw) if raw else None
        else:
            parsed = None

        if parsed:
            result = {
                "tech_stack": parsed.get("tech_stack", industry["tech_stack"]),
                "architecture_style": parsed.get("architecture_style", "Modular Monolith"),
                "system_components": parsed.get("system_components", []),
                "database_schema": parsed.get("database_schema", []),
                "api_endpoints": parsed.get("api_endpoints", []),
                "scalability_notes": parsed.get("scalability_notes", ""),
                "estimated_monthly_infra_cost": parsed.get("estimated_monthly_infra_cost", "$25–$80/mo"),
            }
        else:
            ts = industry["tech_stack"]
            result = {
                "tech_stack": ts,
                "architecture_style": "Modular Monolith (evolve to microservices at $1M ARR)",
                "system_components": [
                    {"component": "Streamlit / React Frontend", "purpose": "User-facing UI and dashboards"},
                    {"component": "FastAPI Backend", "purpose": "Business logic, authentication, and API gateway"},
                    {"component": "AI Orchestration Layer", "purpose": "LLM prompt management, caching, and fallback"},
                    {"component": "PostgreSQL Database", "purpose": "Persistent user data, sessions, and analytics"},
                    {"component": "Redis Cache", "purpose": "Session store, rate limiting, and AI response cache"},
                    {"component": f"{ts.get('infra', 'Railway')}", "purpose": "Hosting, CI/CD, and auto-scaling"},
                ],
                "database_schema": [
                    {"table": "users", "key_fields": ["id", "email", "plan", "created_at", "last_active"]},
                    {"table": "projects", "key_fields": ["id", "user_id", "idea", "status", "results_json"]},
                    {"table": "reports", "key_fields": ["id", "project_id", "type", "content", "created_at"]},
                    {"table": "usage_events", "key_fields": ["id", "user_id", "event_type", "metadata", "timestamp"]},
                ],
                "api_endpoints": [
                    "POST /api/auth/register — Create new user account",
                    "POST /api/auth/login — Authenticate and return JWT",
                    "POST /api/validate — Run full agent pipeline on startup idea",
                    "GET  /api/projects/{id} — Retrieve project results",
                    "GET  /api/reports/{id}/export — Download report as Markdown/PDF",
                    "GET  /api/user/dashboard — Fetch user metrics and history",
                ],
                "scalability_notes": (
                    "0–1k users: single Railway container. "
                    "1k–50k: add Redis cache + read replica DB. "
                    "50k+: break AI service into separate worker queue (Celery + RabbitMQ)."
                ),
                "estimated_monthly_infra_cost": "$20–$60/mo at launch (Railway Starter Plan)",
            }

        self.status.output = result
        self._set_done("Architecture designed. Tech stack and components defined.")
        return result
