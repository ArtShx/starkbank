from google.cloud import datastore
from google.auth.exceptions import DefaultCredentialsError

from ..exceptions import ErrorGoogleAuth, InvalidEntity


class BaseDB:
    """
    Base class for DB handler.
    TODO: make it abstract and make implementation for each Entity.
    """

    try:
        client = datastore.Client()
    except DefaultCredentialsError as e:
        raise ErrorGoogleAuth(str(e))

    def __init__(self, entity: str) -> None:
        if not isinstance(entity, str) and entity != "":
            raise InvalidEntity(f"Invalid entity: {entity}")

        self._entity = entity

    def create(self, properties: dict):
        key = self.client.key(self._entity)
        entity = datastore.Entity(key=key)
        entity.update(properties)
        self.client.put(entity)
        return entity.key

    def get(self, entity_id: str):
        key = self.client.key(self._entity, entity_id)
        entity = self.client.get(key)
        if entity:
            return self._parse_entity(entity)
        return None

    @staticmethod
    def _parse_entity(entity) -> dict:
        data = {"id": entity.id}
        for key, val in entity.items():
            data[key] = val
        return data

    def get_all(self, limit=100) -> list:
        """Returns all entities from this kind up to `limit`"""
        query = self.client.query(kind=self._entity)
        return [self._parse_entity(x) for x in query.fetch(limit=limit)]

    def update(self, entity_id: str, properties: dict):
        key = self.client.key(self._entity, entity_id)
        entity = self.client.get(key)
        if entity is not None:
            entity.update(properties)
            self.client.put(entity)
            return True
        return False

    def delete(self, entity_id: str):
        key = self.client.key(self._entity, entity_id)
        self.client.delete(key)
