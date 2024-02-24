import pytest

from starkbank_integration.auth import Authentication


def test_not_auth():
    Authentication.reset()
    assert Authentication.is_auth() == False

