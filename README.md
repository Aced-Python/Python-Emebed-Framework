# Frame

> **Build beautiful Discord UIs with Python.**

Frame is a lightweight developer-experience layer on top of [`discord.py`](https://github.com/Rapptz/discord.py). It makes the common path short, keeps Discord concepts visible, and compiles directly to native `discord.py` objects.

[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.6%2B-5865F2)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-2ea44f)](LICENSE)

## Why Frame?

`discord.py` gives you the primitives. Frame gives you a better authoring experience without taking the primitives away.

| Raw discord.py | Frame |
| --- | --- |
| `discord.Embed(...)` | `frame.embed(...)` |
| `embed.add_field(...)` | `fields=[("Members", "100", True)]` |
| `embed.set_thumbnail(...)` | `thumbnail=avatar_url` |
| `discord.ui.Button(...)` | `frame.ui.button(...)` |
| manual CV2 composition | `frame.ui.container(...)` |

The output is still native `discord.py` objects. You can keep your existing bot, cogs, commands, checks, views, and interaction handling.

## Installation

```bash
python -m pip install discord-frame
```

Frame currently targets `discord.py >= 2.6` because Components V2 support landed in that line. The current verified PyPI release is 2.7.1. Classic embed helpers do not require network access or a running bot.

## Quick start

```python
import frame

embed = frame.embed(
    "Welcome to the server!",
    "We're glad you're here.",
    color="blurple",
    thumbnail=user.display_avatar.url,
)

await channel.send(embed=embed)
```

### From simple to advanced

```python
frame.embed("Hello", "World")
```

```python
frame.embed(
    title="Server Information",
    description="## Welcome",
    color="#5865F2",
    fields=[
        ("Members", "1,240", True),
        ("Channels", "42", True),
    ],
    footer="Powered by Frame",
)
```

```python
embed = (
    frame.Embed("Profile", "A fluent builder for advanced code")
    .color(frame.colors.blurple)
    .field("Level", 20, inline=True)
    .field("XP", 4300, inline=True)
    .footer("Powered by Frame")
    .build()
)
```

## Components V2

Discord's current component reference includes layout components such as Containers, Sections, Text Displays, Media Galleries and Separators, alongside interactive buttons and select menus. Discord also documents modal-oriented Label, File Upload, Radio Group, Checkbox Group and Checkbox components. Frame's first CV2 surface focuses on message layouts and interactive message components; modal-only primitives remain an extension point rather than being faked into the message API.

```python
view = frame.ui.container(
    frame.ui.text("# Welcome"),
    frame.ui.text("Choose an option below."),
    frame.ui.separator(),
    frame.ui.action_row(
        frame.ui.button("Documentation", url="https://example.com/docs"),
        frame.ui.button("Support", custom_id="support", style="primary"),
    ),
)

await interaction.response.send_message(view=view)
```

Frame wraps a real `discord.ui.LayoutView`, which is the native `discord.py` abstraction for Components V2. `discord.py` enforces the 40-component total and 4000-character display-text constraints; Frame also validates before send so errors happen in application code rather than as a Discord HTTP 400.

## Markdown

Frame intentionally does **not** implement a new markdown language. Its helpers emit Discord-compatible syntax:

```python
description = frame.md(
    frame.md.heading("Welcome"),
    "Thanks for joining ",
    frame.md.bold("our community"),
    "!",
)
```

Useful helpers include `bold`, `italic`, `underline`, `strike`, `code`, `codeblock`, `link`, `heading`, `quote`, `mention`, `channel`, and `role`.

## Colors

```python
frame.colors.blurple
frame.colors.green
frame.colors.red
frame.Color.from_hex("#5865F2")
frame.Color.from_rgb(88, 101, 242)
```

All common forms normalize to a 24-bit RGB value. Named colors are deliberately small and predictable rather than pretending to be a complete design system.

## Local attachments

Frame does not pretend a local path is a URL. It keeps upload creation explicit:

```python
image = frame.Image.file("./assets/banner.png")
embed = frame.embed("Welcome", image=image)
files = frame.to_discord_files(embed)
await channel.send(embed=embed, files=files)
```

Discord requires actual multipart file uploads for local assets; when a file is referenced from an embed/component payload, it is referenced with an `attachment://filename` URL. `discord.py` exposes `discord.File` for the upload itself.

## Interaction callbacks

Buttons can opt into a tiny decorator without replacing `discord.py`'s interaction system:

```python
button = frame.ui.button("Click me", custom_id="hello", style="primary")

@button.on_click
async def clicked(interaction):
    await interaction.response.send_message("Hello!")
```

For larger applications, prefer normal `discord.ui.View`/`LayoutView` subclasses and keep Frame as the authoring layer. That is a deliberate boundary: Frame should make UI construction nicer, not become a second bot framework.

## Validation

Frame validates documented Discord limits before send. Embed limits currently include a 256-character title, 4096-character description, up to 25 fields, 256-character field names, 1024-character field values, a 2048-character footer, a 256-character author name, and a 6000-character aggregate text limit per message's embeds.

Errors are written to be actionable:

```text
Embed description exceeds Discord's 4096 character limit
Current: 4381
Maximum: 4096
```

## Compatibility

Frame is intentionally incremental:

```python
# Existing discord.py code remains valid.
embed = frame.embed("Hello", "World")
await channel.send(embed=embed)
```

There is no Frame client, no replacement slash-command system, and no network service hidden behind your UI code.

## Architecture

```text
Your bot / cogs / commands
           │
           ▼
         Frame
   ┌───────┼────────┐
   ▼       ▼        ▼
 Embeds    UI     Markdown
   │       │
   └───────┴───────┐
                   ▼
             discord.py
                   │
                   ▼
              Discord API
```

The model layer is serializable and deterministic so a future visual editor can consume the same representation without requiring the Python process to be the preview engine.

## Roadmap

- **P0:** embeds, validation, colors, markdown, attachments, Buttons, CV2 message layouts, serialization/debugging, docs, examples, CI
- **P1:** select callbacks, reusable component factories, persistent-view helpers, modal builders, localization hooks, snapshot utilities
- **P2:** pagination, confirmation dialogs, component state, permission-aware UI, `frame check`, visual preview protocol, design tokens
- **P3:** rate-limit abstraction, hidden networking, a second bot runtime, CSS-like layout semantics

## Project name

The working import name is `frame`, but the distribution is `discord-frame`. The bare `frame` name is already occupied on PyPI by an unrelated 2013 MVC web framework, so using `frame` as the package distribution would create an avoidable namespace collision.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
mypy src
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the maintainer workflow.

## License

MIT. See [LICENSE](LICENSE).
