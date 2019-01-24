import uuid

from .domain_event_collection import DomainEventCollection


class Entity:
    def __init__(self, id_: uuid.UUID):
        super().__init__()
        self.id = id_
        self.domain_events = DomainEventCollection()
