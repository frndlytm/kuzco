from typing import Callable

from ._interfaces import IFilter
from ._types import Channel, Message


class Include(IFilter):
    def __init__(self, condition: Callable[[Message], bool]):
        self.condition = condition

    async def filter_(self, channel: Channel) -> Channel:
        async for message in channel:
            if self.condition(message):
                yield message


class Exclude(IFilter):
    def __init__(self, condition: Callable[[Message], bool]):
        self.condition = condition

    async def filter_(self, channel: Channel) -> Channel:
        async for message in channel:
            if not self.condition(message):
                yield message


class Map(IFilter):
    def __init__(self, f: Callable[[Message], Message]):
        self.f = f

    async def filter_(self, channel: Channel) -> Channel:
        async for message in channel:
            yield self.f(message)


class Flatten(IFilter):
    async def filter_(self, channel: Channel) -> Channel:
        async for message in channel:
            if isinstance(message, dict):
                yield message
            elif isinstance(message, list):
                for submessage in message:
                    yield submessage
            else:
                raise ValueError("Primitives not streamable")

