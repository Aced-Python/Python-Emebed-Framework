from io import BytesIO

import pytest

import frame
from frame.exceptions import AttachmentError


def test_attachment_url_requires_filename():
    with pytest.raises(AttachmentError):
        frame.attachment(BytesIO(b"x")).attachment_url


def test_attachment_url():
    assert frame.attachment(BytesIO(b"x"), filename="x.png").attachment_url == "attachment://x.png"
