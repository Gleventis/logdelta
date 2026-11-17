from pathlib import Path

from logdelta.comparison.comparator import compare_templates
from logdelta.controller.controller import Controller
from logdelta.mining.miner import Miner
from logdelta.reading.reader import read_logs


def test_comparator_produces_correct_delta(
    load_log_file: Path, load_log_after_file: Path
) -> None:
    miner1 = Miner()
    before_logs = read_logs(load_log_file)
    before_templates = Controller(miner1).process(before_logs)
    miner2 = Miner()
    after_logs = read_logs(load_log_after_file)
    after_templates = Controller(miner2).process(after_logs)

    comparison = compare_templates(before=before_templates, after=after_templates)

    comparison_dict = {comp.template: comp.delta for comp in comparison}

    assert len(comparison_dict) == 3
    assert comparison_dict["Database connection failed"] == -2
    assert comparison_dict["Request timeout exceeded"] == 2
    assert comparison_dict["Application started"] == 1
