"""Integration tests for the end-to-end analysis pipeline."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from arceval.core.models.config import AnalysisConfig
from arceval.core.models.report import AnalysisReport, CategoryScore
from arceval.core.use_cases.analyze_project import AnalyzeProjectUseCase


@pytest.fixture
def mock_report() -> AnalysisReport:
    """Create a mock report that the AI client will return."""
    return AnalysisReport(
        project_name="sample-project",
        overall_score=7.6,
        overall_label="Strong Enterprise-Level System",
        categories=[
            CategoryScore(name="Architecture", score=9, notes="Good."),
            CategoryScore(name="Security", score=8, notes="Solid."),
            CategoryScore(name="Features", score=7, notes="Decent."),
            CategoryScore(name="Code Quality", score=8, notes="Clean."),
            CategoryScore(name="Scalability", score=6, notes="Needs work."),
            CategoryScore(name="Observability", score=5, notes="Basic."),
            CategoryScore(name="Documentation", score=7, notes="OK."),
            CategoryScore(name="DevOps", score=6, notes="Minimal."),
        ],
        recommendations=["Add tests", "Add CI/CD"],
    )


@pytest.mark.integration
class TestAnalysisPipeline:
    """End-to-end pipeline tests with mocked AI client."""

    @pytest.mark.asyncio
    async def test_full_pipeline(
        self, sample_project_path: Path, mock_report: AnalysisReport
    ) -> None:
        """Should run the full pipeline and return a validated report."""
        # Create a mock AI client
        mock_ai_client = AsyncMock()
        mock_ai_client.analyze.return_value = mock_report

        config = AnalysisConfig()
        use_case = AnalyzeProjectUseCase(ai_client=mock_ai_client, config=config)

        project_data, report = await use_case.execute(str(sample_project_path))

        # Verify project data was collected
        assert project_data.name == "sample-project"
        assert project_data.total_files_found >= 3

        # Verify report was validated
        assert report.overall_score > 0
        assert len(report.categories) == 8
        assert all(1 <= cat.score <= 10 for cat in report.categories)

    @pytest.mark.asyncio
    async def test_pipeline_rejects_invalid_path(self, mock_report: AnalysisReport) -> None:
        """Should raise InvalidPathError for nonexistent path."""
        from arceval.shared.exceptions import InvalidPathError

        mock_ai_client = AsyncMock()
        mock_ai_client.analyze.return_value = mock_report

        use_case = AnalyzeProjectUseCase(ai_client=mock_ai_client)

        with pytest.raises(InvalidPathError):
            await use_case.execute("/nonexistent/path/xyz")
