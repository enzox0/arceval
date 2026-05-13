"""OpenAI SDK implementation of the AIClient port."""

from __future__ import annotations

import logging

from arceval.core.models.report import AnalysisReport
from arceval.core.ports.ai_client import AIClient
from arceval.infrastructure.ai.response_parser import parse_analysis_response
from arceval.shared.exceptions import AIClientError, APIResponseError

logger = logging.getLogger("arceval")


class OpenAIClient(AIClient):
    """Concrete implementation of AIClient using the OpenAI SDK.

    Supports OpenAI GPT models, Azure OpenAI, and any OpenAI-compatible API.
    """

    def __init__(
        self, api_key: str, model: str, max_tokens: int, base_url: str = ""
    ) -> None:
        self.model = model
        self.max_tokens = max_tokens

        try:
            import openai
        except ImportError as e:
            raise AIClientError(
                "OpenAI SDK not installed. Install it with: "
                "uv pip install arceval[openai]  or  pip install openai"
            ) from e

        kwargs: dict = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url

        self.client = openai.OpenAI(**kwargs)
        self._openai = openai

    async def analyze(self, system_prompt: str, user_prompt: str) -> AnalysisReport:
        """Send prompts to OpenAI and return a parsed report.

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
            logger.debug(f"Sending request to OpenAI ({self.model})")
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
            )
        except self._openai.AuthenticationError as e:
            raise AIClientError(
                "Authentication failed. Check your OPENAI_API_KEY."
            ) from e
        except self._openai.RateLimitError as e:
            raise AIClientError(
                "Rate limited by OpenAI API. Please wait and try again."
            ) from e
        except self._openai.APIError as e:
            raise AIClientError(f"OpenAI API error: {e}") from e
        except Exception as e:
            raise AIClientError(f"Unexpected error calling OpenAI: {e}") from e

        # Extract text content
        if not response.choices:
            raise APIResponseError("OpenAI returned an empty response.")

        raw_text = response.choices[0].message.content or ""

        if not raw_text.strip():
            raise APIResponseError("OpenAI returned no text content.")

        logger.debug(f"Received {len(raw_text)} chars from OpenAI")

        return parse_analysis_response(raw_text)
