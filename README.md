# Arceval

**Architecture, evaluated.** AI-powered enterprise readiness analyzer for codebases.

<img width="1115" height="913" alt="Screenshot 2026-05-13 105433" src="https://github.com/user-attachments/assets/d9acafae-2f37-49fe-8e89-3a8c5aa2be37" />

Arceval is a CLI tool that walks a software project, samples the files that matter,
and asks an AI model to score it across eight enterprise-readiness dimensions:
architecture, security, features, code quality, scalability, observability,
documentation, and DevOps. The report prints to your terminal in full color.

Supports **Claude**, **GPT**, and **Gemini** — switch providers with a single env var.

## Install

Arceval is designed to run with [`uv`](https://docs.astral.sh/uv/):

```bash
# from a checkout
uv sync
uv run arceval

# or one-shot from a published build
uvx arceval
```

Or install with pip:

```bash
pip install arceval
arceval

# if arceval isn't on your PATH, use:
python -m arceval
```

## Configure

Copy `.env.example` to `.env` and set your provider and API key:

```bash
cp .env.example .env
```

Example configurations:

```bash
# Anthropic Claude
ARCEVAL_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# OpenAI GPT
ARCEVAL_PROVIDER=openai
OPENAI_API_KEY=sk-...

# Google Gemini
ARCEVAL_PROVIDER=gemini
GEMINI_API_KEY=...
```

See [`docs/configuration.md`](docs/configuration.md) for all available options.

## Use

```bash
# interactive — prompts for a path (defaults to the current directory)
uv run arceval

# direct — point it at a project
uv run arceval --path /home/you/my-saas-app

# export alongside the terminal render
uv run arceval --path . --json report.json --markdown report.md
```

## Layers

```
cli/            presentation / command parsing   (typer)
core/           domain models, services, ports   (pure python)
infrastructure/ AI SDK clients, filesystem I/O
presentation/   rich terminal renderer, exporters
shared/         config, logging, constants, errors
```

Inner layers never import from outer layers. AI providers, the terminal,
and the filesystem all sit behind abstract ports defined in `core/`.

See [`docs/architecture.md`](docs/architecture.md) for the full layer design.

## Author

Developed by **Renz Siguenza** ([@enzox0](https://github.com/enzox0))

## License

MIT — see [LICENSE](LICENSE).
