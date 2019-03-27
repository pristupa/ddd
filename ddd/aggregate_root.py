from .domain_event_queue import DomainEvents


class AggregateRoot:
    domain_events = DomainEvents()

