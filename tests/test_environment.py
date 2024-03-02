import os
from tempfile import NamedTemporaryFile

import pytest

from starkbank_integration.environment import Environment
from starkbank_integration.exceptions import InvalidEnvironment


def test_env_does_not_exists():
    with pytest.raises(InvalidEnvironment):
        Environment.from_file("/file/does/not/exist")


def test_env():
    my_secret_key = "/tmp/my_secret_key.pem"
    content = b"""
var1=val1
var2=value2
# should ignore this line with a comment and the blank line below

api_site= http://localhost:1234
private_key=/tmp/my_secret_key.pem
starkbank_env=sandbox
organization_id=organization_id
access_id=project/123
"""
    with open(my_secret_key, "w") as f:
        f.write("Secret content")
    with NamedTemporaryFile(delete=False) as fp:
        fp.write(content)
        fp.close()

        env = Environment.from_file(fp.name)
        assert env.keys() == [
            "var1",
            "var2",
            "api_site",
            "private_key",
            "starkbank_env",
            "organization_id",
            "access_id",
            "private_key_content"
        ]
        assert "var1" in env
        assert env["var2"] == "value2"
        assert env["api_site"] == " http://localhost:1234"

        with pytest.raises(KeyError):
            env["KeyError when trying to get any keys that does not exists"]

        # Cleaning
        os.remove(fp.name)
        os.remove(my_secret_key)


def test_missing_mandatory_keys():
    content = b"""
api_site=http://localhost:1234
# missing organization_id, private_key, starkbank_env, etc.
"""
    with NamedTemporaryFile(delete=False) as fp:
        fp.write(content)
        fp.close()

        with pytest.raises(InvalidEnvironment):
            Environment.from_file(fp.name)

        # Cleaning
        os.remove(fp.name)
