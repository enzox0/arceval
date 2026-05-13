"""Unit tests for the AI provider factory."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from arceval.infrastructure.ai.provider_factory import create_ai_client
from arceval.shared.config import Settings
from arceval.shared.exceptions import ConfigurationError


class TestProviderFactory:
    """Tests for create_ai_client factory."""

    def test_rejects_unsupported_provider(self) -> None:
        """Should raise ConfigurationError for unknown provider."""
        settings = Settings(
            arceval_provider="llama",
            anthropic_api_key="test",
        )
        with pytest.raises(ConfigurationError, match="Unsupported provider"):
            create_ai_client(settings)

    def test_rejects_missing_api_key(self) -> None:
        """Should raise ConfigurationError when API key is empty."""
        settings = Settings(
            arceval_provider="anthropic",
            anthropic_api_key="",
        )
        with pytest.raises(ConfigurationError, match="API key not set"):
            create_ai_client(settings)

    def test_creates_anthropic_client(self) -> None:
        """Should create a ClaudeClient for anthropic provider."""
        settings = Settings(
            arceval_provider="anthropic",
            anthropic_api_key="sk-ant-test",
        )
        client = create_ai_client(settings)
        from arceval.infrastructure.ai.claude_client import ClaudeClient

        assert isinstance(client, ClaudeClient)

    def test_creates_openai_client(self) -> None:
        """Should create an OpenAIClient for openai provider."""
        settings = Settings(
            arceval_provider="openai",
            openai_api_key="sk-test",
        )
        client = create_ai_client(settings)
        from arceval.infrastructure.ai.openai_client import OpenAIClient

        assert isinstance(client, OpenAIClient)

    def test_creates_gemini_client(self) -> None:
        """Should create a GeminiClient for gemini provider."""
        settings = Settings(
            arceval_provider="gemini",
            gemini_api_key="test-key",
        )
        client = create_ai_client(settings)
        from arceval.infrastructure.ai.gemini_client import GeminiClient

        assert isinstance(client, GeminiClient)

    def test_resolved_model_uses_provider_default(self) -> None:
        """Should use provider-specific default model when none specified."""
        settings = Settings(
            arceval_provider="openai",
            openai_api_key="sk-test",
            arceval_model="",
        )
        assert settings.resolved_model == "gpt-4o"

    def test_resolved_model_uses_override(self) -> None:
        """Should use explicit model when specified."""
        settings = Settings(
            arceval_provider="openai",
            openai_api_key="sk-test",
            arceval_model="gpt-4-turbo",
        )
        assert settings.resolved_model == "gpt-4-turbo"

    def test_active_api_key_returns_correct_key(self) -> None:
        """Should return the key matching the active provider."""
        settings = Settings(
            arceval_provider="gemini",
            anthropic_api_key="wrong",
            openai_api_key="wrong",
            gemini_api_key="correct-key",
        )
        assert settings.active_api_key == "correct-key"
