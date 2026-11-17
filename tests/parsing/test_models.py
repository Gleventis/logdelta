import datetime

import pytest

from logdelta.parsing.models import Log


def test_log_accepts_valid_message() -> None:
    entry = Log(message="User logged in", timestamp=datetime.datetime.now(datetime.UTC))
    assert entry.message == "User logged in"


def test_log_rejects_empty_message() -> None:
    with pytest.raises(ValueError):
        _ = Log(message="      ", timestamp=datetime.datetime.now(datetime.UTC))

    with pytest.raises(ValueError):
        _ = Log(message="", timestamp=datetime.datetime.now(datetime.UTC))


def test_log_rejects_incorrect_message_type() -> None:
    with pytest.raises(TypeError):
        _ = Log(
            message=123,  # pyright: ignore[reportArgumentType] # ty: ignore[invalid-argument-type]
            timestamp=datetime.datetime.now(tz=datetime.UTC),
        )


def test_log_rejects_naive_ts() -> None:
    dt = datetime.datetime(2026, 10, 7, 14, 17, 30)
    with pytest.raises(ValueError):
        _ = Log(message="Hi", timestamp=dt)


def test_log_accepts_aware_ts() -> None:
    dt = datetime.datetime(2026, 10, 7, 14, 17, 30, tzinfo=datetime.UTC)
    entry = Log(message="Hi", timestamp=dt)
    assert entry.timestamp == dt


def test_log_rejects_empty_ts() -> None:
    with pytest.raises(ValueError):
        _ = Log(message="Hi", timestamp=None)  # pyright: ignore[reportArgumentType] # ty: ignore[invalid-argument-type]


def test_parse_plain_message() -> None:
    raw = "This is a raw message"

    ts = datetime.datetime.now(datetime.UTC)

    log = Log(raw, timestamp=ts)

    assert log.message == raw
    assert log.timestamp == ts
    assert log.level is None
