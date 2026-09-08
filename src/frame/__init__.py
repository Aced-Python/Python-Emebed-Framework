"""Frame — build beautiful Discord messages and Components V2 UIs with less ceremony."""

from contextvars import ContextVar
from importlib import import_module
from typing import Any

from frame.attachments import Attachment, Image, attachment, to_discord_files
from frame.options import Option
from frame.colors import Color
from frame.embed import Author, Embed, EmbedBuilder, EmbedField, Footer, Theme
from frame.embed.builder import embed as _embed
from frame.exceptions import AttachmentError, CompatibilityError, FrameError, FrameValidationError, InvalidColorError, InvalidComponentError, InvalidEmbedError
from frame.markdown import Markdown
import frame.markdown as _markdown

__version__ = "0.1.0"
_theme: ContextVar[Theme | None] = ContextVar("frame_theme", default=None)


def set_theme(theme: Theme | None) -> None:
    """Set the default theme for the current async/context-local execution context."""
    _theme.set(theme)


def get_theme() -> Theme | None:
    return _theme.get()


def embed(*args: Any, theme: Theme | None = None, **kwargs: Any):
    """Create a native ``discord.Embed`` with Frame's ergonomic API."""
    return _embed(*args, theme=theme or _theme.get(), **kwargs)


class _MarkdownNamespace:
    Markdown = Markdown
    bold = staticmethod(_markdown.bold)
    italic = staticmethod(_markdown.italic)
    underline = staticmethod(_markdown.underline)
    strike = staticmethod(_markdown.strike)
    code = staticmethod(_markdown.code)
    codeblock = staticmethod(_markdown.codeblock)
    link = staticmethod(_markdown.link)
    heading = staticmethod(_markdown.heading)
    quote = staticmethod(_markdown.quote)
    mention = staticmethod(_markdown.mention)
    channel = staticmethod(_markdown.channel)
    role = staticmethod(_markdown.role)
    __call__ = staticmethod(_markdown.md)


md = _MarkdownNamespace()


def __getattr__(name: str):
    if name == "colors":
        return import_module("frame.colors")
    if name == "ui":
        return import_module("frame.ui")
    raise AttributeError(name)


__all__ = ["__version__", "embed", "Embed", "EmbedBuilder", "EmbedField", "Author", "Footer", "Theme", "Color", "colors", "md", "ui", "Option", "Attachment", "Image", "attachment", "to_discord_files", "set_theme", "get_theme", "FrameError", "FrameValidationError", "InvalidEmbedError", "InvalidColorError", "InvalidComponentError", "AttachmentError", "CompatibilityError"]
