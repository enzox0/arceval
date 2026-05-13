"""Score averaging and label computation service."""

from __future__ import annotations

from arceval.core.models.report import AnalysisReport, CategoryScore


def compute_overall_score(categories: list[CategoryScore]) -> float:
    """Compute the average score across all categories.

    Args:
        categories: List of scored categories.

    Returns:
        Average score rounded to 1 decimal place.
    """
    if not categories:
        return 0.0
    total = sum(cat.score for cat in categories)
    return round(total / len(categories), 1)


def compute_overall_label(score: float) -> str:
    """Generate a human-readable label for the overall score.

    Args:
        score: The overall numeric score (1-10 scale).

    Returns:
        A descriptive label string.
    """
    if score >= 9.0:
        return "Exceptional Enterprise-Grade System"
    elif score >= 8.0:
        return "Strong Enterprise-Level System"
    elif score >= 7.0:
        return "Solid Foundation with Room for Growth"
    elif score >= 6.0:
        return "Developing System — Key Gaps to Address"
    elif score >= 5.0:
        return "Early Stage — Significant Improvements Needed"
    elif score >= 3.0:
        return "Prototype Stage — Not Enterprise Ready"
    else:
        return "Minimal Viability — Major Overhaul Required"


def validate_report(report: AnalysisReport) -> AnalysisReport:
    """Validate and normalize a report's scores.

    Ensures all scores are within 1-10 range and recalculates
    the overall score if needed.

    Args:
        report: The raw report from AI parsing.

    Returns:
        A validated report with clamped scores.
    """
    for category in report.categories:
        category.score = max(1, min(10, category.score))

    recalculated = compute_overall_score(report.categories)
    report.overall_score = recalculated
    report.overall_label = compute_overall_label(recalculated)

    return report
