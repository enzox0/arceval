"""Backward-compatible entry point.

The pyproject.toml `[project.scripts]` points here for `arceval = "arceval.main:app"`.
This re-exports the typer app from the CLI layer.
"""

from arceval.cli.app import app  # noqa: F401
