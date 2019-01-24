import collections
from typing import Iterator
from typing import List


class DomainEventCollection(collections.abc.Collection):
    def __init__(self):
        self._events: List[object] = []

    def register(self, event: object):
        self._events.append(event)

    def clear(self) -> None:
        self._events.clear()

    def __contains__(self, event: object) -> bool:
        return event in self._events

    def __iter__(self) -> Iterator[object]:
        return iter(self._events)

    def __len__(self) -> int:
        return len(self._events)
