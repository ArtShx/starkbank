from typing import List
from dataclasses import dataclass

import starkbank


from .auth import Authentication
from .exceptions import InvalidInvoiceCreationgRequest, InvalidUser
from .models.user import User
from .utils import get_logger


logger = get_logger()


# TODO: use a more stable payload validator (swagger, jsonschema, etc.)
@dataclass
class InvoiceCreateRequest:
    amount: int
    name: str
    tax_id: str
    user_type: str  # either CPF or CNPJ

    def __init__(self, name: str, user_type: str, tax_id: str, amount: int):
        try:
            User(name, user_type, tax_id)
        except InvalidUser:
            raise InvalidInvoiceCreationgRequest
        if amount < 0 or not isinstance(amount, int) or isinstance(amount, bool):
            raise InvalidInvoiceCreationgRequest("Amount cannot be negative.")

        self.name = name
        self.user_type = user_type
        self.tax_id = tax_id
        self.amount = amount


class Invoice:
    @staticmethod
    @Authentication.auth_needed
    def create(invoice_request: List[InvoiceCreateRequest]) -> List[bool]:
        """
        Creates up to 100 invoices.

        Parameters
        ----------
        InvoiceRequests: List[InvoiceCreateRequest]:
            name: str
                Payer's name.
            user_type: str
                User's type, must be either CPF or CNPJ.
            tax_id: str
                User's identification, must be either formatted properly or unformatted.
            amount: int
                 A non-negative integer that represents the amount in cents to be invoiced.
                 When the invoice is paid, this parameter is updated with the amount actually
                 paid. Example: 100 (R$1.00)

        Returns
        -------
        List[bool]
            List of booleans indicating whether the Invoices was created successfully.
        """

        if (
            not isinstance(invoice_request, list)
            or len(invoice_request) < 1
            or not isinstance(invoice_request[0], InvoiceCreateRequest)
        ):
            raise InvalidInvoiceCreationgRequest()

        invoice_req = [
            starkbank.Invoice(amount=req.amount, tax_id=req.tax_id, name=req.name)
            for req in invoice_request
        ]
        invoices = starkbank.invoice.create(invoice_req)
        failed = []

        for i, invoice in enumerate(invoices):
            if invoice.status != "created":
                failed.append(i)
                inv_req = invoice_req[i]
                logger.error(
                    f"Failed to create invoice: {i}\n"
                    + f"Name: {inv_req.name}, tax_id: {inv_req.tax_id}, amount: {inv_req.amount}"
                )

        return failed
