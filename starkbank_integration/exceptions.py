
class _BaseException(Exception):
    code = 0xa1
    msg = "Unknown Error"

class InvalidUser(_BaseException):
    code = 0xa2
    msg = "Invalid user."

class InvalidTaxId(_BaseException):
    code = 0xa3
    msg = "Invalid TaxId!"

class InvalidInvoiceCreationgRequest(_BaseException):
    code = 0xa4
    msg = "Failed to create invoice."

class NotAuthenticated(_BaseException):
    code = 0xa5
    msg = "A user is required to access StarkBank API. Check StarkBank docs in ..."

class InvalidBankAccount(_BaseException):
    code = 0xa6
    msg = "Bank Account is invalid."

class InvalidTransferCreationgRequest(_BaseException):
    code = 0xa7
    msg = "Failed to create transfer."

class InvalidEnvironment(_BaseException):
    code = 0xa7
    msg = "Invalid data on Environment."

class ErrorCreatingInvoice(_BaseException):
    code = 0xa8
    msg = "Failed to create Invoice."

class InvalidEntity(_BaseException):
    code = 0xa9
    msg = "Invalid Entity"
