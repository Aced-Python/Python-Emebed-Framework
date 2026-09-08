from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from frame.exceptions import InvalidColorError


@dataclass(frozen=True, slots=True)
class Color:
    """Immutable RGB color normalized to a Discord-compatible 24-bit integer."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int) or not 0 <= self.value <= 0xFFFFFF:
            raise InvalidColorError(f"Color must be an integer between 0x000000 and 0xFFFFFF; got {self.value!r}.")

    @classmethod
    def from_hex(cls, value: str) -> "Color":
        raw = value.strip().lstrip("#")
        if len(raw) == 3:
            raw = "".join(ch * 2 for ch in raw)
        if len(raw) != 6:
            raise InvalidColorError(f"Hex colors must contain 3 or 6 hexadecimal digits; got {value!r}.")
        try:
            return cls(int(raw, 16))
        except ValueError as exc:
            raise InvalidColorError(f"Invalid hexadecimal color: {value!r}.") from exc

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> "Color":
        channels = (r, g, b)
        if any(not isinstance(c, int) or not 0 <= c <= 255 for c in channels):
            raise InvalidColorError(f"RGB channels must each be integers from 0 to 255; got {channels!r}.")
        return cls((r << 16) | (g << 8) | b)

    @property
    def rgb(self) -> tuple[int, int, int]:
        return ((self.value >> 16) & 255, (self.value >> 8) & 255, self.value & 255)

    def to_discord(self):
        import discord

        return discord.Color(self.value)

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return f"#{self.value:06X}"


def normalize(value: Color | str | int | tuple[int, int, int] | None):
    """Normalize common color representations to a Frame Color."""
    if value is None:
        return None
    if isinstance(value, Color):
        return value
    if isinstance(value, str):
        key = value.strip().lower().replace(" ", "_")
        if key in NAMED:
            return NAMED[key]
        return Color.from_hex(value)
    if isinstance(value, tuple):
        if len(value) != 3:
            raise InvalidColorError("RGB tuples must contain exactly three values: (r, g, b).")
        return Color.from_rgb(*value)
    if isinstance(value, int):
        return Color(value)
    raise InvalidColorError(f"Unsupported color value: {value!r}.")


blurple: Final[Color] = Color(0x5865F2)
green: Final[Color] = Color(0x57F287)
red: Final[Color] = Color(0xED4245)
yellow: Final[Color] = Color(0xFEE75C)
fuchsia: Final[Color] = Color(0xEB459E)
white: Final[Color] = Color(0xFFFFFF)
black: Final[Color] = Color(0x000000)
discord: Final[Color] = blurple

NAMED: Final[dict[str, Color]] = {
    "blurple": blurple,
    "green": green,
    "success": green,
    "red": red,
    "danger": red,
    "yellow": yellow,
    "fuchsia": fuchsia,
    "white": white,
    "black": black,
    "discord": discord,
}

__all__ = ["Color", "normalize", "blurple", "green", "red", "yellow", "fuchsia", "white", "black", "discord"]
