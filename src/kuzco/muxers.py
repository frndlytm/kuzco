import queue

from . import IMuxer, Message, MessageStream, Primitive


class Recurrent(IMuxer):
    def __init__(self, wrapped: IMuxer, *args, **kwargs):
        self.wrapped = wrapped
        self.queue = queue.Queue(*args, **kwargs)

    def mux(self, message: Message) -> MessageStream:
        # Populate the queue with our first message
        self.queue.push(message)

        # Pull from the queue
        while not self.queue.is_empty():
            parent = self.queue.pop()

            # Process the wrapped muxer and push results
            # into the queue
            for child in self.wrapped(parent):
                self.queue.push(child)

            # Yield the processed message
            yield parent
