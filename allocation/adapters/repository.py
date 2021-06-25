import abc
from typing import Set
from uuid import UUID

from allocation.domain.models import Resource, Pool


class AbstractRepository:
    def __init__(self):
        self.seen = set()  # type: Set[Resource]

    def add(self, resource: Resource):
        self._add(resource)
        self.seen.add(resource)

    def get_by_id(self, resource_id: UUID) -> Resource:
        resource = self._get_by_id(resource_id)
        if resource:
            self.seen.add(resource)
        return resource

    def get_by_pool_id(self, pool_id: UUID) -> Resource:
        resource = self._get_by_pool_id(pool_id)
        if resource:
            self.seen.add(resource)
        return resource

    @abc.abstractmethod
    def _add(self, resource: Resource):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, resource_id: UUID) -> Resource:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_pool_id(self, pool_id: UUID) -> Resource:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, resource):
        self.session.add(resource)

    def _get_by_id(self, resource_id: UUID) -> Resource:
        return self.session.query(Resource).filter_by(resource_id=resource_id).first()

    def _get_by_pool_id(self, pool_id: UUID) -> Resource:
        return self.session.query(Resource).join(Pool).filter(Pool.pool_id == pool_id).first()
