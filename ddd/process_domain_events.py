from typing import Callable
from typing import Iterable

from ddd import DomainEvent
from .domain_event_handler import handle_domain_event

MAXIMUM_RECURSION_DEPTH = 10


class MaximumRecursionException(Exception):
    pass


def process_domain_events(domain_events_collector: Callable[[], Iterable[DomainEvent]]):
    depth = 0
    while True:
        domain_events = domain_events_collector()
        if not domain_events:
            break

        for domain_event in domain_events:
            handle_domain_event(domain_event)

        depth += 1
        if depth > MAXIMUM_RECURSION_DEPTH:
            raise MaximumRecursionException()
