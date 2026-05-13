"""File-related utility functions."""

from __future__ import annotations

from pathlib import Path

from arceval.shared.constants import SOURCE_EXTENSIONS


def get_extension(path: Path) -> str:
    """Return the lowercase file extension including the dot."""
    return path.suffix.lower()


def is_source_file(path: Path) -> bool:
    """Check if a file is a recognized source code file."""
    return get_extension(path) in SOURCE_EXTENSIONS


def format_size(size_bytes: int) -> str:
    """Format a byte count into a human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def file_size_kb(path: Path) -> float:
    """Return file size in kilobytes."""
    try:
        return path.stat().st_size / 1024
    except OSError:
        return 0.0
