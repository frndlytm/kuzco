"""
Top-level package for Kuzco
"""
from ._interfaces import IAggregator, IFilter, IMuxer, ITransformer
from ._types import Message, MessageStream, Primitive

__author__ = "Christian J. DiMare-Baits"
__email__ = "frndlytm@gmail.com"
__version__ = "0.1.0"

__all__ = [
    "aggregators",
    "filters",
    "muxers",
    "transformers",
    "util",
    "IAggregator",
    "IFilter",
    "IMuxer",
    "ITransformer",
    "Message",
    "MessageStream",
    "Primitive",
]
