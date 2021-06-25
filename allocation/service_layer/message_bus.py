from __future__ import annotations
import logging
import inspect
from typing import Callable, Dict, List, Union, Type
import importlib.util

from allocation.domain import commands, events
from allocation.service_layer import handlers, unit_of_work
from allocation.adapters.transactionnal import AbstractTransactional

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


class MessageBus:
    """
    Allocation internal event loop
    """

    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message = None) -> object:
        self.queue = [message]
        returned_object = None

        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                result = self.handle_command(message)
                if not returned_object:
                    returned_object = result
            else:
                raise Exception(f"{message} was not an Event or Command")

        return returned_object

    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    def handle_command(self, command: commands.Command) -> object:
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            command_result = handler(command)
            self.queue.extend(self.uow.collect_new_events())
            return command_result

        except Exception:
            logger.exception("Exception handling command %s", command)
            raise


def service_bus_factory(
    uow: unit_of_work.AbstractUnitOfWork,
    transactional=AbstractTransactional,
    start_orm: bool = True,
) -> MessageBus:

    dependencies = {
        "uow": uow,
        "transactional": transactional,
    }

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    """
    Helper to inject the adapter dependencies to the function handlers according to their signature
    """
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)


def load_config(file_path: str):
    """Helper to load config file as module"""
    spec = importlib.util.spec_from_file_location("config", file_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config
