# Contributing to Frame

Thanks for helping improve Frame.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

Run the fast checks before opening a pull request:

```bash
pytest
ruff check .
mypy src
```

## API changes

Frame values are public API. Prefer additive changes, explicit deprecations, and compatibility aliases over silent behavior changes. Any behavior that maps to Discord constraints should have a regression test and a documentation note.

## Pull requests

Keep pull requests focused. Include tests for new branches and update the README/docs when the public API changes.
