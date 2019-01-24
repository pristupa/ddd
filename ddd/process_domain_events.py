from typing import Iterable

from .domain_event_collection import DomainEventCollection
from .domain_event_handler import handle_domain_event
from .entity import Entity

MAXIMUM_RECURSION_DEPTH = 10


class MaximumRecursionException(Exception):
    pass


def process_domain_events(entities: Iterable[Entity], domain_events: DomainEventCollection = None):
    depth = 0
    while True:
        for entity in entities:
            for domain_event in entity.domain_events:
                handle_domain_event(domain_event)
            entity.domain_events.clear()

        if domain_events:
            for domain_event in domain_events:
                handle_domain_event(domain_event)
            domain_events.clear()

        depth += 1
        if depth > MAXIMUM_RECURSION_DEPTH:
            raise MaximumRecursionException()
