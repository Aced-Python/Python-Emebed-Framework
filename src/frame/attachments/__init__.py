"""Attachment and image handling.

Discord embeds can only reference images by URL — including a special
``attachment://filename`` URL that points at a file uploaded alongside the
message. Frame's :class:`Image` models both cases and knows how to
produce the real ``discord.File`` a local image needs, and the URL an
embed should point at, without you having to remember the
``attachment://`` convention yourself.

    frame.embed("Welcome", image=frame.attachment("./assets/banner.png"))
    frame.embed("Welcome", image="https://example.com/banner.png")

Both forms work anywhere Frame accepts an image/thumbnail — pass a plain
URL string, or a :class:`Image` for local files.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Union

from ..exceptions import AttachmentError

if TYPE_CHECKING:
    import discord

ImageInput = Union[str, "Image", None]


class Image:
    """A reference to an image: either a remote URL or a local file.

    Local files are only resolvable once actually attached to a message —
    use :meth:`Image.file` (or the ``frame.attachment(...)`` shortcut) and
    Frame will wire up the ``attachment://`` URL and the ``discord.File``
    together automatically when you send the embed.
    """

    __slots__ = ("_url", "_path", "_filename")

    def __init__(self, *, url: str | None = None, path: str | None = None) -> None:
        if bool(url) == bool(path):
            raise AttachmentError(
                "Image must be constructed with exactly one of `url=` or `path=`."
            )
        self._url = url
        self._path = path
        self._filename = os.path.basename(path) if path else None

    @classmethod
    def url(cls, url: str) -> Image:
        """An image hosted at a remote URL."""
        return cls(url=url)

    @classmethod
    def file(cls, path: str) -> Image:
        """A local image file to be uploaded alongside the message.

        Raises :class:`AttachmentError` immediately if the file doesn't
        exist, so mistakes surface at embed-construction time rather than
        when Discord rejects the request.
        """
        if not os.path.isfile(path):
            raise AttachmentError(
                f"Local image not found: {path!r}. Check the path is correct "
                "and relative to your working directory."
            )
        return cls(path=path)

    @property
    def is_local(self) -> bool:
        return self._path is not None

    @property
    def filename(self) -> str | None:
        return self._filename

    @property
    def as_url(self) -> str:
        """The URL this image resolves to inside an embed."""
        if self._url is not None:
            return self._url
        return f"attachment://{self._filename}"

    def to_discord_file(self) -> discord.File:
        """Build the real ``discord.File`` this image needs to be sent."""
        import discord

        if self._path is None:
            raise AttachmentError(
                "to_discord_file() only applies to local images created "
                "with Image.file(...)."
            )
        return discord.File(self._path, filename=self._filename)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        if self.is_local:
            return f"Image.file({self._path!r})"
        return f"Image.url({self._url!r})"


def attachment(path: str) -> Image:
    """Shortcut for :meth:`Image.file`."""
    return Image.file(path)


def coerce_image(value: ImageInput) -> Image | None:
    """Normalize a plain URL string or an ``Image`` into an ``Image`` (or ``None``)."""
    if value is None:
        return None
    if isinstance(value, Image):
        return value
    if isinstance(value, str):
        return Image.url(value)
    raise AttachmentError(
        f"Expected a URL string or a frame.Image, got {value!r} ({type(value).__name__})."
    )


__all__ = ["Image", "attachment", "ImageInput", "coerce_image"]
