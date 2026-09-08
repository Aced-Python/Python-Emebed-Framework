import discord
import frame

button = frame.ui.button("Click me", custom_id="hello", style="primary")


@button.on_click
async def clicked(interaction: discord.Interaction):
    await interaction.response.send_message("Hello from Frame!")


async def send(channel: discord.abc.Messageable):
    view = frame.ui.container(
        frame.ui.text("# Welcome"),
        frame.ui.action_row(button),
    )
    await channel.send(view=view)
