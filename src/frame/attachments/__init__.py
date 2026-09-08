from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import IO, Union, Any

from frame.exceptions import AttachmentError

PathLike = Union[str, Path]


@dataclass(frozen=True, slots=True)
class Attachment:
    """A local file that Frame can turn into a discord.File at send time."""

    source: PathLike | IO[bytes]
    filename: str | None = None
    description: str | None = None
    spoiler: bool = False

    def to_discord(self):
        import discord

        if isinstance(self.source, (str, Path)):
            path = Path(self.source)
            if not path.is_file():
                raise AttachmentError(f"Attachment file does not exist: {path}")
            return discord.File(path, filename=self.filename, description=self.description, spoiler=self.spoiler)
        if self.filename is None:
            raise AttachmentError("File-like attachments require filename= so Discord can reference them.")
        return discord.File(self.source, filename=self.filename, description=self.description, spoiler=self.spoiler)

    @property
    def attachment_url(self) -> str:
        if not self.filename:
            raise AttachmentError("An explicit filename is required to construct an attachment:// URL.")
        return f"attachment://{self.filename}"


def attachment(source: PathLike | IO[bytes], *, filename: str | None = None, description: str | None = None, spoiler: bool = False) -> Attachment:
    """Describe a local upload without opening it until ``to_discord()`` is called."""
    return Attachment(source, filename=filename, description=description, spoiler=spoiler)


def to_discord_files(value: Any) -> list[Any]:
    """Extract Frame-managed local uploads from a native embed/view."""
    attachments = getattr(value, "_frame_attachments", ())
    return [item.to_discord() for item in attachments]


class Image:
    @staticmethod
    def file(source: PathLike | IO[bytes], *, filename: str | None = None, description: str | None = None, spoiler: bool = False) -> Attachment:
        return attachment(source, filename=filename, description=description, spoiler=spoiler)


__all__ = ["Attachment", "attachment", "to_discord_files", "Image"]
