from ddd import DomainEvent
from ddd.domain_event_queue import DomainEventQueue


def test_new_domain_event_collection_is_empty():
    collection = DomainEventQueue()
    assert len(collection) == 0


def test_domain_event_collection_registers_events():
    collection = DomainEventQueue()
    event1 = DomainEvent()
    event2 = DomainEvent()
    collection.register(event1)
    collection.register(event2)
    assert len(collection) == 2
    assert list(collection) == [event1, event2]


def test_domain_event_collection_clears_events():
    collection = DomainEventQueue()
    collection.register(DomainEvent())
    collection.register(DomainEvent())
    list(collection)  # Empty handle all events
    assert len(collection) == 0
