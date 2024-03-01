import pytest

from starkbank_integration.exceptions import ErrorGoogleAuth

try:
    from starkbank_integration.db.base import BaseDB
except ErrorGoogleAuth:
    ...


@pytest.mark.skip("Running only locally")
def test_db():
    db = BaseDB("TestEntity")
    key = db.create({"Property1": "Carlinhos", "Prop2": 2, "Prop3": True})

    entity = db.get(key.id)
    assert entity is not None
    assert isinstance(entity["id"], int)
    assert entity["Property1"] == "Carlinhos"
    assert entity["Prop2"] == 2
    assert entity["Prop3"]

    assert db.update(entity["id"], {"Prop2": 22})
    entity = db.get(key.id)
    assert entity["Prop2"] == 22

    db.delete(entity["id"])

    # make sure there is registry was deleted
    assert db.get(entity["id"]) is None


@pytest.mark.skip()
def test_get():
    db = BaseDB("TestEntity")
    entities = db.get_all()
    assert len(entities) == 3
    assert list(entities[0].keys()) == ["id", "age", "color", "name"]

    entities = db.get_all(limit=2)
    assert len(entities) == 2
