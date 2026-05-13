"""Color-coded category score table component."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from arceval.core.models.report import CategoryScore
from arceval.presentation.terminal.themes.default import (
    CATEGORY_NAME_STYLE,
    NOTES_STYLE,
    TABLE_HEADER_STYLE,
    score_color,
    score_emoji,
)


def render_score_table(console: Console, categories: list[CategoryScore]) -> None:
    """Render the scored category table.

    Args:
        console: Rich console instance.
        categories: List of scored categories.
    """
    table = Table(show_header=True, header_style=TABLE_HEADER_STYLE, expand=True)
    table.add_column("Category", style=CATEGORY_NAME_STYLE, min_width=16)
    table.add_column("Score", justify="center", min_width=8)
    table.add_column("Notes", style=NOTES_STYLE)

    for cat in categories:
        emoji = score_emoji(cat.score)
        color = score_color(cat.score)
        score_str = f"[{color}]{emoji} {cat.score}/10[/{color}]"
        table.add_row(cat.name, score_str, cat.notes)

    console.print(table)
