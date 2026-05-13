"""Rich implementation of the ReportRenderer port."""

from __future__ import annotations

from rich.console import Console

from arceval.core.models.report import AnalysisReport
from arceval.core.ports.report_renderer import ReportRenderer
from arceval.presentation.terminal.components.header import render_header
from arceval.presentation.terminal.components.recommendations import render_recommendations
from arceval.presentation.terminal.components.score_table import render_score_table
from arceval.presentation.terminal.components.summary_bar import render_summary


class TerminalRenderer(ReportRenderer):
    """Renders an AnalysisReport to the terminal using rich."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def render(self, report: AnalysisReport) -> None:
        """Render the full report to the terminal.

        Args:
            report: The analysis report to display.
        """
        render_header(self.console, report.project_name)
        render_score_table(self.console, report.categories)
        render_summary(self.console, report.overall_score, report.overall_label)
        render_recommendations(self.console, report.recommendations)
