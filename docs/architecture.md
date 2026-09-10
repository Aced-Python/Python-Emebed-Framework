# Architecture

## Layering

```
your bot code
      │
      ▼
   frame            (this package — pure developer-experience layer)
      │
      ▼
  discord.py         (does everything Discord-protocol-related: gateway, REST, caching)
      │
      ▼
  Discord API
```

Frame never talks to Discord's API or gateway directly, never opens a connection, and never runs a background task. It is exclusively a construction/validation layer: you build a `frame.embed(...)` or `frame.ui.container(...)`, get back a real discord.py object, and hand that to discord.py exactly as you would have built it by hand.

## Two-stage component construction

The riskiest part of a library like this is Components V2, because Discord's placement rules (a button must be in an action row or a section accessory; an action row can't mix a select with buttons; etc.) are easy to violate by accident, and violating them is only discovered as an HTTP 400 at send time.

Frame splits construction into two stages to catch these earlier:

1. **Spec objects** (`frame/ui/*.py`, `frame/embed/models.py`) — plain Python objects with no discord.py dependency at construction time. `frame.ui.text(...)`, `frame.ui.button(...)`, `frame.ui.section(...)`, etc. all return these. Each has:
   - `.validate()` — raises `InvalidComponentError`/`InvalidEmbedError` with a message naming the rule, the value, and the limit
   - `.to_dict()` — a JSON-ish summary for debugging/logging/tests, no Discord connection needed
   - `.to_discord()` — converts this one object to its real `discord.ui.*` (or `discord.Embed`) counterpart

2. **Tree validation + conversion** (`frame/ui/containers.py`'s `Container.validate()`, invoked from `frame.ui.container(...)`) — walks the whole tree, checking cross-component rules that no single component can check about itself (e.g. "this button's parent is a bare container, not an action row"), then converts every node to its real discord.py object and wraps the result in a `discord.ui.LayoutView`.

This means:

- Individual components are unit-testable without any Discord connection (`frame/tests/test_ui.py` never imports a live bot).
- Validation errors happen at construction time, in your code, with a stack trace pointing at your call — not as an opaque Discord API rejection.
- The final object returned to your bot code is never a frame-specific wrapper — it's the genuine discord.py object, so it composes normally with everything else discord.py offers (persistent views, `bot.add_view(...)`, etc.).

## Why embeds don't need the two-stage split

Embeds have no cross-field placement rules the way Components V2 does — every embed limit (title length, field count, total length) is checkable against the embed's own data. So `frame.embed(...)` validates and converts in one step. The `frame.Embed()` fluent builder still separates "build up state" from "validate + convert" (via `.to_discord()`/`.to_dict()`), which is what makes conditional/incremental embed construction pleasant.

## Where local image files fit in

Discord embeds can only reference images by URL, including the special `attachment://filename` form for files uploaded alongside the message. `frame.Image` (constructed via `frame.attachment(path)`) models this: it resolves to an `attachment://` URL for embed purposes, and separately exposes `.to_discord_file()` to produce the real `discord.File` needed in the `files=` kwarg of `channel.send(...)`. `Embed.files()` collects every local image referenced by an embed so you don't have to track them by hand.

## Errors

Every exception frame raises derives from `frame.FrameError`. The two validation subtypes — `InvalidEmbedError` and `InvalidComponentError` — both carry structured `current`/`maximum` attributes in addition to a formatted message, so downstream tooling (like the planned `frame check` CLI) can consume them programmatically rather than parsing strings.

## What frame deliberately does not do

- **No second event system.** Interaction callbacks (`on_click=`, `@button.on_click`) are thin wrappers that get assigned directly to the real `discord.ui.Item.callback` — dispatch is still discord.py's.
- **No metaclass magic.** Class-based views (see the roadmap) are deferred specifically because discord.py's own view metaclass is intricate, and a half-correct reimplementation would be worse than not having the feature.
- **No hidden network calls.** Frame never fetches a URL, resolves a Discord ID, or makes an API request on your behalf.
