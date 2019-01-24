from typing import Callable
from typing import Type
from typing import TypeVar

T = TypeVar('T')

_instance_getter: Callable[[Type[T]], T] = lambda cls: cls()


def get_instance(cls: Type[T]) -> T:
    return _instance_getter(cls)


def set_instance_getter(func: Callable[[Type[T]], T]):
    global _instance_getter
    _instance_getter = func
