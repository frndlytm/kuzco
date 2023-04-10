from functools import reduce
from typing import Callable

from . import ITransformer, Message
from .util import compose


class Identity(ITransformer):
    def transform(self, message: Message) -> Message:
        return message


class Apply(ITransformer):
    def __init__(self, f: Callable[[Message], Message]):
        self.f = f

    def transform(self, message: Message) -> Message:
        return self.f(message)


class Composite(ITransformer):
    def __init__(self, root: ITransformer, **components):
        self.root = root
        self.components = dict(components)

    def add(self, key: str, transform: ITransformer) -> "Composite":
        self.components[key] = transform
        return self

    def transform(self, message: Message) -> Message:
        return dict(
            self.root(message), **{
                key: transform(message)
                for key, transform in self.components.items()
            }
        )


class Chain(ITransformer):
    def __init__(self, *steps: ITransformer):
        self.steps = [Identity(), *steps]
        self._transform = reduce(compose, self.steps)

    def then(self, step: ITransformer) -> "Chain":
        self.steps.append(step)
        self._transform = reduce(compose, self.steps)
        return self

    def transform(self, message: Message) -> Message:
        return self._transform(message)
