from collections.abc import Sequence


def lcs(first: Sequence[str], second: Sequence[str]) -> list[str]:
    """implementation for computing the longest common subsequence

    Args:
        first: first sequence of tokens
        second: second sequence of tokens

    Returns:
        list of longest common subsequence
    """
    m: int = len(first)
    n: int = len(second)

    dp: list[list[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result: list[str] = []
    while m > 0 and n > 0:
        if first[m - 1] == second[n - 1]:
            result.append(first[m - 1])
            m -= 1
            n -= 1
        elif dp[m - 1][n] >= dp[m][n - 1]:
            m -= 1
        else:
            n -= 1

    result.reverse()

    return result
