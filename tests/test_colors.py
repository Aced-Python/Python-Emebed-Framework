import pytest

import frame


def test_hex_string_with_and_without_hash():
    assert int(frame.Color("#5865F2")) == 0x5865F2
    assert int(frame.Color("5865F2")) == 0x5865F2


def test_int_and_rgb_tuple():
    assert int(frame.Color(0x5865F2)) == 0x5865F2
    assert int(frame.Color((88, 101, 242))) == 0x5865F2


def test_named_colors():
    assert int(frame.colors.blurple) == 0x5865F2
    assert int(frame.colors.red) == 0xED4245
    assert int(frame.Color("blurple")) == int(frame.colors.blurple)


def test_named_color_case_and_alias_insensitive():
    assert int(frame.Color("BLURPLE")) == int(frame.Color("blurple"))
    assert int(frame.colors.dark_gray) == int(frame.colors.dark_grey)
    assert int(frame.Color("dark-gray")) == int(frame.Color("dark_gray"))


def test_color_round_trip_rgb_hex():
    c = frame.Color("#5865F2")
    assert c.to_rgb() == (0x58, 0x65, 0xF2)
    assert c.to_hex() == "#5865F2"


def test_invalid_hex_raises():
    with pytest.raises(frame.InvalidColorError):
        frame.Color("#zzzzzz")


def test_invalid_name_raises_with_suggestion():
    with pytest.raises(frame.InvalidColorError) as exc:
        frame.Color("blurpl")
    assert "blurple" in str(exc.value)


def test_out_of_range_int_raises():
    with pytest.raises(frame.InvalidColorError):
        frame.Color(0x1FFFFFF)


def test_invalid_rgb_component_raises():
    with pytest.raises(frame.InvalidColorError):
        frame.Color((300, 0, 0))


def test_unknown_attribute_on_palette_raises_attribute_error():
    with pytest.raises(AttributeError):
        _ = frame.colors.not_a_real_color


def test_to_discord_produces_real_colour():
    import discord

    c = frame.Color("blurple").to_discord()
    assert isinstance(c, discord.Colour)
    assert c.value == 0x5865F2
