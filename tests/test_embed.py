import discord
import pytest

import frame


def test_simple_embed():
    e = frame.embed("Hello", "World")
    assert isinstance(e, discord.Embed)
    assert e.title == "Hello"
    assert e.description == "World"


def test_embed_with_color_and_fields():
    e = frame.embed(
        title="Server Info",
        color="blurple",
        fields=[("Members", "1,240", True), ("Channels", "42", True)],
        footer="Powered by Frame",
    )
    assert int(e.color) == 0x5865F2
    assert len(e.fields) == 2
    assert e.fields[0].name == "Members"
    assert e.fields[0].inline is True
    assert e.footer.text == "Powered by Frame"


def test_embed_field_tuple_and_dict_inputs():
    fields = [
        ("A", "1"),
        ("B", "2", True),
        {"name": "C", "value": "3", "inline": True},
    ]
    e = frame.embed("T", fields=fields)
    assert [f.name for f in e.fields] == ["A", "B", "C"]
    assert e.fields[0].inline is False
    assert e.fields[1].inline is True


def test_builder_chains_and_matches_functional():
    built = (
        frame.Embed()
        .title("Welcome")
        .description("Hi")
        .color("#5865F2")
        .field("Members", "100", inline=True)
        .footer("Powered by Frame")
        .to_discord()
    )
    assert built.title == "Welcome"
    assert int(built.color) == 0x5865F2
    assert built.fields[0].name == "Members"


def test_title_length_validation():
    with pytest.raises(frame.InvalidEmbedError) as exc:
        frame.embed(title="x" * 300)
    assert "256" in str(exc.value)
    assert "300" in str(exc.value)


def test_description_length_validation():
    with pytest.raises(frame.InvalidEmbedError):
        frame.embed(description="x" * 5000)


def test_too_many_fields():
    fields = [(f"n{i}", "v") for i in range(26)]
    with pytest.raises(frame.InvalidEmbedError) as exc:
        frame.embed("T", fields=fields)
    assert "25" in str(exc.value)


def test_field_value_length_validation():
    with pytest.raises(frame.InvalidEmbedError):
        frame.embed("T", fields=[("name", "v" * 2000)])


def test_total_length_validation():
    with pytest.raises(frame.InvalidEmbedError):
        frame.embed(description="x" * 4096, fields=[("n", "v" * 1024)] * 3)


def test_to_dict_matches_discord_shape():
    e = frame.Embed().title("Hi").description("There").color("red")
    data = e.to_dict()
    assert data["title"] == "Hi"
    assert data["description"] == "There"
    assert data["color"] == 0xED4245


def test_theme_fills_unset_fields_only():
    theme = frame.Theme(color="blurple", footer="My Bot")
    e = frame.Embed().title("Hi").footer("Custom footer").apply_theme(theme).to_discord()
    assert int(e.color) == 0x5865F2  # filled from theme
    assert e.footer.text == "Custom footer"  # explicit value wins


def test_global_theme_applies_via_embed_kwarg():
    theme = frame.Theme(color="green")
    e = frame.embed("Hi", theme=theme)
    assert int(e.color) == 0x57F287


def test_embed_integrates_with_discord_send_signature():
    e = frame.embed("Hi", "there")
    # discord.py's abc.Messageable.send(embed=...) just needs a discord.Embed.
    assert isinstance(e, discord.Embed)
