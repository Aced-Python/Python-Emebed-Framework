from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


def _escape(text: Any) -> str:
    return str(text)


def bold(text: Any) -> str:
    return f"**{_escape(text)}**"


def italic(text: Any) -> str:
    return f"*{_escape(text)}*"


def underline(text: Any) -> str:
    return f"__{_escape(text)}__"


def strike(text: Any) -> str:
    return f"~~{_escape(text)}~~"


def code(text: Any) -> str:
    return f"`{_escape(text)}`"


def codeblock(language: str, text: Any) -> str:
    return f"```{language}\n{_escape(text)}\n```"


def link(label: Any, url: str) -> str:
    return f"[{_escape(label)}]({url})"


def heading(text: Any, level: int = 2) -> str:
    if level not in (1, 2, 3):
        raise ValueError("Discord headings support levels 1, 2, and 3.")
    return f"{'#' * level} {_escape(text)}"


def quote(text: Any) -> str:
    return "\n".join(f"> {line}" for line in _escape(text).splitlines())


def mention(user: Any) -> str:
    return getattr(user, "mention", f"<@{getattr(user, 'id', user)}>")


def channel(channel: Any) -> str:
    return getattr(channel, "mention", f"<#{getattr(channel, 'id', channel)}>")


def role(role: Any) -> str:
    return getattr(role, "mention", f"<@&{getattr(role, 'id', role)}>")


@dataclass(frozen=True, slots=True)
class Markdown:
    """Small compositional markdown value; no parser and no non-Discord syntax."""

    parts: tuple[str, ...]

    def __str__(self) -> str:
        return "".join(self.parts)

    def __add__(self, other: Any) -> "Markdown":
        return Markdown(self.parts + (str(other),))

    def __radd__(self, other: Any) -> "Markdown":
        return Markdown((str(other),) + self.parts)


def md(*parts: Any) -> Markdown:
    """Compose Discord-compatible markdown fragments without parsing markdown."""
    return Markdown(tuple(str(part) for part in parts))


__all__ = ["Markdown", "md", "bold", "italic", "underline", "strike", "code", "codeblock", "link", "heading", "quote", "mention", "channel", "role"]
