import discord
import frame


async def send_dashboard(interaction: discord.Interaction) -> None:
    view = frame.ui.container(
        frame.ui.text("# Server dashboard"),
        frame.ui.text("Choose an action to continue."),
        frame.ui.separator(),
        frame.ui.section(
            frame.ui.text("**Moderation**\nReview pending cases."),
            accessory=frame.ui.button("Open", custom_id="mod-open", style="primary"),
        ),
        frame.ui.action_row(
            frame.ui.button("Settings", custom_id="settings", style="secondary"),
            frame.ui.button("Docs", url="https://discordpy.readthedocs.io/"),
        ),
    )
    await interaction.response.send_message(view=view)
