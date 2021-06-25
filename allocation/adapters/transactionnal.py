from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class AbstractTransactional(ABC):
    """
    Abstract class for all transactionnal service adapters
    """

    @abstractmethod
    def send_message(self, message):
        pass


class NullTransactionnal(AbstractTransactional):
    def send_message(self, message):
        logger.info(message)
