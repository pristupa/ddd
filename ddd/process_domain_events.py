from typing import Iterable

from ddd import DomainEvent
from .domain_event_handler import handle_domain_event

MAXIMUM_RECURSION_DEPTH = 10


class MaximumRecursionException(Exception):
    pass


def process_domain_events(domain_events: Iterable[DomainEvent]):
    for domain_event in domain_events:
        handle_domain_event(domain_event)
