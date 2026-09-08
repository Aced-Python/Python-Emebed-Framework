import pytest

import frame
from frame.exceptions import CompatibilityError, InvalidComponentError


def ui_or_skip():
    discord = pytest.importorskip("discord")
    if not hasattr(discord.ui, "LayoutView"):
        pytest.skip("Components V2 requires discord.py 2.6+")
    return discord


def test_button_is_native_and_supports_callback_registration():
    discord = ui_or_skip()
    button = frame.ui.button("Click", custom_id="click", style="primary")
    assert isinstance(button, discord.ui.Button)

    async def callback(interaction):
        return None

    assert button.on_click(callback) is button


def test_link_button_rules():
    ui_or_skip()
    with pytest.raises(InvalidComponentError):
        frame.ui.button("Bad", url="https://example.com", custom_id="bad")
    with pytest.raises(InvalidComponentError):
        frame.ui.button("Bad", style="link")


def test_container_serializes():
    ui_or_skip()
    view = frame.ui.container(frame.ui.text("Hello"))
    assert view.to_discord() is view
    assert view.to_dict()["is_components_v2"] is True
