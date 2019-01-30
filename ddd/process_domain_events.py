from itertools import chain
from typing import Iterable

from .domain_event_collection import DomainEventCollection
from .domain_event_handler import handle_domain_event

MAXIMUM_RECURSION_DEPTH = 10


class MaximumRecursionException(Exception):
    pass


def process_domain_events(*collections: Iterable[DomainEventCollection]):
    depth = 0
    found_domain_events = True

    while found_domain_events:
        found_domain_events = False

        for domain_event in chain.from_iterable(collections):
            handle_domain_event(domain_event)
            found_domain_events = True

        depth += 1
        if depth > MAXIMUM_RECURSION_DEPTH:
            raise MaximumRecursionException()
