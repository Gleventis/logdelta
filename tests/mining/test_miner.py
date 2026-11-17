import datetime

from drain3.template_miner_config import TemplateMinerConfig

from logdelta.mining.miner import Miner, MinerConfig
from logdelta.parsing.models import Log


def test_miner_config_accepts_configuration() -> None:
    miner_config = MinerConfig(5, 0.5, 50)
    miner = Miner(miner_config)

    assert miner.config.depth == 5
    assert miner.config.similarity_threshold == 0.5
    assert miner.config.max_children == 50


def test_correct_mine_config_translation() -> None:
    miner_config = MinerConfig(5, 0.5, 50)
    miner = Miner(miner_config=miner_config)
    drain3_config = TemplateMinerConfig()
    drain3_config.drain_depth = 5
    drain3_config.drain_max_children = 50
    drain3_config.drain_sim_th = 0.5
    assert miner.config.depth == drain3_config.drain_depth
    assert miner.config.max_children == drain3_config.drain_max_children
    assert miner.config.similarity_threshold == drain3_config.drain_sim_th


def test_mines_log_message() -> None:
    log = Log(
        message="Hi there",
        timestamp=datetime.datetime(2026, 10, 15, 14, 20, 45, tzinfo=datetime.UTC),
        level="INFO",
    )
    miner = Miner()
    template = miner.add(log)
    assert template.template == "Hi there"


def test_miner_add_multiple_logs() -> None:
    log1 = Log(
        message="Hi there user 1",
        timestamp=datetime.datetime(2026, 10, 15, 14, 20, 45, tzinfo=datetime.UTC),
        level="INFO",
    )
    log2 = Log(
        message="Hi there user 2",
        timestamp=datetime.datetime(2026, 10, 15, 14, 20, 45, tzinfo=datetime.UTC),
        level="INFO",
    )
    miner = Miner()
    _ = miner.add(log1)
    template2 = miner.add(log2)
    assert template2.template == "Hi there user <*>"
    assert template2.cluster_size == 2


def test_mines_get_template() -> None:
    log1 = Log(
        message="Hi there user 1",
        timestamp=datetime.datetime(2026, 10, 15, 14, 20, 45, tzinfo=datetime.UTC),
        level="INFO",
    )
    log2 = Log(
        message="Hi there user 2",
        timestamp=datetime.datetime(2026, 10, 15, 14, 20, 45, tzinfo=datetime.UTC),
        level="INFO",
    )
    log3 = Log(
        message="User 5 logged in",
        timestamp=datetime.datetime(2026, 10, 15, 14, 20, 45, tzinfo=datetime.UTC),
        level="INFO",
    )
    miner = Miner()
    _ = miner.add(log1)
    _ = miner.add(log2)
    _ = miner.add(log3)
    templates = miner.get_templates()
    assert len(templates) == 2
    assert templates[0].template == "Hi there user <*>"
    assert templates[0].size == 2

    assert templates[1].template == "User 5 logged in"
    assert templates[1].size == 1


def test_miner_returns_empty_list_when_no_logs_mined() -> None:
    miner = Miner()
    templates = miner.get_templates()
    assert templates == []
