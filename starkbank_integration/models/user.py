from abc import ABC, abstractmethod
import re

from ..exceptions import InvalidTaxId, InvalidUser
from ..utils import contains_only_numbers, get_logger


logger = get_logger()

class UserType(ABC):
    """
    Abstract base class for UserType (CPF and CNPJ)
    """
    def __init__(self, val: str):
        if not self._is_valid(val):
            raise InvalidTaxId
        self._val = val

    @staticmethod
    @abstractmethod
    def _is_valid(val: str) -> bool:
        ...

    @property
    def val(self) -> str:
        return self._val


class CPFUser(UserType):
    def __init__(self, val: str):
        super().__init__(val)
        self.name = "CPF"

    @staticmethod
    def _is_valid(val: str) -> bool:
        # TODO: basic validator, find a complex regex for CPF validator
        # this solution should not be used in production
        # logger.warning("CPF validator for tests purpose, do not use in production")
        if not isinstance(val, str):
            return False

        # 3 numbers + "." + 3 numbers + "." + 3 numbers + "-" + 2 numbers
        # or 11 numbers
        pattern = "^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$|^[0-9]{11}$"
        return bool(re.match(pattern, val))


class CNPJUser(UserType):
    def __init__(self, val: str):
        super().__init__(val)
        self.name = "CNPJ"

    @staticmethod
    def _is_valid(val: str) -> bool:
        # TODO: basic validator, find a complex regex for CNPJ validator
        # this solution should not be used in production
        # logger.warning("CPF validator for tests purpose, do not use in production")
        if not isinstance(val, str):
            return False

        # Atleast 3 "." and 1 number between then + "/" + 4 digitis + "-" + 2 digits
        # or 14 numbers
        pattern = "^[0-9]+.[0-9]+.[0-9]+/[0-9]{4}-[0-9]{2}$|^[0-9]{14}$"
        return bool(re.match(pattern, val))


class User:
    def __init__(self, name: str, user_type: str, tax_id: str) -> None:
        """
        Creates a User.

        Parameters
        ----------
        name: str
            User name.
        user_type: str
            Must be either "CPF" or "CNPJ".
        tax_id: str
            Payer identification.
        """
        if not isinstance(name, str) or name == "" or user_type not in ["CPF", "CNPJ"]:
            raise InvalidUser

        self._name = name
        _user_type = CPFUser(tax_id) if user_type in "CPF" else CNPJUser(tax_id)
        self._user_type = _user_type.name
        self._tax_id = _user_type.val

    @property
    def name(self) -> str:
        return self._name

    @property
    def user_type(self) -> str:
        return self._user_type

    @property
    def tax_id(self) -> str:
        return self._tax_id


