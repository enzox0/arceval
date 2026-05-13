"""The `arceval analyze` command — main entry point for analysis."""

from __future__ import annotations

import asyncio
import os
import sys

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from arceval.cli.middleware.error_handler import handle_errors
from arceval.core.models.config import AnalysisConfig
from arceval.core.use_cases.analyze_project import AnalyzeProjectUseCase
from arceval.infrastructure.ai.provider_factory import create_ai_client
from arceval.presentation.exporters.json_exporter import export_json
from arceval.presentation.exporters.markdown_exporter import export_markdown
from arceval.presentation.terminal.renderer import TerminalRenderer
from arceval.presentation.terminal.themes.default import EMOJI_CHECK
from arceval.shared.config import get_settings

console = Console()


def analyze_command(
    path: str = typer.Option(
        "",
        "--path",
        "-p",
        help="Path to the project to analyze. Defaults to current directory.",
    ),
    json_output: str = typer.Option(
        "",
        "--json",
        "-j",
        help="Export report as JSON to this file path.",
    ),
    markdown_output: str = typer.Option(
        "",
        "--markdown",
        "-m",
        help="Export report as Markdown to this file path.",
    ),
) -> None:
    """Analyze a project and generate an Enterprise Readiness Report."""
    with handle_errors(console):
        # Show banner
        _show_banner()

        # Resolve project path
        project_path = _resolve_path(path)

        # Load settings
        settings = get_settings()

        # Build AI client via provider factory (validates key + provider)
        ai_client = create_ai_client(settings)

        provider_name = settings.arceval_provider
        model_name = settings.resolved_model
        console.print(
            f"  {EMOJI_CHECK} Using provider: [bold]{provider_name}[/bold] "
            f"(model: [dim]{model_name}[/dim])"
        )
        console.print(
            f"  {EMOJI_CHECK} Project found: [bold]{os.path.basename(project_path)}[/bold]"
        )

        # Build config
        config = AnalysisConfig(
            max_source_files=settings.arceval_max_source_files,
            max_file_size_kb=settings.arceval_max_file_size_kb,
            max_file_lines=settings.arceval_max_file_lines,
            max_context_chars=settings.arceval_max_context_chars,
        )

        # Run analysis
        use_case = AnalyzeProjectUseCase(ai_client=ai_client, config=config)

        with console.status(
            f"[bold cyan]Analyzing with {provider_name}...[/bold cyan]", spinner="dots"
        ):
            project_data, report = asyncio.run(use_case.execute(project_path))

        console.print(
            f"  {EMOJI_CHECK} Collected {project_data.total_files_found} files "
            f"across {project_data.total_dirs_found} directories"
        )

        # Render terminal report
        renderer = TerminalRenderer(console=console)
        renderer.render(report)

        # Export if requested
        if json_output:
            out_path = export_json(report, json_output)
            console.print(f"  {EMOJI_CHECK} JSON report saved to: [dim]{out_path}[/dim]")

        if markdown_output:
            out_path = export_markdown(report, markdown_output)
            console.print(f"  {EMOJI_CHECK} Markdown report saved to: [dim]{out_path}[/dim]")


def _show_banner() -> None:
    """Display the Arceval banner."""
    banner = Text("Arceval — Code Analyzer", style="bold cyan", justify="center")
    console.print(Panel(banner, padding=(0, 2)))
    console.print()


def _resolve_path(path: str) -> str:
    """Resolve the project path, prompting if not provided."""
    if path:
        return path

    # Try to prompt interactively
    if sys.stdin.isatty():
        user_input = console.input(
            "  [bold]? Enter project path[/bold] (Enter = current directory): "
        ).strip()
        if user_input:
            return user_input

    return os.getcwd()
