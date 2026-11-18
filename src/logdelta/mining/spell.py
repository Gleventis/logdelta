from collections.abc import Sequence

from logdelta.helpers.lcs import lcs

WILDCARD = "<*>"


def generate_template(
    template_tokens: Sequence[str], log_tokens: Sequence[str]
) -> list[str]:
    """Generate a common log template from two log sequences

    Args:
        template_tokens: Tokens of existing template
        log_tokens: tokens of incoming log message

    Returns:
        log template that contains wildcard in regions that differ
    """
    common_tokens = lcs(template_tokens, log_tokens)

    i, j = 0, 0

    result = []

    for token in common_tokens:
        next_i = template_tokens.index(token, i)
        next_j = log_tokens.index(token, j)

        if (next_i > i or next_j > j) and (not result or result[-1] != WILDCARD):
            result.append(WILDCARD)

        if token != WILDCARD or not result or result[-1] != WILDCARD:
            result.append(token)

        i = next_i + 1
        j = next_j + 1

    if (i < len(template_tokens) or j < len(log_tokens)) and (
        not result or result[-1] != WILDCARD
    ):
        result.append(WILDCARD)

    return result
