"""module for the spell miner"""

from collections.abc import Sequence
from dataclasses import dataclass

from logdelta.helpers.lcs import lcs
from logdelta.mining.models import LogTemplate, MiningResult
from logdelta.parsing.models import Log

WILDCARD = "<*>"


@dataclass(slots=True)
class SpellCluster:
    """dataclass for the clusters created by spell"""

    cluster_id: int
    template_tokens: list[str]
    size: int = 1


class Spell:
    """the spell miner class"""

    def __init__(self, similarity_threshold: float = 0.5) -> None:
        """constructor"""
        self._clusters: dict[int, SpellCluster] = {}
        self._next_cluster_id: int = 1
        self.similarity_threshold: float = similarity_threshold

    def add(self, log: Log) -> MiningResult:
        """adds a log to the templates

        Args:
            log: the log

        Returns:
            MiningResult object
        """
        tokens = log.message.split()

        similarities: dict[int, float] = {}
        for cluster_id, temp_cluster in self._clusters.items():
            common_tokens = lcs(temp_cluster.template_tokens, tokens)
            similarity = len(common_tokens) / len(tokens)
            similarities[cluster_id] = similarity

        if similarities:
            best_cluster_id, best_similarity = max(
                similarities.items(), key=lambda item: item[1]
            )

            if best_similarity >= self.similarity_threshold:
                cluster = self._clusters[best_cluster_id]

                updated_template = generate_template(cluster.template_tokens, tokens)
                template_changed = updated_template != cluster.template_tokens
                cluster.template_tokens = updated_template

                cluster.size += 1

                return MiningResult(
                    template=" ".join(cluster.template_tokens),
                    cluster_id=cluster.cluster_id,
                    cluster_size=cluster.size,
                    cluster_count=len(self._clusters),
                    change_type="cluster_template_changed"
                    if template_changed
                    else "none",
                )

        cluster = SpellCluster(cluster_id=self._next_cluster_id, template_tokens=tokens)

        self._clusters[cluster.cluster_id] = cluster
        self._next_cluster_id += 1

        return MiningResult(
            template=" ".join(cluster.template_tokens),
            cluster_id=cluster.cluster_id,
            cluster_size=cluster.size,
            cluster_count=len(self._clusters),
            change_type="cluster_created",
        )

    def get_templates(self) -> list[LogTemplate]:
        """returns the templates that have been mined up till now

        Returns:
            list of log templates
        """
        return [
            LogTemplate(
                cluster_id=cluster.cluster_id,
                template=" ".join(cluster.template_tokens),
                size=cluster.size,
            )
            for cluster in self._clusters.values()
        ]


def generate_template(
    template_tokens: Sequence[str], log_tokens: Sequence[str]
) -> list[str]:
    """Generate a common log template from two log sequences

    Args:
        template_tokens: Tokens of existing template
        log_tokens: tokens of incoming log message

    Returns:
        log template that contains wildcard in regions that differ
    """
    common_tokens = lcs(template_tokens, log_tokens)

    i, j = 0, 0

    result: list[str] = []

    for token in common_tokens:
        next_i = template_tokens.index(token, i)
        next_j = log_tokens.index(token, j)

        if (next_i > i or next_j > j) and (not result or result[-1] != WILDCARD):
            result.append(WILDCARD)

        if token != WILDCARD or not result or result[-1] != WILDCARD:
            result.append(token)

        i = next_i + 1
        j = next_j + 1

    if (i < len(template_tokens) or j < len(log_tokens)) and (
        not result or result[-1] != WILDCARD
    ):
        result.append(WILDCARD)

    return result
