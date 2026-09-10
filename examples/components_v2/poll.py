"""A simple poll using a select menu and Components V2."""

import discord
import frame


async def send_poll(interaction: discord.Interaction, question: str, choices: list[str]) -> None:
    async def on_vote(vote_interaction: discord.Interaction) -> None:
        picked = vote_interaction.data["values"][0]  # type: ignore[index]
        await vote_interaction.response.send_message(f"You voted for **{picked}**.", ephemeral=True)

    menu = frame.ui.select(
        [frame.Option(choice) for choice in choices],
        placeholder="Cast your vote",
        on_select=on_vote,
    )

    view = frame.ui.container(
        frame.ui.text(f"## {question}"),
        frame.ui.separator(),
        frame.ui.action_row(menu),
    )
    await interaction.response.send_message(view=view)
