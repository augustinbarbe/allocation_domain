import abc
import time
import logging
from google.cloud import pubsub

logger = logging.getLogger(__name__)


class AbstractPubSub(abc.ABC):
    @abc.abstractmethod
    def listen(self, *args):
        raise NotImplementedError


class NullPubSub(AbstractPubSub):
    def listen(self):
        while True:
            time.sleep(1)


class GooglePubSub(AbstractPubSub):
    def __init__(self, project_id: str, subscription: str, topic: str):
        self.project_id = project_id
        self.subscription = subscription
        self.topic = topic

    def listen(self, callback):
        with pubsub.SubscriberClient() as subscriber:
            subscription_path = subscriber.subscription_path(
                self.project_id, self.subscription
            )

            def _acknoledge_message(message):
                callback(message)
                message.ack()
                logger.debug("Message processed, acknowledging")

            future = subscriber.subscribe(subscription_path, _acknoledge_message)

            try:
                future.result()
            except Exception as e:
                logger.error(e)
                raise
