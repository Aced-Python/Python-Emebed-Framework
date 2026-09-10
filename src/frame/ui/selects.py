"""Select menus.

    frame.ui.select(
        options=[
            frame.Option("Python", "python"),
            frame.Option("JavaScript", "javascript"),
        ],
        placeholder="Pick a language",
        on_select=handle_pick,
    )
"""

from __future__ import annotations

import uuid
from collections.abc import Callable, Coroutine, Sequence
from typing import TYPE_CHECKING

from ..exceptions import InvalidComponentError
from .base import Component

if TYPE_CHECKING:
    import discord

MAX_OPTIONS = 25
SelectCallback = Callable[["discord.Interaction"], Coroutine]


class Option:
    """One choice in a :class:`Select`."""

    def __init__(
        self,
        label: str,
        value: str | None = None,
        *,
        description: str | None = None,
        emoji: str | None = None,
        default: bool = False,
    ) -> None:
        self.label = label
        self.value = value if value is not None else label
        self.description = description
        self.emoji = emoji
        self.default = default

    def to_discord(self) -> discord.SelectOption:
        import discord

        return discord.SelectOption(
            label=self.label,
            value=self.value,
            description=self.description,
            emoji=self.emoji,
            default=self.default,
        )


class Select(Component):
    kind = "select"
    interactive = True

    def __init__(
        self,
        options: Sequence[Option],
        *,
        placeholder: str | None = None,
        custom_id: str | None = None,
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False,
        on_select: SelectCallback | None = None,
    ) -> None:
        self.options = list(options)
        self.placeholder = placeholder
        self.custom_id = custom_id or f"frame:{uuid.uuid4().hex}"
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled
        self._select_callback = on_select

    def validate(self) -> None:
        if not self.options:
            raise InvalidComponentError("Select menu needs at least one option")
        if len(self.options) > MAX_OPTIONS:
            raise InvalidComponentError(
                "Select menu has too many options",
                current=len(self.options),
                maximum=MAX_OPTIONS,
            )
        if self.min_values > self.max_values:
            raise InvalidComponentError(
                f"min_values ({self.min_values}) cannot be greater than "
                f"max_values ({self.max_values})."
            )

    def on_select(self, func: SelectCallback) -> SelectCallback:
        """Decorator: ``@select.on_select`` registers the interaction callback."""
        self._select_callback = func
        return func

    def to_discord(self) -> discord.ui.Select:
        import discord

        item: discord.ui.Select = discord.ui.Select(
            custom_id=self.custom_id,
            placeholder=self.placeholder,
            min_values=self.min_values,
            max_values=self.max_values,
            options=[o.to_discord() for o in self.options],
            disabled=self.disabled,
        )
        callback = self._select_callback
        if callback is not None:
            async def _callback(interaction: discord.Interaction, _cb=callback) -> None:
                await _cb(interaction)

            item.callback = _callback  # type: ignore[method-assign]
        return item
