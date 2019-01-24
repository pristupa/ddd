from ddd.domain_event_collection import DomainEventCollection


def test_new_domain_event_collection_is_empty():
    collection = DomainEventCollection()
    assert len(collection) == 0


def test_domain_event_collection_registers_events():
    collection = DomainEventCollection()
    event1 = object()
    event2 = object()
    collection.register(event1)
    collection.register(event2)
    assert len(collection) == 2
    assert list(collection) == [event1, event2]


def test_domain_event_collection_clears_events():
    collection = DomainEventCollection()
    collection.register(object())
    collection.register(object())
    collection.clear()
    assert len(collection) == 0
    assert list(collection) == []
