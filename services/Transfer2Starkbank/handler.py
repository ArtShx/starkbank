"""
Serverless function receive callbacks from webhooks from Starkbank API.
"""

from typing import Tuple

import functions_framework

from starkbank_integration.auth import Authentication
from starkbank_integration.exceptions import ErrorCreatingInvoice
from starkbank_integration.transfer import Transfer, TransferCreateRequest
from starkbank_integration.models.bank import BankAccount
from starkbank_integration.utils import get_logger

logger = get_logger()


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
    request_json = request.get_json(silent=True)
    success, transfer_id_or_msg = handler(request_json)
    if success:
        logger.debug(f"Made transfer to: {transfer_id_or_msg}")
    return str(transfer_id_or_msg)


def handler(payload) -> Tuple[bool, str]:
    """
    Transfers the amount received to Starkbank account.
    Returns a tuple indicating if the transfer was made and it's id if yes or an error or
    """
    payload = payload["event"]["log"]
    if payload["type"] != "credited":
        return False, 'Skipping callbacks that are not "credited"'

    invoice = payload["invoice"]
    nominal_amount = invoice["nominalAmount"]
    discount_amount = invoice["discountAmount"]
    fine_amount = invoice["fineAmount"]
    intereset_amount = invoice["interestAmount"]

    # :REVIEW not sure if this is correct
    fees_amount = fine_amount + intereset_amount
    final_amount = nominal_amount + discount_amount - fees_amount

    Authentication.init()
    starkbank_acc = BankAccount(
        name="Stark Bank S. A.",
        user_type="CNPJ",
        tax_id="20.018.183/0001-80",
        bank_code="20018183",
        branch_code="0001",
        account_number="6341320293482496",
        account_type="payment",
    )
    transfer_req = TransferCreateRequest(
        starkbank_acc.name,
        starkbank_acc.user_type,
        starkbank_acc.tax_id,
        final_amount,
        starkbank_acc.bank_code,
        starkbank_acc.branch_code,
        starkbank_acc.account_number,
    )
    try:
        transfer = Transfer.create(transfer_req)
        return True, transfer.id
    except ErrorCreatingInvoice as e:
        return False, str(e)


if __name__ == "__main__":
    payload = {
        "event": {
            "created": "2024-02-29T05:00:12.051456+00:00",
            "id": "5813904772956160",
            "log": {
                "created": "2024-02-29T05:00:11.794243+00:00",
                "errors": [],
                "id": "6417929088270336",
                "invoice": {
                    "amount": 12345,
                    "brcode": "00020101021226890014br.gov.bcb.pix2567brcode-h.sandbox.starkinfra.com/v2/"
                    + "ea937a2753cb47579b655b6a5cc2a5355204000053039865802BR5925Stark Bank S.A. - "
                    + "Institu6009Sao Paulo62070503***630482E8",
                    "created": "2024-02-29T04:51:21.066899+00:00",
                    "descriptions": [],
                    "discountAmount": 0,
                    "discounts": [],
                    "due": "2024-03-02T04:51:21.041467+00:00",
                    "expiration": 5097600,
                    "fee": 0,
                    "fine": 2.0,
                    "fineAmount": 0,
                    "id": "5166945473134592",
                    "interest": 1.0,
                    "interestAmount": 0,
                    "link": "https://test4380438.sandbox.starkbank.com/invoicelink/ea937a2753cb47579b655b6a5cc2a535",
                    "name": "Arthur Hideyuki Miada da Silva",
                    "nominalAmount": 12345,
                    "pdf": "https://sandbox.api.starkbank.com/v2/invoice/ea937a2753cb47579b655b6a5cc2a535.pdf",
                    "rules": [],
                    "splits": [],
                    "status": "paid",
                    "tags": ["e34471744202402290500ivhivwiq2kp"],
                    "taxId": "012.345.678-90",
                    "transactionIds": ["42243899797196738924666148216171"],
                    "updated": "2024-02-29T05:00:11.794335+00:00",
                },
                "type": "credited",
            },
            "subscription": "invoice",
            "workspaceId": "6010044957065216",
        }
    }

    # handler()
