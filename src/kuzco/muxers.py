import queue

from . import Channel, IMuxer, Message


class Recurrent(IMuxer):
    def __init__(self, wrapped: IMuxer, *args, **kwargs):
        self.wrapped = wrapped
        self.queue = queue.Queue(*args, **kwargs)

    def mux(self, message: Message) -> Channel:
        # Populate the queue with our first message
        for child in self.wrapped(message):
            self.queue.put(child)

        # Pull from the queue
        while not self.queue.empty():
            parent = self.queue.get()

            # Process the wrapped muxer and push results
            # into the queue
            for child in self.wrapped(parent):
                self.queue.put(child)

            # Yield the processed message
            yield parent
