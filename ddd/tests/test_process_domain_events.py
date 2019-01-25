import uuid

from ddd import DomainEvent
from ddd import DomainEventCollection
from ddd import Entity
from ddd import process_domain_events


def test_not_going_to_infinite_loop_for_empty_domain_events():
    process_domain_events(entities=[])


def test_not_going_to_infinite_loop_for_entities():
    entity = Entity(uuid.uuid4())
    entity.domain_events.register(DomainEvent())
    process_domain_events(entities=[entity])


def test_not_going_to_infinite_loop_for_additional_domain_events():
    additional_domain_events = DomainEventCollection()
    additional_domain_events.register(DomainEvent())
    process_domain_events(entities=[], additional_domain_events=additional_domain_events)
