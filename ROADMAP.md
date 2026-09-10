# Roadmap

Prioritization key: `P0` required for the next release, `P1` important and planned, `P2` future/exploratory, `P3` probably not core (may live outside the main package).

## P0 — required before 1.0

- [ ] Stabilize the public API surface (no more renames of `frame.embed`/`frame.ui.*` signatures)
- [ ] Full docstring coverage on every public function (in progress — see `src/frame/`)
- [ ] CI matrix across Python 3.10–3.13 and the last two discord.py minor versions

## P1 — important, actively planned

- **Class-based views** — `class MyView(frame.View): @frame.button(...) async def on_click(self, interaction): ...`. Deliberately deferred past 0.1.0: discord.py's view metaclass is intricate, and a half-correct reimplementation for Components V2 would be worse than the functional callback pattern frame ships today. Needs its own design doc before implementation starts.
- **`frame.presets`** — a real extension mechanism beyond the built-in `frame.ui.confirm(...)`, so third parties can ship reusable component bundles (pagination, profile cards, etc.) without forking frame.
- **Pagination** — `frame.ui.pagination(pages)`, built on the container/action-row primitives that already exist.
- **Localisation-ready content** — helpers for building embeds/components from a translation table without hand-rolling string interpolation.

## P2 — future / exploratory

- **`frame check` CLI** — statically scan a bot's source for `frame.embed(...)` / `frame.ui...` calls with literal string arguments and flag ones that would fail validation, before runtime.
- **`frame dev` live preview** — a local browser-based preview that updates as `frame.embed(...)` / `frame.ui.container(...)` calls change. Requires the serialization layer (`to_dict()`) to be complete enough to render outside Discord, which is already a design goal of the current `to_dict()` methods.
- **Modal/form helpers** — `frame.ui.modal(...)`, `frame.form(...)`. Discord's modal flow is a separate interaction type from message components, so this needs its own validation rules rather than reusing `container`'s.
- **Permission-aware components** — helpers that disable/hide buttons based on the invoking member's permissions, computed client-side before sending.
- **Snapshot testing utilities** — a `frame.testing` module for asserting on `.to_dict()` output in downstream bots' test suites.

## P3 — probably not core

- **Frame Cloud / Frame Studio** — a hosted visual embed/component builder that exports `frame.embed(...)` / `frame.ui.container(...)` code. This would be a separate product built *on* frame's serialization layer, not part of the open-source package. Mentioned here only so the core's `to_dict()` design doesn't accidentally foreclose it later.
- **`frame-core` / `frame-ui` / `frame-themes` package split** — not planned unless the single package's dependency footprint or release cadence actually becomes a problem. Splitting prematurely adds versioning overhead for no current benefit.

## Explicitly out of scope

- Frame will never become a second bot framework. It sits on top of discord.py's client/gateway/command handling and always will.
- Frame will not invent Discord functionality that doesn't exist (no fake "CSS for Discord", no components Discord doesn't support).
