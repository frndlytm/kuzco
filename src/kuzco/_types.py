from datetime import date, datetime, time
from collections.abc import Generator

__all__ = ["Primitive", "Message", "Channel"]

# A Primitve is a basic data type, think a data type that you would
# expect a database to provide first-class support for
Primitive = str | bytes | int | date | time | datetime | None

# A Message is a finite parcel of data 
Message = dict[str, Primitive | "Message"] | list["Message"]

# A Channel is a place where you can send and receive Messages
Channel = Generator[Message, Message, None]
