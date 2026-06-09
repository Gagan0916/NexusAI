from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentStatus:
    name: str
    role: str
    emoji: str
    status: str = "waiting"   # waiting | running | done | error
    message: str = ""
    output: dict = field(default_factory=dict)


class BaseAgent(ABC):
    name: str = "Base Agent"
    role: str = "Generic agent"
    emoji: str = "🤖"

    def __init__(self):
        self.status = AgentStatus(
            name=self.name,
            role=self.role,
            emoji=self.emoji,
        )

    @abstractmethod
    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute agent logic. Reads from context, returns output dict."""

    def _set_running(self, message: str = ""):
        self.status.status = "running"
        self.status.message = message or f"{self.name} is working..."

    def _set_done(self, message: str = ""):
        self.status.status = "done"
        self.status.message = message or f"{self.name} completed successfully."

    def _set_error(self, message: str = ""):
        self.status.status = "error"
        self.status.message = message or f"{self.name} encountered an error."
