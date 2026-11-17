import datetime

import pytest

from logdelta.parsing.parser import (
    parse_level,
    parse_log,
    parse_message,
    parse_timestamp,
)


@pytest.fixture
def structured_log_line() -> str:
    return "2026-10-08T12:30:45+00:00 INFO This is a message"


@pytest.fixture
def expected_timestamp() -> datetime.datetime:
    return datetime.datetime(2026, 10, 8, 12, 30, 45, tzinfo=datetime.UTC)


def test_correct_parse_line(structured_log_line: str) -> None:
    log = parse_log(structured_log_line)

    assert log is not None
    assert log.message == "This is a message"
    assert log.timestamp == datetime.datetime(
        2026, 10, 8, 12, 30, 45, tzinfo=datetime.UTC
    )
    assert log.level == "INFO"


def test_parse_log_removes_trailing_newline() -> None:
    raw = "2026-10-08T12:30:45+00:00 this is a message\n"
    log = parse_log(raw)

    assert log is not None
    assert log.message == "this is a message"


def test_parse_timestamp_from_iso_log_line(
    expected_timestamp: datetime.datetime, structured_log_line: str
) -> None:
    dt, remainder = parse_timestamp(structured_log_line)

    assert dt == expected_timestamp
    assert remainder == "INFO This is a message"


def test_parse_ts_returns_None_on_no_datetime() -> None:
    raw = "INFO This is a message"
    ts, remainder = parse_timestamp(raw)
    assert ts is None
    assert remainder == raw


@pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_parse_level_from_raw_line(level: str) -> None:
    raw = f"{level} This is a message"

    log_level, remainder = parse_level(raw=raw)

    assert log_level == level
    assert remainder == "This is a message"


def test_parse_level_returns_None_when_no_level() -> None:
    raw = "2026-10-08T12:30:45+00:00 This is a message"
    level, remainder = parse_level(raw)
    assert level is None
    assert remainder == "2026-10-08T12:30:45+00:00 This is a message"


def test_parse_message_populates_message() -> None:
    raw = "This is a message"
    msg = parse_message(raw)
    assert raw == msg


def test_parse_log_populates_level(structured_log_line: str) -> None:
    log = parse_log(structured_log_line)
    assert log is not None
    assert log.level == "INFO"


def test_parse_log_parses_structured_log(
    structured_log_line: str, expected_timestamp: datetime.datetime
) -> None:

    log = parse_log(structured_log_line)

    assert log is not None
    assert log.message == "This is a message"
    assert log.level == "INFO"
    assert log.timestamp == expected_timestamp


@pytest.mark.parametrize(
    "raw",
    [
        "INFORMATION this is a message",
        "SUCCESS this is a message",
        "TRACE this is a message",
    ],
)
def test_parse_level_ignores_unknown_levels(raw: str) -> None:
    log_level, remainder = parse_level(raw)
    assert log_level is None
    assert remainder == raw


@pytest.mark.parametrize(
    ("raw_level", "expected_level"),
    [("info", "INFO"), ("Info", "INFO"), ("Error", "ERROR"), ("erRoR", "ERROR")],
)
def test_parse_level_case_insensitive(raw_level: str, expected_level: str) -> None:
    raw = f"{raw_level} This is a message"
    log_level, remainder = parse_level(raw)
    assert log_level == expected_level
    assert remainder == "This is a message"


def test_parse_log_handles_multiple_spaces_between_fields() -> None:
    raw = "2026-10-09T12:30:45+02:00    INFO    Application started"
    log = parse_log(raw)

    assert log is not None
    assert log.level == "INFO"
    assert log.message == "Application started"


def test_parse_log_handles_tabs_between_fields() -> None:
    raw = "2026-10-09T12:30:45+00:00\tINFO\tApplication started"
    log = parse_log(raw)
    assert log is not None
    assert log.level == "INFO"
    assert log.message == "Application started"
    assert log.timestamp == datetime.datetime(
        2026, 10, 9, 12, 30, 45, tzinfo=datetime.UTC
    )


def test_parse_ts_raises_ValueError_on_incorrect_datetime() -> None:
    raw = "2026-13-40T25:61:00+02:00 INFO Something happened"
    with pytest.raises(ValueError):
        _, _ = parse_timestamp(raw)


def test_parse_log_returns_None_when_empty_message() -> None:
    raw = "2026-10-12T12:30:45+02:00 INFO"
    log = parse_log(raw)

    assert log is None
