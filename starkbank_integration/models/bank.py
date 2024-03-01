
import re

from ..exceptions import InvalidBankAccount
from .user import User


class BankAccount(User):
    def __init__(self, 
                 name: str,
                 user_type: str,
                 tax_id: str,
                 bank_code: str,
                 branch_code: str,
                 account_number: str,
                 account_type: str = "checking") -> None:
        super().__init__(name, user_type, tax_id)
        self._bank_code = bank_code
        self._branch_code = branch_code
        self._account_number = account_number
        self._account_type = account_type

        if not self._is_valid():
            raise InvalidBankAccount

    def _is_valid(self) -> bool:
        return self._is_valid_bank_code(self.bank_code) \
            and self._is_valid_branch_code(self.branch_code) \
            and (self._is_valid_account_number(self.account_number) or True)
    @staticmethod
    def _is_valid_bank_code(bank_code: str) -> bool:
        if not isinstance(bank_code, str):
            return False
        # either 8 or 3 digits
        pattern = "^[0-9]{8}$|^[0-9]{3}$"
        return bool(re.match(pattern, bank_code))

    @staticmethod
    def _is_valid_branch_code(code: str) -> bool:
        if not isinstance(code, str):
            return False
        # atleast 1 digits + "-" (0 or 1 "-") + [0-9] (0 or 1)
        pattern = "^[0-9]+-?[0-9]?$"
        return bool(re.match(pattern, code))

    @staticmethod
    def _is_valid_account_number(code: str) -> bool:
        if not isinstance(code, str):
            return False
        # The account number must be a sequence of 1 to 12 numbers 
        # followed by a hyphen and another digit (ex: 12345-2 or 123456-0)
        pattern = "^[0-9]{1,12}-[0-9]$"
        return bool(re.match(pattern, code))
    
    @property
    def bank_code(self) -> str:
        return self._bank_code

    @property
    def branch_code(self) -> str:
        return self._branch_code

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def account_type(self) -> str:
        return self._account_type
