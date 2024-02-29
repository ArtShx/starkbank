import os

import starkbank

from .environment import Environment
from .exceptions import NotAuthenticated


class Authentication:
    
    @classmethod
    def init(cls):
        if starkbank.user is not None:
            # Already authenticated
            return

        env_file = os.environ["env_file"]
        env = Environment.from_file(env_file)
        user = starkbank.Project(
            environment=env["starkbank_env"],
            id=env["access_id"],
            private_key=env["private_key_content"]
        )
        starkbank.user = user
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

