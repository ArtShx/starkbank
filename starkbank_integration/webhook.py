import os
from typing import List

import starkbank

from starkbank_integration.auth import Authentication
from starkbank_integration.environment import Environment

class WebhookHandler:

    @classmethod
    def create(cls, route: str, subscriptions: List[str]) -> int:
        Authentication.init()
        env = Environment()
        # env is singleton, when Auth in made the environment was init, maybe can remove below assetion
        assert env.init

        url = os.path.join(env["api_site"], route)
        webhook = starkbank.webhook.create(
            url=url,
            subscriptions=subscriptions
        )
        return webhook.id

