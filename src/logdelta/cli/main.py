"""module that holds the cli"""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from logdelta.cli.formatting import build_comp_table, build_sum_table
from logdelta.comparison.comparator import compare_templates
from logdelta.controller.controller import Controller
from logdelta.mining.miner import Miner
from logdelta.mining.models import LogTemplate
from logdelta.parsing.models import Log
from logdelta.reading.reader import read_logs

app = typer.Typer()


@app.callback()
def main() -> None:
    return None


@app.command()
def summary(
    log_files: Annotated[
        list[Path],
        typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True),
    ],
) -> None:
    total_logs: list[Log] = []
    for file in log_files:
        total_logs.extend(read_logs(file))

    miner = Miner()

    controller = Controller(miner)

    results: list[LogTemplate] = controller.process(total_logs)

    console = Console()

    if results:
        table = build_sum_table(templates=results)

        console.print(table)

    else:
        console.print("No log templates found")


@app.command()
def compare(
    log_file: Annotated[
        Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)
    ],
    compare_with: Annotated[
        Path, typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)
    ],
) -> None:

    logs_before = read_logs(log_file)
    logs_after = read_logs(compare_with)

    miner_before, miner_after = Miner(), Miner()

    controller_before, controller_after = (
        Controller(miner_before),
        Controller(miner_after),
    )

    tl_before, tl_after = (
        controller_before.process(logs_before),
        controller_after.process(logs_after),
    )

    comparison = compare_templates(before=tl_before, after=tl_after)

    console = Console()

    if comparison:
        table = build_comp_table(comparison=comparison)

        console.print(table)
    else:
        console.print("No log templates to compare")
