from pathlib import Path

import pytest


@pytest.fixture
def load_log_file() -> Path:
    return Path(__file__).resolve().parent.parent / "examples" / "before.log"


@pytest.fixture
def load_log_after_file() -> Path:
    return Path(__file__).resolve().parent.parent / "examples" / "after.log"


@pytest.fixture
def load_wrong_file() -> Path:
    return Path(__file__).resolve().parent.parent / "examples" / "wrong.log"
