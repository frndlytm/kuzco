from typing import Any, Callable, Iterable, Sequence

from ._types import Channel, Message


def compose(f: Callable, g: Callable) -> Callable:
    def h(*args, **kwargs):
        return g(f(*args, **kwargs))

    return h


def isiterable(x: Any) -> bool:
    return isinstance(x, Iterable)


def flatten(xs: Sequence) -> Sequence:
    for x in xs:
        if isinstance(x, Message):
            yield x
        elif isiterable(x):
            yield from x
        else:
            raise ValueError("Primitives not streamable")


def chan(*messages: Message) -> Channel:
    for message in messages:
        yield message
