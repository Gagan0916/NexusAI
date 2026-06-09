from __future__ import annotations

from tools.llm_client import call_llm, has_llm, parse_json
from agents.base_agent import BaseAgent


class BusinessAnalystAgent(BaseAgent):
    name = "Business Analyst Agent"
    role = "Models business viability, revenue streams, unit economics, and risk register"
    emoji = "📈"

    def run(self, context: dict) -> dict:
        self._set_running("Building financial model and risk register...")
        idea = context["startup_idea"]
        industry = context["ceo"]["industry"]
        research = context["research"]

        if has_llm():
            prompt = f"""You are a startup business analyst.

Startup idea: "{idea}"
Industry: {industry['name']}
Market size: {research['market_size']}
Competition score: {research['competition_score']}/10

Create a concise business analysis. Return ONLY valid JSON:
{{
  "feasibility_score": 8.5,
  "business_model": "B2C SaaS subscription",
  "revenue_streams": [
    {{"stream": "Individual subscription", "price": "$19/mo", "type": "Recurring"}},
    {{"stream": "Team plan", "price": "$99/mo", "type": "Recurring"}},
    {{"stream": "Enterprise license", "price": "$999/mo", "type": "Recurring"}}
  ],
  "unit_economics": {{
    "cac": "$45",
    "ltv": "$540",
    "ltv_cac_ratio": "12:1",
    "payback_period": "2.4 months",
    "gross_margin": "82%"
  }},
  "risks": [
    {{"risk": "Risk description", "severity": "High|Medium|Low", "mitigation": "Strategy"}},
    {{"risk": "Risk description", "severity": "Medium", "mitigation": "Strategy"}},
    {{"risk": "Risk description", "severity": "Low", "mitigation": "Strategy"}}
  ],
  "go_to_market": ["GTM step 1", "GTM step 2", "GTM step 3"],
  "break_even_months": 14
}}"""
            raw = call_llm(prompt)
            parsed = parse_json(raw) if raw else None
        else:
            parsed = None

        if parsed:
            result = {
                "feasibility_score": parsed.get("feasibility_score", industry["feasibility_score"]),
                "business_model": parsed.get("business_model", industry["business_model"]),
                "revenue_streams": parsed.get("revenue_streams", []),
                "unit_economics": parsed.get("unit_economics", {}),
                "risks": parsed.get("risks", []),
                "go_to_market": parsed.get("go_to_market", []),
                "break_even_months": parsed.get("break_even_months", 14),
            }
        else:
            rev_models = industry["revenue_models"]
            prices = ["$19/mo", "$49/mo", "$199/mo"]
            streams = []
            for i, rm in enumerate(rev_models[:3]):
                streams.append({"stream": rm, "price": prices[i] if i < len(prices) else "Custom", "type": "Recurring"})

            fs = industry["feasibility_score"]
            result = {
                "feasibility_score": fs,
                "business_model": industry["business_model"],
                "revenue_streams": streams,
                "unit_economics": {
                    "cac": "$35–$65",
                    "ltv": "$420–$780",
                    "ltv_cac_ratio": "10:1 – 12:1",
                    "payback_period": "2–3 months",
                    "gross_margin": "78–85%",
                },
                "risks": [
                    {
                        "risk": r["risk"],
                        "severity": "High" if i == 0 else "Medium",
                        "mitigation": r["mitigation"],
                    }
                    for i, r in enumerate(industry["risks"][:3])
                ],
                "go_to_market": [
                    "Launch on Product Hunt + LinkedIn with 100 waitlist signups as proof",
                    "Partner with 3 micro-influencers in the target niche",
                    f"Offer free tier for {industry['target_users'].split()[0].lower()} users — convert 15 % to paid",
                    "Publish weekly thought-leadership content to drive SEO traffic",
                ],
                "break_even_months": 12 if fs >= 8.5 else 16,
            }

        self.status.output = result
        self._set_done(f"Business model built. Feasibility: {result['feasibility_score']}/10")
        return result
