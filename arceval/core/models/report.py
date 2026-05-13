"""Domain models for the analysis report."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CategoryScore:
    """A single scored category in the report."""

    name: str
    score: int
    notes: str

    @property
    def color(self) -> str:
        """Return a color label based on score range."""
        if self.score >= 8:
            return "green"
        elif self.score >= 5:
            return "yellow"
        else:
            return "red"

    @property
    def emoji(self) -> str:
        """Return an emoji indicator based on score range."""
        if self.score >= 8:
            return "🟢"
        elif self.score >= 5:
            return "🟡"
        else:
            return "🔴"


@dataclass
class AnalysisReport:
    """The full enterprise readiness report."""

    project_name: str
    overall_score: float
    overall_label: str
    categories: list[CategoryScore] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    @property
    def overall_color(self) -> str:
        """Color for the overall score."""
        if self.overall_score >= 8.0:
            return "green"
        elif self.overall_score >= 5.0:
            return "yellow"
        else:
            return "red"
