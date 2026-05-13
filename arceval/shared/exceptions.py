"""Custom exception hierarchy for Arceval."""

from __future__ import annotations


class ArcevalError(Exception):
    """Base exception for all Arceval errors."""

    def __init__(self, message: str = "An unexpected error occurred.") -> None:
        self.message = message
        super().__init__(self.message)


class ConfigurationError(ArcevalError):
    """Raised when required configuration is missing or invalid."""

    def __init__(self, message: str = "Configuration error.") -> None:
        super().__init__(message)


class APIKeyMissingError(ConfigurationError):
    """Raised when the Anthropic API key is not set."""

    def __init__(self) -> None:
        super().__init__(
            "ANTHROPIC_API_KEY not set. "
            "Add it to a .env file or export it as an environment variable."
        )


class InvalidPathError(ArcevalError):
    """Raised when the provided project path is invalid."""

    def __init__(self, path: str) -> None:
        super().__init__(f"Invalid project path: '{path}' does not exist or is not a directory.")


class ProjectTooSmallError(ArcevalError):
    """Raised when the project has too few files for meaningful analysis."""

    def __init__(self) -> None:
        super().__init__(
            "Project may be too small for a full analysis. "
            "Ensure the path points to a project with source files."
        )


class AIClientError(ArcevalError):
    """Raised when the AI backend returns an error."""

    def __init__(self, message: str = "AI client error.") -> None:
        super().__init__(message)


class APIResponseError(AIClientError):
    """Raised when the Claude API returns an unexpected response."""

    def __init__(self, message: str = "Unexpected API response.") -> None:
        super().__init__(message)


class JSONParseError(AIClientError):
    """Raised when Claude's response cannot be parsed as valid JSON."""

    def __init__(self, raw_response: str) -> None:
        self.raw_response = raw_response
        super().__init__(
            "Failed to parse Claude's response as JSON. "
            "Raw response saved for debugging."
        )


class AnalysisError(ArcevalError):
    """Raised when the analysis pipeline encounters an unrecoverable error."""

    def __init__(self, message: str = "Analysis failed.") -> None:
        super().__init__(message)
