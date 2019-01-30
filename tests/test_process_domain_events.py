import inspect
import uuid

import pytest

from ddd import DomainEvent
from ddd import DomainEventCollection
from ddd import Entity
from ddd import domain_event_handler
from ddd import process_domain_events
from ddd.domain_event_collection import DomainEvents
from ddd.domain_event_collection import Locked
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


class Aggregate(Entity):
    domain_events = DomainEvents()


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


def test_not_going_to_infinite_loop_for_empty_domain_events():
    process_domain_events()


def test_not_going_to_infinite_loop_for_entities(empty_handler):
    aggregate = Aggregate(id_=uuid.uuid4())
    domain_event = DomainEvent()
    aggregate.domain_events.register(domain_event)
    assert inspect.isfunction(empty_handler.empty_handle)
    assert domain_event in aggregate.domain_events
    process_domain_events(aggregate.domain_events)


@pytest.mark.usefixtures("empty_handler")
def test_not_going_to_infinite_loop_for_additional_domain_events():
    domain_event_collection = DomainEventCollection()
    domain_event_collection.register(DomainEvent())
    process_domain_events(domain_event_collection)


def test_try_handle_event_without_handler():
    domain_event_collection = DomainEventCollection()
    domain_event_collection.register(DomainEvent())

    with pytest.raises(ValueError):
        process_domain_events(domain_event_collection)


def test_try_set_domain_events_for_entity_with_domain_events():
    aggregate = Aggregate(uuid.uuid4())
    with pytest.raises(AttributeError):
        aggregate.domain_events = []
    assert isinstance(Aggregate.domain_events, DomainEvents)


@pytest.mark.usefixtures("recursive_handler")
def test_adding_domain_event_during_iteration_domain_events():
    aggregate = Aggregate(id_=uuid.uuid4())
    domain_event = RecursiveDomainEvent(aggregate, aggregate)
    aggregate.domain_events.register(domain_event)

    with pytest.raises(Locked):
        process_domain_events(aggregate.domain_events)


@pytest.mark.usefixtures("recursive_handler")
def test_recursive_domain_events():
    aggregate1 = Aggregate(id_=uuid.uuid4())
    aggregate2 = Aggregate(id_=uuid.uuid4())
    domain_event1 = RecursiveDomainEvent(aggregate1, aggregate2)
    domain_event2 = RecursiveDomainEvent(aggregate2, aggregate1)
    aggregate1.domain_events.register(domain_event1)
    aggregate2.domain_events.register(domain_event2)

    with pytest.raises(MaximumRecursionException):
        process_domain_events(aggregate1.domain_events, aggregate2.domain_events)


@pytest.mark.usefixtures("instance_getter")
def test_instance_set():
    process_domain_events()