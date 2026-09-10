# frame

**Build beautiful Discord messages and interactive UIs without fighting Discord's API.**

`frame` is a developer-experience layer on top of [discord.py](https://github.com/Rapptz/discord.py). It doesn't replace discord.py, doesn't add a second bot framework, and doesn't hide anything you need to understand, isn't overcomplicated — it just makes the parts of the Discord API you write over and over (embeds, buttons, Components V2 layouts) dramatically less verbose, with validation that catches mistakes before Discord does.

```python
import frame

embed = frame.embed(
    "Welcome!",
    "Thanks for joining our server.",
    thumbnail="https://example.com/logo.png",
)

await channel.send(embed=embed)
```

```python
view = frame.ui.container(
    frame.ui.text("## Welcome"),
    frame.ui.separator(),
    frame.ui.section(
        "Need help?",
        accessory=frame.ui.button("Open Support", style="primary", custom_id="support"),
    ),
)

await interaction.response.send_message(view=view)
```

Everything `frame` produces is a **real discord.py object** underneath — `frame.embed(...)` returns an actual `discord.Embed`, `frame.ui.container(...)` returns an actual `discord.ui.LayoutView`. You can drop back to raw discord.py at any point, mid-project, mid-function, forever.

---

## Why not just use discord.py directly?

discord.py

```python
embed = discord.Embed(
    title="Welcome",
    description="Hello!",
    color=discord.Color.blurple(),
)
embed.set_thumbnail(url=avatar)
embed.add_field(name="Members", value="100", inline=True)
```

frame

```python
embed = frame.embed(
    "Welcome",
    "Hello!",
    color="blurple",
    thumbnail=avatar,
    fields=[("Members", "100", True)],
)
```

Same result. Less ceremony. And when something's wrong, frame tells you exactly what and how to fix it, instead of Discord returning a `400` with a JSON blob:

```
InvalidEmbedError: Embed description exceeds Discord's 4096 character limit
Current: 4381
Maximum: 4096
```

Components V2 is where this gets more valuable, not less — discord.py's `ui.Container`/`ui.Section`/`ui.ActionRow` model is powerful but easy to misuse (a bare button outside an action row, mixing a select with buttons in one row). `frame.ui` validates the whole tree up front:

```
InvalidComponentError: A bare button can't be placed directly in a container —
Discord requires it to be inside frame.ui.action_row(...), or used as a
frame.ui.section(...) accessory.
```

## Installation

```bash
pip install frame-discord
```

Requires Python 3.10+ and `discord.py>=2.7.1` (frame's Components V2 support relies on discord.py's native `ui.LayoutView`, added in that release).

> **Note on the name:** the package installs as `frame-discord` (the plain `frame` name was already taken on PyPI) but you still `import frame` in code.

## Quick start

```python
import discord
import frame

bot = discord.Bot()

@bot.slash_command()
async def welcome(ctx, member: discord.Member):
    embed = frame.embed(
        f"Welcome, {member.display_name}!",
        "We're glad you're here.",
        color="blurple",
        thumbnail=member.display_avatar.url,
    )
    await ctx.respond(embed=embed)
```

That's it — `frame.embed(...)` is a drop-in replacement wherever you'd hand discord.py a `discord.Embed`. Nothing else about your bot changes.

## Table of contents

- [Embeds](#embeds)
- [Markdown](#markdown)
- [Colors](#colors)
- [Images & attachments](#images--attachments)
- [Buttons](#buttons)
- [Components V2](#components-v2)
- [Interaction callbacks](#interaction-callbacks)
- [Select menus](#select-menus)
- [Themes](#themes)
- [Validation](#validation)
- [Serialization](#serialization)
- [Migrating from raw discord.py](#migrating-from-raw-discordpy)
- [Design philosophy](#design-philosophy)
- [Project status & roadmap](#project-status--roadmap)
- [Contributing](#contributing)

## Embeds

The simplest thing is extremely simple:

```python
frame.embed("Hello", "Welcome!")
```

Complexity is opt-in:

```python
frame.embed(
    title="Server Information",
    description="## Welcome\nHere is your server information.",
    color=frame.colors.blurple,
    fields=[
        ("Members", "1,240", True),
        ("Channels", "42", True),
        ("Created", "2024", True),
    ],
    footer="Powered by Frame",
)
```

Or use the fluent builder when you're assembling an embed conditionally:

```python
embed = (
    frame.Embed()
    .title("Welcome")
    .description("Hello!")
    .color("#5865F2")
    .thumbnail(user.display_avatar.url)
    .field("Members", "100", inline=True)
    .field("Channels", "20", inline=True)
    .footer("Powered by Frame")
    .to_discord()
)
```

`frame.embed(...)` and `frame.Embed().to_discord()` both produce a plain `discord.Embed`. Supported: title, description, url, timestamp, color, fields (with an inline flag), footer (+ icon), author (+ icon/url), thumbnail, image — all validated against Discord's documented limits.

## Markdown

Discord's Markdown dialect is small and fixed, so `frame.md` is a thin set of formatting helpers rather than a full Markdown engine:

```python
frame.md.bold("hello")
frame.md.italic("hello")
frame.md.code("print('hello')")
frame.md.codeblock("python", "print('hello')")
frame.md.link("Discord", "https://discord.com")
frame.md.mention(user)
frame.md.channel(channel)
frame.md.role(role)
frame.md.timestamp(some_datetime)
```

Compose fragments by calling the module itself:

```python
description = frame.md(
    frame.md.heading("Welcome"),
    "\nThanks for joining ",
    frame.md.bold("our community"),
    "!",
)
```

Every helper returns a plain `str` — there's no separate AST to learn, and the output is always valid Discord Markdown.

## Colors

```python
frame.colors.blurple
frame.colors.green
frame.colors.red
frame.colors.gold
```

Or construct one directly — hex strings, ints, RGB tuples, named colors, or a real `discord.Colour` all work anywhere Frame accepts a color:

```python
frame.Color("#5865F2")
frame.Color(0x5865F2)
frame.Color((88, 101, 242))
frame.Color("blurple")
```

Unknown names get a helpful suggestion instead of a bare `KeyError`:

```
InvalidColorError: Invalid color: 'blurpl' is not a valid hex string ('#RRGGBB')
or a known named color. Did you mean 'blurple'?
```

## Images & attachments

Remote images are just URLs:

```python
frame.embed("Image", image="https://example.com/image.png")
```

Local files go through `frame.attachment(...)` (or `frame.Image.file(...)`), which validates the file exists immediately and wires up the `attachment://` reference Discord expects:

```python
embed = frame.Embed().title("Welcome").image(frame.attachment("./assets/banner.png"))

await channel.send(embed=embed.to_discord(), files=embed.files())
```

`embed.files()` returns the real `discord.File` objects for every local image referenced — pass them straight to `files=`.

## Buttons

```python
frame.ui.button("Click me", style="primary", custom_id="hello")
frame.ui.button("Documentation", url="https://example.com")  # style is inferred as "link"
```

Styles: `primary` (alias `blurple`), `secondary` (alias `grey`/`gray`), `success` (alias `green`), `danger` (alias `red`), and `link` (inferred automatically from `url=`).

## Components V2

Discord's Components V2 message layout system — containers, sections, action rows, separators, media galleries, and file displays — with the same "simple things are simple" philosophy:

```python
view = frame.ui.container(
    frame.ui.text("## Account"),
    frame.ui.section(
        frame.ui.text("Manage your account"),
        accessory=frame.ui.button("Settings", custom_id="settings"),
    ),
    frame.ui.separator(),
    frame.ui.action_row(
        frame.ui.button("Save", style="success", custom_id="save"),
        frame.ui.button("Cancel", style="secondary", custom_id="cancel"),
    ),
)

await interaction.response.send_message(view=view)
```

`frame.ui.container(...)` is the entry point. It validates the entire tree against Discord's real placement rules before converting anything, and returns a genuine, ready-to-send `discord.ui.LayoutView` (`isinstance(view, discord.ui.LayoutView)` is `True` — it composes normally with the rest of discord.py, including `bot.add_view(...)` for persistent views).

Rules frame enforces, with messages that explain the fix:

| Rule | What frame does |
|---|---|
| A button/select can't sit directly in a container | `InvalidComponentError` naming the offending component and where it needs to go |
| An action row can't mix a select with buttons | Caught before sending |
| An action row holds at most 5 buttons, or exactly 1 select | Caught before sending |
| A section holds 1–3 text children plus one accessory (button or thumbnail) | Caught before sending |
| Text/button/select length limits | Caught before sending, with current/maximum in the message |

Components V2 messages can't be combined with legacy `content=`/`embeds=` on the same message — that's a Discord API constraint, not a frame limitation.

## Interaction callbacks

Wire a button up to a handler directly:

```python
support_button = frame.ui.button("Open Support", style="primary", custom_id="support")

@support_button.on_click
async def open_support(interaction: discord.Interaction):
    await interaction.response.send_message("A team member will be with you shortly.", ephemeral=True)

view = frame.ui.container(frame.ui.text("Need help?"), frame.ui.action_row(support_button))
```

Or pass the callback up front:

```python
frame.ui.button("Save", style="success", on_click=handle_save)
```

Frame wires these onto the real `discord.ui.Button`'s `.callback`, so they integrate with discord.py's normal interaction dispatch — no second event system involved.

There's also a ready-made confirmation preset:

```python
view = frame.ui.confirm(
    "Are you sure you want to delete this?",
    on_confirm=do_delete,
)
await interaction.response.send_message(view=view, ephemeral=True)
```

## Select menus

```python
menu = frame.ui.select(
    options=[
        frame.Option("Python", "python"),
        frame.Option("JavaScript", "javascript"),
    ],
    placeholder="Pick a language",
    on_select=handle_pick,
)

view = frame.ui.container(frame.ui.text("Choose one:"), frame.ui.action_row(menu))
```

## Themes

Optional, process-wide (or per-call) default branding for embeds:

```python
theme = frame.Theme(color="#5865F2", footer="My Bot", thumbnail="https://example.com/logo.png")
frame.set_theme(theme)

# any embed that doesn't set its own color/footer/thumbnail uses the theme's
frame.embed("Welcome", "Hello!")
```

Values you set explicitly on an embed always win over the theme — themes only fill gaps.

## Validation

Frame validates against Discord's documented limits before anything is sent, with messages that state the rule, the current value, and the limit:

```python
frame.embed(description="x" * 5000)
# InvalidEmbedError: Embed description exceeds Discord's 4096 character limit
# Current: 5000
# Maximum: 4096
```

Exception hierarchy: `FrameError` → `FrameValidationError` → `InvalidEmbedError` / `InvalidComponentError`; plus `InvalidColorError` and `AttachmentError` for their respective failure modes. Catch `frame.FrameError` if you don't care which subtype.

## Serialization

Every frame object can be inspected without a live Discord connection:

```python
embed = frame.Embed().title("Hi")
embed.to_dict()      # raw embed JSON shape, for logging/tests
embed.to_discord()   # real discord.Embed

text = frame.ui.text("hello")
text.to_dict()        # {'kind': 'text', 'content': 'hello'}
```

This is what makes frame's test suite fully offline — component and embed construction, and validation, never need a Discord connection.

## Migrating from raw discord.py

frame is designed to be adopted incrementally, file by file, function by function — you never have to rewrite your whole bot.

```python
# Before
embed = discord.Embed(title="Welcome", description="Hello!", color=discord.Color.blurple())
embed.set_thumbnail(url=avatar)
embed.add_field(name="Members", value="100", inline=True)

# After
embed = frame.embed(
    "Welcome", "Hello!", color="blurple", thumbnail=avatar,
    fields=[("Members", "100", True)],
)
```

Everything downstream — `channel.send(embed=embed)`, `ctx.respond(embed=embed)` — is unchanged, because the result is still a `discord.Embed`.

## Design philosophy

1. The simplest thing should be extremely simple: `frame.embed("Hello", "World")`.
2. Complexity is opt-in, never required.
3. Frame never hides a Discord concept you need to understand — it removes ceremony, not understanding.
4. No abstraction exists unless it removes real, repeated boilerplate.
5. Everything is type-annotated; autocomplete should do most of the teaching.
6. Every frame object degrades to a real discord.py object at the boundary.
7. Error messages state the rule, the current value, and the limit — they should be enough to fix the bug without opening Discord's docs.
8. Explicit over magical. No metaclasses, no decorators that silently register global state.

## Project status & roadmap

Frame is pre-1.0 (`0.1.0`) — the core API (embeds, colors, markdown, attachments, and Components V2: text/separator/thumbnail/media gallery/file/button/select/section/action row/container, plus callback wiring) is implemented, tested, and validated against real discord.py 2.7.1. Treat the public API as stable-ish but not yet semver-guaranteed until 1.0.

**Not yet implemented** (tracked, not promised):

- `P1` — class-based views (`class MyView(frame.View):` with a `@frame.button(...)` decorator). The functional `on_click=` / `@button.on_click` pattern above is the fully-supported path today; a class-based layer is being designed carefully rather than bolted on, since correctly reimplementing discord.py's view metaclass for Components V2 is easy to get subtly wrong.
- `P1` — `frame.presets` extension system beyond `frame.ui.confirm(...)`.
- `P2` — `frame check` CLI for auditing embeds/components against Discord limits ahead of runtime; a `frame dev` live-preview server.
- `P2` — modal/form helpers (Discord's modal API is a separate flow from message components).
- `P3` — hosted "Frame Studio" visual builder. Not part of the open-source core; noted here only because the serialization layer (`to_dict()` everywhere) is deliberately designed to make it possible later.

See [ROADMAP.md](ROADMAP.md) for the full prioritized list.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports, docs fixes, and small PRs are very welcome; for anything that changes the public API, please open an issue first so we can talk through the design — see [Design philosophy](#design-philosophy) above for what we're protecting.

## License

MIT — see [LICENSE](LICENSE).
