"""Frame's color API.

Accepts hex strings, raw ints, RGB tuples, ``discord.Colour`` objects, or
named colors from Discord's default palette, and normalizes them all to a
single :class:`Color` (an ``int`` subclass, so it's already a valid
``discord.py`` color wherever one is expected).

    frame.colors.blurple
    frame.Color("#5865F2")
    frame.Color(0x5865F2)
    frame.Color((88, 101, 242))
"""

from __future__ import annotations

import re
from difflib import get_close_matches
from typing import TYPE_CHECKING, Union

from ..exceptions import InvalidColorError

if TYPE_CHECKING:
    import discord

_HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})$")

# Discord's documented default embed/role color palette, plus a handful of
# conventional aliases developers reach for constantly.
_NAMED_COLORS: dict[str, int] = {
    "default": 0x000000,
    "blurple": 0x5865F2,
    "discord": 0x5865F2,
    "old_blurple": 0x7289DA,
    "greyple": 0x99AAB5,
    "grayple": 0x99AAB5,
    "dark_but_not_black": 0x2C2F33,
    "not_quite_black": 0x23272A,
    "teal": 0x1ABC9C,
    "dark_teal": 0x11806A,
    "green": 0x57F287,
    "dark_green": 0x1F8B4C,
    "blue": 0x3498DB,
    "dark_blue": 0x206694,
    "purple": 0x9B59B6,
    "dark_purple": 0x71368A,
    "magenta": 0xE91E63,
    "dark_magenta": 0xAD1457,
    "gold": 0xF1C40F,
    "yellow": 0xFEE75C,
    "dark_gold": 0xC27C0E,
    "orange": 0xE67E22,
    "dark_orange": 0xA84300,
    "red": 0xED4245,
    "dark_red": 0x992D22,
    "lighter_grey": 0x95A5A6,
    "lighter_gray": 0x95A5A6,
    "dark_grey": 0x607D8B,
    "dark_gray": 0x607D8B,
    "light_grey": 0x979C9F,
    "light_gray": 0x979C9F,
    "darker_grey": 0x546E7A,
    "darker_gray": 0x546E7A,
    "og_blurple": 0x7289DA,
    "black": 0x000000,
    "white": 0xFFFFFF,
    "fuchsia": 0xEB459E,
}

ColorInput = Union[str, int, "Color", tuple, "discord.Colour"]


class Color(int):
    """An RGB color, always representable as a plain ``int``.

    Because ``Color`` *is* an ``int``, the result of ``frame.Color(...)``
    can be passed anywhere ``discord.py`` expects a color integer, and
    also anywhere Frame expects a :data:`ColorInput`.
    """

    __slots__ = ()

    def __new__(cls, value: ColorInput) -> Color:
        return int.__new__(cls, _parse_color(value))

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> Color:
        """Build a color from individual 0-255 red/green/blue components."""
        for name, component in (("red", r), ("green", g), ("blue", b)):
            if not 0 <= component <= 255:
                raise InvalidColorError(
                    f"Invalid RGB {name} component: {component!r}. "
                    "Each component must be an integer between 0 and 255."
                )
        return cls((r << 16) + (g << 8) + b)

    @property
    def r(self) -> int:
        return (int(self) >> 16) & 0xFF

    @property
    def g(self) -> int:
        return (int(self) >> 8) & 0xFF

    @property
    def b(self) -> int:
        return int(self) & 0xFF

    def to_rgb(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

    def to_hex(self) -> str:
        return f"#{int(self):06X}"

    def to_discord(self) -> discord.Colour:
        """Convert to a real ``discord.Colour``."""
        import discord

        return discord.Colour(int(self))

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"Color({self.to_hex()})"


def _parse_color(value: ColorInput) -> int:
    if isinstance(value, Color):
        return int(value)

    if isinstance(value, bool):  # bool is an int subclass; reject explicitly
        raise InvalidColorError(f"Invalid color: {value!r} is not a valid color.")

    if isinstance(value, int):
        if not 0 <= value <= 0xFFFFFF:
            raise InvalidColorError(
                f"Invalid color integer: {value!r}. "
                "Color integers must be between 0x000000 and 0xFFFFFF."
            )
        return value

    if isinstance(value, str):
        text = value.strip()
        match = _HEX_RE.match(text)
        if match:
            return int(match.group(1), 16)

        key = text.lower().replace(" ", "_").replace("-", "_")
        if key in _NAMED_COLORS:
            return _NAMED_COLORS[key]

        suggestions = get_close_matches(key, _NAMED_COLORS.keys(), n=3)
        hint = (
            f" Did you mean {', '.join(repr(s) for s in suggestions)}?"
            if suggestions
            else f" Known names: {', '.join(sorted(_NAMED_COLORS))}."
        )
        raise InvalidColorError(
            f"Invalid color: {value!r} is not a valid hex string "
            f"('#RRGGBB') or a known named color.{hint}"
        )

    if isinstance(value, tuple):
        if len(value) != 3:
            raise InvalidColorError(
                f"Invalid RGB tuple: {value!r}. Expected exactly 3 values (r, g, b)."
            )
        return int(Color.from_rgb(*value))

    # discord.Colour / discord.Color duck-typing, without a hard import.
    inner = getattr(value, "value", None)
    if isinstance(inner, int):
        return inner

    raise InvalidColorError(
        f"Invalid color: {value!r} ({type(value).__name__}). "
        "Expected a hex string, an int, an (r, g, b) tuple, a frame.Color, "
        "or a discord.Colour."
    )


class _ColorPalette:
    """Attribute access over the named color table: ``frame.colors.blurple``."""

    def __getattr__(self, name: str) -> Color:
        key = name.lower()
        if key in _NAMED_COLORS:
            return Color(_NAMED_COLORS[key])
        suggestions = get_close_matches(key, _NAMED_COLORS.keys(), n=3)
        hint = f" Did you mean {', '.join(suggestions)}?" if suggestions else ""
        raise AttributeError(f"frame.colors has no color named {name!r}.{hint}")

    def __dir__(self):  # pragma: no cover - cosmetic/autocomplete support
        return sorted(_NAMED_COLORS)


colors = _ColorPalette()

__all__ = ["Color", "colors", "ColorInput"]
