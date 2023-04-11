from itertools import filterfalse
from typing import Callable

from ._interfaces import IFilter
from ._types import Channel, Message


class Include(IFilter):
    def __init__(self, condition: Callable[[Message], bool]):
        self.condition = condition

    def filter_(self, channel: Channel) -> Channel:
        yield from filter(self.condition, channel)


class Exclude(IFilter):
    def __init__(self, condition: Callable[[Message], bool]):
        self.condition = condition

    def filter_(self, channel: Channel) -> Channel:
        yield from filterfalse(self.condition, channel)


class Map(IFilter):
    def __init__(self, f: Callable[[Message], Message]):
        self.f = f

    def filter_(self, channel: Channel) -> Channel:
        yield from map(self.f, channel)


class Flatten(IFilter):
    def filter_(self, channel: Channel) -> Channel:
        for message in channel:
            if isinstance(message, dict):
                yield message
            elif isinstance(message, list):
                for submessage in message:
                    yield submessage
            else:
                raise ValueError("Primitives not streamable")
