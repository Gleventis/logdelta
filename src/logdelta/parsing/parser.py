"""module for parsing the logs"""

import logging
import re
from datetime import datetime

from logdelta.parsing.models import Log

TIMESTAMP_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))"
)
LEVEL_PATTERN = re.compile(
    r"^(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\b", flags=re.IGNORECASE
)
FIELD_SEPARATOR_PATTERN = re.compile(r"^[ \t]+")

logger = logging.getLogger(__name__)


def parse_log(raw: str) -> Log | None:
    """function  for parsing a raw log line

    Args:
        raw: the raw log line

    Returns:
        instance of dataclass Log or none
    """
    raw = raw.rstrip("\r\n")  # Removing trailing whitespaces
    try:
        ts, remainder = parse_timestamp(raw)
    except ValueError:
        logger.warning(f"failed to parse log {raw} due to incorrect timestamp")
        return None

    if not ts:
        return None

    level, remainder = parse_level(remainder)

    message = parse_message(remainder)

    try:
        log = Log(message=message, timestamp=ts, level=level)
        return log
    except ValueError as error:
        logger.warning(f"failed to parse {raw} due to {error} ")
        return None


def parse_timestamp(raw: str) -> tuple[datetime | None, str]:
    """parsing the timestamp of a raw log

    Args:
        raw: the raw log

    Returns:
        a tuple of datetime | None and the remainder line
    """
    match = TIMESTAMP_PATTERN.match(raw)

    if match is None:
        return None, raw

    try:
        ts = datetime.fromisoformat(match.group("timestamp").replace("Z", "00:00"))
    except ValueError:
        logger.warning(f"datetime {match.group('timestamp')} is not valid isoformat")
        raise

    remainder = raw[match.end() :]
    remainder = separate_fields(remainder)

    return (ts, remainder)


def parse_level(raw: str) -> tuple[str | None, str]:
    """extracting the log level

    Args:
        raw: the raw log

    Returns:
        a tuple of level | None and the remainder line
    """
    match = LEVEL_PATTERN.match(raw)

    if match is None:
        return None, raw

    level = match.group("level").upper()

    remainder = raw[match.end() :]
    remainder = separate_fields(remainder)

    return (level, remainder)


def parse_message(raw: str) -> str:
    """extracting the message from the raw log

    Args:
        raw: the raw log

    Returns:
        the extracted message
    """
    return raw


def separate_fields(raw: str) -> str:
    """strips the fields of unecessary whitespace characters

    Args:
        raw: the raw log

    Returns:
        the field without whitespace chars
    """
    match = FIELD_SEPARATOR_PATTERN.match(raw)
    if match is None:
        return raw

    return raw[match.end() :]
