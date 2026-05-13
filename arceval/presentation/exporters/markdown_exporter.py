"""Save report as a Markdown file."""

from __future__ import annotations

from pathlib import Path

from arceval.core.models.report import AnalysisReport


def export_markdown(report: AnalysisReport, output_path: str) -> Path:
    """Export the analysis report as a Markdown file.

    Args:
        report: The analysis report to export.
        output_path: File path for the Markdown output.

    Returns:
        The resolved path of the written file.
    """
    lines: list[str] = []

    lines.append(f"# Enterprise Readiness Report — {report.project_name}")
    lines.append("")
    lines.append(f"**Overall Score:** {report.overall_score}/10 — {report.overall_label}")
    lines.append("")
    lines.append("## Category Scores")
    lines.append("")
    lines.append("| Category | Score | Notes |")
    lines.append("|----------|-------|-------|")

    for cat in report.categories:
        emoji = "🟢" if cat.score >= 8 else ("🟡" if cat.score >= 5 else "🔴")
        lines.append(f"| {cat.name} | {emoji} {cat.score}/10 | {cat.notes} |")

    lines.append("")

    if report.recommendations:
        lines.append("## Recommendations")
        lines.append("")
        for i, rec in enumerate(report.recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

    content = "\n".join(lines)

    path = Path(output_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
