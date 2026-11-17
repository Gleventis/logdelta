from pathlib import Path

import pytest

from logdelta.parsing.models import Log
from logdelta.reading.reader import read_logs


def test_reads_example_log_file(load_log_file: Path) -> None:
    logs = list(read_logs(load_log_file))

    assert len(logs) > 0


def test_read_logs_raises_error(load_wrong_file: Path) -> None:
    with pytest.raises(FileNotFoundError):
        _ = list(read_logs(load_wrong_file))


def test_read_logs_with_proper_data(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"

    _ = log_file.write_text(
        "2026-10-08T12:30:45+00:00 INFO Application started\n2026-10-08T12:30:45+00:00 ERROR Something failed\n"
    )
    logs = list(read_logs(log_file))
    assert len(logs) == 2

    assert logs[0].message == "Application started"
    assert logs[0].level == "INFO"

    assert logs[1].message == "Something failed"
    assert logs[1].level == "ERROR"


def test_read_logs_valid_invalid_valid(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"

    _ = log_file.write_text(
        "2026-10-08T12:30:45+00:00 INFO Application started properly\n 2026-10-08T12:30:45 ERROR \n2026-10-08T12:30:45+00:00 INFO This should be a proper message\n 2026-10-08T12:30:45 ERROR "
    )
    logs: list[Log] = list(read_logs(log_file))
    assert len(logs) == 2

    assert logs[0].message == "Application started properly"
    assert logs[0].level == "INFO"

    assert logs[1].message == "This should be a proper message"
    assert logs[1].level == "INFO"


def test_read_logs_handles_multiline_logs(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"

    _ = log_file.write_text(
        "2026-10-08T12:30:45+00:00 ERROR Failed to process request\n"
        + "Traceback (most recent call last):\n"
        + '  File "application.py", line 10, in process\n'
        + "ValueError: invalid value\n"
        + "2026-10-08T12:31:00+00:00 INFO Application recovered\n"
    )

    logs = list(read_logs(log_file))

    assert len(logs) == 2
    assert logs[0].level == "ERROR"
    assert logs[0].message == (
        "Failed to process request\n"
        "Traceback (most recent call last):\n"
        '  File "application.py", line 10, in process\n'
        "ValueError: invalid value"
    )


def test_read_logs_handles_EOF(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"

    _ = log_file.write_text(
        "2026-10-08T12:30:45+00:00 ERROR Failed request\n"
        + "Traceback (most recent call last):\n"
        + "ValueError: invalid value"
    )

    logs = list(read_logs(log_file))

    assert len(logs) == 1

    assert logs[0].level == "ERROR"
    assert logs[0].message == (
        "Failed request\nTraceback (most recent call last):\nValueError: invalid value"
    )


def test_read_empty_file(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"
    _ = log_file.write_text("")
    logs = list(read_logs(log_file))
    assert len(logs) == 0


def test_reader_discards_garbage_before_valid_line(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"

    _ = log_file.write_text(
        "This is garbage\n2026-10-08T12:30:45+00:00 INFO App started"
    )
    logs = list(read_logs(log_file))
    assert len(logs) == 1
    assert logs[0].level == "INFO"
    assert logs[0].message == "App started"


def test_read_last_line_malformed(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"
    _ = log_file.write_text(
        "2026-10-08T12:30:45+00:00 INFO App started\nThis is garbage\n2026-10-08T12:30:45 ERROR Message"
    )
    logs = list(read_logs(log_file))
    assert len(logs) == 1
    assert logs[0].level == "INFO"


def test_read_blanklines_in_multiline(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"
    _ = log_file.write_text(
        "2026-10-08T12:30:45+00:00 ERROR Failed to process request\n"
        + "Traceback (most recent call last):\n\n\n\n"
        + '  File "application.py", line 10, in process\n'
        + "ValueError: invalid value\n"
        + "2026-10-08T12:31:00+00:00 INFO Application recovered\n"
    )
    logs = list(read_logs(log_file))
    assert len(logs) == 2
    assert logs[0].level == "ERROR"
    assert logs[1].level == "INFO"
