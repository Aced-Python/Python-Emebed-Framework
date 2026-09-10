"""Ticket panel: buttons + interaction callbacks, no Components V2 needed."""

import discord
import frame


async def open_ticket(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(
        f"Ticket opened for {interaction.user.mention}. A team member will be with you shortly.",
        ephemeral=True,
    )


def build_ticket_embed() -> discord.Embed:
    return frame.embed(
        "Need help?",
        "Click the button below to open a support ticket.",
        color="blurple",
    )


def build_ticket_view() -> discord.ui.View:
    import discord

    button = frame.ui.button("Open Ticket", style="primary", custom_id="open_ticket")

    @button.on_click
    async def _clicked(interaction: discord.Interaction) -> None:
        await open_ticket(interaction)

    view = discord.ui.View(timeout=None)
    view.add_item(button.to_discord())
    return view
