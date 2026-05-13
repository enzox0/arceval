"""Analysis configuration model."""

from __future__ import annotations

from dataclasses import dataclass

from arceval.shared.constants import (
    DEFAULT_DIRECTORY_DEPTH,
    DEFAULT_MAX_CONTEXT_CHARS,
    DEFAULT_MAX_FILE_LINES,
    DEFAULT_MAX_FILE_SIZE_KB,
    DEFAULT_MAX_SOURCE_FILES,
)


@dataclass
class AnalysisConfig:
    """Configuration thresholds and limits for a single analysis run."""

    max_source_files: int = DEFAULT_MAX_SOURCE_FILES
    max_file_size_kb: int = DEFAULT_MAX_FILE_SIZE_KB
    max_file_lines: int = DEFAULT_MAX_FILE_LINES
    max_context_chars: int = DEFAULT_MAX_CONTEXT_CHARS
    directory_depth: int = DEFAULT_DIRECTORY_DEPTH
