"""Unit tests for output rendering (report formatter)."""

from __future__ import annotations

from io import StringIO

from rich.console import Console

from arceval.core.models.report import AnalysisReport, CategoryScore
from arceval.presentation.terminal.renderer import TerminalRenderer


class TestTerminalRenderer:
    """Tests for TerminalRenderer."""

    def test_render_produces_output(self, sample_report: AnalysisReport) -> None:
        """Renderer should produce non-empty output."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=100)
        renderer = TerminalRenderer(console=console)

        renderer.render(sample_report)

        rendered = output.getvalue()
        assert len(rendered) > 0

    def test_render_contains_project_name(self, sample_report: AnalysisReport) -> None:
        """Rendered output should contain the project name."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=100)
        renderer = TerminalRenderer(console=console)

        renderer.render(sample_report)

        rendered = output.getvalue()
        assert "test-project" in rendered

    def test_render_contains_scores(self, sample_report: AnalysisReport) -> None:
        """Rendered output should contain score values."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=100)
        renderer = TerminalRenderer(console=console)

        renderer.render(sample_report)

        rendered = output.getvalue()
        assert "9/10" in rendered
        assert "10/10" in rendered

    def test_render_contains_recommendations(self, sample_report: AnalysisReport) -> None:
        """Rendered output should contain recommendations."""
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=100)
        renderer = TerminalRenderer(console=console)

        renderer.render(sample_report)

        rendered = output.getvalue()
        assert "Recommendations" in rendered
        assert "APM" in rendered

    def test_render_empty_recommendations(self) -> None:
        """Renderer should handle empty recommendations gracefully."""
        report = AnalysisReport(
            project_name="empty",
            overall_score=5.0,
            overall_label="Test",
            categories=[CategoryScore(name="A", score=5, notes="ok")],
            recommendations=[],
        )
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=100)
        renderer = TerminalRenderer(console=console)

        renderer.render(report)

        rendered = output.getvalue()
        assert "empty" in rendered
