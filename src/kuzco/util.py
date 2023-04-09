from typing import Callable


def compose(f: Callable, g: Callable) -> Callable:
    def h(*args, **kwargs):
        return g(f(*args, **kwargs))
    return h
