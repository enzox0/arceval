"""JSON extraction and schema validation for Claude responses."""

from __future__ import annotations

import json
import logging
import re

from arceval.core.models.report import AnalysisReport, CategoryScore
from arceval.shared.exceptions import JSONParseError

logger = logging.getLogger("arceval")


def parse_analysis_response(raw_response: str) -> AnalysisReport:
    """Parse Claude's raw text response into an AnalysisReport.

    Attempts to extract JSON from the response, handling cases where
    Claude may wrap JSON in markdown code fences.

    Args:
        raw_response: The raw text from Claude's API response.

    Returns:
        A parsed AnalysisReport.

    Raises:
        JSONParseError: If the response cannot be parsed as valid JSON.
    """
    json_str = _extract_json(raw_response)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        raise JSONParseError(raw_response) from e

    return _build_report(data, raw_response)


def _extract_json(text: str) -> str:
    """Extract JSON from text, handling markdown code fences."""
    # Try to find JSON in code fences first
    fence_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if fence_match:
        return fence_match.group(1).strip()

    # Try to find a JSON object directly
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        return brace_match.group(0)

    # Return as-is and let json.loads handle the error
    return text.strip()


def _build_report(data: dict, raw_response: str) -> AnalysisReport:
    """Build an AnalysisReport from parsed JSON data.

    Args:
        data: Parsed JSON dictionary.
        raw_response: Original response for error reporting.

    Returns:
        A constructed AnalysisReport.

    Raises:
        JSONParseError: If required fields are missing.
    """
    try:
        categories = [
            CategoryScore(
                name=cat["name"],
                score=int(cat["score"]),
                notes=str(cat.get("notes", "")),
            )
            for cat in data.get("categories", [])
        ]

        return AnalysisReport(
            project_name=str(data.get("project_name", "unknown")),
            overall_score=float(data.get("overall_score", 0.0)),
            overall_label=str(data.get("overall_label", "")),
            categories=categories,
            recommendations=[str(r) for r in data.get("recommendations", [])],
        )
    except (KeyError, TypeError, ValueError) as e:
        logger.error(f"Failed to build report from JSON: {e}")
        raise JSONParseError(raw_response) from e
