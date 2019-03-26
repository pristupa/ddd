import inspect
from collections import defaultdict
from threading import Lock
from typing import Callable
from typing import Type
from typing import TypeVar
import warnings

from .domain_event import DomainEvent

T = TypeVar('T')

_instance_getter: Callable[[Type[T]], T] = lambda cls: cls()
_domain_event_handlers = defaultdict(list)


# noinspection PyPep8Naming
class domain_event_handler:
    """Decorator for method in class"""

    def __init__(self, method):
        self._method = method
        func_spec = inspect.getfullargspec(self._method)

        if len(func_spec.args) != 2:  # One argument and self
            raise AssertionError(
                f'Method must have only 1 arguments: {method.__qualname__}. Count arguments : {len(func_spec.args) - 1}'
            )
        domain_event_class: Type[DomainEvent] = func_spec.annotations[func_spec.args[1]]

        if not inspect.isclass(domain_event_class):
            raise AssertionError('First argument must have annotation and this annotation must be class')
        self._domain_event_class = domain_event_class

    def __get__(self, instance, owner):
        return self._method.__get__(instance, owner)

    def __set_name__(self, owner, name):
        with Lock():
            _domain_event_handlers[self._domain_event_class].append((owner, self._method))


def handle_domain_event(domain_event: DomainEvent) -> None:
    domain_event_class = type(domain_event)
    if domain_event_class not in _domain_event_handlers:
        warnings.warn(f'Unknown domain event {domain_event_class}. Please register at least one domain event handler')
    for handler_cls, handler in _domain_event_handlers[domain_event_class]:
        handler_instance = _instance_getter(handler_cls)
        handler(handler_instance, domain_event)


def delete_domain_event_handler(cls):
    with Lock():
        del _domain_event_handlers[cls]


def get_instance_getter():
    return _instance_getter


def set_instance_getter(func: Callable[[Type[T]], T]):
    global _instance_getter
    _instance_getter = func
