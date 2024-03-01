"""
Serverless function to issue invoices for random users.
"""

import functions_framework

from random import randint

from starkbank_integration.auth import Authentication
from starkbank_integration.exceptions import ErrorCreatingInvoice
from starkbank_integration.invoice import Invoice, InvoiceCreateRequest
from starkbank_integration.db.base import BaseDB


@functions_framework.http
def entrypoint(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    success = handler()
    return f"Success {success}!"


def handler():
    """Creates 8-12 invoices to random peoples."""
    Authentication.init()
    nb_users_to_send = randint(8, 12)

    db = BaseDB("User")
    user_data = db.get_all(limit=nb_users_to_send)

    inv_req = [
        InvoiceCreateRequest(
            user["name"], user["user_type"], user["tax_id"], amount=randint(1, 1000)
        )
        for user in user_data
    ]
    try:
        Invoice.create(inv_req)
        return True
    except ErrorCreatingInvoice:
        return False


if __name__ == "__main__":
    handler()
