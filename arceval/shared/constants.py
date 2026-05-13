"""Global constants for Arceval."""

from __future__ import annotations

# Directories to always skip during file traversal
SKIP_DIRS: set[str] = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    "coverage",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    ".tox",
    "env",
    ".eggs",
    "egg-info",
    ".terraform",
    "target",  # Rust/Java build output
}

# Key files to always collect from the project root
KEY_FILES: list[str] = [
    "README.md",
    "README.rst",
    "package.json",
    "pyproject.toml",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "requirements.txt",
    "tsconfig.json",
    ".env.example",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "Makefile",
]

# Glob patterns for CI configuration files
CI_PATTERNS: list[str] = [
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    ".circleci/config.yml",
    "azure-pipelines.yml",
]

# Source file extensions to sample
SOURCE_EXTENSIONS: set[str] = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".go",
    ".java",
    ".rs",
    ".rb",
    ".cs",
    ".kt",
    ".swift",
    ".scala",
    ".ex",
    ".exs",
}

# Defaults (overridable via env vars / config)
DEFAULT_MAX_FILE_SIZE_KB: int = 30
DEFAULT_MAX_SOURCE_FILES: int = 5
DEFAULT_MAX_FILE_LINES: int = 300
DEFAULT_MAX_CONTEXT_CHARS: int = 60_000
DEFAULT_MAX_TOKENS: int = 4096
DEFAULT_DIRECTORY_DEPTH: int = 3

# Provider defaults
DEFAULT_PROVIDER: str = "anthropic"
DEFAULT_MODEL: dict[str, str] = {
    "anthropic": "claude-sonnet-4-5",
    "openai": "gpt-4o",
    "gemini": "gemini-2.0-flash",
}

# Supported providers
SUPPORTED_PROVIDERS: set[str] = {"anthropic", "openai", "gemini"}
