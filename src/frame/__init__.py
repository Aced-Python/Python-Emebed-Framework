"""
frame — a developer-experience layer for building Discord embeds and
Components V2 interfaces on top of discord.py.

    import frame

    embed = frame.embed("Welcome!", "Thanks for joining.")
    await channel.send(embed=embed)

Everything Frame produces is a real discord.py object underneath — you can
always drop back to raw discord.py at any point.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

try:
    __version__ = _version("frame-discord")
except PackageNotFoundError:  # pragma: no cover - local/editable checkout
    __version__ = "0.0.0.dev0"

from . import ui
from .attachments import Image, attachment
from .colors import Color, colors
from .embed.builder import Embed, embed
from .embed.theme import Theme, get_theme, set_theme
from .exceptions import (
    AttachmentError,
    FrameError,
    FrameValidationError,
    InvalidColorError,
    InvalidComponentError,
    InvalidEmbedError,
)
from .markdown import _Markdown
from .ui import Option

md = _Markdown()
"""Markdown helpers and composition — see :mod:`frame.markdown`.

Callable directly to compose fragments (``frame.md(a, b, c)``), and exposes
formatting helpers as attributes (``frame.md.bold(...)``).
"""

__all__ = [
    "__version__",
    "embed",
    "Embed",
    "Theme",
    "set_theme",
    "get_theme",
    "colors",
    "Color",
    "attachment",
    "Image",
    "md",
    "ui",
    "Option",
    "FrameError",
    "FrameValidationError",
    "InvalidEmbedError",
    "InvalidColorError",
    "InvalidComponentError",
    "AttachmentError",
]
