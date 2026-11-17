"""module for holding the models for the parsing"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Log:
    """dataclass for holding information regarding a log line

    Attributes:
        message: the message
        timestamp: the timestamp
        level: the level
    """

    message: str
    timestamp: datetime
    level: str | None = None

    def __post_init__(self) -> None:

        if not isinstance(self.message, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("message needs to be a str")

        if not self.message:
            raise ValueError("message can't be empty")

        if not self.message.strip():
            raise ValueError("message can't be blank")

        if self.timestamp is None or self.timestamp.utcoffset() is None:  # pyright: ignore[reportUnnecessaryComparison]
            raise ValueError("timestamp needs to be timezone aware")

        if not self.timestamp:
            raise ValueError("timestamp can't be empty")
