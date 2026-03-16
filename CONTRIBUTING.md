# Contributing to dual-sdk-python

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/ro-ro-b/dual-sdk-python.git
cd dual-sdk-python
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
ruff check src/ tests/
ruff format src/ tests/
```

## Type Checking

```bash
mypy src/dual_sdk/
```

## Pull Request Process

1. Fork the repo and create a feature branch from `main`.
2. Add tests for any new functionality.
3. Ensure `pytest`, `ruff check`, and `mypy` all pass.
4. Open a PR with a clear description of your changes.

## Code of Conduct

Be respectful and constructive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).
