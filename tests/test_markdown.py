import frame


def test_basic_formatting_helpers():
    assert frame.md.bold("hi") == "**hi**"
    assert frame.md.italic("hi") == "*hi*"
    assert frame.md.underline("hi") == "__hi__"
    assert frame.md.strikethrough("hi") == "~~hi~~"
    assert frame.md.spoiler("hi") == "||hi||"
    assert frame.md.code("print(1)") == "`print(1)`"


def test_code_with_backtick_uses_double_backtick_fence():
    assert frame.md.code("a`b") == "``a`b``"


def test_codeblock_with_and_without_language():
    assert frame.md.codeblock("python", "print(1)") == "```python\nprint(1)\n```"
    assert frame.md.codeblock("print(1)") == "```\nprint(1)\n```"


def test_heading_levels():
    assert frame.md.heading("Welcome") == "# Welcome"
    assert frame.md.heading("Welcome", level=2) == "## Welcome"
    assert frame.md.heading("Welcome", level=3) == "### Welcome"


def test_heading_invalid_level_raises():
    import pytest

    with pytest.raises(ValueError):
        frame.md.heading("x", level=4)


def test_link():
    assert frame.md.link("Discord", "https://discord.com") == "[Discord](https://discord.com)"


def test_mentions_accept_int_str_and_object():
    assert frame.md.mention(123) == "<@123>"
    assert frame.md.mention("123") == "<@123>"

    class Fake:
        id = 123

    assert frame.md.mention(Fake()) == "<@123>"
    assert frame.md.channel(123) == "<#123>"
    assert frame.md.role(123) == "<@&123>"


def test_bullet_and_numbered_lists():
    assert frame.md.bullet_list(["a", "b"]) == "- a\n- b"
    assert frame.md.numbered_list(["a", "b"]) == "1. a\n2. b"


def test_compose_joins_fragments():
    result = frame.md(
        frame.md.heading("Welcome"),
        "\n",
        "Thanks for joining ",
        frame.md.bold("friend"),
        "!",
    )
    assert result == "# Welcome\nThanks for joining **friend**!"
