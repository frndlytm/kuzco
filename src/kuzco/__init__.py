"""
Top-level package for Kuzco
"""
from ._interfaces import IFilter, IMuxer, IReducer, ITransformer
from ._types import Channel, Message, Primitive
from .util import chan

__author__ = "Christian J. DiMare-Baits"
__email__ = "frndlytm@gmail.com"
__version__ = "0.1.0"

__all__ = [
    "chan",
    "filters",
    "muxers",
    "reducers",
    "transformers",
    "util",

    # Interfaces
    "IFilter",
    "IMuxer",
    "ITransformer",
    "IReducer",

    # Types
    "Channel",
    "Message",
    "Primitive",
]
