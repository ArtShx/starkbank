"""
Serverless function to issue invoices for random users.

TODO: move to a cloud service (GCP Functions, AWS Lambda) and add a scheduler to run every 3 hours for the next 24 hours.
"""

from random import randint

from dummy import Dummy

from starkbank_integration.auth import Authentication
from starkbank_integration.invoice import Invoice, InvoiceCreateRequest


def main():
    """Issues 8-12 invoices to random peoples."""
    Authentication.init()
    nb_users_to_send = randint(8, 12)
    # TODO: replace fake user data for request payload
    user_data = Dummy.get_users(nb_users_to_send)

    inv_req = [
        InvoiceCreateRequest(user.name, user.user_type, user.tax_id, amount=randint(0, 100))
        for user in user_data
    ]
    Invoice.create(inv_req)


if __name__ == "__main__":
    main()

