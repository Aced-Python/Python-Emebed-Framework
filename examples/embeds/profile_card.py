"""A user profile card built with the fluent Embed builder."""

import discord
import frame


def build_profile_embed(member: discord.Member, *, level: int, xp: int) -> discord.Embed:
    return (
        frame.Embed()
        .title(f"{member.display_name}'s Profile")
        .description(frame.md(frame.md.bold(f"Level {level}"), f" · {xp:,} XP"))
        .color(frame.colors.blurple)
        .thumbnail(member.display_avatar.url)
        .field("Joined", frame.md.timestamp(member.joined_at, style="D"), inline=True)
        .field("Roles", str(len(member.roles) - 1), inline=True)
        .footer("Powered by Frame")
        .to_discord()
    )
