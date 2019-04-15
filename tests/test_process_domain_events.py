import inspect
import uuid

import pytest

from ddd import AggregateRoot
from ddd import DomainEvent
from ddd import DomainEvents
from ddd import Entity
from ddd import domain_event_handler
from ddd import process_domain_events
from ddd.domain_event_handler import delete_domain_event_handler
from ddd.domain_event_handler import get_instance_getter
from ddd.domain_event_handler import set_instance_getter
from ddd.process_domain_events import MaximumRecursionException


@pytest.fixture
def empty_handler():
    class Handler:

        @domain_event_handler
        def empty_handle(self, domain_event: DomainEvent):
            pass

    yield Handler
    delete_domain_event_handler(DomainEvent)


class Aggregate(Entity, AggregateRoot):
    pass


class RecursiveDomainEvent(DomainEvent):

    def __init__(self, owner, entity):
        self.owner = owner
        self.entity = entity


@pytest.fixture
def recursive_handler():
    class Handler:

        @domain_event_handler
        def recursive_handler(self, domain_event: RecursiveDomainEvent):
            new_domain_event = RecursiveDomainEvent(domain_event.entity, domain_event.owner)
            domain_event.entity.domain_events.register(new_domain_event)

    yield Handler
    delete_domain_event_handler(RecursiveDomainEvent)


@pytest.fixture
def instance_getter():
    def instance_getter(cls):
        return cls()

    old_instance_getter = get_instance_getter()
    set_instance_getter(instance_getter)
    yield
    set_instance_getter(old_instance_getter)


def create_domain_events_collector(*aggregate_roots: AggregateRoot):
    def take_domain_events():
        domain_events = []
        for aggregate_root in aggregate_roots:
            domain_events.extend(aggregate_root.domain_events)
            aggregate_root.clear_domain_events()
        return domain_events
    return take_domain_events


def test_not_going_to_infinite_loop_for_empty_domain_events():
    process_domain_events(lambda: [])


def test_not_going_to_infinite_loop_for_entities(empty_handler):
    aggregate = Aggregate(id_=uuid.uuid4())
    domain_event = DomainEvent()
    aggregate.domain_events.register(domain_event)
    assert inspect.isfunction(empty_handler.empty_handle)
    assert domain_event in aggregate.domain_events
    process_domain_events(create_domain_events_collector(aggregate))


@pytest.mark.usefixtures("empty_handler")
def test_not_going_to_infinite_loop_for_additional_domain_events():
    domain_events = DomainEvents()
    domain_events.register(DomainEvent())

    def domain_event_collector():
        domain_events_copy = list(domain_events)
        domain_events.clear()
        return domain_events_copy
    process_domain_events(domain_event_collector)


@pytest.mark.usefixtures("recursive_handler")
def test_recursive_domain_events():
    aggregate1 = Aggregate(id_=uuid.uuid4())
    aggregate2 = Aggregate(id_=uuid.uuid4())
    domain_event1 = RecursiveDomainEvent(aggregate1, aggregate2)
    domain_event2 = RecursiveDomainEvent(aggregate2, aggregate1)
    aggregate1.domain_events.register(domain_event1)
    aggregate2.domain_events.register(domain_event2)

    with pytest.raises(MaximumRecursionException):
        process_domain_events(create_domain_events_collector(aggregate1, aggregate2))


@pytest.mark.usefixtures("instance_getter")
def test_instance_set():
    process_domain_events(lambda: [])
