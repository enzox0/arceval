"""Main use case: orchestrate the full project analysis pipeline."""

from __future__ import annotations

import logging
from pathlib import Path

from arceval.core.models.config import AnalysisConfig
from arceval.core.models.project import ProjectData
from arceval.core.models.report import AnalysisReport
from arceval.core.ports.ai_client import AIClient
from arceval.core.services.collector import ProjectCollector
from arceval.core.services.sanitizer import validate_project_path
from arceval.core.services.scorer import validate_report
from arceval.shared.exceptions import ProjectTooSmallError

logger = logging.getLogger("arceval")


class AnalyzeProjectUseCase:
    """Orchestrates the full analysis pipeline.

    Steps:
        1. Validate the project path.
        2. Collect project files and structure.
        3. Send data to the AI client for analysis.
        4. Validate and return the report.
    """

    def __init__(self, ai_client: AIClient, config: AnalysisConfig | None = None) -> None:
        self.ai_client = ai_client
        self.config = config or AnalysisConfig()
        self.collector = ProjectCollector(self.config)

    async def execute(self, path_str: str) -> tuple[ProjectData, AnalysisReport]:
        """Run the full analysis pipeline.

        Args:
            path_str: The raw project path string.

        Returns:
            A tuple of (collected project data, analysis report).

        Raises:
            InvalidPathError: If the path is invalid.
            ProjectTooSmallError: If the project has too few files.
            AIClientError: If the AI analysis fails.
        """
        # Step 1: Validate path
        project_path: Path = validate_project_path(path_str)
        logger.info(f"Validated project path: {project_path}")

        # Step 2: Collect project data
        project_data = self.collector.collect(project_path)
        logger.info(
            f"Collected {project_data.total_files_found} files "
            f"across {project_data.total_dirs_found} directories"
        )

        if project_data.total_files_found < 2:
            raise ProjectTooSmallError()

        # Step 3: Build prompts and call AI
        from arceval.infrastructure.ai.prompt_builder import PromptBuilder

        prompt_builder = PromptBuilder(max_context_chars=self.config.max_context_chars)
        system_prompt = prompt_builder.build_system_prompt()
        user_prompt = prompt_builder.build_user_prompt(project_data)

        report = await self.ai_client.analyze(system_prompt, user_prompt)

        # Step 4: Validate and normalize
        report = validate_report(report)
        logger.info(f"Analysis complete: {report.overall_score}/10 — {report.overall_label}")

        return project_data, report
