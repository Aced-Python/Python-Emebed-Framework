"""Server dashboard: themed embeds + a Components V2 confirmation flow together."""

import discord
import frame

BRAND_THEME = frame.Theme(
    color="#5865F2",
    footer="Powered by Frame",
)


async def handle_reset_confirmed(interaction: discord.Interaction) -> None:
    embed = frame.embed("Server settings reset", "All settings were restored to defaults.", theme=BRAND_THEME)
    await interaction.response.edit_message(embed=embed, view=None)


async def show_reset_confirmation(interaction: discord.Interaction) -> None:
    view = frame.ui.confirm(
        "Reset all server settings to their defaults? This can't be undone.",
        on_confirm=handle_reset_confirmed,
        confirm_label="Reset",
    )
    await interaction.response.send_message(view=view, ephemeral=True)


def build_dashboard_embed(guild: discord.Guild) -> discord.Embed:
    frame.set_theme(BRAND_THEME)
    return frame.embed(
        title=f"{guild.name} — Server Dashboard",
        fields=[
            ("Members", str(guild.member_count), True),
            ("Channels", str(len(guild.channels)), True),
            ("Roles", str(len(guild.roles)), True),
        ],
    )
