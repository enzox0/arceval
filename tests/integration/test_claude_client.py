"""Integration tests for the Claude client (mocked API)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from arceval.infrastructure.ai.claude_client import ClaudeClient
from arceval.shared.exceptions import APIResponseError


@pytest.fixture
def mock_response_data() -> dict:
    """Load the mock Claude response fixture."""
    fixture_path = (
        Path(__file__).parent.parent / "fixtures" / "mock_responses" / "claude_analysis.json"
    )
    return json.loads(fixture_path.read_text(encoding="utf-8"))


@pytest.mark.integration
class TestClaudeClient:
    """Integration tests for ClaudeClient with mocked Anthropic SDK."""

    @pytest.mark.asyncio
    async def test_analyze_returns_report(self, mock_response_data: dict) -> None:
        """Should parse a valid response into an AnalysisReport."""
        raw_json = json.dumps(mock_response_data)

        # Mock the Anthropic client
        mock_message = MagicMock()
        mock_block = MagicMock()
        mock_block.text = raw_json
        mock_message.content = [mock_block]

        with patch(
            "arceval.infrastructure.ai.claude_client.anthropic.Anthropic"
        ) as mock_anthropic:
            mock_client_instance = MagicMock()
            mock_client_instance.messages.create.return_value = mock_message
            mock_anthropic.return_value = mock_client_instance

            client = ClaudeClient(
                api_key="sk-ant-test-key",
                model="claude-sonnet-4-5",
                max_tokens=4096,
            )
            report = await client.analyze("system prompt", "user prompt")

        assert report.project_name == "sample-project"
        assert report.overall_score == 7.6
        assert len(report.categories) == 8
        assert report.categories[0].name == "Architecture"
        assert report.categories[0].score == 9
        assert len(report.recommendations) == 4

    @pytest.mark.asyncio
    async def test_analyze_handles_empty_response(self) -> None:
        """Should raise APIResponseError on empty response."""
        mock_message = MagicMock()
        mock_message.content = []

        with patch(
            "arceval.infrastructure.ai.claude_client.anthropic.Anthropic"
        ) as mock_anthropic:
            mock_client_instance = MagicMock()
            mock_client_instance.messages.create.return_value = mock_message
            mock_anthropic.return_value = mock_client_instance

            client = ClaudeClient(
                api_key="sk-ant-test-key",
                model="claude-sonnet-4-5",
                max_tokens=4096,
            )

            with pytest.raises(APIResponseError):
                await client.analyze("system", "user")
