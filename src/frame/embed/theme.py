"""Optional theming for consistent embed branding.

A :class:`Theme` supplies fallback values for color/footer/author/thumbnail
that individual ``frame.embed(...)`` calls don't specify. This is purely
opt-in — embeds work identically with no theme at all.

    theme = frame.Theme(color="#5865F2", footer="My Bot")
    frame.set_theme(theme)              # process-wide default
    frame.embed("Welcome", theme=theme)  # or pass explicitly per-call
"""

from __future__ import annotations

from dataclasses import dataclass

from ..attachments import ImageInput
from ..colors import Color, ColorInput


@dataclass(frozen=True)
class Theme:
    """Reusable default styling for embeds.

    Any field left as ``None`` simply doesn't override that embed
    property — the embed's own value (or Discord's default) is used.
    """

    color: ColorInput | None = None
    footer: str | None = None
    footer_icon: str | None = None
    author: str | None = None
    author_icon: str | None = None
    author_url: str | None = None
    thumbnail: ImageInput | None = None

    def resolved_color(self) -> Color | None:
        return Color(self.color) if self.color is not None else None


_active_theme: Theme | None = None


def set_theme(theme: Theme | None) -> None:
    """Set the process-wide default theme (used when an embed doesn't pass one)."""
    global _active_theme
    _active_theme = theme


def get_theme() -> Theme | None:
    """The current process-wide default theme, if any."""
    return _active_theme


__all__ = ["Theme", "set_theme", "get_theme"]
