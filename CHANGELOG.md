# Changelog

All notable changes to this project are documented in this file. Frame follows [Semantic Versioning](https://semver.org/) once it reaches 1.0; until then, minor versions may include breaking changes, called out explicitly below.

## [Unreleased]

## [0.1.0] — Initial release

### Added

- **Embeds:** `frame.embed(...)` (functional) and `frame.Embed()` (fluent builder) — title, description, url, timestamp, color, fields (with inline flag), footer + icon, author + icon/url, thumbnail, image. Validated against Discord's documented embed limits (title 256, description 4096, field name 256 / value 1024, footer 2048, author 256, 25 fields max, 6000 total).
- **Colors:** `frame.Color` (hex strings, ints, RGB tuples, `discord.Colour` duck-typing) and `frame.colors` (Discord's default palette + common aliases), with typo suggestions on unknown names.
- **Markdown:** `frame.md` — bold/italic/underline/strikethrough/spoiler/code/codeblock/heading/quote/lists/link/mention/channel/role/timestamp, composable via `frame.md(...)`.
- **Attachments:** `frame.Image` / `frame.attachment(...)` — local file references that resolve to `attachment://` URLs and real `discord.File` objects.
- **Components V2:** `frame.ui` — `text`, `separator`, `thumbnail`, `media_gallery`, `file`, `button`, `select`, `section`, `action_row`, `container`. `container(...)` validates the full tree against Discord's placement rules and returns a real, ready-to-send `discord.ui.LayoutView`.
- **Interaction callbacks:** `on_click=` / `@button.on_click` and `on_select=` / `@select.on_select`, wired directly onto real discord.py `Item.callback`.
- **Presets:** `frame.ui.confirm(...)` — a ready-made confirm/cancel action row.
- **Themes:** `frame.Theme` / `frame.set_theme(...)` — optional default color/footer/author/thumbnail for embeds that don't set their own.
- **Serialization:** `.to_dict()` on embeds and every UI component, for offline inspection/testing/logging.
- **Exceptions:** `FrameError` → `FrameValidationError` → `InvalidEmbedError` / `InvalidComponentError`; `InvalidColorError`; `AttachmentError`. All validation errors state the rule, current value, and limit.

### Notes

- Requires `discord.py>=2.7.1` for native Components V2 (`discord.ui.LayoutView`) support.
- Class-based views (`class MyView(frame.View): ...`) are intentionally not included in this release — see the README roadmap.
