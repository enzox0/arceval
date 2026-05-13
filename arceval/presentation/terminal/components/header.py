"""Banner / title panel component."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from arceval.presentation.terminal.themes.default import HEADER_BORDER_STYLE, HEADER_STYLE


def render_header(console: Console, project_name: str) -> None:
    """Render the report header panel.

    Args:
        console: Rich console instance.
        project_name: Name of the analyzed project.
    """
    title_text = Text()
    title_text.append("Enterprise Readiness Score\n", style=HEADER_STYLE)
    title_text.append(f"Project: {project_name}", style="bold white")
    title_text.justify = "center"

    panel = Panel(
        title_text,
        border_style=HEADER_BORDER_STYLE,
        padding=(1, 4),
    )
    console.print()
    console.print(panel)
    console.print()
