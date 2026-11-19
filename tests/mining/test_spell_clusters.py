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


def test_spell_selects_cluster_with_highest_similarity() -> None:
    timestamp = datetime.datetime(
        year=2026,
        month=11,
        day=19,
        tzinfo=datetime.UTC,
    )

    miner = Spell(similarity_threshold=0.5)

    # Create three distinct clusters.
    for message in ("A B X Y", "A C D E", "Q R S"):
        _ = miner.add(
            Log(
                timestamp=timestamp,
                message=message,
                level="INFO",
            )
        )

    assert len(miner.get_templates()) == 3

    result = miner.add(Log(timestamp=timestamp, message="A B C D", level="INFO"))

    assert result.cluster_id == 2
    assert result.cluster_id == 2
    assert result.cluster_count == 3

    templates = {template.cluster_id: template for template in miner.get_templates()}

    assert templates[1].template == "A B X Y"
    assert templates[1].size == 1

    assert templates[2].template == "A <*> C D <*>"
    assert templates[2].size == 2

    assert templates[3].template == "Q R S"
    assert templates[3].size == 1
