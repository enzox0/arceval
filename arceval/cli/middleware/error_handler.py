"""Global CLI exception formatting."""

from __future__ import annotations

import contextlib
import sys
from collections.abc import Generator

from rich.console import Console

from arceval.shared.exceptions import (
    AIClientError,
    APIKeyMissingError,
    ArcevalError,
    ConfigurationError,
    InvalidPathError,
    JSONParseError,
    ProjectTooSmallError,
)


@contextlib.contextmanager
def handle_errors(console: Console) -> Generator[None, None, None]:
    """Context manager that catches ArcevalError and prints user-friendly messages.

    Args:
        console: Rich console for styled output.
    """
    try:
        yield
    except ConfigurationError as e:
        console.print(f"\n  [bold red]Error:[/bold red] {e.message}")
        console.print(
            "  [dim]Tip: Set ARCEVAL_PROVIDER and the matching API key in your .env file.\n"
            "  Supported providers: anthropic, openai, gemini[/dim]"
        )
        sys.exit(1)
    except APIKeyMissingError as e:
        console.print(f"\n  [bold red]Error:[/bold red] {e.message}")
        console.print(
            "  [dim]Tip: Set the API key for your provider in .env or your shell.[/dim]"
        )
        sys.exit(1)
    except InvalidPathError as e:
        console.print(f"\n  [bold red]Error:[/bold red] {e.message}")
        console.print("  [dim]Tip: Provide a valid directory path with --path.[/dim]")
        sys.exit(1)
    except ProjectTooSmallError as e:
        console.print(f"\n  [bold yellow]Warning:[/bold yellow] {e.message}")
        sys.exit(1)
    except JSONParseError as e:
        console.print(f"\n  [bold red]Error:[/bold red] {e.message}")
        console.print("\n  [dim]Raw AI response for debugging:[/dim]")
        console.print(f"  {e.raw_response[:500]}")
        sys.exit(1)
    except AIClientError as e:
        console.print(f"\n  [bold red]Error:[/bold red] {e.message}")
        console.print("  [dim]Tip: Check your API key and try again.[/dim]")
        sys.exit(1)
    except ArcevalError as e:
        console.print(f"\n  [bold red]Error:[/bold red] {e.message}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n  [dim]Interrupted.[/dim]")
        sys.exit(130)
