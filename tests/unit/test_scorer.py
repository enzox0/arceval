"""Unit tests for the scoring engine."""

from __future__ import annotations

from arceval.core.models.report import AnalysisReport, CategoryScore
from arceval.core.services.scorer import (
    compute_overall_label,
    compute_overall_score,
    validate_report,
)


class TestComputeOverallScore:
    """Tests for compute_overall_score."""

    def test_average_of_scores(self) -> None:
        """Should compute the average of all category scores."""
        categories = [
            CategoryScore(name="A", score=8, notes=""),
            CategoryScore(name="B", score=6, notes=""),
        ]
        assert compute_overall_score(categories) == 7.0

    def test_empty_categories(self) -> None:
        """Should return 0.0 for empty list."""
        assert compute_overall_score([]) == 0.0

    def test_single_category(self) -> None:
        """Should return the single score."""
        categories = [CategoryScore(name="A", score=9, notes="")]
        assert compute_overall_score(categories) == 9.0

    def test_rounds_to_one_decimal(self) -> None:
        """Should round to 1 decimal place."""
        categories = [
            CategoryScore(name="A", score=7, notes=""),
            CategoryScore(name="B", score=8, notes=""),
            CategoryScore(name="C", score=6, notes=""),
        ]
        assert compute_overall_score(categories) == 7.0


class TestComputeOverallLabel:
    """Tests for compute_overall_label."""

    def test_exceptional(self) -> None:
        assert "Exceptional" in compute_overall_label(9.5)

    def test_strong(self) -> None:
        assert "Strong" in compute_overall_label(8.0)

    def test_solid(self) -> None:
        assert "Solid" in compute_overall_label(7.0)

    def test_developing(self) -> None:
        assert "Developing" in compute_overall_label(6.0)

    def test_early_stage(self) -> None:
        assert "Early" in compute_overall_label(5.0)

    def test_prototype(self) -> None:
        assert "Prototype" in compute_overall_label(3.0)

    def test_minimal(self) -> None:
        assert "Minimal" in compute_overall_label(2.0)


class TestValidateReport:
    """Tests for validate_report."""

    def test_clamps_high_scores(self) -> None:
        """Scores above 10 should be clamped to 10."""
        report = AnalysisReport(
            project_name="test",
            overall_score=0,
            overall_label="",
            categories=[CategoryScore(name="A", score=15, notes="")],
        )
        validated = validate_report(report)
        assert validated.categories[0].score == 10

    def test_clamps_low_scores(self) -> None:
        """Scores below 1 should be clamped to 1."""
        report = AnalysisReport(
            project_name="test",
            overall_score=0,
            overall_label="",
            categories=[CategoryScore(name="A", score=-3, notes="")],
        )
        validated = validate_report(report)
        assert validated.categories[0].score == 1

    def test_recalculates_overall(self) -> None:
        """Should recalculate overall score from categories."""
        report = AnalysisReport(
            project_name="test",
            overall_score=0,
            overall_label="",
            categories=[
                CategoryScore(name="A", score=8, notes=""),
                CategoryScore(name="B", score=6, notes=""),
            ],
        )
        validated = validate_report(report)
        assert validated.overall_score == 7.0
        assert validated.overall_label != ""
