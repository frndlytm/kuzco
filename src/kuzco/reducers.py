from ._interfaces import IReducer
from ._types import Channel, Message


class Collect(IReducer):
    def reduce(self, channel: Channel) -> Message:
        return list(channel)
