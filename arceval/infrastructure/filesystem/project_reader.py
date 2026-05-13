"""Disk I/O and gitignore-aware file reading."""

from __future__ import annotations

import logging
from pathlib import Path

from arceval.shared.constants import SKIP_DIRS

logger = logging.getLogger("arceval")


def read_gitignore_patterns(project_path: Path) -> list[str]:
    """Read .gitignore patterns from the project root.

    Args:
        project_path: The project root directory.

    Returns:
        A list of gitignore pattern strings.
    """
    gitignore_path = project_path / ".gitignore"
    if not gitignore_path.is_file():
        return []

    try:
        content = gitignore_path.read_text(encoding="utf-8", errors="replace")
        patterns = []
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
        return patterns
    except OSError:
        return []


def should_skip_path(path: Path, skip_dirs: set[str] | None = None) -> bool:
    """Determine if a path should be skipped during traversal.

    Args:
        path: The path to check.
        skip_dirs: Set of directory names to skip. Defaults to SKIP_DIRS.

    Returns:
        True if the path should be skipped.
    """
    dirs_to_skip = skip_dirs or SKIP_DIRS
    return any(part in dirs_to_skip for part in path.parts)


def safe_read_text(filepath: Path, max_size_kb: int = 30) -> str | None:
    """Safely read a text file with size limits.

    Args:
        filepath: Path to the file.
        max_size_kb: Maximum file size in KB.

    Returns:
        File content as string, or None if unreadable/too large.
    """
    try:
        size_kb = filepath.stat().st_size / 1024
        if size_kb > max_size_kb:
            logger.debug(f"Skipping {filepath} — too large ({size_kb:.1f} KB)")
            return None
        return filepath.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError) as e:
        logger.debug(f"Cannot read {filepath}: {e}")
        return None
