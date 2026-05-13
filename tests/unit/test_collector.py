"""Unit tests for the file collection service."""

from __future__ import annotations

from pathlib import Path

from arceval.core.models.config import AnalysisConfig
from arceval.core.services.collector import ProjectCollector


class TestProjectCollector:
    """Tests for ProjectCollector."""

    def test_collect_finds_readme(self, sample_project_path: Path) -> None:
        """Collector should find README.md in key files."""
        config = AnalysisConfig()
        collector = ProjectCollector(config)
        data = collector.collect(sample_project_path)

        key_file_names = [f.relative_path for f in data.key_files]
        assert "README.md" in key_file_names

    def test_collect_finds_pyproject(self, sample_project_path: Path) -> None:
        """Collector should find pyproject.toml in key files."""
        config = AnalysisConfig()
        collector = ProjectCollector(config)
        data = collector.collect(sample_project_path)

        key_file_names = [f.relative_path for f in data.key_files]
        assert "pyproject.toml" in key_file_names

    def test_collect_finds_source_files(self, sample_project_path: Path) -> None:
        """Collector should sample source files."""
        config = AnalysisConfig()
        collector = ProjectCollector(config)
        data = collector.collect(sample_project_path)

        assert len(data.source_files) > 0
        extensions = {f.extension for f in data.source_files}
        assert ".py" in extensions

    def test_collect_respects_max_source_files(self, sample_project_path: Path) -> None:
        """Collector should not exceed max_source_files limit."""
        config = AnalysisConfig(max_source_files=1)
        collector = ProjectCollector(config)
        data = collector.collect(sample_project_path)

        assert len(data.source_files) <= 1

    def test_collect_builds_directory_tree(self, sample_project_path: Path) -> None:
        """Collector should produce a non-empty directory tree."""
        config = AnalysisConfig()
        collector = ProjectCollector(config)
        data = collector.collect(sample_project_path)

        assert data.directory_tree
        assert "src" in data.directory_tree

    def test_collect_detects_project_name(self, sample_project_path: Path) -> None:
        """Collector should detect the project name from the directory."""
        config = AnalysisConfig()
        collector = ProjectCollector(config)
        data = collector.collect(sample_project_path)

        assert data.name == "sample-project"

    def test_collect_counts_files_and_dirs(self, sample_project_path: Path) -> None:
        """Collector should count total files and directories."""
        config = AnalysisConfig()
        collector = ProjectCollector(config)
        data = collector.collect(sample_project_path)

        assert data.total_files_found >= 3  # README, pyproject, main.py, utils.py, test
        assert data.total_dirs_found >= 2  # src, tests

    def test_collect_skips_node_modules(self, sample_project_path: Path) -> None:
        """Collector should skip node_modules directory."""
        # Create a node_modules dir with a file
        nm = sample_project_path / "node_modules"
        nm.mkdir()
        (nm / "package.json").write_text("{}")

        config = AnalysisConfig()
        collector = ProjectCollector(config)
        data = collector.collect(sample_project_path)

        all_paths = [f.relative_path for f in data.all_collected_files]
        assert not any("node_modules" in p for p in all_paths)
