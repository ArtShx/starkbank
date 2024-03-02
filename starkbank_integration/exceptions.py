class _BaseException(Exception):
    code = 0xA1
    msg = "Unknown Error"


class InvalidUser(_BaseException):
    code = 0xA2
    msg = "Invalid user."


class InvalidTaxId(_BaseException):
    code = 0xA3
    msg = "Invalid TaxId!"


class InvalidInvoiceCreationgRequest(_BaseException):
    code = 0xA4
    msg = "Failed to create invoice."


class NotAuthenticated(_BaseException):
    code = 0xA5
    msg = "A user is required to access StarkBank API. Check StarkBank docs in ..."


class InvalidBankAccount(_BaseException):
    code = 0xA6
    msg = "Bank Account is invalid."


class InvalidTransferCreationgRequest(_BaseException):
    code = 0xA7
    msg = "Failed to create transfer."


class InvalidEnvironment(_BaseException):
    code = 0xA7
    msg = "Invalid data on Environment."


class ErrorCreatingInvoice(_BaseException):
    code = 0xA8
    msg = "Failed to create Invoice."


class InvalidEntity(_BaseException):
    code = 0xA9
    msg = "Invalid Entity"


class ErrorGoogleAuth(_BaseException):
    code = 0xAA
    msg = "Failed Authenticating with GCP."


class ErrorGetInvoice(_BaseException):
    code = 0xAB
    msg = "Failed to get Invoice"


class ErrorGetTransfer(_BaseException):
    code = 0xAC
    msg = "Failed to get Transfer."
