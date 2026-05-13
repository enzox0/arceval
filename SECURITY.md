# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | Yes                |

## Reporting a Vulnerability

If you discover a security vulnerability in Arceval, please report it responsibly.
Do not open a public GitHub issue for security-related concerns.

To report a vulnerability:

1. Email the maintainers at: security@arceval.dev (or open a private security
   advisory via GitHub's "Report a vulnerability" feature on this repository).
2. Include a clear description of the vulnerability.
3. Provide steps to reproduce, if applicable.
4. Indicate the potential impact and severity.

We will acknowledge receipt within 72 hours and provide an initial assessment
within 7 business days.

## Scope

The following are in scope for security reports:

- Arbitrary code execution via crafted project files.
- API key leakage through logs, error messages, or exported reports.
- Path traversal or unauthorized filesystem access during project scanning.
- Injection vulnerabilities in prompts sent to AI providers.
- Dependency vulnerabilities in direct dependencies.

## Security Practices

Arceval follows these security practices:

- API keys are loaded from environment variables or `.env` files and are never
  logged, displayed in output, or included in exported reports.
- The `.env` file is gitignored by default to prevent accidental credential commits.
- File reading is bounded by size limits and restricted to the target project directory.
- No network requests are made other than to the configured AI provider endpoint.
- Dependencies are pinned to minimum versions and reviewed for known vulnerabilities.

## Disclosure Policy

We follow coordinated disclosure. Once a fix is available, we will:

1. Release a patched version.
2. Publish a security advisory on GitHub.
3. Credit the reporter (unless anonymity is requested).
