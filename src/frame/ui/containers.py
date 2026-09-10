"""Layout components: ``section``, ``action_row``, and ``container``.

These are the components that enforce Discord's placement rules:

* A **button** or **select menu** can never sit directly inside a
  container — it must be inside an :func:`action_row`, or be a
  :func:`section`'s ``accessory``.
* An **action row** holds either up to 5 buttons, or exactly 1 select
  menu — never a mix.
* A **section** holds 1-3 text components plus one accessory (a button
  or a thumbnail).
* A **container** is the outermost layout wrapper Discord allows nesting
  everything else inside.

Frame validates every rule above *before* touching the network, with an
error message that names the exact rule broken.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..colors import Color, ColorInput
from ..exceptions import InvalidComponentError
from .base import Component
from .buttons import Button
from .components import FileDisplay, MediaGallery, Separator, Text, Thumbnail
from .selects import Select

if TYPE_CHECKING:
    import discord

MAX_ACTION_ROW_BUTTONS = 5
MAX_SECTION_TEXT_CHILDREN = 3
MAX_CONTAINER_CHILDREN = 40


class ActionRow(Component):
    kind = "action_row"

    def __init__(self, *children: Component) -> None:
        self.children = list(children)

    def validate(self) -> None:
        if not self.children:
            raise InvalidComponentError("ActionRow needs at least one button or select menu")

        selects = [c for c in self.children if isinstance(c, Select)]
        buttons = [c for c in self.children if isinstance(c, Button)]
        others = [c for c in self.children if not isinstance(c, (Select, Button))]

        if others:
            raise InvalidComponentError(
                f"ActionRow can only contain buttons or select menus, got a "
                f"{others[0].kind} component. Move it into the container directly, "
                "or into a section's accessory."
            )
        if selects and buttons:
            raise InvalidComponentError(
                "ActionRow cannot mix a select menu with buttons — Discord requires "
                "a select menu to be the row's only component. Put the buttons in "
                "their own action_row(...)."
            )
        if len(selects) > 1:
            raise InvalidComponentError(
                "ActionRow can only contain one select menu",
                current=len(selects),
                maximum=1,
            )
        if len(buttons) > MAX_ACTION_ROW_BUTTONS:
            raise InvalidComponentError(
                "ActionRow has too many buttons",
                current=len(buttons),
                maximum=MAX_ACTION_ROW_BUTTONS,
            )
        for child in self.children:
            child.validate()

    def to_discord(self) -> discord.ui.ActionRow:
        import discord

        return discord.ui.ActionRow(*(c.to_discord() for c in self.children))

    def local_images(self):
        return []


class Section(Component):
    kind = "section"

    def __init__(self, *children: Component | str, accessory: Component) -> None:
        self.children = [Text(c) if isinstance(c, str) else c for c in children]
        self.accessory = accessory

    def validate(self) -> None:
        if not self.children:
            raise InvalidComponentError("Section needs at least one text component")
        if len(self.children) > MAX_SECTION_TEXT_CHILDREN:
            raise InvalidComponentError(
                "Section has too many text components",
                current=len(self.children),
                maximum=MAX_SECTION_TEXT_CHILDREN,
            )
        for child in self.children:
            if not isinstance(child, Text):
                raise InvalidComponentError(
                    f"Section children must be text, got a {child.kind} component. "
                    "Non-text content belongs in the section's accessory=..."
                )
            child.validate()
        if not isinstance(self.accessory, (Button, Thumbnail)):
            raise InvalidComponentError(
                f"Section accessory must be a button or a thumbnail, got a "
                f"{getattr(self.accessory, 'kind', type(self.accessory).__name__)} component."
            )
        self.accessory.validate()

    def to_discord(self) -> discord.ui.Section:
        import discord

        return discord.ui.Section(
            *(c.to_discord() for c in self.children),
            accessory=self.accessory.to_discord(),
        )

    def local_images(self):
        return self.accessory.local_images() if isinstance(self.accessory, Thumbnail) else []


_ALLOWED_CONTAINER_CHILDREN = (Text, Separator, Section, ActionRow, MediaGallery, FileDisplay)


class Container(Component):
    kind = "container"

    def __init__(
        self,
        *children: Component,
        accent_color: ColorInput | None = None,
        spoiler: bool = False,
    ) -> None:
        self.children = list(children)
        self.accent_color = Color(accent_color) if accent_color is not None else None
        self.spoiler = spoiler

    def validate(self) -> None:
        if not self.children:
            raise InvalidComponentError("Container needs at least one component")
        if len(self.children) > MAX_CONTAINER_CHILDREN:
            raise InvalidComponentError(
                "Container has too many top-level components",
                current=len(self.children),
                maximum=MAX_CONTAINER_CHILDREN,
            )
        for child in self.children:
            if isinstance(child, (Button, Select)):
                raise InvalidComponentError(
                    f"A bare {child.kind} can't be placed directly in a container — "
                    f"Discord requires it to be inside frame.ui.action_row(...), or "
                    f"used as a frame.ui.section(...) accessory."
                )
            if not isinstance(child, _ALLOWED_CONTAINER_CHILDREN):
                child_kind = getattr(child, "kind", type(child).__name__)
                raise InvalidComponentError(
                    f"Container cannot directly hold a {child_kind} component."
                )
            child.validate()

    def to_discord(self) -> discord.ui.Container:
        import discord

        return discord.ui.Container(
            *(c.to_discord() for c in self.children),
            accent_color=self.accent_color.to_discord() if self.accent_color else None,
            spoiler=self.spoiler,
        )

    def local_images(self):
        images = []
        for child in self.children:
            get = getattr(child, "local_images", None)
            if get is not None:
                images.extend(get())
        return images
