import os
from typing import Tuple

import starkbank
from starkbank.error import InputErrors

from .environment import Environment
from .exceptions import ErrorAuthenticating, NotAuthenticated, InvalidEnvironment


class Authentication:
    @classmethod
    def init(cls):
        if starkbank.user is not None:
            # Already authenticated
            return

        try:
            if "env_file" not in os.environ:
                raise InvalidEnvironment("env_file was not defined.")
            env_file = os.environ["env_file"]
            env = Environment.from_file(env_file)
            user = starkbank.Project(
                environment=env["starkbank_env"],
                id=env["access_id"],
                private_key=env["private_key_content"],
            )
            starkbank.user = user
        except (KeyError, InvalidEnvironment) as e:
            raise ErrorAuthenticating(e)
        return

    @staticmethod
    def is_auth():
        return starkbank.user is not None

    @staticmethod
    def auth_needed(func):
        def wrapper(*args, **kwargs):
            if not Authentication.is_auth():
                raise NotAuthenticated()
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def reset():
        starkbank.user = None

    @staticmethod
    def test() -> Tuple[bool, str]:
        """
        Performs a test on Starkbank API.
        Returns a boolean indicating if the test has passed and a
        string with some detailed information of errors (if any).
        """
        try:
            Authentication.init()
            balance = starkbank.balance.get()
            _ = balance.amount
            return True, ""
        except (ErrorAuthenticating, InputErrors) as err:
            return False, str(err)
