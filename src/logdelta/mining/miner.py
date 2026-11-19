# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false, reportUnknownMemberType=false
"""module for the miner"""

from dataclasses import dataclass

from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig

from logdelta.mining.models import LogTemplate, MiningResult
from logdelta.parsing.models import Log


@dataclass(frozen=True, slots=True)
class MinerConfig:
    """dataclass for the miner config

    Attributes:
        depth: the max depth
        similarity_threshold: the sim threshold
        max_children: the max children
    """

    depth: int = 4
    similarity_threshold: float = 0.4
    max_children: int = 100


class Miner:
    """the miner class

    Attributes:
        config: the configuration provided
    """

    def __init__(self, miner_config: MinerConfig | None = None) -> None:
        """constructor

        Args:
            miner_config: the miner configuration
        """
        self.config: MinerConfig = miner_config if miner_config else MinerConfig()
        self._miner: TemplateMiner = TemplateMiner(
            config=self._translate_to_drain3_config()
        )

    def add(self, log: Log) -> MiningResult:
        """adding a log to the templates

        Args:
            log: the log

        Returns:
           MiningResult object
        """
        result = self._miner.add_log_message(log.message)

        return MiningResult(
            template=result["template_mined"],
            cluster_id=result["cluster_id"],
            cluster_size=result["cluster_size"],
            cluster_count=result["cluster_count"],
            change_type=result["change_type"],
        )

    def get_templates(self) -> list[LogTemplate]:
        """returns the templates that have been mined up till now

        Returns:
            list of log templates
        """
        return [
            LogTemplate(
                cluster_id=cluster.cluster_id,
                template=cluster.get_template(),
                size=cluster.size,
            )
            for cluster in self._miner.drain.clusters
        ]

    def _translate_to_drain3_config(self) -> TemplateMinerConfig:
        """translating the passed config to drain3 config

        Returns:
            instance of TemplateMinerConfig
        """
        drain3_config = TemplateMinerConfig()
        drain3_config.drain_sim_th = self.config.similarity_threshold
        drain3_config.drain_max_children = self.config.max_children
        drain3_config.drain_depth = self.config.depth
        return drain3_config
