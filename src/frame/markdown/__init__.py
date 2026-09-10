"""Discord-compatible markdown helpers.

Frame doesn't implement a general-purpose Markdown engine — Discord's
Markdown dialect is small and fixed, so this module is a thin set of
string-formatting helpers plus a tiny composition function. The output is
always a plain ``str``; there's no separate AST to learn.

    frame.md.bold("hello")
    frame.md.link("Discord", "https://discord.com")
    frame.md(frame.md.heading("Welcome"), "Thanks for joining, ", frame.md.bold("friend"), "!")

Calling the module itself (``frame.md(...)``) joins its arguments into one
string — every helper below returns plain text, so composition is just
concatenation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    import discord

_Mentionable = Union[str, int, "discord.abc.Snowflake"]


def _snowflake_id(obj: _Mentionable) -> int:
    if isinstance(obj, int):
        return obj
    if isinstance(obj, str):
        return int(obj)
    obj_id = getattr(obj, "id", None)
    if obj_id is None:
        raise TypeError(
            f"Expected an int, a numeric str, or an object with an .id "
            f"attribute; got {obj!r}."
        )
    return int(obj_id)


def compose(*parts: str) -> str:
    """Join markdown fragments into one string. Also callable as ``frame.md(...)``."""
    return "".join(str(part) for part in parts)


def bold(text: str) -> str:
    return f"**{text}**"


def italic(text: str) -> str:
    return f"*{text}*"


def bold_italic(text: str) -> str:
    return f"***{text}***"


def underline(text: str) -> str:
    return f"__{text}__"


def strikethrough(text: str) -> str:
    return f"~~{text}~~"


def spoiler(text: str) -> str:
    return f"||{text}||"


def code(text: str) -> str:
    """Inline code span. Escapes stray backticks so the span can't break."""
    if "`" in text:
        return f"``{text}``"
    return f"`{text}`"


def codeblock(language: str, text: str = "") -> str:
    """A fenced code block. Call with just one argument for no language."""
    if not text:
        language, text = "", language
    return f"```{language}\n{text}\n```"


def heading(text: str, level: int = 1) -> str:
    """A markdown heading (Discord supports levels 1-3)."""
    if not 1 <= level <= 3:
        raise ValueError(f"Discord only supports heading levels 1-3, got {level}.")
    return f"{'#' * level} {text}"


def quote(text: str) -> str:
    """A single-line blockquote. For multi-line, pass the whole block."""
    return "\n".join(f"> {line}" for line in text.splitlines()) or "> "


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered_list(items: list[str]) -> str:
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, start=1))


def link(label: str, url: str) -> str:
    return f"[{label}]({url})"


def mention(user: _Mentionable) -> str:
    """A user mention, e.g. ``<@123456789012345678>``."""
    return f"<@{_snowflake_id(user)}>"


def channel(chan: _Mentionable) -> str:
    """A channel mention, e.g. ``<#123456789012345678>``."""
    return f"<#{_snowflake_id(chan)}>"


def role(role_obj: _Mentionable) -> str:
    """A role mention, e.g. ``<@&123456789012345678>``."""
    return f"<@&{_snowflake_id(role_obj)}>"


def timestamp(dt, style: str = "f") -> str:
    """A dynamic Discord timestamp from a ``datetime`` (renders in each viewer's timezone)."""
    epoch = int(dt.timestamp())
    return f"<t:{epoch}:{style}>"


class _Markdown:
    """Callable module facade: ``frame.md(...)`` composes, ``frame.md.bold(...)`` formats."""

    __call__ = staticmethod(compose)
    bold = staticmethod(bold)
    italic = staticmethod(italic)
    bold_italic = staticmethod(bold_italic)
    underline = staticmethod(underline)
    strikethrough = staticmethod(strikethrough)
    spoiler = staticmethod(spoiler)
    code = staticmethod(code)
    codeblock = staticmethod(codeblock)
    heading = staticmethod(heading)
    quote = staticmethod(quote)
    bullet_list = staticmethod(bullet_list)
    numbered_list = staticmethod(numbered_list)
    link = staticmethod(link)
    mention = staticmethod(mention)
    channel = staticmethod(channel)
    role = staticmethod(role)
    timestamp = staticmethod(timestamp)


__all__ = [
    "compose",
    "bold",
    "italic",
    "bold_italic",
    "underline",
    "strikethrough",
    "spoiler",
    "code",
    "codeblock",
    "heading",
    "quote",
    "bullet_list",
    "numbered_list",
    "link",
    "mention",
    "channel",
    "role",
    "timestamp",
]
