# Deploy

1. Install `keyrings` and `twine` to be able to push to artifact registry.
`pip install keyrings.google-artifactregistry-auth`

P.S.: Make sure to authenticate to gcloud environment on twine environment following the instructions in here.
```
gcloud artifacts print-settings python \
    --project=starkbank-415623 \                                  
    --repository=python-repo \
    --location=us-central1
```

2. Gerar tar.gz do package
`python setup.py sdist`

3. Upload to Artifact Registry
`python -m twine upload --repository-url https://us-central1-python.pkg.dev/starkbank-415623/python-repo/ dist/*`

