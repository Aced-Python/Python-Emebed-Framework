"""Buttons.

    frame.ui.button("Click me", style="primary", custom_id="hello")
    frame.ui.button("Docs", url="https://example.com")

Callback-based interaction is supported directly:

    btn = frame.ui.button("Click me", custom_id="hello")

    @btn.on_click
    async def clicked(interaction):
        await interaction.response.send_message("Clicked!")

or pass the callback up front with ``on_click=``.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING

from ..exceptions import InvalidComponentError
from .base import Component

if TYPE_CHECKING:
    import discord

LABEL_LIMIT = 80

_STYLE_ALIASES = {
    "primary": "primary",
    "blurple": "primary",
    "secondary": "secondary",
    "grey": "secondary",
    "gray": "secondary",
    "success": "success",
    "green": "success",
    "danger": "danger",
    "red": "danger",
    "link": "link",
    "url": "link",
}

ClickCallback = Callable[["discord.Interaction"], Coroutine]


class Button(Component):
    kind = "button"
    interactive = True

    def __init__(
        self,
        label: str | None = None,
        *,
        style: str | None = None,
        custom_id: str | None = None,
        url: str | None = None,
        emoji: str | None = None,
        disabled: bool = False,
        on_click: ClickCallback | None = None,
    ) -> None:
        self.label = label
        # None means "not explicitly chosen" — resolved lazily below, so an
        # explicit conflicting style (e.g. style="danger" with url=...) can
        # still be reported instead of being silently overridden.
        self.style = style
        self.custom_id = custom_id
        self.url = url
        self.emoji = emoji
        self.disabled = disabled
        self._click_callback: ClickCallback | None = on_click

        if self.url is None and self.custom_id is None:
            # Every non-link button needs a custom_id to be addressable.
            self.custom_id = f"frame:{uuid.uuid4().hex}"

    def _resolved_style(self) -> str:
        if self.style is not None:
            return self.style
        return "link" if self.url is not None else "secondary"

    def validate(self) -> None:
        if self.label is None and self.emoji is None:
            raise InvalidComponentError(
                "Button needs a label and/or an emoji — Discord won't render "
                "a button with neither."
            )
        if self.label is not None and len(self.label) > LABEL_LIMIT:
            raise InvalidComponentError(
                "Button label exceeds Discord's character limit",
                current=len(self.label),
                maximum=LABEL_LIMIT,
            )
        style = self._resolved_style()
        style_key = style.lower()
        if style_key not in _STYLE_ALIASES:
            raise InvalidComponentError(
                f"Invalid button style {style!r}. Expected one of: "
                f"{', '.join(sorted(set(_STYLE_ALIASES.values())))}."
            )
        resolved_style = _STYLE_ALIASES[style_key]
        if resolved_style == "link" and not self.url:
            raise InvalidComponentError(
                "A 'link' style button requires url=... (or just pass url=... "
                "and the style is inferred automatically)."
            )
        if resolved_style != "link" and self.url:
            raise InvalidComponentError(
                "Buttons with a url= are always link buttons and cannot use "
                f"style={style!r}. Drop the style, or drop the url."
            )
        if resolved_style != "link" and not self.custom_id:
            raise InvalidComponentError(
                "Non-link buttons require a custom_id (Frame generates one "
                "automatically unless you explicitly set custom_id=None)."
            )

    def on_click(self, func: ClickCallback) -> ClickCallback:
        """Decorator: ``@button.on_click`` registers the interaction callback."""
        self._click_callback = func
        return func

    def to_discord(self) -> discord.ui.Button:
        import discord

        style_map = {
            "primary": discord.ButtonStyle.primary,
            "secondary": discord.ButtonStyle.secondary,
            "success": discord.ButtonStyle.success,
            "danger": discord.ButtonStyle.danger,
            "link": discord.ButtonStyle.link,
        }
        resolved_style = _STYLE_ALIASES[self._resolved_style().lower()]
        item: discord.ui.Button = discord.ui.Button(
            style=style_map[resolved_style],
            label=self.label,
            custom_id=self.custom_id if resolved_style != "link" else None,
            url=self.url,
            emoji=self.emoji,
            disabled=self.disabled,
        )
        callback = self._click_callback
        if callback is not None:
            async def _callback(interaction: discord.Interaction, _cb=callback) -> None:
                await _cb(interaction)

            item.callback = _callback  # type: ignore[method-assign]
        return item

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "label": self.label,
            "style": self._resolved_style(),
            "custom_id": self.custom_id,
            "url": self.url,
            "disabled": self.disabled,
        }

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"Button(label={self.label!r}, style={self._resolved_style()!r})"
