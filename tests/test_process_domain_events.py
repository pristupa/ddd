import pytest

from ddd import AggregateRoot
from ddd import DomainEvent
from ddd import Entity
from ddd import domain_event_handler
from ddd import process_domain_events
from ddd.domain_event_handler import delete_domain_event_handler
from ddd.domain_event_handler import get_instance_getter
from ddd.domain_event_handler import set_instance_getter


class CustomDomainEvent(DomainEvent):
    pass


@pytest.fixture
def empty_handler():
    class Handler:
        handled_domain_events = []

        @domain_event_handler
        def empty_handle(self, domain_event: CustomDomainEvent):
            self.handled_domain_events.append(domain_event)

    yield Handler()
    delete_domain_event_handler(CustomDomainEvent)


class Aggregate(Entity, AggregateRoot):
    pass


@pytest.fixture
def instance_getter():
    def instance_getter(cls):
        return cls()

    old_instance_getter = get_instance_getter()
    set_instance_getter(instance_getter)
    yield
    set_instance_getter(old_instance_getter)


@pytest.mark.usefixtures('instance_getter')
def test_process_domain_events(empty_handler):
    domain_event = CustomDomainEvent()

    # Act
    process_domain_events([domain_event])

    # Assert
    assert empty_handler.handled_domain_events == [domain_event]