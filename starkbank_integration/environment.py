import os
from typing import Union


from .exceptions import InvalidEnvironment
from .singleton import Singleton


class Environment(Singleton):
    _mandatory_keys = [
        "api_site",
        "access_id",
        "private_key",
        "organization_id",
        "starkbank_env",
    ]

    def __init__(self) -> None:
        self.args = {}
        self.init = False

    @staticmethod
    def from_file(env_file: Union[str, os.PathLike], ignore_err: bool = False):
        """
        Creates a Environment instance from a file.

        Parameters
        ----------
            env_file: str | os.PathLike
                Environment file path.
            ignore_err: bool
                Boolean indicating whether should raise an error if provided data are valid.
                Added for ignoring errors on unit tests with mock data.
        """

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

        if not is_env_valid(env) and not ignore_err:
            raise InvalidEnvironment()

        try:
            env._read_key()
        except InvalidEnvironment:
            ...

        env.init = True
        return env

    @staticmethod
    def from_environment():
        """Creates a Environment instance from a system/user environment variable."""
        raise NotImplementedError()

    def __getitem__(self, name):
        return self.args[name]

    def __contains__(self, item):
        return item in self.args

    def __str__(self) -> str:
        return str(self.args)

    def __repr__(self) -> str:
        return str(self.args)

    def keys(self):
        return list(self.args.keys())

    def _read_key(self):
        key_file = self.args["private_key"]
        if not os.path.isfile(key_file):
            raise InvalidEnvironment(f"Key not found: {key_file}")

        with open(key_file) as f:
            self.args["private_key_content"] = f.read()


def is_env_valid(env: Environment):
    check = True
    for key in Environment._mandatory_keys:
        check = check and key in env and env[key] != "" and isinstance(env[key], str)

    return check
