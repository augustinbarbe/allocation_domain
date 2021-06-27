from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID
from typing import List, Optional
import datetime

from allocation.domain import events


class Resource:
    def __init__(
        self,
        resource_id: UUID,
        pools: List[Pool],
    ):
        self.resource_id = resource_id
        self.pools = pools
        self.events = []  # type: List[events.Event]

    def allocate(self, request: Request) -> UUID:
        try:
            pool = next(b for b in sorted(self.pools) if b.can_allocate(request))
            pool.allocate(request)
            self.events.append(
                events.Allocated(
                    resource_id=request.resource_id,
                    quantity=request.quantity,
                    allocation_id=request.request_id,
                    pool_id=pool.pool_id,
                )
            )
            return request.request_id

        except StopIteration:
            self.events.append(events.UnavailableResource(request.resource_id))
            return None

    def change_pool_quantity(self, pool_id: str, quantity: int):
        pool = next(b for b in self.pools if b.pool_id == pool_id)
        pool._allocated_quantity = quantity
        while pool.available_quantity < 0:
            request = pool.deallocate_one()
            self.events.append(
                events.Deallocated(
                    request.request_id, request.resource_id, request.quantity
                )
            )

    @property
    def available_quantity(self):
        return sum([pool.available_quantity for pool in self.pools])


class Pool:
    def __init__(self, resource_id: UUID, quantity: int, eta: Optional[datetime]):
        self.resource_id = resource_id
        self.quantity = quantity
        self._allocations = set()  # type Set[Request]
        self.eta = eta

    def __repr__(self):
        return f"<Pool {self.pool_id}>"

    def __eq__(self, other):
        if not isinstance(other, Pool):
            return False
        return other.pool_id == self.pool_id

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other: Pool):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, request: Request):
        if self.can_allocate(request):
            self._allocations.add(request)

    def deallocate_one(self) -> Request:
        return self._allocations.pop()

    @property
    def allocated_quantity(self) -> int:
        return sum(request.quantity for request in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.allocated_quantity

    def can_allocate(self, request: Request) -> bool:
        return (
            self.resource_id == request.resource_id and self.available_quantity >= request.quantity
        )


@dataclass(unsafe_hash=True)
class Request:
    resource_id: UUID
    quantity: int
