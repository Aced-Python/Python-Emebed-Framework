import pytest


@pytest.fixture(autouse=True)
def _reset_theme():
    """Every test starts with no active global theme."""
    import frame

    frame.set_theme(None)
    yield
    frame.set_theme(None)
