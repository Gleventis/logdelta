from logdelta.cli.formatting import format_delta


def test_positive_delta_is_green() -> None:
    result = format_delta(5)
    assert result.plain == "+5"
    assert result.style == "green"


def test_negative_delta_is_red() -> None:
    result = format_delta(-2)
    assert result.plain == "-2"
    assert result.style == "red"


def test_zero_has_no_color() -> None:
    result = format_delta(0)
    assert result.plain == "+0"
    assert result.style == ""
