from dataclasses import dataclass

from logdelta.mining.models import LogTemplate


@dataclass(frozen=True, slots=True)
class TemplateComparison:
    """dataclass for holding info for the log templates comparison"""

    template: str
    before_count: int
    after_count: int
    delta: int


def template_lookup_creation(templates: list[LogTemplate]) -> dict[str, int]:
    return {item.template: item.size for item in templates}


def compare_templates(
    before: list[LogTemplate], after: list[LogTemplate]
) -> list[TemplateComparison]:
    """function for returning the comparison between two lists of LogTemplates

    Args:
        before: the log templates for the first file
        after: the log templates for the second file

    Returns:
        the comparison
    """
    template_comparison: list[TemplateComparison] = []

    before_dict = template_lookup_creation(before)
    after_dict = template_lookup_creation(after)

    all_templates = before_dict.keys() | after_dict.keys()

    for template in all_templates:
        before_size = before_dict.get(template, 0)
        after_size = after_dict.get(template, 0)

        delta = after_size - before_size

        comparison = TemplateComparison(
            template=template,
            before_count=before_size,
            after_count=after_size,
            delta=delta,
        )

        template_comparison.append(comparison)

    return template_comparison
