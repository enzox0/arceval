"""Factory for creating the appropriate AI client based on provider config."""

from __future__ import annotations

from arceval.core.ports.ai_client import AIClient
from arceval.shared.config import Settings
from arceval.shared.constants import SUPPORTED_PROVIDERS
from arceval.shared.exceptions import AIClientError, ConfigurationError


def create_ai_client(settings: Settings) -> AIClient:
    """Create and return the appropriate AI client for the configured provider.

    Args:
        settings: Application settings with provider and API key info.

    Returns:
        An AIClient implementation ready to use.

    Raises:
        ConfigurationError: If the provider is unsupported or API key is missing.
        AIClientError: If the provider SDK is not installed.
    """
    provider = settings.arceval_provider.lower().strip()

    if provider not in SUPPORTED_PROVIDERS:
        raise ConfigurationError(
            f"Unsupported provider: '{provider}'. "
            f"Supported providers: {', '.join(sorted(SUPPORTED_PROVIDERS))}"
        )

    api_key = settings.active_api_key
    if not api_key:
        key_var = _get_key_env_var(provider)
        raise ConfigurationError(
            f"API key not set for provider '{provider}'. "
            f"Set {key_var} in your .env file or environment."
        )

    model = settings.resolved_model
    max_tokens = settings.arceval_max_tokens

    if provider == "anthropic":
        return _create_anthropic_client(api_key, model, max_tokens)
    elif provider == "openai":
        return _create_openai_client(api_key, model, max_tokens, settings.openai_base_url)
    elif provider == "gemini":
        return _create_gemini_client(api_key, model, max_tokens)
    else:
        raise ConfigurationError(f"Unsupported provider: '{provider}'")


def _create_anthropic_client(api_key: str, model: str, max_tokens: int) -> AIClient:
    """Create an Anthropic Claude client."""
    try:
        from arceval.infrastructure.ai.claude_client import ClaudeClient
    except ImportError as e:
        raise AIClientError(
            "Anthropic SDK not installed. Install it with: "
            "uv pip install arceval[anthropic]  or  pip install anthropic"
        ) from e
    return ClaudeClient(api_key=api_key, model=model, max_tokens=max_tokens)


def _create_openai_client(
    api_key: str, model: str, max_tokens: int, base_url: str
) -> AIClient:
    """Create an OpenAI client."""
    from arceval.infrastructure.ai.openai_client import OpenAIClient

    return OpenAIClient(api_key=api_key, model=model, max_tokens=max_tokens, base_url=base_url)


def _create_gemini_client(api_key: str, model: str, max_tokens: int) -> AIClient:
    """Create a Google Gemini client."""
    from arceval.infrastructure.ai.gemini_client import GeminiClient

    return GeminiClient(api_key=api_key, model=model, max_tokens=max_tokens)


def _get_key_env_var(provider: str) -> str:
    """Return the environment variable name for a provider's API key."""
    return {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
    }.get(provider, "UNKNOWN_API_KEY")
