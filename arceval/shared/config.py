"""Application settings loaded from environment variables via pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

from arceval.shared.constants import (
    DEFAULT_MAX_CONTEXT_CHARS,
    DEFAULT_MAX_FILE_LINES,
    DEFAULT_MAX_FILE_SIZE_KB,
    DEFAULT_MAX_SOURCE_FILES,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
)


class Settings(BaseSettings):
    """Typed, validated application settings.

    Values are loaded from environment variables (and .env files).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Provider selection: "anthropic", "openai", "gemini"
    arceval_provider: str = DEFAULT_PROVIDER

    # API keys — only the one matching the provider is required
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    gemini_api_key: str = ""

    # Optional — model name (auto-detected per provider if empty)
    arceval_model: str = ""

    # Optional — limits
    arceval_max_tokens: int = DEFAULT_MAX_TOKENS
    arceval_max_context_chars: int = DEFAULT_MAX_CONTEXT_CHARS
    arceval_max_source_files: int = DEFAULT_MAX_SOURCE_FILES
    arceval_max_file_lines: int = DEFAULT_MAX_FILE_LINES
    arceval_max_file_size_kb: int = DEFAULT_MAX_FILE_SIZE_KB

    # Optional — logging
    arceval_log_level: str = "INFO"

    # Optional — OpenAI base URL (for Azure OpenAI or compatible APIs)
    openai_base_url: str = ""

    @property
    def resolved_model(self) -> str:
        """Return the model name, falling back to provider defaults."""
        if self.arceval_model:
            return self.arceval_model
        return DEFAULT_MODEL.get(self.arceval_provider, "claude-sonnet-4-5")

    @property
    def active_api_key(self) -> str:
        """Return the API key for the active provider."""
        key_map = {
            "anthropic": self.anthropic_api_key,
            "openai": self.openai_api_key,
            "gemini": self.gemini_api_key,
        }
        return key_map.get(self.arceval_provider, "")


def get_settings() -> Settings:
    """Create and return a Settings instance (reads env on each call)."""
    return Settings()
