import datetime
from logdelta.parsing.models import Log
from logdelta.mining.spell import Spell


def test_spell_creates_cluster_from_first_log() -> None:
    miner = Spell()

    log = Log(
        timestamp=datetime.datetime(2026, 11, 18, tzinfo=datetime.UTC),
        message="Application started on server 1",
        level="INFO",
    )

    _ = miner.add(log)

    templates = miner.get_templates()

    assert len(templates) == 1
    assert templates[0].template == "Application started on server 1"
    assert templates[0].size == 1


def test_spell_modifies_existing_cluster_for_similar_log() -> None:

    log1 = Log(
        timestamp=datetime.datetime(2026, 11, 18, tzinfo=datetime.UTC),
        message="Application started on server 1",
        level="INFO",
    )
    log2 = Log(
        timestamp=datetime.datetime(2026, 11, 18, tzinfo=datetime.UTC),
        message="Application started on server 2",
        level="INFO",
    )
    miner = Spell()

    _ = miner.add(log1)
    _ = miner.add(log2)
    templates = miner.get_templates()

    assert len(templates) == 1
    assert templates[0].template == "Application started on server <*>"
    assert templates[0].size == 2


def test_spell_creates_separate_clusters_for_different_logs() -> None:

    log1 = Log(
        timestamp=datetime.datetime(2026, 11, 18, tzinfo=datetime.UTC),
        message="Application started on server 1",
        level="INFO",
    )
    log2 = Log(
        timestamp=datetime.datetime(2026, 11, 18, tzinfo=datetime.UTC),
        message="Connection failed",
        level="INFO",
    )
    miner = Spell()

    _ = miner.add(log1)
    _ = miner.add(log2)

    templates = miner.get_templates()
    assert len(templates) == 2
    assert templates[0].template == "Application started on server 1"
    assert templates[1].template == "Connection failed"
