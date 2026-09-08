import frame


def test_theme_applies_defaults_when_available():
    import pytest
    pytest.importorskip("discord")
    theme = frame.Theme(color="blurple", footer="My Bot")
    frame.set_theme(theme)
    embed = frame.embed("Hello", "World")
    data = embed.to_dict()
    assert data["color"] == 0x5865F2
    assert data["footer"]["text"] == "My Bot"
    frame.set_theme(None)
