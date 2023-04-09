from abc import ABC, abstractmethod
from functools import singledispatchmethod
from typing import Generic, Iterable

from ._types import Message, MessageStream


class IAggregator(ABC):
    @abstractmethod
    def aggregate(self, messages: MessageStream) -> Message:
        raise NotImplementedError()

    def __call__(self, messages: MessageStream) -> Message:
        return self.aggregate(messages)


class IFilter(ABC):
    @abstractmethod
    def filter_(self, messages: MessageStream) -> MessageStream:
        raise NotImplementedError()

    def __call__(self, messages: MessageStream) -> MessageStream:
        yield from self.filter_(messages)


class IMuxer(ABC):
    @abstractmethod
    def mux(self, message: Message) -> MessageStream:
        raise NotImplementedError()

    def __call__(self, message: Message) -> MessageStream:
        yield from self.mux(message)


class ITransformer(ABC):
    @abstractmethod
    def transform(self, message: Message) -> Message:
        raise NotImplementedError()

    def __call__(self, message: Message) -> Message:
        return self.transform(message)
