import os
from tempfile import NamedTemporaryFile

import pytest

from starkbank_integration.environment import Environment
from starkbank_integration.exceptions import InvalidEnvironment


def test_env():

    content=b"""
var1=val1
var2=value2
# should ignore this line with a comment and the blank line below

api_site= http://localhost:1234
private_key=/path/to/key
starkbank_env=sandbox
organization_id=organization_id
access_id=project/123
"""
    with NamedTemporaryFile(delete=False) as fp:
        fp.write(content)
        fp.close()

        env = Environment.from_file(fp.name)
        assert env.keys() == ["var1", "var2", "api_site", "private_key",
                              "starkbank_env", "organization_id", "access_id"]
        assert "var1" in env
        assert env["var2"] == "value2"
        assert env["api_site"] == " http://localhost:1234"

        with pytest.raises(KeyError):
            env["KeyError when trying to get any keys that does not exists"]

        # Cleaning
        os.remove(fp.name)


def test_missing_mandatory_keys():
    content=b"""
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

