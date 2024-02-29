"""
Serverless function to issue invoices for random users.

TODO: move to a cloud service (GCP Functions, AWS Lambda) and add a scheduler to run every 3 hours for the next 24 hours.
"""

from random import randint

# this won't work on GCP, what should we do?
# add to packages? use a simple db? duplicate this file on the functions code base?
from dummy import Dummy

from starkbank_integration.auth import Authentication
from starkbank_integration.exceptions import ErrorCreatingInvoice
from starkbank_integration.invoice import Invoice, InvoiceCreateRequest


def handler():
    """ Creates 8-12 invoices to random peoples. """
    Authentication.init()
    nb_users_to_send = randint(8, 12)

    user_data = Dummy.get_users(nb_users_to_send)

    inv_req = [
        InvoiceCreateRequest(user.name, user.user_type, user.tax_id, amount=randint(1, 1000))
        for user in user_data
    ]
    try:
        Invoice.create(inv_req)
        return True
    except ErrorCreatingInvoice:
        return False


if __name__ == "__main__":
    handler()

