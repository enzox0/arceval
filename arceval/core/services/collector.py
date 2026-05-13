"""File tree walking and content sampling service."""

from __future__ import annotations

import logging
from pathlib import Path

from arceval.core.models.config import AnalysisConfig
from arceval.core.models.project import FileNode, ProjectData
from arceval.core.services.sanitizer import detect_project_name
from arceval.shared.constants import CI_PATTERNS, KEY_FILES, SKIP_DIRS, SOURCE_EXTENSIONS
from arceval.shared.utils.file_utils import file_size_kb
from arceval.shared.utils.text_utils import truncate_lines

logger = logging.getLogger("arceval")


class ProjectCollector:
    """Walks a project directory and collects relevant files for analysis."""

    def __init__(self, config: AnalysisConfig) -> None:
        self.config = config

    def collect(self, project_path: Path) -> ProjectData:
        """Collect project data from the given path.

        Args:
            project_path: Resolved path to the project root.

        Returns:
            A ProjectData instance with all collected information.
        """
        project_name = detect_project_name(project_path)
        directory_tree = self._build_directory_tree(project_path)
        key_files = self._collect_key_files(project_path)
        ci_files = self._collect_ci_files(project_path)
        source_files = self._collect_source_files(project_path)

        total_files, total_dirs = self._count_entries(project_path)

        return ProjectData(
            name=project_name,
            root_path=project_path,
            directory_tree=directory_tree,
            key_files=key_files,
            ci_files=ci_files,
            source_files=source_files,
            total_files_found=total_files,
            total_dirs_found=total_dirs,
        )

    def _build_directory_tree(self, root: Path, depth: int = 0) -> str:
        """Build a text representation of the directory tree up to configured depth."""
        if depth >= self.config.directory_depth:
            return ""

        lines: list[str] = []
        try:
            entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            return ""

        for entry in entries:
            if entry.name in SKIP_DIRS:
                continue
            if entry.name.startswith(".") and entry.name not in (".github", ".gitlab-ci.yml"):
                continue

            indent = "  " * depth
            if entry.is_dir():
                lines.append(f"{indent}{entry.name}/")
                subtree = self._build_directory_tree(entry, depth + 1)
                if subtree:
                    lines.append(subtree)
            else:
                lines.append(f"{indent}{entry.name}")

        return "\n".join(lines)

    def _collect_key_files(self, root: Path) -> list[FileNode]:
        """Collect known key files from the project root."""
        collected: list[FileNode] = []
        for filename in KEY_FILES:
            filepath = root / filename
            if filepath.is_file():
                node = self._read_file_node(filepath, root)
                if node:
                    collected.append(node)
        return collected

    def _collect_ci_files(self, root: Path) -> list[FileNode]:
        """Collect CI configuration files (up to 2)."""
        collected: list[FileNode] = []
        for pattern in CI_PATTERNS:
            for filepath in root.glob(pattern):
                if filepath.is_file() and len(collected) < 2:
                    node = self._read_file_node(filepath, root)
                    if node:
                        collected.append(node)
        return collected

    def _collect_source_files(self, root: Path) -> list[FileNode]:
        """Sample source files sorted by size (smallest first)."""
        candidates: list[Path] = []

        for filepath in root.rglob("*"):
            if not filepath.is_file():
                continue
            if any(skip in filepath.parts for skip in SKIP_DIRS):
                continue
            if filepath.suffix.lower() not in SOURCE_EXTENSIONS:
                continue
            if file_size_kb(filepath) > self.config.max_file_size_kb:
                continue
            candidates.append(filepath)

        # Sort by size ascending — prefer smaller files for context efficiency
        candidates.sort(key=lambda p: p.stat().st_size)

        collected: list[FileNode] = []
        for filepath in candidates[: self.config.max_source_files]:
            node = self._read_file_node(filepath, root)
            if node:
                collected.append(node)

        return collected

    def _read_file_node(self, filepath: Path, root: Path) -> FileNode | None:
        """Read a file and return a FileNode, or None on failure."""
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
            content = truncate_lines(content, self.config.max_file_lines)
            return FileNode(
                path=filepath,
                relative_path=str(filepath.relative_to(root)),
                content=content,
                size_bytes=filepath.stat().st_size,
                extension=filepath.suffix.lower(),
            )
        except (OSError, UnicodeDecodeError) as e:
            logger.debug(f"Skipping file {filepath}: {e}")
            return None

    def _count_entries(self, root: Path) -> tuple[int, int]:
        """Count total files and directories (respecting skip rules)."""
        total_files = 0
        total_dirs = 0
        try:
            for entry in root.rglob("*"):
                if any(skip in entry.parts for skip in SKIP_DIRS):
                    continue
                if entry.is_file():
                    total_files += 1
                elif entry.is_dir():
                    total_dirs += 1
        except PermissionError:
            pass
        return total_files, total_dirs
