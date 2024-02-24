import os
from typing import Union


from .exceptions import InvalidEnvironment
from .singleton import Singleton

class Environment(Singleton):
    def __init__(self) -> None:
        self.args = {}
        self.init = False

    @staticmethod
    def from_file(env_file: Union[str, os.PathLike]):
        """Creates a Environment instance from a file."""

        assert os.path.isfile(env_file), f"Env file: {env_file} not found."
        env = Environment()
        env.args = {}

        with open(env_file) as f:
            for line in f.read().splitlines():
                try:
                    k, v = line.split("=")
                    env.args[k] = v
                except ValueError:
                    ...

        if not is_env_valid(env):
            raise InvalidEnvironment()
        env.init = True
        return env

    @staticmethod
    def from_environment():
        """Creates a Environment instance from a system/user environment variable."""
        raise NotImplemented()

    def __getitem__(self, name):
        return self.args[name]

    def __contains__(self, item):
        return item in self.args

    def keys(self):
        return list(self.args.keys())


def is_env_valid(env: Environment):
    api_site_check = "api_site" in env and env["api_site"] != "" and isinstance(env["api_site"], str)
    org_id_check = "organization_id" in env and env["organization_id"] != "" and isinstance(env["organization_id"], str)
    key_check = "private_key" in env and env["private_key"] != "" and isinstance(env["private_key"], str)
    starkbank_env_check = "starkbank_env" in env and env["starkbank_env"] != "" and isinstance(env["starkbank_env"], str)

    return api_site_check and org_id_check and key_check and starkbank_env_check
