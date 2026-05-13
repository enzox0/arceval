# Contributing to Arceval

Thank you for your interest in contributing to Arceval. This document outlines
the process for contributing code, reporting issues, and submitting improvements.

## Getting Started

1. Fork the repository and clone your fork locally.
2. Install dependencies:
   ```bash
   uv sync --extra dev
   ```
3. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
4. Verify your setup:
   ```bash
   uv run pytest
   uv run ruff check .
   uv run mypy arceval/
   ```

## Development Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes following the project's architecture and coding standards.
3. Write or update tests for any new functionality.
4. Ensure all checks pass before submitting:
   ```bash
   uv run ruff check .
   uv run ruff format .
   uv run mypy arceval/ --ignore-missing-imports
   uv run pytest --cov=arceval -v
   ```
5. Commit with clear, descriptive messages following conventional commit format:
   ```
   feat: add support for custom scoring weights
   fix: handle empty directory tree gracefully
   docs: update configuration reference for new env vars
   ```
6. Push your branch and open a Pull Request against `main`.

## Architecture Guidelines

Arceval follows Clean Architecture with strict layer boundaries:

- `shared/` — Cross-cutting concerns (config, constants, exceptions, utilities)
- `core/` — Domain models, services, ports (abstract interfaces), and use cases
- `infrastructure/` — External integrations (AI SDKs, filesystem I/O)
- `presentation/` — Output rendering (terminal, exporters)
- `cli/` — Command-line interface (typer commands, middleware)

Key rules:
- `core/` must never import from `infrastructure/`, `presentation/`, or `cli/`.
- New external integrations must implement a port defined in `core/ports/`.
- All business logic belongs in `core/services/` or `core/use_cases/`.

## Pull Request Standards

- PRs should address a single concern (one feature, one fix, one refactor).
- Include tests for new functionality or bug fixes.
- Update documentation if behavior or configuration changes.
- Ensure CI passes before requesting review.
- Keep commits atomic and well-described.

## Reporting Issues

When filing an issue, include:
- A clear description of the problem or feature request.
- Steps to reproduce (for bugs).
- Expected vs. actual behavior.
- Environment details (OS, Python version, provider used).

## Code Style

- Follow PEP 8 conventions enforced by ruff.
- Use type annotations on all public functions and methods.
- Write docstrings for all public modules, classes, and functions.
- Keep functions focused and under 50 lines where practical.

## License

By contributing, you agree that your contributions will be licensed under the
MIT License that covers this project.
