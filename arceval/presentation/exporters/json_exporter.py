"""Save report as a JSON file."""

from __future__ import annotations

import json
from pathlib import Path

from arceval.core.models.report import AnalysisReport


def export_json(report: AnalysisReport, output_path: str) -> Path:
    """Export the analysis report as a JSON file.

    Args:
        report: The analysis report to export.
        output_path: File path for the JSON output.

    Returns:
        The resolved path of the written file.
    """
    data = {
        "project_name": report.project_name,
        "overall_score": report.overall_score,
        "overall_label": report.overall_label,
        "categories": [
            {
                "name": cat.name,
                "score": cat.score,
                "notes": cat.notes,
            }
            for cat in report.categories
        ],
        "recommendations": report.recommendations,
    }

    path = Path(output_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
