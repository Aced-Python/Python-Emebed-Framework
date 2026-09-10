"""Welcome bot: a member-join embed with a thumbnail and fields.

Run inside any discord.py bot's on_member_join / slash command.
"""

import discord
import frame


async def send_welcome(channel: discord.abc.Messageable, member: discord.Member) -> None:
    embed = frame.embed(
        f"Welcome, {member.display_name}!",
        f"Glad to have you here, {member.mention}. Check out the rules channel to get started.",
        color="blurple",
        thumbnail=member.display_avatar.url,
        fields=[
            ("Account created", frame.md.timestamp(member.created_at, style="R"), True),
            ("Member #", str(member.guild.member_count), True),
        ],
        footer=f"Powered by Frame · {member.guild.name}",
    )
    await channel.send(embed=embed)
