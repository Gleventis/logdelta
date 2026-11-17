from pathlib import Path

from logdelta.controller.controller import Controller
from logdelta.mining.miner import Miner
from logdelta.reading.reader import read_logs


def test_controller_feeds_logs_to_miner(tmp_path: Path) -> None:
    miner = Miner()
    controller = Controller(miner)

    log_file = tmp_path / "application.log"

    _ = log_file.write_text(
        "2026-10-08T12:30:45+00:00  User 1 logged in\n 2026-10-08T12:30:45 ERROR \n2026-10-08T12:30:45+00:00 INFO User 2 logged in\n 2026-10-08T12:30:45 ERROR "
    )

    logs = list(read_logs(log_file))

    templates = controller.process(logs)

    assert len(templates) == 1

    assert templates[0].template == "User <*> logged in"
