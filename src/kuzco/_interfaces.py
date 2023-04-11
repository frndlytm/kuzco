from abc import ABC, abstractmethod

from ._types import Message, Channel

__all__ = ["IFilter", "IMuxer", "IReducer", "ITransformer"]


class IFilter(ABC):
    @abstractmethod
    def filter_(self, channel: Channel) -> Channel:
        raise NotImplementedError()

    def __call__(self, channel: Channel) -> Channel:
        yield from self.filter_(channel)


class IMuxer(ABC):
    @abstractmethod
    def mux(self, message: Message) -> Channel:
        raise NotImplementedError()

    def __call__(self, message: Message) -> Channel:
        yield from self.mux(message)


class IReducer(ABC):
    @abstractmethod
    def reduce(self, channel: Channel) -> Message:
        raise NotImplementedError()

    def __call__(self, channel: Channel) -> Message:
        return self.reduce(channel)


class ITransformer(ABC):
    @abstractmethod
    def transform(self, message: Message) -> Message:
        raise NotImplementedError()

    def __call__(self, message: Message) -> Message:
        return self.transform(message)
