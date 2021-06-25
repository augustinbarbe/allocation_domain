import uuid
import logging
from sqlalchemy import (
    Table,
    Integer,
    MetaData,
    Column,
    DateTime,
    ForeignKey,
    event,
)
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.dialects.postgresql import UUID

from allocation.domain import models


logger = logging.getLogger(__name__)


metadata = MetaData()

requests = Table(
    "request",
    metadata,
    Column(
        "request_id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    ),
    Column("resource_id", ForeignKey("resource.resource_id")),
    Column("quantity", Integer, nullable=False),
)


resources = Table(
    "resource",
    metadata,
    Column(
        "resource_id",
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
    ),
)

allocations = Table(
    "allocation",
    metadata,
    Column(
        "allocation_id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    ),
    Column("request_id", ForeignKey("request.request_id")),
    Column("pool_id", ForeignKey("pool.pool_id")),
)

pools = Table(
    "pool",
    metadata,
    Column(
        "pool_id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    ),
    Column("resource_id", ForeignKey("resource.resource_id")),
    Column("quantity", Integer, nullable=False),
    Column("eta", DateTime, nullable=True),
)


def start_mappers():
    logger.info("Starting mappers")
    request_mapper = mapper(models.Request, requests)
    pool_mapper = mapper(
        models.Pool,
        pools,
        properties={
            "_allocations": relationship(
                request_mapper,
                secondary=allocations,
                collection_class=set,
                lazy="joined",
            )
        },
    )
    mapper(
        models.Resource,
        resources,
        properties={"pools": relationship(pool_mapper, lazy="joined")},
    )


@event.listens_for(models.Resource, "load")
def receive_study(study, _):
    study.events = []
