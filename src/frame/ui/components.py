"""Non-interactive layout components: text, separator, thumbnail, media, file."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..attachments import Image, ImageInput, coerce_image
from ..exceptions import InvalidComponentError
from .base import Component

if TYPE_CHECKING:
    import discord

TEXT_DISPLAY_LIMIT = 4000


@dataclass
class Text(Component):
    """A Markdown text block (``discord.ui.TextDisplay``)."""

    content: str
    kind: str = "text"

    def validate(self) -> None:
        if not self.content:
            raise InvalidComponentError("TextDisplay content cannot be empty")
        if len(self.content) > TEXT_DISPLAY_LIMIT:
            raise InvalidComponentError(
                "Text component content exceeds Discord's character limit",
                current=len(self.content),
                maximum=TEXT_DISPLAY_LIMIT,
            )

    def to_discord(self) -> discord.ui.TextDisplay:
        import discord

        return discord.ui.TextDisplay(self.content)

    def to_dict(self) -> dict:
        return {"kind": self.kind, "content": self.content}


_VALID_SPACING = {"small", "large"}


@dataclass
class Separator(Component):
    """A divider/spacer (``discord.ui.Separator``)."""

    visible: bool = True
    spacing: str = "small"
    kind: str = "separator"

    def validate(self) -> None:
        if self.spacing not in _VALID_SPACING:
            raise InvalidComponentError(
                f"Invalid separator spacing {self.spacing!r}. "
                f"Expected one of: {', '.join(sorted(_VALID_SPACING))}."
            )

    def to_discord(self) -> discord.ui.Separator:
        import discord

        spacing = (
            discord.SeparatorSpacing.large
            if self.spacing == "large"
            else discord.SeparatorSpacing.small
        )
        return discord.ui.Separator(visible=self.visible, spacing=spacing)


@dataclass
class Thumbnail(Component):
    """A small accessory image, typically used as a Section's accessory."""

    media: ImageInput
    description: str | None = None
    spoiler: bool = False
    kind: str = "thumbnail"
    interactive: bool = False  # placement rules match Section-accessory items

    def validate(self) -> None:
        coerce_image(self.media)

    def to_discord(self) -> discord.ui.Thumbnail:
        import discord

        image = coerce_image(self.media)
        assert image is not None  # `media` is required, never None
        return discord.ui.Thumbnail(
            image.as_url, description=self.description, spoiler=self.spoiler
        )

    def local_images(self) -> list[Image]:
        image = coerce_image(self.media)
        return [image] if image and image.is_local else []


@dataclass
class MediaGallery(Component):
    """A grid of images (``discord.ui.MediaGallery``)."""

    items: tuple  # tuple[ImageInput | tuple[ImageInput, str | None]]
    kind: str = "media_gallery"

    def __init__(self, *items: ImageInput | tuple) -> None:
        if not items:
            raise InvalidComponentError("MediaGallery needs at least one image")
        if len(items) > 10:
            raise InvalidComponentError(
                "MediaGallery has too many images", current=len(items), maximum=10
            )
        self.items = items

    def validate(self) -> None:
        for item in self.items:
            image, _description = self._split(item)
            coerce_image(image)

    @staticmethod
    def _split(item) -> tuple[ImageInput, str | None]:
        if isinstance(item, tuple):
            return item[0], (item[1] if len(item) > 1 else None)
        return item, None

    def to_discord(self) -> discord.ui.MediaGallery:
        import discord

        gallery_items = []
        for item in self.items:
            image, description = self._split(item)
            resolved = coerce_image(image)
            assert resolved is not None  # each gallery item is a required image
            gallery_items.append(
                discord.MediaGalleryItem(resolved.as_url, description=description)
            )
        return discord.ui.MediaGallery(*gallery_items)

    def local_images(self) -> list[Image]:
        images = []
        for item in self.items:
            image, _ = self._split(item)
            resolved = coerce_image(image)
            if resolved and resolved.is_local:
                images.append(resolved)
        return images


@dataclass
class FileDisplay(Component):
    """An attached file shown inline (``discord.ui.File``). Requires a local file."""

    media: str | Image
    spoiler: bool = False
    kind: str = "file"

    def validate(self) -> None:
        image = self.media if isinstance(self.media, Image) else None
        if image is None and isinstance(self.media, str) and not self.media.startswith(
            "attachment://"
        ):
            raise InvalidComponentError(
                "File component requires a local attachment "
                "(frame.attachment(path) or an 'attachment://name' reference), "
                f"got a plain URL: {self.media!r}. Discord's File component only "
                "displays uploaded attachments, not arbitrary URLs."
            )

    def to_discord(self) -> discord.ui.File:
        import discord

        if isinstance(self.media, Image):
            ref = self.media.as_url
        else:
            ref = self.media
        return discord.ui.File(ref, spoiler=self.spoiler)

    def local_images(self) -> list[Image]:
        return [self.media] if isinstance(self.media, Image) and self.media.is_local else []
