# Services

To execute the services, run: 
`functions-framework --target entrypoint --source services/{service name}`
Open a new terminal and run `curl localhost:8080`

### IssueInvoice
To run `IssueInvoice`:
```
functions-framework --target entrypoint --source services/IssueInvoice/handler.py
```

In other terminal
```
curl localhost:8080 --header 'Content-Type: application/json' \
    --data '{"force": true}' localhost:8080
```

This service is also accessible via HTTPS: https://us-central1-starkbank-415623.cloudfunctions.net/InvoiceIssue

### Transfer2Starkbank
```
functions-framework --target entrypoint --source services/Transfer2Starkbank/handler.py
```

In other terminal
```
curl localhost:8080 --header 'Content-Type: application/json' \
    --data '{"..."}' localhost:8080
```

This service is also accessible via HTTPS: https://us-central1-starkbank-415623.cloudfunctions.net/Transfer2Starkbank

## Deploy
The code executed by these services on GCP are pulled from Artifact Registry, for deployment of the `starkbank_integration` package follow these steps.

1. Install `keyrings` and `twine` to be able to push to artifact registry.
`pip install keyrings.google-artifactregistry-auth`

P.S.: Make sure to authenticate to gcloud environment and on twine environment following the instructions in here.
```
gcloud artifacts print-settings python \
    --project=starkbank-415623 \                                  
    --repository=python-repo \
    --location=us-central1
```

2. Build `starkbank_integration` `tar.gz` package
`python setup.py sdist`

3. Upload to Artifact Registry
`python -m twine upload --repository-url https://us-central1-python.pkg.dev/starkbank-415623/python-repo/ dist/*`

