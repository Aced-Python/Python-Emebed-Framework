"""Base machinery shared by every Frame Components V2 spec object.

Frame builds Components V2 trees in two stages:

1. Each helper (``frame.ui.text(...)``, ``frame.ui.button(...)``, etc.)
   returns a lightweight *spec* object — plain data, no discord.py
   dependency, cheap to construct and inspect.
2. ``frame.ui.container(...)`` walks the whole tree, validates Discord's
   placement/nesting rules, converts every spec to its real
   ``discord.ui`` counterpart, and wraps the result in a ready-to-send
   ``discord.ui.LayoutView``.

This keeps individual components testable in isolation (``.to_dict()``
works with no Discord connection) while the final output is always a
genuine discord.py object.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import discord


class Component:
    """Base class for every Frame UI spec object."""

    #: Human-readable name used in error messages, e.g. "button".
    kind: str = "component"

    #: True for components that must live inside an ActionRow or be used
    #: as a Section accessory (buttons, select menus).
    interactive: bool = False

    def validate(self) -> None:
        """Override to raise :class:`~frame.exceptions.InvalidComponentError`."""

    def to_discord(self) -> discord.ui.Item:
        raise NotImplementedError

    def to_dict(self) -> dict[str, Any]:
        """A JSON-ish summary for debugging/logging/tests. Not Discord's wire format."""
        return {"kind": self.kind}
