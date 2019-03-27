import collections
from typing import Iterator
from typing import List

from .domain_event import DomainEvent


class Locked(Exception):
    pass


class DomainEvents:

    def __init__(self):
        self.field = None

    def __get__(self, instance, owner):
        if instance is None:
            return self

        queue = instance.__dict__.get(self.field)

        if queue is None:
            instance.__dict__[self.field] = queue = DomainEventQueue()

        return queue

    def __set__(self, instance, value):
        raise AttributeError("Сan't set attribute")

    def __set_name__(self, owner, name):
        self.field = name


class DomainEventQueue(collections.abc.Collection):

    def __init__(self):
        self._events: List[DomainEvent] = []
        self._locked = False

    def register(self, event: DomainEvent):
        if self._locked:
            raise Locked('You can not register events during the iteration')
        self._events.append(event)

    def __contains__(self, event: DomainEvent) -> bool:
        return event in self._events

    def __iter__(self) -> Iterator[DomainEvent]:
        if self._locked:
            raise Locked('You can not iterate multiple times simultaneously')
        self._locked = True
        yield from self._events
        self._events.clear()
        self._locked = False

    def __len__(self) -> int:
        return len(self._events)
