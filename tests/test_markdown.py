import frame


def test_markdown_helpers():
    assert frame.md.bold("hello") == "**hello**"
    assert frame.md.codeblock("python", "print(1)") == "```python\nprint(1)\n```"
    assert frame.md.heading("Welcome") == "## Welcome"


def test_markdown_composition():
    value = frame.md(frame.md.heading("Welcome"), "Hello ", frame.md.bold("world"), "!")
    assert str(value) == "## WelcomeHello **world**!"


def test_mention_falls_back_to_snowflake():
    class User:
        id = 123

    assert frame.md.mention(User()) == "<@123>"
