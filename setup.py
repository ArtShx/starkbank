from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='starkbank_int',
    version='0.1',
    description='StarkBank integration',
    author='Arhtur Miada',
    packages=['starkbank_integration'],
    install_requires=required
)
