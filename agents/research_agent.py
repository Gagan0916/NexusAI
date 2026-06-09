from __future__ import annotations

from tools.llm_client import call_llm, has_llm, parse_json
from agents.base_agent import BaseAgent


class MarketResearchAgent(BaseAgent):
    name = "Market Research Agent"
    role = "Analyses market size, demand, growth trends, and competitive landscape"
    emoji = "📊"

    def run(self, context: dict) -> dict:
        self._set_running("Scanning market data and competitor intelligence...")
        idea = context["startup_idea"]
        industry = context["ceo"]["industry"]

        if has_llm():
            prompt = f"""You are a senior market analyst. Research this startup idea:

"{idea}"
Industry: {industry['name']}

Return ONLY valid JSON with this exact structure:
{{
  "market_size": "$X.XB",
  "growth_rate": 14.5,
  "market_demand_score": 8.5,
  "competition_score": 6.2,
  "key_trends": ["trend1", "trend2", "trend3"],
  "competitors": [
    {{"name": "CompanyA", "stage": "Series B / $50M", "weakness": "No mobile app"}},
    {{"name": "CompanyB", "stage": "Public", "weakness": "Legacy UX"}},
    {{"name": "CompanyC", "stage": "Bootstrapped", "weakness": "Limited scale"}},
    {{"name": "CompanyD", "stage": "$20M raised", "weakness": "B2B only"}}
  ],
  "market_gap": "One sentence on the gap this startup can exploit",
  "tam_sam_som": {{
    "TAM": "$XXB — total addressable market",
    "SAM": "$XXM — serviceable addressable market",
    "SOM": "$XXM — realistically capturable in year 1-2"
  }}
}}"""
            raw = call_llm(prompt)
            parsed = parse_json(raw) if raw else None
        else:
            parsed = None

        if parsed:
            result = {
                "market_size": parsed.get("market_size", industry["market_size"]),
                "growth_rate": parsed.get("growth_rate", industry["growth_rate"]),
                "market_demand_score": parsed.get("market_demand_score", industry["market_demand_score"]),
                "competition_score": parsed.get("competition_score", industry["competition_score"]),
                "key_trends": parsed.get("key_trends", []),
                "competitors": parsed.get("competitors", industry["competitors"]),
                "market_gap": parsed.get("market_gap", ""),
                "tam_sam_som": parsed.get("tam_sam_som", {}),
            }
        else:
            mrr = 49
            users_y1 = 500
            som = round(mrr * users_y1 * 12 / 1_000_000, 1)
            sam = round(som * 20, 0)
            result = {
                "market_size": industry["market_size"],
                "growth_rate": industry["growth_rate"],
                "market_demand_score": industry["market_demand_score"],
                "competition_score": industry["competition_score"],
                "key_trends": [
                    f"AI adoption in {industry['name']} accelerating post-GPT-4",
                    "Shift from horizontal platforms to vertical AI specialists",
                    "SMBs prioritising automation to offset rising labour costs",
                ],
                "competitors": industry["competitors"],
                "market_gap": (
                    f"No existing player combines AI-native UX with {industry['name'].lower()} "
                    f"domain depth — that gap is the opportunity."
                ),
                "tam_sam_som": {
                    "TAM": f"{industry['market_size']} — total global {industry['name']} market",
                    "SAM": f"${int(sam)}M — SMB + mid-market segment you can realistically reach",
                    "SOM": f"${som}M — year-1 capture with 500 paying customers at ${mrr}/mo",
                },
            }

        self.status.output = result
        self._set_done(f"Market analysis complete. Demand score: {result['market_demand_score']}/10")
        return result
