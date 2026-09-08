from __future__ import annotations

from typing import Any, Awaitable, Callable, Iterable

from frame.colors import normalize
from frame.exceptions import CompatibilityError, FrameValidationError, InvalidComponentError
from frame.options import Option

Callback = Callable[[Any], Awaitable[Any]]


def _ui():
    import discord

    if not hasattr(discord.ui, "LayoutView"):
        raise CompatibilityError("Frame Components V2 requires discord.py 2.6 or newer (discord.ui.LayoutView).")
    return discord.ui


def _button_style(style: str | int | None):
    ui = _ui()
    if style is None:
        return ui.ButtonStyle.secondary
    if isinstance(style, int):
        return ui.ButtonStyle(style)
    key = style.lower().replace("-", "_")
    mapping = {"primary": ui.ButtonStyle.primary, "secondary": ui.ButtonStyle.secondary, "success": ui.ButtonStyle.success, "danger": ui.ButtonStyle.danger, "link": ui.ButtonStyle.link}
    try:
        return mapping[key]
    except KeyError as exc:
        raise InvalidComponentError(f"Unknown button style {style!r}; use primary, secondary, success, danger, or link.") from exc


class _CallbackMixin:
    _frame_callback: Callback | None = None

    def on_click(self, function: Callback):
        """Register an async interaction callback with decorator syntax."""
        self._frame_callback = function
        return self


class FrameButton(_CallbackMixin, _ui().Button):
    """A native discord.py Button with a small decorator convenience."""

    def __init__(self, label: str | None = None, *, style: str | int | None = None, custom_id: str | None = None, url: str | None = None, emoji: Any = None, disabled: bool = False, row: int | None = None):
        if url is not None and custom_id is not None:
            raise InvalidComponentError("Link buttons cannot specify custom_id; Discord uses the URL as the target.")
        chosen = _button_style(style)
        if url is not None:
            chosen = _button_style("link")
        elif chosen == _button_style("link"):
            raise InvalidComponentError("A link button requires url=.")
        if label is not None and len(label) > 80:
            raise FrameValidationError(f"Button label exceeds Discord's 80 character limit; current: {len(label)}.")
        super().__init__(style=chosen, label=label, custom_id=custom_id, url=url, emoji=emoji, disabled=disabled, row=row)

    async def callback(self, interaction: Any) -> None:
        if self._frame_callback is not None:
            await self._frame_callback(interaction)
        else:
            await super().callback(interaction)


class FrameSelect(_CallbackMixin, _ui().Select):
    """Native string select with the same callback convenience as FrameButton."""

    async def callback(self, interaction: Any) -> None:
        if self._frame_callback is not None:
            await self._frame_callback(interaction)
        else:
            await super().callback(interaction)


class FrameView(_ui().LayoutView):
    """Native LayoutView with deterministic JSON/debug helpers."""

    def __init__(self, *items: Any, timeout: float | None = 180) -> None:
        super().__init__(timeout=timeout)
        for item in items:
            self.add_item(item)
        self._validate_tree()

    def _validate_tree(self) -> None:
        if len(self.walk_children()) > 40:
            raise InvalidComponentError("Components V2 messages may contain at most 40 total components.")
        if self.content_length() > 4000:
            raise FrameValidationError("Components V2 text exceeds Discord's 4000 character display limit.")

    def to_dict(self) -> dict[str, Any]:
        return {"components": self.to_components(), "is_components_v2": True}

    def to_discord(self) -> "FrameView":
        return self


def button(label: str | None = None, *, style: str | int | None = None, custom_id: str | None = None, url: str | None = None, emoji: Any = None, disabled: bool = False, row: int | None = None) -> FrameButton:
    return FrameButton(label, style=style, custom_id=custom_id, url=url, emoji=emoji, disabled=disabled, row=row)


def text(content: Any):
    ui = _ui()
    value = str(content)
    if len(value) > 4000:
        raise FrameValidationError(f"Text display exceeds Discord's 4000 character limit; current: {len(value)}.")
    return ui.TextDisplay(value)


def separator(*, visible: bool = True, spacing: str | int | None = None):
    ui = _ui()
    if spacing is None:
        return ui.Separator(visible=visible)
    mapping = {"small": getattr(ui.SeparatorSpacing, "small", 1), "large": getattr(ui.SeparatorSpacing, "large", 2)}
    if isinstance(spacing, str) and spacing not in mapping:
        raise InvalidComponentError("Separator spacing must be 'small' or 'large'.")
    return ui.Separator(visible=visible, spacing=mapping[spacing] if isinstance(spacing, str) else spacing)


def section(*children: Any, accessory: Any):
    ui = _ui()
    if not children:
        raise InvalidComponentError("A section requires at least one text display child.")
    if len(children) > 3:
        raise InvalidComponentError("A Discord section can contain at most 3 text display items.")
    if not all(isinstance(child, ui.TextDisplay) for child in children):
        raise InvalidComponentError("Section children must be TextDisplay components.")
    if not isinstance(accessory, (ui.Thumbnail, ui.Button)):
        raise InvalidComponentError("Section accessories must be a thumbnail or button.")
    return ui.Section(*children, accessory=accessory)


def thumbnail(media: Any, *, spoiler: bool = False):
    return _ui().Thumbnail(media, spoiler=spoiler)


def media_item(media: Any, *, description: str | None = None, spoiler: bool = False):
    return _ui().MediaGalleryItem(media, description=description, spoiler=spoiler)


def media_gallery(*items: Any):
    ui = _ui()
    normalized = [item if isinstance(item, ui.MediaGalleryItem) else media_item(item) for item in items]
    if len(normalized) > 10:
        raise InvalidComponentError("A media gallery may contain at most 10 items.")
    return ui.MediaGallery(*normalized)


def action_row(*items: Any):
    ui = _ui()
    if len(items) == 1 and hasattr(ui, "BaseSelect") and isinstance(items[0], ui.BaseSelect):
        return ui.ActionRow(*items)
    if len(items) == 1 and isinstance(items[0], ui.Select):
        return ui.ActionRow(*items)
    if len(items) > 5:
        raise InvalidComponentError("An action row may contain at most 5 buttons.")
    if not all(isinstance(item, ui.Button) for item in items):
        raise InvalidComponentError("Action rows accept buttons or a single select menu.")
    return ui.ActionRow(*items)


def container(*children: Any, accent_color: Any = None, spoiler: bool = False, timeout: float | None = 180) -> FrameView:
    ui = _ui()
    color = normalize(accent_color)
    root = ui.Container(*children, accent_color=int(color) if color else None, spoiler=spoiler)
    return FrameView(root, timeout=timeout)


def file(media: Any, *, spoiler: bool = False):
    return _ui().File(media, spoiler=spoiler)


def select(options: Iterable[Any], *, placeholder: str | None = None, custom_id: str | None = None, min_values: int = 1, max_values: int = 1, disabled: bool = False) -> FrameSelect:
    ui = _ui()
    normalized = [option.to_discord() if isinstance(option, Option) else option for option in options]
    return FrameSelect(options=normalized, placeholder=placeholder, custom_id=custom_id, min_values=min_values, max_values=max_values, disabled=disabled)
