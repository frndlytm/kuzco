from datetime import date, datetime
from typing import *

Primitive = str | bytes | int | date | datetime | None
Message = Dict[str, Primitive | "Message"]
MessageStream = Iterable[Message]
