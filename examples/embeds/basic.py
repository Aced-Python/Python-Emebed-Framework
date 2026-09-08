import discord
import frame


class Bot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")


async def send_profile(channel: discord.abc.Messageable, user: discord.User) -> None:
    embed = frame.embed(
        "Profile",
        f"## {user.display_name}\nSoftware developer",
        color=frame.colors.blurple,
        thumbnail=user.display_avatar.url,
        fields=[
            ("Members", "1,240", True),
            ("Channels", "42", True),
        ],
        footer="Powered by Frame",
    )
    await channel.send(embed=embed)
