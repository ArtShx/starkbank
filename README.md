# StarkBank skill test
Integration with StarkBank server

1. Issuance of boletos (between 8 to 12) every 3 hours to random individuals for 24 hours;
2. Receive a webhook callback for the credits received (from task 1) and transfer the received amount (subtracting any fees) to the StarkBank account.

## Tools
- Python 3.10;
- Flake8 (linter) / Black (formatter);
- Pytest / coverage;
- GCP:
    * Cloud Functions (run microservices);
    * Cloud Scheduler (schedule microservice executions);
    * Artifact Registry (python package repository);
    * Secret Manager (store sensitive files);

## Setup
```ssh
git clone https://github.com/ArtShx/starkbank_int
cd starkbank_int
virtualenv venv
source venv/bin/activate

# Install dependencies
pip install .
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest
```

#### Edit the env file doing the following steps:
You need to update the `env` file to be able to authenticate with Starkbank API. Follow steps below:
1. Update the path of your private_key.pem (make sure this the same key that is already registered on Starkbank API)
`private_key=/path/to/your/key.pem`

2. Update the access_id (Starkbank project id):
`access_id=...`

3. Create a environment variable to set the path of this env file:
`export env_file=/path/to/starkbank_int/file/env`

4. Try executing the `HelloWorld`  service by running the following command:
`functions-framework --target entrypoint --source services/HelloWorld/handler.py`

Open a new terminal and run `curl localhost:8080` 


## Folder Structure
```
.
├── file                    # General files (mock, configuration)
│   └── keys                # PEM keys
├── services                # Microservices
│   ├── IssueInvoice
│   └── Transfer2Starkbank
├── starkbank_integration   # Base code to be used by microservices
│   ├── db                  # Database interaction
│   └── models              # Entities (business rules)
└── tests                   # Unit tests
```

## TODO
- [x] Create a package for starkbank api integration;
- [ ] Create tests for `services/`;
- [x] Add CI automated tests on commit, run tests and coverage report;
- [x] Setup a GCP freetier account (maybe use Terraform or other IaC tool?);
- [ ] Add CD automated deploy on GCP;
- [x] Deploy `services` and the `starkbank_integration` package into a cloud provider;

