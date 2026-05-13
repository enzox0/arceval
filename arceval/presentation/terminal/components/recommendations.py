"""Recommendations panel component."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from arceval.presentation.terminal.themes.default import RECOMMENDATION_BORDER_STYLE


def render_recommendations(console: Console, recommendations: list[str]) -> None:
    """Render the recommendations panel.

    Args:
        console: Rich console instance.
        recommendations: List of actionable recommendation strings.
    """
    if not recommendations:
        return

    content = Text()
    for i, rec in enumerate(recommendations, 1):
        content.append(f"  {i}. {rec}\n")

    panel = Panel(
        content,
        title="Top Recommendations",
        title_align="left",
        border_style=RECOMMENDATION_BORDER_STYLE,
        padding=(0, 1),
    )
    console.print()
    console.print(panel)
    console.print()
