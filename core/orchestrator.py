from __future__ import annotations

import time
from typing import Generator

from agents.ceo_agent import CEOAgent
from agents.research_agent import MarketResearchAgent
from agents.sentiment_agent import SentimentAgent
from agents.analyst_agent import BusinessAnalystAgent
from agents.architect_agent import TechnicalArchitectAgent
from agents.pm_agent import ProductManagerAgent
from agents.engineer_agent import SoftwareEngineerAgent
from agents.docs_agent import DocumentationAgent


class NexusOrchestrator:
    def __init__(self):
        self.agents = [
            CEOAgent(),
            MarketResearchAgent(),
            SentimentAgent(),
            BusinessAnalystAgent(),
            TechnicalArchitectAgent(),
            ProductManagerAgent(),
            SoftwareEngineerAgent(),
            DocumentationAgent(),
        ]
        self.context: dict = {}

    @property
    def agent_statuses(self):
        return [a.status for a in self.agents]

    def run_streaming(self, startup_idea: str) -> Generator[tuple[str, dict], None, None]:
        """Run all agents sequentially, yielding (agent_name, context) after each step."""
        self.context = {"startup_idea": startup_idea}

        key_map = {
            "CEO Agent": "ceo",
            "Market Research Agent": "research",
            "Sentiment Agent": "sentiment",
            "Business Analyst Agent": "analyst",
            "Technical Architect Agent": "architect",
            "Product Manager Agent": "pm",
            "Software Engineer Agent": "engineer",
            "Documentation Agent": "docs",
        }

        for agent in self.agents:
            start = time.time()
            try:
                output = agent.run(self.context)
                key = key_map.get(agent.name, agent.name.lower().replace(" ", "_"))
                self.context[key] = output
                elapsed = round(time.time() - start, 1)
                agent.status.message += f" ({elapsed}s)"
            except Exception as exc:
                agent._set_error(str(exc))

            yield agent.name, dict(self.context)

    def run(self, startup_idea: str) -> dict:
        """Run the full pipeline and return the final context."""
        result = {}
        for _, ctx in self.run_streaming(startup_idea):
            result = ctx
        return result
