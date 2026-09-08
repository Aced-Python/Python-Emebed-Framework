class FrameError(Exception):
    """Base exception for Frame."""


class FrameValidationError(FrameError, ValueError):
    """Raised when a Frame object violates a Discord or Frame constraint."""


class InvalidComponentError(FrameValidationError):
    """Raised when Components V2 composition rules are violated."""


class InvalidEmbedError(FrameValidationError):
    """Raised when an embed cannot be represented by Discord."""


class InvalidColorError(FrameValidationError):
    """Raised when a color value cannot be normalized."""


class AttachmentError(FrameError, ValueError):
    """Raised for invalid or ambiguous attachment configuration."""


class CompatibilityError(FrameError, RuntimeError):
    """Raised when the installed discord.py version lacks a required API."""
