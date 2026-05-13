"""Text processing utility functions."""

from __future__ import annotations


def truncate_lines(content: str, max_lines: int = 300) -> str:
    """Truncate content to a maximum number of lines.

    Args:
        content: The text content to truncate.
        max_lines: Maximum number of lines to keep.

    Returns:
        Truncated content with a note if lines were removed.
    """
    lines = content.splitlines(keepends=True)
    if len(lines) <= max_lines:
        return content
    truncated = "".join(lines[:max_lines])
    truncated += f"\n\n... [truncated — {len(lines) - max_lines} lines omitted]"
    return truncated


def estimate_tokens(text: str) -> int:
    """Rough token estimate (1 token ≈ 4 characters for English text)."""
    return len(text) // 4
