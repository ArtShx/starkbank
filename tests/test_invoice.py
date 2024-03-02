import pytest

import starkbank

from dummy import Dummy
from starkbank_integration.auth import Authentication
from starkbank_integration.exceptions import (
    NotAuthenticated,
    InvalidInvoiceCreationgRequest,
    ErrorGetInvoice,
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

    invoices = Invoice.create(create_request)

    assert len(invoices) == len(create_request)
    for invoice, create_req in zip(invoices, create_request):
        assert Invoice.get(invoice.id).id == invoice.id
        assert invoice.name == create_req.name
        assert invoice.tax_id == create_req.tax_id
        assert invoice.amount == create_req.amount


@pytest.mark.skip("Not running this on GH actions.")
def test_get():
    id_does_not_exists = "0000000000000000"
    Authentication.init()
    with pytest.raises(ErrorGetInvoice):
        Invoice.get(id_does_not_exists)

    valid_id = "5280164615290880"
    invoice = Invoice.get(valid_id)
    assert isinstance(invoice, starkbank.Invoice)
    assert invoice.id == valid_id
    assert invoice.name == "Ana"
    assert invoice.tax_id == "455.333.354-63"
    assert invoice.amount == 868


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
