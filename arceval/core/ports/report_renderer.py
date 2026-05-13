"""Abstract interface for report rendering."""

from __future__ import annotations

from abc import ABC, abstractmethod

from arceval.core.models.report import AnalysisReport


class ReportRenderer(ABC):
    """Port for rendering an AnalysisReport to an output target."""

    @abstractmethod
    def render(self, report: AnalysisReport) -> None:
        """Render the report.

        Args:
            report: The analysis report to render.
        """
        ...
