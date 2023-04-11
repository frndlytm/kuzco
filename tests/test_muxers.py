from kuzco import Channel, Message, IMuxer
from kuzco.muxers import Recurrent


class RecurrentLetterMuxer(IMuxer):
    def mux(self, message: Message) -> Channel:
        if not message.get("letter", None):
            for letter in message.get("world"):
                yield {**message, "letter": letter}


def test_recurrent(earth):
    mux = Recurrent(RecurrentLetterMuxer())
    assert list(mux(earth)) == [
        {"id": 3, "world": "Earth", "letter": "E"},
        {"id": 3, "world": "Earth", "letter": "a"},
        {"id": 3, "world": "Earth", "letter": "r"},
        {"id": 3, "world": "Earth", "letter": "t"},
        {"id": 3, "world": "Earth", "letter": "h"},
    ]
