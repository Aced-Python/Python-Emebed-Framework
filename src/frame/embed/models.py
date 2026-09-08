from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from frame.colors import Color, normalize
from frame.exceptions import FrameValidationError

EMBED_TITLE_MAX = 256
EMBED_DESCRIPTION_MAX = 4096
EMBED_FIELDS_MAX = 25
EMBED_FIELD_NAME_MAX = 256
EMBED_FIELD_VALUE_MAX = 1024
EMBED_FOOTER_MAX = 2048
EMBED_AUTHOR_NAME_MAX = 256
EMBED_TOTAL_MAX = 6000


@dataclass(frozen=True, slots=True)
class EmbedField:
    name: str
    value: str
    inline: bool = False


@dataclass(frozen=True, slots=True)
class Author:
    name: str
    url: str | None = None
    icon_url: str | None = None


@dataclass(frozen=True, slots=True)
class Footer:
    text: str
    icon_url: str | None = None


@dataclass(slots=True)
class Theme:
    color: Color | str | int | tuple[int, int, int] | None = None
    footer: str | None = None
    footer_icon: str | None = None
    author: Author | None = None
    thumbnail: str | Any | None = None

    def apply(self, *, color: Any, footer: Any, footer_icon: Any, author: Any, thumbnail: Any) -> tuple[Any, ...]:
        return (
            color if color is not None else self.color,
            footer if footer is not None else self.footer,
            footer_icon if footer_icon is not None else self.footer_icon,
            author if author is not None else self.author,
            thumbnail if thumbnail is not None else self.thumbnail,
        )


def _s(value: Any) -> str | None:
    return None if value is None else str(value)


def validate_embed(*, title: str | None, description: str | None, fields: list[EmbedField], footer: Footer | None, author: Author | None) -> None:
    checks = [
        ("Embed title", title, EMBED_TITLE_MAX),
        ("Embed description", description, EMBED_DESCRIPTION_MAX),
        ("Embed footer.text", footer.text if footer else None, EMBED_FOOTER_MAX),
        ("Embed author.name", author.name if author else None, EMBED_AUTHOR_NAME_MAX),
    ]
    for label, value, limit in checks:
        if value is not None and len(value) > limit:
            raise FrameValidationError(f"{label} exceeds Discord's {limit} character limit\nCurrent: {len(value)}\nMaximum: {limit}")
    if len(fields) > EMBED_FIELDS_MAX:
        raise FrameValidationError(f"Embed has {len(fields)} fields; Discord allows at most {EMBED_FIELDS_MAX}.")
    for index, field in enumerate(fields, start=1):
        for label, value, limit in (("name", field.name, EMBED_FIELD_NAME_MAX), ("value", field.value, EMBED_FIELD_VALUE_MAX)):
            if len(value) > limit:
                raise FrameValidationError(f"Embed field {index} {label} exceeds Discord's {limit} character limit\nCurrent: {len(value)}\nMaximum: {limit}")
    total = sum(len(x or "") for x in [title, description, footer.text if footer else None, author.name if author else None])
    total += sum(len(f.name) + len(f.value) for f in fields)
    if total > EMBED_TOTAL_MAX:
        raise FrameValidationError(f"Embed text exceeds Discord's 6000 character aggregate limit\nCurrent: {total}\nMaximum: {EMBED_TOTAL_MAX}")


class EmbedBuilder:
    """Fluent builder that compiles to a native ``discord.Embed``."""

    def __init__(self, title: Any = None, description: Any = None, *, theme: Theme | None = None) -> None:
        self._title = _s(title)
        self._description = _s(description)
        self._url: str | None = None
        self._timestamp: datetime | None = None
        self._color: Color | None = None
        self._fields: list[EmbedField] = []
        self._footer: Footer | None = None
        self._author: Author | None = None
        self._thumbnail: Any = None
        self._image: Any = None
        self._theme = theme

    def title(self, value: Any) -> "EmbedBuilder": self._title = _s(value); return self
    def description(self, value: Any) -> "EmbedBuilder": self._description = _s(value); return self
    def url(self, value: str | None) -> "EmbedBuilder": self._url = value; return self
    def timestamp(self, value: datetime | None) -> "EmbedBuilder": self._timestamp = value; return self
    def color(self, value: Any) -> "EmbedBuilder": self._color = normalize(value); return self
    def thumbnail(self, value: Any) -> "EmbedBuilder": self._thumbnail = value; return self
    def image(self, value: Any) -> "EmbedBuilder": self._image = value; return self

    def field(self, name: Any, value: Any, inline: bool = False) -> "EmbedBuilder":
        self._fields.append(EmbedField(str(name), str(value), inline)); return self

    def footer(self, text: Any, *, icon_url: str | None = None) -> "EmbedBuilder":
        self._footer = Footer(str(text), icon_url); return self

    def author(self, name: Any, *, url: str | None = None, icon_url: str | None = None) -> "EmbedBuilder":
        self._author = Author(str(name), url, icon_url); return self

    def build(self):
        from frame.embed.builder import _compile_embed
        return _compile_embed(self)

    def to_dict(self) -> dict[str, Any]:
        return self.build().to_dict()

    def to_discord(self):
        return self.build()
