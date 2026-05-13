"""Typer app factory and command registration."""

from __future__ import annotations

import typer

from arceval.cli.commands.analyze import analyze_command
from arceval.cli.commands.version import version_command

app = typer.Typer(
    name="arceval",
    help="Architecture, evaluated. AI-powered enterprise readiness analyzer.",
    add_completion=False,
    no_args_is_help=False,
    invoke_without_command=True,
)


def _version_callback(value: bool) -> None:
    """Handle --version flag."""
    if value:
        version_command()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
    path: str = typer.Option(
        "",
        "--path",
        "-p",
        help="Path to the project to analyze.",
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
    """Run analysis when invoked without a subcommand."""
    if ctx.invoked_subcommand is None:
        analyze_command(path=path, json_output=json_output, markdown_output=markdown_output)


@app.command()
def analyze(
    path: str = typer.Option(
        "",
        "--path",
        "-p",
        help="Path to the project to analyze.",
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
    analyze_command(path=path, json_output=json_output, markdown_output=markdown_output)


# Keep backward compat: arceval.main:app
if __name__ == "__main__":
    app()
