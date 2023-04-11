from collections.abc import Generator
from datetime import date, datetime, time
from typing import ForwardRef

__all__ = ["Primitive", "Message", "Channel"]

# A Primitve is a basic data type, think a data type that you would
# expect a database to provide first-class support for
Primitive = str | bytes | int | float | date | time | datetime | None

# A Message is a finite parcel of data 
Message = dict[str, Primitive | ForwardRef("Message")] | list[ForwardRef("Message")]

# A Channel is a place where you can send and receive Messages
Channel = Generator[Message, Message | None, None]
