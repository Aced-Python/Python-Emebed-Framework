from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Option:
    """Small serializable description of a string-select option."""

    label: str
    value: str
    description: str | None = None
    emoji: Any = None
    default: bool = False

    def to_discord(self):
        import discord
        return discord.SelectOption(label=self.label, value=self.value, description=self.description, emoji=self.emoji, default=self.default)
