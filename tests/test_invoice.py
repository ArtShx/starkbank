import pytest

from dummy import Dummy

from starkbank_integration.auth import Authentication
from starkbank_integration.exceptions import (
    NotAuthenticated,
    InvalidInvoiceCreationgRequest,
)
from starkbank_integration.invoice import Invoice, InvoiceCreateRequest


user = Dummy.get_users(1)[0]


@pytest.mark.skip("Not running this on GH actions.")
def test_create_invoice():
    create_request = [
        InvoiceCreateRequest(
            amount=1000, name=user.name, user_type=user.user_type, tax_id=user.tax_id
        )
    ]

    Authentication.reset()
    with pytest.raises(NotAuthenticated):
        Invoice.create(create_request)

    Authentication.init()
    with pytest.raises(InvalidInvoiceCreationgRequest):
        Invoice.create(["Not a InvoiceCreateRequest"])

    Invoice.create(create_request)


def test_schema_validation():
    with pytest.raises(InvalidInvoiceCreationgRequest):
        InvoiceCreateRequest(
            name=user.name, user_type=user.user_type, tax_id=user.tax_id, amount=-1
        )

    with pytest.raises(InvalidInvoiceCreationgRequest):
        InvoiceCreateRequest(
            name=user.name, user_type="InvalidUserType", tax_id=user.tax_id, amount=1
        )

    with pytest.raises(InvalidInvoiceCreationgRequest):
        InvoiceCreateRequest(
            name=user.name, user_type=user.user_type, tax_id=user.tax_id, amount=1.5
        )

    with pytest.raises(InvalidInvoiceCreationgRequest):
        InvoiceCreateRequest(
            name=user.name, user_type=user.user_type, tax_id=user.tax_id, amount=False
        )
