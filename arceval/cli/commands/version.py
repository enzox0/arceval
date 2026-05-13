"""Version command."""

from __future__ import annotations

import typer
from rich.console import Console

from arceval import __version__

console = Console()


def version_command() -> None:
    """Display the current Arceval version."""
    console.print(f"arceval [bold cyan]v{__version__}[/bold cyan]")
    raise typer.Exit()
