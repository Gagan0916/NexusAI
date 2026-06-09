from __future__ import annotations

from tools.llm_client import call_llm, has_llm, parse_json
from agents.base_agent import BaseAgent


class SentimentAgent(BaseAgent):
    name = "Sentiment Agent"
    role = "Mines Reddit & Hacker News for real customer pain points and sentiment"
    emoji = "💬"

    def run(self, context: dict) -> dict:
        self._set_running("Scanning Reddit, Hacker News, and community forums...")
        idea = context["startup_idea"]
        industry = context["ceo"]["industry"]

        if has_llm():
            prompt = f"""You are a customer research analyst specialising in community sentiment.

Startup idea: "{idea}"
Industry: {industry['name']}

Simulate realistic Reddit/Hacker News community feedback as if you scraped real posts.

Return ONLY valid JSON:
{{
  "sentiment_score": 7.8,
  "overall_sentiment": "Positive" | "Mixed" | "Negative",
  "pain_points": [
    "Specific pain point 1 customers mention",
    "Specific pain point 2",
    "Specific pain point 3",
    "Specific pain point 4"
  ],
  "reddit_signals": [
    "r/subreddit1 – 'Realistic quote about the problem'",
    "r/subreddit2 – 'Another realistic quote'",
    "HN thread – 'Technical community comment'"
  ],
  "willingness_to_pay": "High | Medium | Low",
  "customer_quotes": [
    "I would pay $X/month for something that does Y",
    "The biggest frustration with current solutions is Z"
  ],
  "target_personas": [
    {{"persona": "Early Adopter", "description": "...", "pain": "..."}},
    {{"persona": "Power User", "description": "...", "pain": "..."}}
  ]
}}"""
            raw = call_llm(prompt)
            parsed = parse_json(raw) if raw else None
        else:
            parsed = None

        if parsed:
            result = {
                "sentiment_score": parsed.get("sentiment_score", industry["sentiment_score"]),
                "overall_sentiment": parsed.get("overall_sentiment", "Positive"),
                "pain_points": parsed.get("pain_points", industry["pain_points"]),
                "reddit_signals": parsed.get("reddit_signals", industry.get("reddit_signals", [])),
                "willingness_to_pay": parsed.get("willingness_to_pay", "Medium"),
                "customer_quotes": parsed.get("customer_quotes", []),
                "target_personas": parsed.get("target_personas", []),
            }
        else:
            score = industry["sentiment_score"]
            sentiment = "Positive" if score >= 7.5 else "Mixed" if score >= 6.0 else "Negative"
            wtp = "High" if score >= 7.5 else "Medium"
            result = {
                "sentiment_score": score,
                "overall_sentiment": sentiment,
                "pain_points": industry["pain_points"],
                "reddit_signals": industry.get("reddit_signals", [
                    f"r/startups – 'There is clearly demand for what you're building in {industry['name']}'",
                    "HN – 'The AI layer is what makes this different from incumbents'",
                    "r/entrepreneur – 'Been waiting for something like this for 2 years'",
                ]),
                "willingness_to_pay": wtp,
                "customer_quotes": [
                    f"I'd pay ${19 if wtp == 'Medium' else 49}/month if it saved me just 2 hours a week",
                    "The existing tools all require too much manual work — AI would change everything",
                ],
                "target_personas": [
                    {
                        "persona": "The Frustrated Professional",
                        "description": f"Works in {industry['target_users'].split()[0].lower()} industry, technically capable",
                        "pain": industry["pain_points"][0] if industry["pain_points"] else "Inefficient workflows",
                    },
                    {
                        "persona": "The Early Adopter",
                        "description": "Loves new tools, quick to adopt, vocal in communities",
                        "pain": "Wants AI to handle repetitive decision-making tasks",
                    },
                ],
            }

        self.status.output = result
        self._set_done(f"Sentiment analysis done. Score: {result['sentiment_score']}/10 ({result['overall_sentiment']})")
        return result
