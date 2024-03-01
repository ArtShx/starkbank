import json
import os
import random
from typing import List


from starkbank_integration.models.bank import BankAccount
from starkbank_integration.utils import get_logger
from starkbank_integration.models.user import User


logger = get_logger()
logger.warning("Do NOT use `dummy.py` for production code!")

here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(here, "./")
users_data_path = os.path.join(BASE_DIR, "file/users.json")
bank_data_path = os.path.join(BASE_DIR, "file/bank_acc.json")

assert os.path.isfile(users_data_path), f"File {users_data_path} not found."
assert os.path.isfile(bank_data_path), f"File {bank_data_path} not found."

with open(users_data_path) as f:
    user_data = json.load(f)

with open(bank_data_path) as f:
    bank_data = json.load(f)

assert len(user_data["names"]) > 0
assert len(user_data["cpf"]) > 0
assert len(bank_data["bank_codes"]) > 0
assert len(bank_data["branch_codes"]) > 0
assert len(bank_data["account_numbers"]) > 0


class Dummy:
    """Dummy class for generating dummy/fake/random data."""

    @staticmethod
    def get_users(n: int) -> List[User]:
        """Returns `n` users."""
        assert n > 0

        out = []
        for _ in range(n):
            name = random.choice(user_data["names"])
            tax_id = random.choice(user_data["cpf"])
            user = User(name, "CPF", tax_id)
            out.append(user)
        return out

    @staticmethod
    def get_bank_accounts(n: int) -> List[BankAccount]:
        assert n > 0

        out = []
        for _ in range(n):
            name = random.choice(user_data["names"])
            tax_id = random.choice(user_data["cpf"])
            bank_code = random.choice(bank_data["bank_codes"])
            branch_code = random.choice(bank_data["branch_codes"])
            account_numbers = random.choice(bank_data["account_numbers"])
            user = BankAccount(
                name, "CPF", tax_id, bank_code, branch_code, account_numbers
            )
            out.append(user)
        return out
