# Arceval

**Architecture, evaluated.** AI-powered enterprise readiness analyzer for codebases.

<img width="1115" height="913" alt="Screenshot 2026-05-13 105433" src="https://github.com/user-attachments/assets/d9acafae-2f37-49fe-8e89-3a8c5aa2be37" />

Arceval is a CLI tool that walks a software project, samples the files that matter,
and asks Claude to score it across eight enterprise-readiness dimensions:
architecture, security, features, code quality, scalability, observability,
documentation, and DevOps. The report prints to your terminal in full color.

## Install

Arceval is designed to run with [`uv`](https://docs.astral.sh/uv/):

```bash
# from a checkout
uv sync
uv run arceval

# or one-shot from a published build
uvx arceval
```

## Configure

Copy `.env.example` to `.env` and set your Anthropic key:

```bash
cp .env.example .env
# edit .env and add ANTHROPIC_API_KEY=sk-ant-...
```

## Use

```bash
# interactive — prompts for a path (defaults to the current directory)
uv run arceval

# direct — point it at a project
uv run arceval --path /home/you/my-saas-app

# export alongside the terminal render
uv run arceval --path . --json report.json --markdown report.md
```

See [`docs/architecture.md`](docs/architecture.md) for the layer design
and [`docs/configuration.md`](docs/configuration.md) for every env var.

## Layers

```
cli/            presentation / command parsing   (typer)
core/           domain models, services, ports   (pure python)
infrastructure/ anthropic SDK, filesystem I/O
presentation/   rich terminal renderer, exporters
shared/         config, logging, constants, errors
```

Inner layers never import from outer layers. Claude, the terminal,
and the filesystem all sit behind abstract ports defined in `core/`.

## License

MIT — see [LICENSE](LICENSE).
