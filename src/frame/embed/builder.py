from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    import discord

from frame.attachments import Attachment
from frame.colors import Color, normalize
from frame.embed.models import Author, EmbedBuilder, EmbedField, Footer, Theme, validate_embed


def _media_url(value: Any) -> tuple[str | None, list[Attachment]]:
    if value is None:
        return None, []
    if isinstance(value, Attachment):
        return value.attachment_url, [value]
    return str(value), []


def _apply_theme(builder: EmbedBuilder, *, color: Any, footer: Any, footer_icon: Any, author: Any, thumbnail: Any) -> tuple[Any, Any, Any, Any, Any]:
    if builder._theme is None:
        return color, footer, footer_icon, author, thumbnail
    return builder._theme.apply(color=color, footer=footer, footer_icon=footer_icon, author=author, thumbnail=thumbnail)


_FRAME_EMBED_TYPE = None


def _compile_embed(builder: EmbedBuilder):
    # Validate before importing discord so deterministic validation errors do not depend on runtime availability.
    color, footer, footer_icon, author, thumbnail = _apply_theme(
        builder,
        color=builder._color,
        footer=builder._footer.text if builder._footer else None,
        footer_icon=builder._footer.icon_url if builder._footer else None,
        author=builder._author,
        thumbnail=builder._thumbnail,
    )
    normalized_footer = None if footer is None else Footer(str(footer), footer_icon)
    validate_embed(title=builder._title, description=builder._description, fields=builder._fields, footer=normalized_footer, author=author)

    import discord

    global _FRAME_EMBED_TYPE
    if _FRAME_EMBED_TYPE is None:
        class FrameEmbed(discord.Embed):
            """Native discord.py embed with Frame attachment metadata and fluent escape hatches."""

            def to_discord(self):
                return self
        _FRAME_EMBED_TYPE = FrameEmbed

    title = builder._title
    description = builder._description
    normalized_color = normalize(color)
    if isinstance(author, str):
        author = Author(author)

    embed = _FRAME_EMBED_TYPE(title=title, description=description, url=builder._url, timestamp=builder._timestamp, color=int(normalized_color) if normalized_color else None)
    for field in builder._fields:
        embed.add_field(name=field.name, value=field.value, inline=field.inline)
    if normalized_footer:
        embed.set_footer(text=normalized_footer.text, icon_url=normalized_footer.icon_url)
    if author:
        embed.set_author(name=author.name, url=author.url, icon_url=author.icon_url)
    extra_files: list[Attachment] = []
    for attr, method in ((builder._thumbnail, "set_thumbnail"), (builder._image, "set_image")):
        url, files = _media_url(attr)
        extra_files.extend(files)
        if url:
            getattr(embed, method)(url=url)
    embed._frame_attachments = tuple(extra_files)
    return embed


def _parse_fields(fields: Iterable[Any] | None) -> list[EmbedField]:
    result: list[EmbedField] = []
    for field in fields or ():
        if isinstance(field, EmbedField):
            result.append(field)
        else:
            if len(field) not in (2, 3):
                raise ValueError("Embed fields must be (name, value) or (name, value, inline).")
            result.append(EmbedField(str(field[0]), str(field[1]), bool(field[2]) if len(field) == 3 else False))
    return result


def embed(
    title: Any = None,
    description: Any = None,
    *,
    url: str | None = None,
    timestamp: datetime | None = None,
    color: Color | str | int | tuple[int, int, int] | None = None,
    fields: Iterable[Any] | None = None,
    footer: str | Footer | None = None,
    author: str | Author | None = None,
    thumbnail: Any = None,
    image: Any = None,
    theme: Theme | None = None,
):
    """Create a native ``discord.Embed`` with Frame's ergonomic defaults."""
    builder = EmbedBuilder(title, description, theme=theme)
    builder._url = url
    builder._timestamp = timestamp
    builder._color = normalize(color)
    builder._fields = _parse_fields(fields)
    if isinstance(footer, Footer):
        builder._footer = footer
    elif footer is not None:
        builder._footer = Footer(str(footer))
    if isinstance(author, Author):
        builder._author = author
    elif author is not None:
        builder._author = Author(str(author))
    builder._thumbnail = thumbnail
    builder._image = image
    return _compile_embed(builder)


class Embed(EmbedBuilder):
    """Builder alias for advanced fluent construction."""


__all__ = ["embed", "Embed", "EmbedBuilder", "Theme", "Author", "Footer", "EmbedField"]
