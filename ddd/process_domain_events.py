from typing import Iterable

from .domain_event_collection import DomainEventCollection
from .domain_event_handler import handle_domain_event
from .entity import Entity

MAXIMUM_RECURSION_DEPTH = 10


class MaximumRecursionException(Exception):
    pass


def process_domain_events(entities: Iterable[Entity], additional_domain_events: DomainEventCollection = None):
    depth = 0
    while True:
        domain_events = []

        for entity in entities:
            domain_events.extend(entity.domain_events)
            entity.domain_events.clear()

        if additional_domain_events:
            domain_events.extend(additional_domain_events)
            additional_domain_events.clear()

        if not domain_events:
            break

        for domain_event in domain_events:
            handle_domain_event(domain_event)

        depth += 1
        if depth > MAXIMUM_RECURSION_DEPTH:
            raise MaximumRecursionException()
