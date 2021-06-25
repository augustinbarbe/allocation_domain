from dataclasses import dataclass
from uuid import UUID


class Event:
    pass


@dataclass
class Allocated(Event):
    allocation_id: UUID
    resource_id: UUID
    quantity: int
    pool_id: UUID


@dataclass
class UnavailableResource(Event):
    resource_id: UUID


@dataclass
class Deallocated(Event):
    allocation_id: UUID
    resource_id: UUID
    aquantity: int
    pool_id: UUID


@dataclass
class Unavailable(Event):
    resource_id: UUID
