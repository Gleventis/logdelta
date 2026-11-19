from rich.table import Table
from rich.text import Text

from logdelta.comparison.comparator import TemplateComparison
from logdelta.mining.models import LogTemplate


def build_sum_table(templates: list[LogTemplate]) -> Table:
    """helper function for creating the table for the summary command

    Args:
        templates: list of log templates

    Returns:
        the table
    """
    sorted_sum = sorted(templates, key=lambda item: item.template)
    table = Table(title="Logdelta summary")
    table.add_column("Template", justify="right")
    table.add_column("Count", justify="right")

    for result in sorted_sum:
        table.add_row(str(result.template), str(result.size))
    return table


def build_comp_table(comparison: list[TemplateComparison]) -> Table:
    """helper function for creating the table for the comparison command

    Args:
        comparison: list of template comparisons

    Returns:
        the table
    """
    sorted_comp = sorted(comparison, key=lambda item: item.template)
    table = Table(title="Logdelta comparison")
    table.add_column("Template", justify="right")
    table.add_column("Before", justify="right")
    table.add_column("After", justify="right")
    table.add_column("Delta", justify="right")

    for result in sorted_comp:
        table.add_row(
            Text(result.template),
            str(result.before_count),
            str(result.after_count),
            format_delta(result.delta),
        )
    return table


def format_delta(delta: int) -> Text:
    """formatting the delta

    Args:
        delta: the delta

    Returns:
        Text with styling
    """
    if delta > 0:
        return Text(f"{delta:+d}", style="green")
    if delta < 0:
        return Text(f"{delta:+d}", style="red")
    return Text(f"{delta:+d}")
