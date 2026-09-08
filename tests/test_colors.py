import pytest

import frame
from frame.exceptions import InvalidColorError


def test_named_color():
    assert int(frame.colors.blurple) == 0x5865F2
    assert frame.colors.normalize("#5865f2") == frame.colors.blurple


def test_rgb_and_int():
    assert frame.Color.from_rgb(88, 101, 242).rgb == (88, 101, 242)
    assert frame.colors.normalize(0x57F287).value == 0x57F287


def test_invalid_hex():
    with pytest.raises(InvalidColorError):
        frame.colors.normalize("#xyz")
