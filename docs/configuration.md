# Configuration

All configuration is done via environment variables. Use a `.env` file
in the project root or export variables in your shell.

## Provider Selection

Arceval supports multiple AI providers. Set `ARCEVAL_PROVIDER` to choose:

| Provider    | Value        | Default Model         | API Key Variable     |
|-------------|--------------|----------------------|----------------------|
| Anthropic   | `anthropic`  | `claude-sonnet-4-5`  | `ANTHROPIC_API_KEY`  |
| OpenAI      | `openai`     | `gpt-4o`             | `OPENAI_API_KEY`     |
| Google      | `gemini`     | `gemini-2.0-flash`   | `GEMINI_API_KEY`     |

## Required

| Variable           | Description                                      |
|--------------------|--------------------------------------------------|
| `ARCEVAL_PROVIDER` | AI provider to use (`anthropic`, `openai`, `gemini`) |
| Provider API key   | The API key matching your chosen provider        |

## Optional

| Variable                    | Default              | Description                                    |
|-----------------------------|----------------------|------------------------------------------------|
| `ARCEVAL_MODEL`             | (per provider)       | Override the model name                        |
| `ARCEVAL_MAX_TOKENS`        | `4096`               | Maximum output tokens the AI may generate      |
| `ARCEVAL_MAX_CONTEXT_CHARS` | `60000`              | Hard cap on project context sent to AI         |
| `ARCEVAL_MAX_SOURCE_FILES`  | `5`                  | Maximum sampled source files                   |
| `ARCEVAL_MAX_FILE_LINES`    | `300`                | Truncate individual files to this many lines   |
| `ARCEVAL_MAX_FILE_SIZE_KB`  | `30`                 | Skip files larger than this                    |
| `ARCEVAL_LOG_LEVEL`         | `INFO`               | Log level: DEBUG, INFO, WARNING, ERROR         |
| `OPENAI_BASE_URL`           | (empty)              | Custom base URL for Azure OpenAI or compatible APIs |

## Installation by Provider

Install only the SDK you need:

```bash
# Anthropic Claude
uv pip install arceval[anthropic]

# OpenAI GPT
uv pip install arceval[openai]

# Google Gemini
uv pip install arceval[gemini]

# All providers
uv pip install arceval[all]

# Development (includes all providers + test tools)
uv sync --extra dev
```

## Example .env Files

### Using Claude (Anthropic)

```bash
ARCEVAL_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### Using GPT-4o (OpenAI)

```bash
ARCEVAL_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
ARCEVAL_MODEL=gpt-4o
```

### Using Gemini (Google)

```bash
ARCEVAL_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-key-here
ARCEVAL_MODEL=gemini-2.5-pro
```

### Using Azure OpenAI

```bash
ARCEVAL_PROVIDER=openai
OPENAI_API_KEY=your-azure-key
OPENAI_BASE_URL=https://your-resource.openai.azure.com/
ARCEVAL_MODEL=gpt-4o
```

## Loading Order

1. Shell environment variables (highest priority)
2. `.env` file in the current working directory
3. Built-in defaults (lowest priority)
