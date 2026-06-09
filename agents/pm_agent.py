from __future__ import annotations

from tools.llm_client import call_llm, has_llm, parse_json
from agents.base_agent import BaseAgent


class ProductManagerAgent(BaseAgent):
    name = "Product Manager Agent"
    role = "Writes the PRD, defines MVP scope, and builds the 90-day roadmap"
    emoji = "📋"

    def run(self, context: dict) -> dict:
        self._set_running("Writing Product Requirements Document and MVP roadmap...")
        idea = context["startup_idea"]
        industry = context["ceo"]["industry"]
        pain_points = context.get("sentiment", {}).get("pain_points", industry["pain_points"])

        if has_llm():
            top_pains = "\n".join(f"- {p}" for p in pain_points[:4])
            prompt = f"""You are a senior Product Manager at a well-funded startup.

Startup idea: "{idea}"
Industry: {industry['name']}
Top customer pain points:
{top_pains}

Write the product requirements. Return ONLY valid JSON:
{{
  "problem_statement": "One clear sentence defining the problem",
  "target_user": "Specific user persona description",
  "value_proposition": "One sentence value prop",
  "mvp_features": [
    {{"feature": "Feature name", "priority": "P0", "description": "What it does", "effort": "3 days"}},
    {{"feature": "Feature name", "priority": "P0", "description": "What it does", "effort": "5 days"}},
    {{"feature": "Feature name", "priority": "P1", "description": "What it does", "effort": "2 days"}},
    {{"feature": "Feature name", "priority": "P1", "description": "What it does", "effort": "4 days"}},
    {{"feature": "Feature name", "priority": "P2", "description": "What it does", "effort": "1 week"}}
  ],
  "roadmap": [
    {{"phase": "Week 1–2", "milestone": "Core MVP", "deliverables": ["item1", "item2"]}},
    {{"phase": "Week 3–4", "milestone": "Beta Launch", "deliverables": ["item1", "item2"]}},
    {{"phase": "Month 2", "milestone": "Paid Launch", "deliverables": ["item1", "item2"]}},
    {{"phase": "Month 3", "milestone": "Growth", "deliverables": ["item1", "item2"]}}
  ],
  "success_metrics": [
    {{"metric": "DAU", "target": "100 in month 1"}},
    {{"metric": "Paid conversion", "target": "10% by month 2"}},
    {{"metric": "NPS", "target": ">50 by month 3"}}
  ],
  "out_of_scope_v1": ["Feature to skip in V1", "Another thing to defer"]
}}"""
            raw = call_llm(prompt)
            parsed = parse_json(raw) if raw else None
        else:
            parsed = None

        if parsed:
            result = {
                "problem_statement": parsed.get("problem_statement", ""),
                "target_user": parsed.get("target_user", industry["target_users"]),
                "value_proposition": parsed.get("value_proposition", ""),
                "mvp_features": parsed.get("mvp_features", []),
                "roadmap": parsed.get("roadmap", []),
                "success_metrics": parsed.get("success_metrics", []),
                "out_of_scope_v1": parsed.get("out_of_scope_v1", []),
            }
        else:
            features_raw = industry["mvp_features"]
            priorities = ["P0", "P0", "P1", "P1", "P2"]
            efforts = ["3 days", "5 days", "3 days", "4 days", "1 week"]
            mvp_features = []
            for i, f in enumerate(features_raw[:5]):
                mvp_features.append({
                    "feature": f,
                    "priority": priorities[i] if i < len(priorities) else "P2",
                    "description": f"Core {f.lower()} functionality addressing primary user need",
                    "effort": efforts[i] if i < len(efforts) else "1 week",
                })

            result = {
                "problem_statement": f"{industry['target_users']} struggle with: {pain_points[0] if pain_points else 'inefficient manual processes'}.",
                "target_user": industry["target_users"],
                "value_proposition": (
                    f"The AI-native solution that helps {industry['target_users'].split()[0].lower()} "
                    f"{pain_points[0].lower().replace('no ', '').replace('lack of ', '') if pain_points else 'work faster'} "
                    f"— without switching tools."
                ),
                "mvp_features": mvp_features,
                "roadmap": [
                    {
                        "phase": "Week 1–2",
                        "milestone": "Core MVP",
                        "deliverables": [mvp_features[0]["feature"], mvp_features[1]["feature"], "Basic user auth"],
                    },
                    {
                        "phase": "Week 3–4",
                        "milestone": "Closed Beta",
                        "deliverables": [mvp_features[2]["feature"], "Onboarding flow", "Feedback collection"],
                    },
                    {
                        "phase": "Month 2",
                        "milestone": "Public Launch",
                        "deliverables": ["Stripe billing integration", "Product Hunt launch", "Referral system"],
                    },
                    {
                        "phase": "Month 3",
                        "milestone": "Growth & Retention",
                        "deliverables": ["Analytics dashboard", "Email drip campaigns", "Power-user features (P2)"],
                    },
                ],
                "success_metrics": [
                    {"metric": "Activated users (week 1)", "target": "50+ beta sign-ups"},
                    {"metric": "Core action completion", "target": ">60 % users complete main flow"},
                    {"metric": "Paid conversion", "target": "10 % free-to-paid by month 2"},
                    {"metric": "Net Promoter Score", "target": "NPS > 40 by month 3"},
                ],
                "out_of_scope_v1": [
                    "Mobile app (web-first, responsive)",
                    "Multi-language support",
                    "Advanced enterprise SSO",
                    "Offline mode",
                ],
            }

        self.status.output = result
        self._set_done(f"PRD complete. {len(result['mvp_features'])} MVP features defined.")
        return result
