import discord
import frame

select = frame.ui.select(
    [
        frame.Option("Python", "python", "Python development"),
        frame.Option("JavaScript", "javascript", "JavaScript development"),
    ],
    placeholder="Choose a language",
    custom_id="language",
)


@select.on_click
async def language_selected(interaction: discord.Interaction):
    await interaction.response.send_message(f"Selected: {select.values[0]}", ephemeral=True)


async def send(interaction: discord.Interaction) -> None:
    view = frame.ui.container(
        frame.ui.text("# Preferences"),
        frame.ui.action_row(select),
    )
    await interaction.response.send_message(view=view)
