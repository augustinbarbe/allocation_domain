from allocation.service_layer.message_bus import service_bus_factory
from allocation.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from allocation.adapters.transactionnal import NullTransactionnal
from allocation.domain.commands import Command


class ServiceAdapter:
    def init(self, config):
        uow = SqlAlchemyUnitOfWork(config.get("SQLALCHEMY_DATABASE_URI"))
        transactional = NullTransactionnal()
        self.message_bus = service_bus_factory(uow, transactional)

    def handle(self, command: Command):
        return self.message_bus.handle(command)


service = ServiceAdapter()
