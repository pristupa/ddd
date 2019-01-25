from typing import Iterable

from .aggregate_root import AggregateRoot
from .domain_event_collection import DomainEventCollection
from .domain_event_handler import handle_domain_event

MAXIMUM_RECURSION_DEPTH = 10


class MaximumRecursionException(Exception):
    pass


def process_domain_events(aggregates: Iterable[AggregateRoot], additional_domain_events: DomainEventCollection = None):
    depth = 0
    while True:
        domain_events = []

        for aggregate in aggregates:
            domain_events.extend(aggregate.domain_events)
            aggregate.domain_events.clear()

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
