# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime

from allocation.domain import exc
from allocation.utils import validate_uuid4


class Command:
    pass


@dataclass
class Allocate(Command):
    resource_id: UUID
    quantity: int

    def __post_init__(self):
        if self.quantity < 0:
            raise exc.UnprocessableEntity(f"Invalid pool quantity {self.quantity}")
        if not validate_uuid4(self.resource_id):
            raise exc.UnprocessableEntity(f"Invalid id format {self.resource_id}")
        self.resource_id = UUID(self.resource_id)


@dataclass
class CreatePool(Command):
    resource_id: UUID
    quantity: int
    eta: datetime

    def __post_init__(self):
        if self.quantity < 0:
            raise exc.UnprocessableEntity(f"Invalid pool quantity {self.quantity}")
        if not validate_uuid4(self.resource_id):
            raise exc.UnprocessableEntity(f"Invalid id format {self.resource_id}")
        self.resource_id = UUID(self.resource_id)


@dataclass
class ChangePoolQuantity(Command):
    pool_id: UUID
    quantity: int
