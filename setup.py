from setuptools import setup, find_packages
from starkbank_integration import __version__
# import os


# here = os.path.dirname(os.path.abspath(__file__))

# with open('requirements.txt') as f:
#     required = f.read().splitlines()
requires = [
    "starkbank==2.24.0",
    "google-cloud-datastore"
]

setup(
    name='starkbank_int',
    version=__version__,
    description='StarkBank integration',
    author='Arthur Miada',
    # packages=['starkbank_integration'],
    packages=find_packages(),
    # include_package_data=True,
    # package_data={"": ["requirements.txt"]},
    install_requires=requires
)

