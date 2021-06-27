import os
from datetime import datetime
import logging

from allocation.service_layer.message_bus import service_bus_factory
from allocation.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from allocation.adapters.transactionnal import NullTransactionnal
from allocation.adapters.pubsub import GooglePubSub
from allocation.domain import commands
from allocation.utils import load_config

logger = logging.getLogger(__name__)


config = load_config(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../config/api.py")
)

uow = SqlAlchemyUnitOfWork(config.get("SQLALCHEMY_DATABASE_URI"))
transactional = NullTransactionnal()
service_bus = service_bus_factory(uow, transactional)


def handle_message_bus(message):
    received_at = datetime.now()
    logger.info(f"message received at {received_at}")
    command = message_adapter(message)
    service_bus.handle(command)


def message_adapter(message):
    """Return the instance command from the pubsub message"""
    # TODO : allow multiple commands
    return commands.ChangePoolQuantity(**message)


if __name__ == "__main__":
    allocation_subscriber = GooglePubSub(
        project_id=config.GCP_PUBSUB_PROJECT,
        subscription=config.GCP_PUBSUB_SUB,
        topic=config.GCP_PUBSUB_TOPIC,
    )
    allocation_subscriber.listen(handle_message_bus)
