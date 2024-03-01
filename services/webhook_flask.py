from flask import Flask, request, json

from starkbank_integration.auth import Authentication
from starkbank_integration.transfer import Transfer, TransferCreateRequest


# TODO: refactor this, maybe use controllers/blueprints

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'


@app.route("/webhook/invoice_credit", methods=["POST"])
def invoice_credit():
    Authentication.init()
    # amount = request
    # TODO: subtract fees 
    # will be easier to test when we have access to sandbox
    amount = 0

    transfer_req = TransferCreateRequest(
        name="Stak Bank S. A.",
        user_type="CNPJ",
        tax_id="20.018.183/0001-80",
        amount=amount,
        bank_code="20018183",
        branch_code="0001",
        account_number="6341320293482496",
        account_type="payment"
    )
    Transfer.create(transfer_req)

if __name__ == '__main__':
    app.run(debug=True)
