"""Anthropic SDK implementation of the AIClient port."""

from __future__ import annotations

import logging

import anthropic

from arceval.core.models.report import AnalysisReport
from arceval.core.ports.ai_client import AIClient
from arceval.infrastructure.ai.response_parser import parse_analysis_response
from arceval.shared.exceptions import AIClientError, APIResponseError

logger = logging.getLogger("arceval")


class ClaudeClient(AIClient):
    """Concrete implementation of AIClient using the Anthropic SDK."""

    def __init__(self, api_key: str, model: str, max_tokens: int) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self.client = anthropic.Anthropic(api_key=api_key)

    async def analyze(self, system_prompt: str, user_prompt: str) -> AnalysisReport:
        """Send prompts to Claude and return a parsed report.

        Uses the synchronous Anthropic client (called from async context
        via the CLI layer).

        Args:
            system_prompt: System-level instruction.
            user_prompt: User-level prompt with project data.

        Returns:
            Parsed AnalysisReport.

        Raises:
            AIClientError: On API failures.
            APIResponseError: On unexpected response format.
        """
        try:
            logger.debug(f"Sending request to Claude ({self.model})")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt},
                ],
            )
        except anthropic.AuthenticationError as e:
            raise AIClientError(
                "Authentication failed. Check your ANTHROPIC_API_KEY."
            ) from e
        except anthropic.RateLimitError as e:
            raise AIClientError(
                "Rate limited by Claude API. Please wait and try again."
            ) from e
        except anthropic.APIError as e:
            raise AIClientError(f"Claude API error: {e}") from e
        except Exception as e:
            raise AIClientError(f"Unexpected error calling Claude: {e}") from e

        # Extract text content from the response
        if not message.content:
            raise APIResponseError("Claude returned an empty response.")

        raw_text = ""
        for block in message.content:
            if hasattr(block, "text"):
                raw_text += block.text

        if not raw_text.strip():
            raise APIResponseError("Claude returned no text content.")

        logger.debug(f"Received {len(raw_text)} chars from Claude")

        return parse_analysis_response(raw_text)
