# Architecture

Arceval follows **Clean Architecture** principles with five distinct layers.
Each layer has a clear responsibility and strict dependency rules.

## Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  CLI (cli/)                                                  │
│  Typer commands, argument parsing, interactive prompts       │
├─────────────────────────────────────────────────────────────┤
│  Presentation (presentation/)                                │
│  Rich terminal renderer, JSON/Markdown exporters             │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure (infrastructure/)                            │
│  Anthropic SDK client, filesystem I/O                        │
├─────────────────────────────────────────────────────────────┤
│  Core (core/)                                                │
│  Domain models, services, use cases, abstract ports          │
├─────────────────────────────────────────────────────────────┤
│  Shared (shared/)                                            │
│  Config, constants, exceptions, logging, utilities           │
└─────────────────────────────────────────────────────────────┘
```

## Dependency Rules

| Layer          | May depend on                     | Must NOT depend on          |
|----------------|-----------------------------------|-----------------------------|
| cli/           | core (use_cases, services)        | infrastructure directly     |
| presentation/  | core/models                       | infrastructure, cli         |
| infrastructure/| core/ports (implements them)      | cli, presentation           |
| core/          | shared only                       | infrastructure, presentation, cli |
| shared/        | nothing internal                  | any other layer             |

## Key Design Decisions

### Ports and Adapters (Hexagonal)

The `core/ports/` directory defines abstract interfaces:

- **AIClient** — any AI backend that can analyze a project
- **ReportRenderer** — any output target (terminal, file, web)

Concrete implementations live in `infrastructure/` and `presentation/`.
This means the domain logic is fully testable without Claude, the terminal,
or the filesystem.

### Use Cases as Orchestrators

`core/use_cases/analyze_project.py` is the single orchestrator that:
1. Validates the path
2. Collects project files
3. Calls the AI client
4. Validates the report

The CLI layer simply wires dependencies and invokes the use case.

### Configuration

All settings flow through `shared/config.py` using pydantic-settings.
Environment variables are the single source of truth, loaded from `.env`
files or the shell environment.

### Error Handling

A custom exception hierarchy in `shared/exceptions.py` ensures every
failure mode has a typed exception. The CLI middleware catches these
and formats user-friendly messages.
