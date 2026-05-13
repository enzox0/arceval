"""System and user prompt assembly for Claude."""

from __future__ import annotations

from arceval.core.models.project import ProjectData
from arceval.shared.constants import DEFAULT_MAX_CONTEXT_CHARS

SYSTEM_PROMPT = (
    "You are an expert software architect and enterprise systems evaluator. "
    "You analyze codebases and produce structured Enterprise Readiness Reports. "
    "Always respond with valid JSON only. No markdown. No explanation outside the JSON."
)

USER_PROMPT_TEMPLATE = """Analyze the following project and return a JSON object with this exact structure:

{{
  "project_name": "<detected project name>",
  "overall_score": <float, 1 decimal>,
  "overall_label": "<e.g. Strong Enterprise-Level System>",
  "categories": [
    {{
      "name": "Architecture",
      "score": <int 1-10>,
      "notes": "<one concise sentence>"
    }},
    {{
      "name": "Security",
      "score": <int 1-10>,
      "notes": "<one concise sentence>"
    }},
    {{
      "name": "Features",
      "score": <int 1-10>,
      "notes": "<one concise sentence>"
    }},
    {{
      "name": "Code Quality",
      "score": <int 1-10>,
      "notes": "<one concise sentence>"
    }},
    {{
      "name": "Scalability",
      "score": <int 1-10>,
      "notes": "<one concise sentence>"
    }},
    {{
      "name": "Observability",
      "score": <int 1-10>,
      "notes": "<one concise sentence>"
    }},
    {{
      "name": "Documentation",
      "score": <int 1-10>,
      "notes": "<one concise sentence>"
    }},
    {{
      "name": "DevOps",
      "score": <int 1-10>,
      "notes": "<one concise sentence>"
    }}
  ],
  "recommendations": [
    "<actionable recommendation 1>",
    "<actionable recommendation 2>",
    "<actionable recommendation 3>",
    "<actionable recommendation 4>"
  ]
}}

Here is the project data:

Project directory structure:
{directory_tree}

Key files collected:
{file_contents}"""


class PromptBuilder:
    """Assembles prompts for the Claude API."""

    def __init__(self, max_context_chars: int = DEFAULT_MAX_CONTEXT_CHARS) -> None:
        self.max_context_chars = max_context_chars

    def build_system_prompt(self) -> str:
        """Return the system prompt."""
        return SYSTEM_PROMPT

    def build_user_prompt(self, project_data: ProjectData) -> str:
        """Build the user prompt with project data.

        Args:
            project_data: Collected project information.

        Returns:
            The formatted user prompt string, truncated to max context chars.
        """
        file_contents = self._format_file_contents(project_data)

        prompt = USER_PROMPT_TEMPLATE.format(
            directory_tree=project_data.directory_tree,
            file_contents=file_contents,
        )

        # Enforce total context limit
        if len(prompt) > self.max_context_chars:
            prompt = prompt[: self.max_context_chars]
            prompt += "\n\n... [context truncated to fit limits]"

        return prompt

    def _format_file_contents(self, project_data: ProjectData) -> str:
        """Format all collected files into a single string."""
        sections: list[str] = []

        for file_node in project_data.all_collected_files:
            section = (
                f"--- {file_node.relative_path} ---\n"
                f"{file_node.content}\n"
            )
            sections.append(section)

        return "\n".join(sections)
