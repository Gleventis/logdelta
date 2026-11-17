import re
from collections.abc import Iterator
from pathlib import Path

from logdelta.parsing.models import Log
from logdelta.parsing.parser import parse_log

TIMESTAMP_PATTERN = re.compile(r"^[ \t]*\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


def starts_new_line(line: str) -> bool:
    return bool(TIMESTAMP_PATTERN.match(line))


def read_logs(log_file: Path) -> Iterator[Log]:
    current_logs: list[str] = []

    with log_file.open() as log_f:
        for line in log_f:
            if starts_new_line(line):
                if current_logs:
                    raw = "".join(current_logs)
                    log = parse_log(raw)

                    if log:
                        yield log
                current_logs = [line]
                continue
            if current_logs:
                current_logs.append(line)
    if current_logs:
        raw = "".join(current_logs)
        log = parse_log(raw)

        if log:
            yield log
