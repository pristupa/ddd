from .domain_events import DomainEvents


class AggregateRoot:
    def __init__(self):
        super().__init__()
        self.domain_events = DomainEvents()

    def clear_domain_events(self):
        self.domain_events.clear()
