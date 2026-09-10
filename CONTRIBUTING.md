# Contributing to frame

Thanks for considering a contribution. Frame is a young project with a strong opinion about its API surface, so the most valuable thing you can do before writing code is to check the shape of the change against [the design philosophy in the README](README.md#design-philosophy).

## Ground rules

- **API changes need an issue first.** Bug fixes, docs, tests, and internal refactors can go straight to a PR. Anything that adds/changes/removes a public function, class, or keyword argument should start as an issue describing the use case, so we can discuss the shape before code is written.
- **Every new component/embed feature needs a test.** Frame's whole pitch is "validated before Discord rejects it" — untested validation logic is a broken promise.
- **Match the existing error-message style.** Frame's validation errors state the rule, the current value, and the limit (see `frame/exceptions.py`). If you add a new validation error, follow the same shape.
- **Don't add a dependency without discussing it in the issue first.** Frame's core value proposition includes staying lightweight.

## Development setup

```bash
git clone https://github.com/frame-discord/frame.git
cd frame
pip install -e ".[dev]"
```

## Running checks locally

```bash
pytest                        # test suite
ruff check src/ tests/        # linting
mypy src/frame                # type checking
```

All three run in CI on every PR; please run them locally first so review cycles stay fast.

## Project layout

```
src/frame/
    embed/        # Embed data model, builder, theming, limit validation
    ui/            # Components V2: spec objects, validation, discord.py conversion
    colors/        # Color parsing + named palette
    markdown/      # Markdown formatting helpers
    attachments/   # Local file / Image abstraction
    exceptions.py  # Exception hierarchy
```

Frame's Components V2 layer is deliberately split into two stages — see the module docstring in `src/frame/ui/base.py` for why (lightweight, offline-testable spec objects → validated conversion to real discord.py objects at the end). New components should follow that pattern: a spec class with `.validate()` and `.to_discord()`, plus a factory function in `src/frame/ui/__init__.py`.

## Commit / PR expectations

- Keep PRs focused — one feature or fix per PR is much easier to review than a grab-bag.
- Update `CHANGELOG.md` under `## [Unreleased]` for any user-facing change.
- If you're adding a new public symbol, add it to the relevant `__all__` and to the README if it's something users will reach for directly.

## Reporting bugs

Please use the bug report issue template and include a minimal reproduction — the exact `frame.embed(...)` / `frame.ui...` call that triggers the problem, and what you expected instead.

## Code of conduct

Be respectful, assume good faith, and keep discussion focused on the technical question at hand. Maintainers may close or redirect discussions that become personal or unproductive.
