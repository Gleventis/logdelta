"""module for the protocol for the miners"""

from typing import Protocol

from logdelta.mining.models import LogTemplate, MiningResult
from logdelta.parsing.models import Log


class MinerProtocol(Protocol):
    """protocol for miners"""

    def add(self, log: Log) -> MiningResult: ...

    def get_templates(self) -> list[LogTemplate]: ...
