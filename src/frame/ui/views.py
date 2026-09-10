"""Turning a Frame component tree into something you can actually send.

``frame.ui.container(...)`` is the entry point: it validates the whole
tree, converts every spec object to its real ``discord.ui`` counterpart,
and returns a ready-to-send ``discord.ui.LayoutView`` — so the exact
pattern from the README works as written:

    view = frame.ui.container(
        frame.ui.text("## Welcome"),
        frame.ui.separator(),
        frame.ui.section(
            "Need help?",
            accessory=frame.ui.button("Open Support", style="primary", custom_id="support"),
        ),
    )
    await interaction.response.send_message(view=view)

The returned object is a genuine ``discord.ui.LayoutView`` subclass
instance — ``isinstance(view, discord.ui.LayoutView)`` is ``True`` — so it
composes with the rest of discord.py normally (persistent views,
``bot.add_view(view)``, etc.).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .containers import Container

if TYPE_CHECKING:
    import discord


class LayoutView:
    """Marker/typing alias — the objects Frame returns from :func:`container`
    are real ``discord.ui.LayoutView`` instances built dynamically; this
    class exists only so ``frame.ui.LayoutView`` is a valid type-hint target
    without importing discord.py eagerly.
    """


def build_view(container: Container, *, timeout: float = 180.0) -> discord.ui.LayoutView:
    """Validate ``container`` and wrap it in a sendable ``discord.ui.LayoutView``."""
    import discord

    container.validate()
    real_container = container.to_discord()

    class _FrameLayoutView(discord.ui.LayoutView):
        pass

    view = _FrameLayoutView(timeout=timeout)
    view.add_item(real_container)
    # Keep the Frame spec around for debugging/serialization (view.to_dict()).
    view._frame_container = container  # type: ignore[attr-defined]
    return view
