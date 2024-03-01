from dataclasses import dataclass

import starkbank


from .auth import Authentication
from .exceptions import (
    InvalidInvoiceCreationgRequest,
    InvalidUser,
    InvalidTaxId,
    InvalidBankAccount,
    InvalidTransferCreationgRequest,
)
from .models.bank import BankAccount
from .utils import get_logger


logger = get_logger()


# TODO: use a more stable payload validator (swagger, jsonschema, etc.)
@dataclass
class TransferCreateRequest:
    amount: int
    name: str
    tax_id: str
    user_type: str  # either CPF or CNPJ
    bank_code: str
    branch_code: str
    account_number: str

    def __init__(
        self,
        name: str,
        user_type: str,
        tax_id: str,
        amount: int,
        bank_code: str,
        branch_code: str,
        account_number: str,
        account_type: str = "checking",
    ):
        try:
            bank_acc = BankAccount(
                name,
                user_type,
                tax_id,
                bank_code,
                branch_code,
                account_number,
                account_type=account_type,
            )
        except (InvalidUser, InvalidBankAccount, InvalidTaxId):
            raise InvalidInvoiceCreationgRequest
        if amount < 0 or not isinstance(amount, int) or isinstance(amount, bool):
            raise InvalidTransferCreationgRequest("Amount cannot be negative.")

        self.name = name
        self.user_type = user_type
        self.tax_id = tax_id
        self.amount = amount
        self.bank_code = bank_acc.bank_code
        self.branch_code = bank_acc.branch_code
        self.account_number = bank_acc.account_number
        self.account_type = bank_acc.account_type


class Transfer:
    @staticmethod
    @Authentication.auth_needed
    def create(transfer_request: TransferCreateRequest) -> bool:
        """
        Creates a new Transfer.

        Parameters
        ----------
            TransferCreateRequest:
                Transfer payload necessary information for creating a Transfer.

        Returns
        -------
            Bool
                Boolean indicating whether the transfer was created successfully.
        """
        if not isinstance(transfer_request, TransferCreateRequest):
            raise InvalidTransferCreationgRequest()

        transfer_req = starkbank.Transfer(
            amount=transfer_request.amount,
            tax_id=transfer_request.tax_id,
            name=transfer_request.name,
            bank_code=transfer_request.bank_code,
            branch_code=transfer_request.branch_code,
            account_number=transfer_request.account_number,
            account_type=transfer_request.account_type,
        )
        transfers = starkbank.transfer.create([transfer_req])
        return transfers[0].status == "created"
