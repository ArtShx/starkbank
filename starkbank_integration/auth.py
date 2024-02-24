import os

import starkbank

from .environment import Environment


class Authentication:
    env_file = os.environ["env_file"]
    env = Environment.from_file(env_file)
    
    @classmethod
    def init(cls):
        if starkbank.user is not None:
            # Already authenticated
            return

        # user = starkbank.Organization(
        #     environment=cls.env["starkbank_env"],
        #     id=cls.env["organization_id"],
        #     private_key=cls.private_key
        # )
        # TODO: workaround to fake auth
        # I don't have access to sandbox for dev yet
        user = "Something"
        starkbank.user = user
        return
 
    @staticmethod
    def is_auth():
        return starkbank.user is not None

    @staticmethod
    def reset():
        starkbank.user = None

