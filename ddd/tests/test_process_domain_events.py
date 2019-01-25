import uuid

from ddd import AggregateRoot
from ddd import DomainEvent
from ddd import DomainEventCollection
from ddd import Entity
from ddd import process_domain_events


class MyAggregate(AggregateRoot, Entity):
    pass


def test_not_going_to_infinite_loop_for_empty_domain_events():
    process_domain_events(aggregates=[])


def test_not_going_to_infinite_loop_for_entities():
    aggregate = MyAggregate(id_=uuid.uuid4())
    aggregate.domain_events.register(DomainEvent())
    process_domain_events(aggregates=[aggregate])


def test_not_going_to_infinite_loop_for_additional_domain_events():
    additional_domain_events = DomainEventCollection()
    additional_domain_events.register(DomainEvent())
    process_domain_events(aggregates=[], additional_domain_events=additional_domain_events)
