"""Abstract interface for the AI analysis backend."""

from __future__ import annotations

from abc import ABC, abstractmethod

from arceval.core.models.report import AnalysisReport


class AIClient(ABC):
    """Port for AI-powered code analysis.

    Implementations must accept a structured prompt and return
    a parsed AnalysisReport.
    """

    @abstractmethod
    async def analyze(self, system_prompt: str, user_prompt: str) -> AnalysisReport:
        """Send prompts to the AI backend and return a structured report.

        Args:
            system_prompt: The system-level instruction.
            user_prompt: The user-level prompt containing project data.

        Returns:
            A fully parsed AnalysisReport.

        Raises:
            AIClientError: If the API call fails.
            JSONParseError: If the response cannot be parsed.
        """
        ...
