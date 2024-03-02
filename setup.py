import os
from setuptools import setup, find_packages
from starkbank_integration import __version__


try:
    here = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(here, "requirements.txt")) as f:
        requires = f.read().splitlines()
except FileNotFoundError:
    # When building with `python setup.py sdist`, the requirements file are not included
    # in the builded file, TODO
    requires = ["starkbank==2.24.0", "google-cloud-datastore", "functions-framework"]

setup(
    name="starkbank_int",
    version=__version__,
    description="StarkBank integration",
    author="Arthur Miada",
    # packages=['starkbank_integration'],
    packages=find_packages(),
    # include_package_data=True,
    # package_data={"": ["requirements.txt"]},
    install_requires=requires,
)
