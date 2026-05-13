"""Abstract ports (interfaces) for dependency inversion."""

from arceval.core.ports.ai_client import AIClient
from arceval.core.ports.report_renderer import ReportRenderer

__all__ = ["AIClient", "ReportRenderer"]
