from dummy import Dummy
from starkbank_integration.models.user import User


def test_get_users():
    users = Dummy.get_users(10)
    assert isinstance(users, list)
    assert len(users) == 10
    assert isinstance(users[0], User)
