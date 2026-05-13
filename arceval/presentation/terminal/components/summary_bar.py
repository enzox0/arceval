"""Overall score summary line component."""

from __future__ import annotations

from rich.console import Console
from rich.text import Text

from arceval.presentation.terminal.themes.default import score_color


def render_summary(console: Console, overall_score: float, overall_label: str) -> None:
    """Render the overall score summary line.

    Args:
        console: Rich console instance.
        overall_score: The computed overall score.
        overall_label: The human-readable label.
    """
    color = score_color(overall_score)

    summary = Text()
    summary.append("\n  Overall Score: ", style="bold")
    summary.append(f"{overall_score}/10", style=color)
    summary.append(f" — {overall_label}", style="bold")
    summary.append("\n")

    console.print(summary)
