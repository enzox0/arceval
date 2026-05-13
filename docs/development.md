# Development Guide

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)

## Setup

```bash
# Clone the repo
git clone https://github.com/arceval/arceval.git
cd arceval

# Install dependencies (creates .venv automatically)
uv sync

# Install dev dependencies
uv sync --extra dev

# Copy env template
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Running

```bash
# Run the CLI
uv run arceval

# Run with a specific path
uv run arceval --path /path/to/project

# Show version
uv run arceval --version
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=arceval --cov-report=term-missing

# Run only unit tests
uv run pytest tests/unit/

# Run only integration tests
uv run pytest tests/integration/ -m integration
```

## Linting & Type Checking

```bash
# Lint with ruff
uv run ruff check .

# Auto-fix lint issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Type check with mypy
uv run mypy arceval/
```

## Project Structure

See [architecture.md](architecture.md) for the full layer breakdown.

## Adding a New Feature

1. Define any new domain models in `core/models/`.
2. If external I/O is needed, define a port in `core/ports/`.
3. Implement the port in `infrastructure/`.
4. Add business logic in `core/services/`.
5. Wire it together in `core/use_cases/`.
6. Expose it via `cli/commands/`.
7. Add tests in `tests/unit/` and `tests/integration/`.
