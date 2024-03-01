import pytest

from starkbank_integration.exceptions import InvalidTaxId
from starkbank_integration.models.user import CPFUser, CNPJUser, User


def test_cpf_validation():
    sample = [
        # CPF values and expected response
        ["123.456.789-00", True],
        ["12345678900", True],
        ["123.456.789.00", False],
        ["123-456.789.00", False],
        ["123.456.789-001", False],
        ["123.456.789-1", False],
        ["ABC.DEF.GHI-JK", False],
        ["ABCD.EF.GHI-JK", False],
        ["ABC.DE.FGHI-JK", False],
        ["ABC.DEF.GH-I-JK", False],
        ["", False],
        ["1", False],
        ["a", False],
        ["A", False],
        [True, False],
        [0, False],
        [None, False],
        [[], False],
        [["a", "b"], False],
        [{}, False],
    ]

    for cpf, expected in sample:
        assert (
            CPFUser._is_valid(cpf) == expected
        ), f"Assertion error: {cpf} != {expected}"


def test_cnpj_validation():
    sample = [
        ["20.018.183/0001-80", True],
        ["20018183000180", True],
        ["20.018.183/0001.80", False],
        ["AA.018.183/0001-80", False],
        ["ABC.DEF.GHI-JK", False],
        ["123.456.789-00", False],
        ["12345678900", False],
        ["", False],
        ["1", False],
        ["a", False],
        ["A", False],
        [True, False],
        [0, False],
        [None, False],
        [[], False],
        [["a", "b"], False],
        [{}, False],
    ]

    for cnpf, expected in sample:
        assert (
            CNPJUser._is_valid(cnpf) == expected
        ), f"Assertion error: {cnpf} != {expected}"


def test_cpf_creations():
    valid_cpf = "123.456.789-00"
    user = CPFUser(valid_cpf)  # should give no exceptions
    assert user.val == valid_cpf  # property should be accessible

    invalid_cpf = "0"
    with pytest.raises(InvalidTaxId):
        CPFUser(invalid_cpf)


def test_cnpj_creations():
    valid_cnpj = "20.018.183/0001-80"
    user = CNPJUser(valid_cnpj)  # should give no exceptions
    assert user.val == valid_cnpj  # property should be accessible

    invalid_cnpj = "0"
    with pytest.raises(InvalidTaxId):
        CPFUser(invalid_cnpj)


def test_user_creation():
    # Creating CNPJ
    cnpj = "20.018.183/0001-80"
    user = User("Stark", "CNPJ", cnpj)
    assert user.name == "Stark"
    assert user.user_type == "CNPJ"
    assert user.tax_id == cnpj

    # Creating CPF
    cpf = "123.456.789-00"
    user = User("Tony", "CPF", cpf)
    assert user.name == "Tony"
    assert user.user_type == "CPF"
    assert user.tax_id == cpf

    # Creating invalid user
    with pytest.raises(InvalidTaxId):
        User("John", "CPF", cnpj)
