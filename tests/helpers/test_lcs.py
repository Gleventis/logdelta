from logdelta.helpers.lcs import lcs


def test_lcs_with_matching_sequences() -> None:
    first = ["Application", "started"]
    second = ["Application", "started"]
    assert lcs(first=first, second=second) == ["Application", "started"]


def test_lcs_with_different_tokens() -> None:
    first = ["Application", "started", "on", "server1"]
    second = ["Application", "started", "on", "server2"]
    assert lcs(first=first, second=second) == ["Application", "started", "on"]


def test_lcs_with_no_matching_tokens() -> None:
    first = ["Application", "started"]
    second = ["server", "crashed"]
    assert lcs(first=first, second=second) == []


def test_lcs_with_empty_sequence() -> None:
    first = ["application", "started"]
    second: list[str] = []
    assert lcs(first=first, second=second) == []


def test_lcs_with_both_sequences_empty() -> None:
    first: list[str] = []
    second: list[str] = []
    assert lcs(first, second) == []


def test_lcs_with_non_consecutive_matches() -> None:
    first = ["A", "B", "X", "Y"]
    second = ["A", "D", "B", "J"]
    assert lcs(first, second) == ["A", "B"]


def test_lcs_with_repeated_tokens() -> None:
    first = ["A", "A", "B", "C"]
    second = ["A", "C", "A"]
    assert lcs(first, second) == ["A", "A"]
