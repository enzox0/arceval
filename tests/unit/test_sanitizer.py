"""Unit tests for input sanitization."""

from __future__ import annotations

from pathlib import Path

import pytest

from arceval.core.services.sanitizer import detect_project_name, validate_project_path
from arceval.shared.exceptions import InvalidPathError


class TestValidateProjectPath:
    """Tests for validate_project_path."""

    def test_valid_directory(self, tmp_path: Path) -> None:
        """Should return resolved path for valid directory."""
        result = validate_project_path(str(tmp_path))
        assert result == tmp_path.resolve()

    def test_nonexistent_path(self) -> None:
        """Should raise InvalidPathError for nonexistent path."""
        with pytest.raises(InvalidPathError):
            validate_project_path("/nonexistent/path/xyz123")

    def test_file_path(self, tmp_path: Path) -> None:
        """Should raise InvalidPathError for a file (not directory)."""
        file = tmp_path / "test.txt"
        file.write_text("hello")
        with pytest.raises(InvalidPathError):
            validate_project_path(str(file))


class TestDetectProjectName:
    """Tests for detect_project_name."""

    def test_detects_directory_name(self, tmp_path: Path) -> None:
        """Should return the directory basename."""
        project = tmp_path / "my-cool-app"
        project.mkdir()
        assert detect_project_name(project) == "my-cool-app"

    def test_handles_root_path(self) -> None:
        """Should handle edge case of root-like paths."""
        # Path("/") has name "" on Unix, but we handle it
        result = detect_project_name(Path("/some/project"))
        assert result == "project"
