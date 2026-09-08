import pytest

import frame
from frame.exceptions import FrameValidationError


def discord_or_skip():
    return pytest.importorskip("discord")


def test_simple_embed_is_native_discord_embed():
    discord = discord_or_skip()
    embed = frame.embed("Hello", "World", color="blurple")
    assert isinstance(embed, discord.Embed)
    assert embed.to_dict()["title"] == "Hello"
    assert embed.to_dict()["description"] == "World"


def test_fields_and_builder():
    discord_or_skip()
    embed = frame.Embed("Profile", "Bio").field("Level", 20, inline=True).footer("Frame").build()
    data = embed.to_dict()
    assert data["fields"][0] == {"inline": True, "name": "Level", "value": "20"}
    assert data["footer"]["text"] == "Frame"
    assert embed.to_discord() is embed


def test_description_limit():
    with pytest.raises(FrameValidationError, match="4096"):
        frame.embed("Bad", "x" * 4097)
