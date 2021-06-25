from __future__ import annotations
import abc
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from allocation.adapters import repository
from allocation.adapters.orm import start_mappers


class AbstractUnitOfWork(abc.ABC):
    resources = repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for item in self.resources.seen:
            while item.events:
                yield item.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, database_uri: str):
        session_factory = sessionmaker(
            create_engine(
                database_uri,
                isolation_level="REPEATABLE READ",
            ),
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
        )
        # engine.dialect.description_encoding = None
        self.session_factory = scoped_session(
            session_factory,
        )
        start_mappers()

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.resources = repository.SqlAlchemyRepository(self.session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()
        self.session.expunge_all()

    def rollback(self):
        self.session.rollback()
