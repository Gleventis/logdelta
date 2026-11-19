"""module that holds the controller for logdelta"""

from collections.abc import Iterable

from logdelta.mining.models import LogTemplate
from logdelta.mining.protocols import MinerProtocol
from logdelta.parsing.models import Log


class Controller:
    def __init__(self, miner: MinerProtocol) -> None:
        self.miner: MinerProtocol = miner

    def process(self, logs: Iterable[Log]) -> list[LogTemplate]:
        """processes a list of logs and returns a list of templates

        Args:
            logs: logs to be processed and extract templates

        Returns:
            list of templates
        """
        for log in logs:
            _ = self.miner.add(log)

        templates: list[LogTemplate] = self.miner.get_templates()

        return templates
