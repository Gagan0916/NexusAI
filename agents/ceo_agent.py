from __future__ import annotations

from tools.industry_data import detect_industry
from tools.llm_client import call_llm, has_llm, parse_json
from agents.base_agent import BaseAgent


class CEOAgent(BaseAgent):
    name = "CEO Agent"
    role = "Controls workflow, assigns tasks, and sets overall strategy"
    emoji = "👔"

    def run(self, context: dict) -> dict:
        self._set_running("Analysing startup idea and planning agent tasks...")
        idea = context["startup_idea"]
        industry = detect_industry(idea)

        task_plan = [
            {"agent": "Market Research Agent", "task": f"Research market size, growth, and competitors for: {idea}"},
            {"agent": "Sentiment Agent", "task": "Find customer pain points and community sentiment on Reddit/HN"},
            {"agent": "Business Analyst Agent", "task": "Model business viability, revenue streams, and risk assessment"},
            {"agent": "Technical Architect Agent", "task": "Design tech stack and system architecture"},
            {"agent": "Product Manager Agent", "task": "Define MVP features and 90-day product roadmap"},
            {"agent": "Software Engineer Agent", "task": "Generate starter code and repository structure"},
            {"agent": "Documentation Agent", "task": "Create README, deployment guide, and pitch summary"},
        ]

        if has_llm():
            prompt = f"""You are a startup CEO. A founder has submitted this idea:

"{idea}"

Detected industry: {industry['name']}

Your job:
1. Write a 2-sentence strategic overview of this startup idea.
2. Identify the single most important success factor.
3. Name the 3 biggest risks.
4. Rate your confidence this idea can reach $1M ARR in 24 months (1-10).

Return ONLY valid JSON:
{{
  "strategic_overview": "...",
  "key_success_factor": "...",
  "top_risks": ["risk1", "risk2", "risk3"],
  "confidence_score": 7,
  "verdict": "Promising" | "Strong" | "Needs Refinement" | "Risky"
}}"""
            raw = call_llm(prompt)
            parsed = parse_json(raw) if raw else None
        else:
            parsed = None

        if parsed:
            result = {
                "strategic_overview": parsed.get("strategic_overview", ""),
                "key_success_factor": parsed.get("key_success_factor", ""),
                "top_risks": parsed.get("top_risks", industry["risks"][:3]),
                "confidence_score": parsed.get("confidence_score", 7),
                "verdict": parsed.get("verdict", "Promising"),
            }
        else:
            risk_titles = [r["risk"] for r in industry["risks"][:3]]
            result = {
                "strategic_overview": (
                    f"This startup targets the {industry['name']} market, a ${industry['market_size']} "
                    f"space growing at {industry['growth_rate']}% CAGR. "
                    f"An AI-native approach can carve a defensible niche where legacy players are slow to adapt."
                ),
                "key_success_factor": f"Build a genuine data moat — {industry['moat']}.",
                "top_risks": risk_titles,
                "confidence_score": round((industry["market_demand_score"] + industry["feasibility_score"]) / 2, 1),
                "verdict": "Strong" if industry["market_demand_score"] >= 8.0 else "Promising",
            }

        result["task_plan"] = task_plan
        result["industry"] = industry
        self.status.output = result
        self._set_done("Strategy defined. Tasks assigned to all agents.")
        return result
