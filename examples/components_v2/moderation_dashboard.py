"""Moderation dashboard built entirely with Components V2."""

import discord
import frame


async def show_dashboard(interaction: discord.Interaction, *, warnings: int, mutes: int) -> None:
    view = frame.ui.container(
        frame.ui.text("## Moderation Dashboard"),
        frame.ui.separator(),
        frame.ui.section(
            "Active warnings",
            frame.md.bold(str(warnings)),
            accessory=frame.ui.button("View Warnings", custom_id="view_warnings"),
        ),
        frame.ui.section(
            "Active mutes",
            frame.md.bold(str(mutes)),
            accessory=frame.ui.button("View Mutes", custom_id="view_mutes"),
        ),
        frame.ui.separator(spacing="large"),
        frame.ui.action_row(
            frame.ui.button("Refresh", style="secondary", custom_id="refresh"),
            frame.ui.button("Close", style="danger", custom_id="close"),
        ),
        accent_color="blurple",
    )
    await interaction.response.send_message(view=view, ephemeral=True)
