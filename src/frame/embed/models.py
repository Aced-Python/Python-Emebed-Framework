"""Internal embed data model — independent of discord.py.

Kept separate from ``discord.Embed`` so embeds can be built, validated,
inspected (``to_dict()``), and unit-tested without a live Discord
connection, then converted to a real ``discord.Embed`` only at the end
(``to_discord()``).
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field

from ..attachments import Image, coerce_image
from ..colors import Color
from . import limits
from .theme import Theme


@dataclass
class Field:
    name: str
    value: str
    inline: bool = False

    def validate(self) -> None:
        limits.check_length(self.name, limits.FIELD_NAME_LIMIT, what="field name")
        limits.check_length(self.value, limits.FIELD_VALUE_LIMIT, what="field value")


@dataclass
class EmbedData:
    """Plain-data representation of an embed, pre-validation."""

    title: str | None = None
    description: str | None = None
    url: str | None = None
    color: Color | None = None
    timestamp: _dt.datetime | None = None
    footer: str | None = None
    footer_icon: Image | None = None
    author: str | None = None
    author_url: str | None = None
    author_icon: Image | None = None
    thumbnail: Image | None = None
    image: Image | None = None
    fields: list[Field] = field(default_factory=list)

    def validate(self) -> None:
        if self.title is not None:
            limits.check_length(self.title, limits.TITLE_LIMIT, what="title")
        if self.description is not None:
            limits.check_length(
                self.description, limits.DESCRIPTION_LIMIT, what="description"
            )
        if self.footer is not None:
            limits.check_length(self.footer, limits.FOOTER_TEXT_LIMIT, what="footer text")
        if self.author is not None:
            limits.check_length(self.author, limits.AUTHOR_NAME_LIMIT, what="author name")
        limits.check_field_count(len(self.fields))
        for f in self.fields:
            f.validate()
        limits.check_total_length(
            title=self.title or "",
            description=self.description or "",
            footer=self.footer or "",
            author=self.author or "",
            fields=[(f.name, f.value, f.inline) for f in self.fields],
        )

    def apply_theme(self, theme: Theme | None) -> None:
        """Fill in unset fields from a theme, in place. Explicit values always win."""
        if theme is None:
            return
        if self.color is None and theme.color is not None:
            self.color = theme.resolved_color()
        if self.footer is None and theme.footer is not None:
            self.footer = theme.footer
        if self.footer_icon is None and theme.footer_icon is not None:
            self.footer_icon = coerce_image(theme.footer_icon)
        if self.author is None and theme.author is not None:
            self.author = theme.author
        if self.author_url is None and theme.author_url is not None:
            self.author_url = theme.author_url
        if self.author_icon is None and theme.author_icon is not None:
            self.author_icon = coerce_image(theme.author_icon)
        if self.thumbnail is None and theme.thumbnail is not None:
            self.thumbnail = coerce_image(theme.thumbnail)

    def local_images(self) -> list[Image]:
        """Every local (non-URL) image referenced by this embed, for attaching."""
        return [
            img
            for img in (self.thumbnail, self.image, self.footer_icon, self.author_icon)
            if img is not None and img.is_local
        ]

    def to_dict(self) -> dict:
        """Serialize to the raw Discord embed JSON shape (for logging/tests/debugging)."""
        data: dict = {"type": "rich"}
        if self.title is not None:
            data["title"] = self.title
        if self.description is not None:
            data["description"] = self.description
        if self.url is not None:
            data["url"] = self.url
        if self.color is not None:
            data["color"] = int(self.color)
        if self.timestamp is not None:
            data["timestamp"] = self.timestamp.isoformat()
        if self.footer is not None or self.footer_icon is not None:
            footer: dict = {}
            if self.footer is not None:
                footer["text"] = self.footer
            if self.footer_icon is not None:
                footer["icon_url"] = self.footer_icon.as_url
            data["footer"] = footer
        if self.author is not None:
            author: dict = {"name": self.author}
            if self.author_url is not None:
                author["url"] = self.author_url
            if self.author_icon is not None:
                author["icon_url"] = self.author_icon.as_url
            data["author"] = author
        if self.thumbnail is not None:
            data["thumbnail"] = {"url": self.thumbnail.as_url}
        if self.image is not None:
            data["image"] = {"url": self.image.as_url}
        if self.fields:
            data["fields"] = [
                {"name": f.name, "value": f.value, "inline": f.inline} for f in self.fields
            ]
        return data

    def to_discord(self):
        """Build a real ``discord.Embed`` from this data."""
        import discord

        e = discord.Embed(
            title=self.title,
            description=self.description,
            url=self.url,
            color=self.color.to_discord() if self.color is not None else None,
            timestamp=self.timestamp,
        )
        if self.footer is not None or self.footer_icon is not None:
            e.set_footer(
                text=self.footer,
                icon_url=self.footer_icon.as_url if self.footer_icon else None,
            )
        if self.author is not None:
            e.set_author(
                name=self.author,
                url=self.author_url,
                icon_url=self.author_icon.as_url if self.author_icon else None,
            )
        if self.thumbnail is not None:
            e.set_thumbnail(url=self.thumbnail.as_url)
        if self.image is not None:
            e.set_image(url=self.image.as_url)
        for f in self.fields:
            e.add_field(name=f.name, value=f.value, inline=f.inline)
        return e

    def to_discord_files(self) -> list:
        """``discord.File`` objects for every local image, ready to pass as ``files=``."""
        return [img.to_discord_file() for img in self.local_images()]
