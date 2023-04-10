from . import IFilter, Message, MessageStream


class Include(IFilter):
    def __init__(self, condition: Callable[[Message], bool]):
        self.condition = condition

    def filter_(self, messages: MessageStream) -> MessageStream:
        for message in messages:
            if self.condition(message):
                yield message


class Exclude(IFilter):
    def __init__(self, condition: Callable[[Message], bool]):
        self.condition = condition

    def filter_(self, messages: MessageStream) -> MessageStream:
        for message in messages:
            if not self.condition(message):
                yield message


class Map(IFilter):
    def __init__(self, f: Callable[[Message], Message]):
        self.f = f

    def filter_(self, messages: MessageStream) -> MessageStream:
        for message in messages:
            yield self.f(message)


def isiterable(x: Any) -> bool:
    return isinstance(x, Iterable)


def flatten(xs: Sequence) -> Sequence:
    for x in xs:
        if isinstance(x, Message): yield x
        elif isiterable(x): yield from x
        else: raise ValueError("Primitives not streamable")


class Flatten(IFilter):
    def filter_(self, messages: MessageStream) -> MessageStream:
        yield from flatten(messages)
