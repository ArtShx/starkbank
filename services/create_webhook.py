"""
Service to create the webhoock for incoming invoices.

TODO: run this code on a serverless cloud environment (AWS Lambda, GCP Functions)
"""
import os

from starkbank_integration.auth import Authentication
from starkbank_integration.webhook import WebhookHandler

here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(here, "../")

env_file = os.path.join(BASE_DIR, "file/env")


def main():
    """Creates a webhook to listen to invoices."""

    Authentication.init()

    # TODO: maybe get route from blueprint of the incoming invoices
    route = "..."
    WebhookHandler.create(route, subscriptions=["invoice"])
    


if __name__ == "__main__":
    main()
    
