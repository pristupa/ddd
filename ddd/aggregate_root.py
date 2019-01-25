from .domain_event_collection import DomainEventCollection


class AggregateRoot:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._domain_events: DomainEventCollection = None

    @property
    def domain_events(self) -> DomainEventCollection:
        if getattr(self, '_domain_events', None) is None:
            self._domain_events = DomainEventCollection()
        return self._domain_events
