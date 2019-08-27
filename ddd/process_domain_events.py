from typing import Iterable

from ddd import DomainEvent
from .domain_event_handler import handle_domain_events

MAXIMUM_RECURSION_DEPTH = 10


class MaximumRecursionException(Exception):
    pass


def process_domain_events(domain_events: Iterable[DomainEvent]):
    domain_events_map = {}

    for domain_event in domain_events:
        domain_event_class = type(domain_event)
        typed_domain_events = domain_events_map.setdefault(domain_event_class, [])
        typed_domain_events.append(domain_event)

    for domain_event_class, typed_domain_events in domain_events_map.items():
        handle_domain_events(domain_event_class, typed_domain_events)
