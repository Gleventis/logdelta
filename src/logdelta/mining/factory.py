from logdelta.mining.miner import Miner
from logdelta.mining.models import MiningAlgorithm
from logdelta.mining.protocols import MinerProtocol
from logdelta.mining.spell import Spell


def create_miner(algorithm: MiningAlgorithm) -> MinerProtocol:
    match algorithm:
        case MiningAlgorithm.DRAIN3:
            return Miner()
        case MiningAlgorithm.SPELL:
            return Spell()
