"""Shared fixtures and test configuration."""

from __future__ import annotations

from pathlib import Path

import pytest

from arceval.core.models.config import AnalysisConfig
from arceval.core.models.report import AnalysisReport, CategoryScore


@pytest.fixture
def sample_project_path(tmp_path: Path) -> Path:
    """Create a minimal fake project for testing."""
    project = tmp_path / "sample-project"
    project.mkdir()

    # README
    (project / "README.md").write_text("# Sample Project\nA test project.\n")

    # pyproject.toml
    (project / "pyproject.toml").write_text(
        '[project]\nname = "sample-project"\nversion = "1.0.0"\n'
    )

    # Source files
    src = project / "src"
    src.mkdir()
    (src / "main.py").write_text("def main():\n    print('hello')\n\nif __name__ == '__main__':\n    main()\n")
    (src / "utils.py").write_text("def add(a: int, b: int) -> int:\n    return a + b\n")

    # A test file
    tests = project / "tests"
    tests.mkdir()
    (tests / "test_main.py").write_text("def test_main():\n    assert True\n")

    return project


@pytest.fixture
def sample_report() -> AnalysisReport:
    """Create a sample AnalysisReport for testing."""
    return AnalysisReport(
        project_name="test-project",
        overall_score=7.6,
        overall_label="Strong Enterprise-Level System",
        categories=[
            CategoryScore(name="Architecture", score=9, notes="Excellent layered design."),
            CategoryScore(name="Security", score=9, notes="Comprehensive security measures."),
            CategoryScore(name="Features", score=10, notes="Rich feature set."),
            CategoryScore(name="Code Quality", score=8, notes="Good TypeScript usage."),
            CategoryScore(name="Scalability", score=7, notes="Good foundation."),
            CategoryScore(name="Observability", score=5, notes="Basic logging."),
            CategoryScore(name="Documentation", score=7, notes="Good README."),
            CategoryScore(name="DevOps", score=6, notes="Basic setup."),
        ],
        recommendations=[
            "Add APM tooling (Datadog, OpenTelemetry)",
            "Set up CI/CD pipeline (GitHub Actions)",
            "Write API specification (OpenAPI/Swagger)",
            "Add caching layer (Redis) for scalability",
        ],
    )


@pytest.fixture
def mock_claude_response() -> str:
    """Return a canned Claude JSON response."""
    fixtures_dir = Path(__file__).parent / "fixtures" / "mock_responses"
    response_file = fixtures_dir / "claude_analysis.json"
    return response_file.read_text(encoding="utf-8")


@pytest.fixture
def analysis_config() -> AnalysisConfig:
    """Return a default AnalysisConfig for tests."""
    return AnalysisConfig()
