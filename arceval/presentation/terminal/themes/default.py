"""Default color palette and style constants for terminal output."""

from __future__ import annotations

# Score color mapping
SCORE_COLOR_HIGH = "bold green"
SCORE_COLOR_MID = "bold yellow"
SCORE_COLOR_LOW = "bold red"

# Panel styles
HEADER_STYLE = "bold cyan"
HEADER_BORDER_STYLE = "bright_cyan"
RECOMMENDATION_BORDER_STYLE = "bright_blue"

# Table styles
TABLE_HEADER_STYLE = "bold white"
TABLE_BORDER_STYLE = "dim"

# Text styles
CATEGORY_NAME_STYLE = "bold"
NOTES_STYLE = "dim"
OVERALL_SCORE_STYLE = "bold"

# Emojis
EMOJI_HIGH = "🟢"
EMOJI_MID = "🟡"
EMOJI_LOW = "🔴"
EMOJI_CHECK = "✔"
EMOJI_SPINNER = "dots"


def score_color(score: int | float) -> str:
    """Return the appropriate color style for a score value."""
    if score >= 8:
        return SCORE_COLOR_HIGH
    elif score >= 5:
        return SCORE_COLOR_MID
    else:
        return SCORE_COLOR_LOW


def score_emoji(score: int | float) -> str:
    """Return the appropriate emoji for a score value."""
    if score >= 8:
        return EMOJI_HIGH
    elif score >= 5:
        return EMOJI_MID
    else:
        return EMOJI_LOW
