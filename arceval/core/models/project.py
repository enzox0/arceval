"""Domain models representing a collected project."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FileNode:
    """A single collected file with its content."""

    path: Path
    relative_path: str
    content: str
    size_bytes: int
    extension: str


@dataclass
class ProjectData:
    """All data collected from a project for analysis."""

    name: str
    root_path: Path
    directory_tree: str
    key_files: list[FileNode] = field(default_factory=list)
    ci_files: list[FileNode] = field(default_factory=list)
    source_files: list[FileNode] = field(default_factory=list)
    total_files_found: int = 0
    total_dirs_found: int = 0

    @property
    def all_collected_files(self) -> list[FileNode]:
        """Return all collected files across categories."""
        return self.key_files + self.ci_files + self.source_files
