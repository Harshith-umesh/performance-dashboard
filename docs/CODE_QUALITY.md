# Code Quality and Linting Setup

This document describes the code quality tools and linting setup for the Performance Dashboard project.

## Overview

The project uses a comprehensive set of tools to ensure code quality, consistency, and security:

- **Ruff**: Fast Python linter (replaces flake8, pylint, and more)
- **Black**: Code formatter
- **isort**: Import sorting
- **mypy**: Static type checking
- **pytest**: Testing framework with coverage
- **pre-commit**: Git hooks for automated checks

## Quick Start

### 1. Set up development environment

```bash

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

### 2. Run code quality checks

```bash
# Format code automatically
make format

# Run all linting checks
make lint

# Run type checking
make type-check

# Run all CI checks locally
make ci-local
```

## Tools Configuration

### Ruff Configuration

Ruff is configured in `pyproject.toml` and includes:

- **Enabled rules**: E, W, F, I, B, C4, UP, ARG, C90, T20, SIM, ICN
- **Line length**: 88 characters (matches Black)
- **Max complexity**: 12

Common rules:

- `E501`: Line too long (handled by Black)
- `F401`: Unused imports
- `B008`: Function calls in argument defaults
- `I001`: Import sorting

### Black Configuration

Black is the primary code formatter with:

- **Line length**: 88 characters
- **Target versions**: Python 3.9+
- **Style**: PEP 8 compliant

### mypy Configuration

Type checking configuration:

- **Python version**: 3.9+
- **Missing imports**: Ignored for external libraries
- **Untyped defs**: Allowed (can be made stricter)

### Pre-commit Hooks

The following hooks run on every commit:

1. **Trailing whitespace removal**
2. **End-of-file fixer**
3. **YAML/JSON validation**
4. **Ruff linting and formatting**
5. **Black formatting**
6. **mypy type checking**
7. **Docstring checking**

## GitLab CI/CD Pipeline

The pipeline includes the following stages:

### Lint Stage

- **format-check**: Validates code formatting
- **ruff-lint**: Runs comprehensive linting
- **isort-check**: Validates import sorting
- **type-check**: Runs static type checking
- **complexity-check**: Analyzes code complexity
- **docs-check**: Validates docstrings

### Security Stage

- **security-scan**: Scans for security vulnerabilities

### Test Stage

- **test**: Runs pytest with coverage reporting

### Build Stage

- **build-docker**: Builds Docker image (manual trigger)

## Customizing Rules

### Disabling Specific Rules

For specific lines:

```python
# ruff: noqa: E501
very_long_line_that_exceeds_the_limit_but_is_necessary_for_some_reason()

# mypy: ignore
problematic_type_annotation = some_complex_function()
```

For entire files:

```python
# ruff: noqa
```

### Project-wide Exceptions

Edit `pyproject.toml`:

```toml
[tool.ruff]
ignore = [
    "E501",  # line too long
    "T201",  # print statements
]

[tool.ruff.per-file-ignores]
"tests/*" = ["T201"]  # Allow prints in tests
```

### Getting Help

1. Check tool documentation:
   - [Ruff](https://beta.ruff.rs/docs/)
   - [Black](https://black.readthedocs.io/)
   - [mypy](https://mypy.readthedocs.io/)

2. Run with verbose flags:

   ```bash
   ruff check . --verbose
   mypy . --verbose
   ```

3. Check GitLab CI logs for specific error details
