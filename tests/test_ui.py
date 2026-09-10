import discord
import pytest

import frame


def test_container_produces_real_layout_view():
    view = frame.ui.container(
        frame.ui.text("## Welcome"),
        frame.ui.separator(),
    )
    assert isinstance(view, discord.ui.LayoutView)


def test_section_with_button_accessory():
    view = frame.ui.container(
        frame.ui.section(
            "Need help?",
            accessory=frame.ui.button("Open Support", style="primary", custom_id="support"),
        ),
    )
    assert isinstance(view, discord.ui.LayoutView)


def test_action_row_with_link_and_normal_button():
    view = frame.ui.container(
        frame.ui.action_row(
            frame.ui.button("Docs", url="https://example.com/docs"),
            frame.ui.button("Support", custom_id="support", style="primary"),
        ),
    )
    assert isinstance(view, discord.ui.LayoutView)


def test_bare_button_in_container_is_rejected():
    with pytest.raises(frame.InvalidComponentError) as exc:
        frame.ui.container(frame.ui.button("Click me"))
    assert "action_row" in str(exc.value)


def test_bare_select_in_container_is_rejected():
    sel = frame.ui.select([frame.Option("A"), frame.Option("B")])
    with pytest.raises(frame.InvalidComponentError):
        frame.ui.container(sel)


def test_action_row_cannot_mix_button_and_select():
    sel = frame.ui.select([frame.Option("A")])
    btn = frame.ui.button("Click")
    with pytest.raises(frame.InvalidComponentError) as exc:
        frame.ui.container(frame.ui.action_row(btn, sel))
    assert "mix" in str(exc.value)


def test_action_row_too_many_buttons():
    buttons = [frame.ui.button(f"B{i}", custom_id=f"b{i}") for i in range(6)]
    with pytest.raises(frame.InvalidComponentError) as exc:
        frame.ui.container(frame.ui.action_row(*buttons))
    assert "5" in str(exc.value)


def test_link_button_requires_no_custom_id_conflict():
    # url= implies style=link automatically, no error
    btn = frame.ui.button("Docs", url="https://example.com")
    assert btn._resolved_style() == "link"
    view = frame.ui.container(frame.ui.action_row(btn))
    assert isinstance(view, discord.ui.LayoutView)


def test_button_with_style_and_url_conflict_raises():
    with pytest.raises(frame.InvalidComponentError):
        frame.ui.container(
            frame.ui.action_row(
                frame.ui.button(
                    "Weird",
                    style="danger",
                    url="https://example.com",
                    custom_id=None,
                )
            )
        )


def test_button_with_no_label_or_emoji_raises():
    with pytest.raises(frame.InvalidComponentError):
        frame.ui.container(frame.ui.action_row(frame.ui.button(custom_id="x")))


def test_section_accessory_must_be_button_or_thumbnail():
    with pytest.raises(frame.InvalidComponentError):
        frame.ui.container(
            frame.ui.section("text", accessory=frame.ui.text("not allowed"))
        )


def test_section_too_many_text_children():
    with pytest.raises(frame.InvalidComponentError):
        frame.ui.container(
            frame.ui.section(
                "a", "b", "c", "d",
                accessory=frame.ui.button("x", custom_id="x"),
            )
        )


def test_empty_container_raises():
    with pytest.raises(frame.InvalidComponentError):
        frame.ui.container()


@pytest.mark.asyncio
async def test_button_on_click_callback_fires():
    calls = []

    async def clicked(interaction):
        calls.append(interaction)

    btn = frame.ui.button("Click me", custom_id="hello", on_click=clicked)
    real_button = btn.to_discord()
    await real_button.callback("fake-interaction")
    assert calls == ["fake-interaction"]


@pytest.mark.asyncio
async def test_button_on_click_decorator():
    calls = []
    btn = frame.ui.button("Click me", custom_id="hello")

    @btn.on_click
    async def clicked(interaction):
        calls.append(interaction)

    real_button = btn.to_discord()
    await real_button.callback("fake-interaction")
    assert calls == ["fake-interaction"]


def test_select_options_and_to_discord():
    sel = frame.ui.select(
        [frame.Option("Python", "python"), frame.Option("JS", "js")],
        placeholder="Pick one",
    )
    view = frame.ui.container(frame.ui.text("pick"), frame.ui.action_row(sel))
    assert isinstance(view, discord.ui.LayoutView)


def test_select_empty_options_raises():
    with pytest.raises(frame.InvalidComponentError):
        frame.ui.container(frame.ui.action_row(frame.ui.select([])))


def test_media_gallery():
    gallery = frame.ui.media_gallery(
        "https://example.com/a.png",
        ("https://example.com/b.png", "second image"),
    )
    view = frame.ui.container(gallery)
    assert isinstance(view, discord.ui.LayoutView)


def test_media_gallery_too_many_items_raises():
    with pytest.raises(frame.InvalidComponentError):
        frame.ui.media_gallery(*[f"https://example.com/{i}.png" for i in range(11)])


def test_confirm_preset_builds_a_view():
    async def do_confirm(interaction):
        pass

    view = frame.ui.confirm("Are you sure?", on_confirm=do_confirm)
    assert isinstance(view, discord.ui.LayoutView)


def test_container_to_dict_free_of_discord_via_spec():
    # The underlying spec objects work without touching discord.py at all.
    text = frame.ui.text("hello")
    assert text.to_dict() == {"kind": "text", "content": "hello"}
