import discord
import frame


def ticket_view() -> frame.ui.FrameView:
    create = frame.ui.button("Create ticket", custom_id="ticket:create", style="success")

    @create.on_click
    async def create_ticket(interaction: discord.Interaction):
        await interaction.response.send_message("Ticket creation started.", ephemeral=True)

    return frame.ui.container(
        frame.ui.text("# Support"),
        frame.ui.text("Need help? Open a private support ticket."),
        frame.ui.action_row(create),
    )
