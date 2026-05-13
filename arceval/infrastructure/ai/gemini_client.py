"""Google Gemini SDK implementation of the AIClient port."""

from __future__ import annotations

import logging

from arceval.core.models.report import AnalysisReport
from arceval.core.ports.ai_client import AIClient
from arceval.infrastructure.ai.response_parser import parse_analysis_response
from arceval.shared.exceptions import AIClientError, APIResponseError

logger = logging.getLogger("arceval")


class GeminiClient(AIClient):
    """Concrete implementation of AIClient using the Google GenAI SDK.

    Supports Gemini models (gemini-2.0-flash, gemini-2.5-pro, etc.).
    """

    def __init__(self, api_key: str, model: str, max_tokens: int) -> None:
        self.model = model
        self.max_tokens = max_tokens

        try:
            from google import genai
        except ImportError as e:
            raise AIClientError(
                "Google GenAI SDK not installed. Install it with: "
                "uv pip install arceval[gemini]  or  pip install google-genai"
            ) from e

        self.client = genai.Client(api_key=api_key)
        self._genai = genai

    async def analyze(self, system_prompt: str, user_prompt: str) -> AnalysisReport:
        """Send prompts to Gemini and return a parsed report.

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
            logger.debug(f"Sending request to Gemini ({self.model})")

            response = self.client.models.generate_content(
                model=self.model,
                contents=f"{system_prompt}\n\n{user_prompt}",
                config={
                    "max_output_tokens": self.max_tokens,
                    "temperature": 0.3,
                },
            )
        except Exception as e:
            error_msg = str(e).lower()
            if "api key" in error_msg or "authentication" in error_msg or "401" in error_msg:
                raise AIClientError(
                    "Authentication failed. Check your GEMINI_API_KEY."
                ) from e
            elif "rate" in error_msg or "429" in error_msg:
                raise AIClientError(
                    "Rate limited by Gemini API. Please wait and try again."
                ) from e
            else:
                raise AIClientError(f"Gemini API error: {e}") from e

        # Extract text content
        if not response or not response.text:
            raise APIResponseError("Gemini returned an empty response.")

        raw_text = response.text

        if not raw_text.strip():
            raise APIResponseError("Gemini returned no text content.")

        logger.debug(f"Received {len(raw_text)} chars from Gemini")

        return parse_analysis_response(raw_text)
