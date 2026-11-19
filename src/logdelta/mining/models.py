from dataclasses import dataclass
from enum import StrEnum


class MiningAlgorithm(StrEnum):
    DRAIN3 = "drain3"
    SPELL = "spell"


@dataclass(frozen=True, slots=True)
class LogTemplate:
    """dataclass for the log templates"""

    cluster_id: int
    template: str
    size: int


@dataclass(frozen=True, slots=True)
class MiningResult:
    """dataclass for the result of mining"""

    template: str
    cluster_id: int
    cluster_size: int
    cluster_count: int
    change_type: str
