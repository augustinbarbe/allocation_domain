import os
from datetime import datetime
import logging

from sumo.service_layer.message_bus import service_bus_factory, load_config
from sumo.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from sumo.domain import commands
from sumo.adapters.transactionnal import SendGridTransactionnal
from sumo.adapters.authorization import Auth0Authorization
from sumo.adapters.storage import GoogleObjectStorage
from sumo.adapters.pubsub import GooglePubSub
from sumo.adapters.notifier import FirebaseNotification

logger = logging.getLogger(__name__)

config = load_config(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../config/api.py")
)

uow = SqlAlchemyUnitOfWork(config.SQLALCHEMY_DATABASE_URI)
transactional = SendGridTransactionnal(config.SENDGRID_API_KEY)
authorization = Auth0Authorization(
    config.AUTH0_DOMAIN, config.AUTH0_CLIENT_ID, config.AUTH0_CLIENT_SECRET
)
object_storage = GoogleObjectStorage(document_storage_name=config.DOCUMENT_STORAGE_NAME)
notification = FirebaseNotification()


service_bus = service_bus_factory(
    uow, transactional, authorization, object_storage, notification
)


def handle_message_bus(message):
    received_at = datetime.now()
    service_bus.handle(commands.RemindPatient(received_at=received_at))


if __name__ == "__main__":
    sumo_sub = GooglePubSub(
        project_id=config.GCP_PUBSUB_PROJECT,
        subscription=config.GCP_PUBSUB_SUB,
        topic=config.GCP_PUBSUB_TOPIC,
    )
    sumo_sub.listen(handle_message_bus)
