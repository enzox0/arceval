## Summary

<!-- Provide a concise description of what this PR does and why. -->

## Type of Change

- [ ] Bug fix (non-breaking change that resolves an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Refactor (code change that neither fixes a bug nor adds a feature)
- [ ] Documentation update
- [ ] CI/CD or tooling change

## Related Issues

<!-- Link any related issues. Use "Closes #123" to auto-close on merge. -->

## Changes Made

<!-- List the specific changes introduced in this PR. -->

-
-
-

## Testing

<!-- Describe how this was tested. Include commands run and results. -->

- [ ] All existing tests pass (`uv run pytest -v`)
- [ ] New tests added for changed functionality
- [ ] Lint passes (`uv run ruff check .`)
- [ ] Type check passes (`uv run mypy arceval/ --ignore-missing-imports`)

## Architecture Compliance

<!-- Confirm layer boundaries are respected. -->

- [ ] `core/` has no imports from `infrastructure/`, `presentation/`, or `cli/`
- [ ] New external integrations implement a port defined in `core/ports/`
- [ ] No new dependencies added without justification

## Screenshots / Output

<!-- If applicable, include terminal output or screenshots demonstrating the change. -->

## Checklist

- [ ] My code follows the project's coding standards
- [ ] I have updated documentation where necessary
- [ ] I have added appropriate type annotations
- [ ] My commits follow conventional commit format
- [ ] This PR addresses a single concern
