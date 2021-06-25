# pylint: disable=unused-argument
from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict, Callable, Type

from allocation.domain import commands, events, models, exc
from allocation.service_layer import unit_of_work
from allocation.adapters import transactionnal


class InvalidResourceId(exc.EntityNotFound):
    pass


def add_pool(
    cmd: commands.CreatePool,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        resource = uow.resources.get_by_id(resource_id=cmd.resource_id)
        if resource is None:
            resource = models.Resource(resource_id=cmd.resource_id, pools=[])
            uow.resources.add(resource)

        resource.pools.append(models.Pool(resource.resource_id, cmd.quantity, cmd.eta))
        uow.commit()


def allocate(
    cmd: commands.Allocate,
    uow: unit_of_work.AbstractUnitOfWork,
):
    request = models.Request(cmd.resource_id, cmd.quantity)
    with uow:
        resource = uow.resources.get_by_id(resource_id=cmd.resource_id)
        if resource is None:
            raise InvalidResourceId(
                f"Invalid resource identifyer {request.resource_id}"
            )
        resource.allocate(request)
        uow.commit()


def reallocate(
    event: events.Deallocated,
    uow: unit_of_work.AbstractUnitOfWork,
):
    allocate(commands.Allocate(**asdict(event)), uow=uow)


def change_pool_quantity(
    cmd: commands.ChangePoolQuantity,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        resource = uow.products.get_by_pool_id(batchref=cmd.pool_id)
        resource.change_pool_quantity(pool_id=cmd.pool_id, quantity=cmd.quantity)
        uow.commit()


# pylint: disable=unused-argument


def send_unavailable_notification(
    event: events.Unavailable,
    notifications: transactionnal.AbstractNotifications,
):
    notifications.send(
        f"Resource {event.quantity} unavailable for {event.resource_id}",
    )


def publish_allocated_event(
    event: events.Allocated,
    publish: Callable,
):
    publish("line_allocated", event)


EVENT_HANDLERS = {
    events.Allocated: [publish_allocated_event],
    events.Deallocated: [reallocate],
    events.Unavailable: [send_unavailable_notification],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.Allocate: allocate,
    commands.CreatePool: add_pool,
    commands.ChangePoolQuantity: change_pool_quantity,
}  # type: Dict[Type[commands.Command], Callable]
