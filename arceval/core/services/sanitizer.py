"""Path validation and input normalization."""

from __future__ import annotations

from pathlib import Path

from arceval.shared.exceptions import InvalidPathError


def validate_project_path(path_str: str) -> Path:
    """Validate and resolve a project path.

    Args:
        path_str: The raw path string from user input.

    Returns:
        A resolved Path object pointing to a valid directory.

    Raises:
        InvalidPathError: If the path does not exist or is not a directory.
    """
    path = Path(path_str).resolve()

    if not path.exists():
        raise InvalidPathError(path_str)

    if not path.is_dir():
        raise InvalidPathError(path_str)

    return path


def detect_project_name(path: Path) -> str:
    """Detect the project name from the directory path.

    Args:
        path: Resolved project directory path.

    Returns:
        The project name (directory basename).
    """
    return path.name or "unknown-project"
