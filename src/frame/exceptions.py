"""Frame's exception hierarchy.

Every exception Frame raises inherits from :class:`FrameError`, so callers
who don't care about the specific failure can catch broadly:

    try:
        embed = frame.embed(title="x" * 500)
    except frame.FrameError as exc:
        ...

Validation failures use :class:`FrameValidationError` subclasses and always
explain *what* was wrong, *what value* triggered it, and *what the limit
is* — the goal is that the exception message alone is enough to fix the
bug without opening Discord's developer docs.
"""

from __future__ import annotations


class FrameError(Exception):
    """Base class for every exception Frame raises."""


class FrameValidationError(FrameError):
    """Raised when content would violate a Discord API limit or rule.

    Subclasses format a message of the shape::

        <What>: <why it's invalid>
        Current: <value>
        Maximum: <limit>
    """

    def __init__(
        self,
        message: str,
        *,
        current: object = None,
        maximum: object = None,
    ) -> None:
        parts = [message]
        if current is not None:
            parts.append(f"Current: {current}")
        if maximum is not None:
            parts.append(f"Maximum: {maximum}")
        super().__init__("\n".join(parts))
        self.current = current
        self.maximum = maximum


class InvalidEmbedError(FrameValidationError):
    """An embed (or one of its fields) violates a Discord limit."""


class InvalidColorError(FrameError):
    """A color value could not be understood.

    Raised for malformed hex strings, out-of-range integers/RGB tuples,
    or unknown named colors — the message always lists what was tried
    and, for named colors, suggests close matches.
    """


class InvalidComponentError(FrameValidationError):
    """A Components V2 tree violates Discord's nesting/placement rules.

    Examples: a bare interactive component outside an ActionRow/Section
    accessory, too many children in a container, or mixing Components V2
    with legacy ``content``/``embeds``.
    """


class AttachmentError(FrameError):
    """A local file or attachment reference could not be resolved."""
