"""Public embed API.

Two equivalent ways to build an embed:

Functional, for the common case::

    frame.embed("Welcome", "Thanks for joining!", color="blurple")

Fluent, when you're assembling an embed conditionally/incrementally::

    (
        frame.Embed()
        .title("Welcome")
        .description("Thanks for joining!")
        .color("blurple")
        .field("Members", "100", inline=True)
    )

Both produce the same object and both ultimately call ``.to_discord()``
to become a real ``discord.Embed``.
"""

from __future__ import annotations

import datetime as _dt
from collections.abc import Sequence
from typing import TYPE_CHECKING

from ..attachments import ImageInput, coerce_image
from ..colors import Color, ColorInput
from .models import EmbedData, Field
from .theme import Theme, get_theme

if TYPE_CHECKING:
    import discord

FieldInput = tuple | Field | dict


def _coerce_field(f: FieldInput) -> Field:
    if isinstance(f, Field):
        return f
    if isinstance(f, dict):
        return Field(
            name=f["name"], value=f["value"], inline=bool(f.get("inline", False))
        )
    if isinstance(f, tuple):
        if len(f) == 2:
            name, value = f
            return Field(name=str(name), value=str(value), inline=False)
        if len(f) == 3:
            name, value, inline = f
            return Field(name=str(name), value=str(value), inline=bool(inline))
    raise TypeError(
        f"Invalid field: {f!r}. Expected a (name, value), (name, value, inline) "
        "tuple, a dict with 'name'/'value'/'inline', or a frame.embed.Field."
    )


class Embed:
    """A fluent, immutable-feeling embed builder.

    Every mutator method returns ``self`` so calls chain, but note this is
    a *builder*, not a frozen value: chaining mutates and returns the same
    instance. Call :meth:`build` (or just pass it wherever a
    ``discord.Embed`` is expected — Frame objects convert automatically at
    the boundary) when you're done.
    """

    def __init__(self) -> None:
        self._data = EmbedData()

    # -- content -----------------------------------------------------
    def title(self, value: str) -> Embed:
        self._data.title = value
        return self

    def description(self, value: str) -> Embed:
        self._data.description = value
        return self

    def url(self, value: str) -> Embed:
        self._data.url = value
        return self

    def color(self, value: ColorInput) -> Embed:
        self._data.color = Color(value)
        return self

    # British spelling alias, since discord.py itself accepts both.
    colour = color

    def timestamp(self, value: _dt.datetime | None = None) -> Embed:
        self._data.timestamp = value or _dt.datetime.now(_dt.timezone.utc)
        return self

    def footer(self, text: str, *, icon: ImageInput = None) -> Embed:
        self._data.footer = text
        if icon is not None:
            self._data.footer_icon = coerce_image(icon)
        return self

    def author(
        self, name: str, *, url: str | None = None, icon: ImageInput = None
    ) -> Embed:
        self._data.author = name
        self._data.author_url = url
        if icon is not None:
            self._data.author_icon = coerce_image(icon)
        return self

    def thumbnail(self, image: ImageInput) -> Embed:
        self._data.thumbnail = coerce_image(image)
        return self

    def image(self, image: ImageInput) -> Embed:
        self._data.image = coerce_image(image)
        return self

    def field(self, name: str, value: str, inline: bool = False) -> Embed:
        self._data.fields.append(Field(name=name, value=value, inline=inline))
        return self

    def fields_from(self, fields: Sequence[FieldInput]) -> Embed:
        for f in fields:
            self._data.fields.append(_coerce_field(f))
        return self

    def clear_fields(self) -> Embed:
        self._data.fields.clear()
        return self

    # -- theming -------------------------------------------------------
    def apply_theme(self, theme: Theme | None = None) -> Embed:
        """Fill unset title/color/footer/author/thumbnail from a theme.

        Uses the active theme set via ``frame.set_theme(...)`` if none is
        given. Values you've already set are never overwritten.
        """
        self._data.apply_theme(theme if theme is not None else get_theme())
        return self

    # -- output ----------------------------------------------------------
    def validate(self) -> Embed:
        """Check this embed against Discord's limits, raising ``InvalidEmbedError``."""
        self._data.validate()
        return self

    def to_dict(self) -> dict:
        """The raw embed JSON payload (validates first)."""
        self.validate()
        return self._data.to_dict()

    def to_discord(self) -> discord.Embed:
        """Build a real ``discord.Embed`` (validates first)."""
        self.validate()
        return self._data.to_discord()

    def files(self) -> list:
        """``discord.File`` objects for any local images — pass as ``files=`` when sending."""
        return self._data.to_discord_files()

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        title = self._data.title
        return f"<Embed title={title!r} fields={len(self._data.fields)}>"


def embed(
    title: str | None = None,
    description: str | None = None,
    *,
    url: str | None = None,
    color: ColorInput | None = None,
    colour: ColorInput | None = None,
    timestamp: _dt.datetime | None = None,
    footer: str | None = None,
    footer_icon: ImageInput = None,
    author: str | None = None,
    author_url: str | None = None,
    author_icon: ImageInput = None,
    thumbnail: ImageInput = None,
    image: ImageInput = None,
    fields: Sequence[FieldInput] | None = None,
    theme: Theme | None = None,
) -> discord.Embed:
    """Build a ``discord.Embed`` in one call.

    The simplest form is just a title and description::

        frame.embed("Hello", "World")

    Everything else is keyword-only. ``color``/``colour`` accepts a hex
    string, an int, an ``(r, g, b)`` tuple, a named color
    (``frame.colors.blurple`` or the string ``"blurple"``), or a real
    ``discord.Colour``. ``fields`` accepts a list of ``(name, value)`` or
    ``(name, value, inline)`` tuples.

    Returns a plain ``discord.Embed`` — ready to pass straight to
    ``channel.send(embed=...)``. If you referenced any local images (via
    ``frame.attachment(...)``), use :func:`frame.Embed` directly instead
    so you can also retrieve the matching ``discord.File`` objects via
    ``.files()``.
    """
    builder = Embed()
    if title is not None:
        builder.title(title)
    if description is not None:
        builder.description(description)
    if url is not None:
        builder.url(url)
    resolved_color = color if color is not None else colour
    if resolved_color is not None:
        builder.color(resolved_color)
    if timestamp is not None:
        builder.timestamp(timestamp)
    if footer is not None or footer_icon is not None:
        builder.footer(footer or "", icon=footer_icon)
        if footer is None:
            builder._data.footer = None  # icon-only footer stays icon-only
    if author is not None:
        builder.author(author, url=author_url, icon=author_icon)
    if thumbnail is not None:
        builder.thumbnail(thumbnail)
    if image is not None:
        builder.image(image)
    if fields:
        builder.fields_from(fields)
    builder.apply_theme(theme)
    return builder.to_discord()
