"""``frame.ui`` — Components V2 helpers.

    view = frame.ui.container(
        frame.ui.text("## Welcome"),
        frame.ui.separator(),
        frame.ui.action_row(
            frame.ui.button("Docs", url="https://example.com/docs"),
            frame.ui.button("Support", custom_id="support", style="primary"),
        ),
    )
    await interaction.response.send_message(view=view)

Every function below returns a lightweight, testable spec object; only
:func:`container` converts the whole tree into a real, sendable
``discord.ui.LayoutView``. See ``frame.ui.views`` for that machinery.
"""

from __future__ import annotations

from collections.abc import Sequence

from .buttons import Button, ClickCallback
from .components import FileDisplay, MediaGallery, Separator, Text, Thumbnail
from .containers import ActionRow, Container, Section
from .selects import Option, Select, SelectCallback
from .views import LayoutView, build_view

__all__ = [
    "text",
    "separator",
    "thumbnail",
    "media_gallery",
    "file",
    "button",
    "select",
    "section",
    "action_row",
    "container",
    "confirm",
    "Option",
    "LayoutView",
    # spec classes, exposed for typing/isinstance checks
    "Button",
    "Select",
    "Text",
    "Separator",
    "Thumbnail",
    "MediaGallery",
    "FileDisplay",
    "ActionRow",
    "Section",
    "Container",
]


def text(content: str) -> Text:
    """A Markdown text block."""
    return Text(content)


def separator(*, visible: bool = True, spacing: str = "small") -> Separator:
    """A divider between components. ``spacing`` is ``"small"`` or ``"large"``."""
    return Separator(visible=visible, spacing=spacing)


def thumbnail(media, *, description: str | None = None, spoiler: bool = False) -> Thumbnail:
    """A small accessory image, typically used as a :func:`section`'s accessory."""
    return Thumbnail(media, description=description, spoiler=spoiler)


def media_gallery(*items) -> MediaGallery:
    """A grid of up to 10 images. Each item is a URL/``Image``, or ``(image, description)``."""
    return MediaGallery(*items)


def file(media, *, spoiler: bool = False) -> FileDisplay:
    """An attached file shown inline. Requires a local attachment, not a bare URL."""
    return FileDisplay(media, spoiler=spoiler)


def button(
    label: str | None = None,
    *,
    style: str | None = None,
    custom_id: str | None = None,
    url: str | None = None,
    emoji: str | None = None,
    disabled: bool = False,
    on_click: ClickCallback | None = None,
) -> Button:
    """A button. Passing ``url=`` makes it a link button automatically."""
    return Button(
        label,
        style=style,
        custom_id=custom_id,
        url=url,
        emoji=emoji,
        disabled=disabled,
        on_click=on_click,
    )


def select(
    options: Sequence[Option],
    *,
    placeholder: str | None = None,
    custom_id: str | None = None,
    min_values: int = 1,
    max_values: int = 1,
    disabled: bool = False,
    on_select: SelectCallback | None = None,
) -> Select:
    """A select (dropdown) menu."""
    return Select(
        options,
        placeholder=placeholder,
        custom_id=custom_id,
        min_values=min_values,
        max_values=max_values,
        disabled=disabled,
        on_select=on_select,
    )


def section(*children: Text | str, accessory) -> Section:
    """1-3 lines of text with a button or thumbnail accessory beside them."""
    return Section(*children, accessory=accessory)


def action_row(*children) -> ActionRow:
    """A row of up to 5 buttons, or exactly one select menu."""
    return ActionRow(*children)


def container(*children, accent_color=None, spoiler: bool = False, timeout: float = 180.0):
    """Build a Components V2 message.

    This is the entry point: it validates the whole tree against
    Discord's placement rules and returns a ready-to-send
    ``discord.ui.LayoutView`` — pass it directly as ``view=...``.
    """
    spec = Container(*children, accent_color=accent_color, spoiler=spoiler)
    return build_view(spec, timeout=timeout)


def confirm(
    prompt: str,
    *,
    on_confirm: ClickCallback,
    on_cancel: ClickCallback | None = None,
    confirm_label: str = "Confirm",
    cancel_label: str = "Cancel",
):
    """A ready-made yes/no confirmation card.

        view = frame.ui.confirm(
            "Are you sure you want to delete this?",
            on_confirm=do_delete,
        )
        await interaction.response.send_message(view=view, ephemeral=True)
    """
    return container(
        text(prompt),
        action_row(
            button(confirm_label, style="danger", on_click=on_confirm),
            button(
                cancel_label,
                style="secondary",
                on_click=on_cancel or (lambda interaction: interaction.response.defer()),
            ),
        ),
    )
