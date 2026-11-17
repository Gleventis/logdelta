from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from logdelta.cli.main import app
from logdelta.comparison.comparator import TemplateComparison

runner = CliRunner()


def test_summary_accepts_multiple_log_files(tmp_path: Path) -> None:
    log_file_1 = tmp_path / "application1.log"
    log_file_2 = tmp_path / "application2.log"
    log_file_3 = tmp_path / "application3.log"

    _ = log_file_1.write_text("INFO User 1 logged in\n")
    _ = log_file_2.write_text("INFO User 2 logged in\n")
    _ = log_file_3.write_text("ERROR User 3 failed login\n")

    result = runner.invoke(
        app,
        [
            "summary",
            str(log_file_1),
            str(log_file_2),
            str(log_file_3),
        ],
    )

    assert result.exit_code == 0


def test_summary_displays_templates(tmp_path: Path) -> None:
    log_file_4 = tmp_path / "application1.log"
    log_file_5 = tmp_path / "application2.log"
    log_file_6 = tmp_path / "application3.log"

    _ = log_file_4.write_text("2026-10-08T12:30:45+00:00 INFO User 1 logged in\n")
    _ = log_file_5.write_text("2026-10-08T12:30:46+00:00 INFO User 2 logged in\n")
    _ = log_file_6.write_text("2026-10-08T12:30:47+00:00 ERROR User 3 failed login\n")

    result = runner.invoke(
        app, ["summary", str(log_file_4), str(log_file_5), str(log_file_6)]
    )

    print(repr(result.output))
    assert "User <*> logged in" in result.output


def test_summary_shows_header(tmp_path: Path) -> None:
    log_file_4 = tmp_path / "application1.log"
    log_file_5 = tmp_path / "application2.log"
    log_file_6 = tmp_path / "application3.log"

    _ = log_file_4.write_text("2026-10-08T12:30:45+00:00 INFO User 1 logged in\n")
    _ = log_file_5.write_text("2026-10-08T12:30:46+00:00 INFO User 2 logged in\n")
    _ = log_file_6.write_text("2026-10-08T12:30:47+00:00 ERROR User 3 failed login\n")

    result = runner.invoke(
        app, ["summary", str(log_file_4), str(log_file_5), str(log_file_6)]
    )

    assert result.exit_code == 0
    assert "Template" in result.output
    assert "Count" in result.output


def test_summary_displays_msg_for_empty_file(tmp_path: Path) -> None:
    log_file = tmp_path / "empty.log"

    log_file.touch()

    result = runner.invoke(app, ["summary", str(log_file)])

    assert result.exit_code == 0
    assert "No log templates found" in result.output


def test_summary_empty_file(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"
    log_file.touch()
    result = runner.invoke(app, ["summary", str(log_file)])

    assert result.exit_code == 0


def test_summary_invalid_file(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"
    result = runner.invoke(app, ["summary", str(log_file)])
    assert result.exit_code != 0


def test_compare_accepts_exactly_two_files(tmp_path: Path) -> None:
    log_file_1 = tmp_path / "application1.log"
    log_file_1.touch()
    log_file_2 = tmp_path / "application2.log"
    log_file_2.touch()
    log_file_3 = tmp_path / "application3.log"
    log_file_3.touch()
    result_faulty = runner.invoke(
        app, ["compare", str(log_file_1), str(log_file_2), str(log_file_3)]
    )
    assert result_faulty.exit_code != 0

    result_faulty_2 = runner.invoke(app, ["compare", str(log_file_1)])
    assert result_faulty_2.exit_code != -0

    result = runner.invoke(app, ["compare", str(log_file_1), str(log_file_2)])
    assert result.exit_code == 0


def test_compare_returns_correct_delta(
    load_log_file: Path, load_log_after_file: Path
) -> None:
    result = runner.invoke(
        app, ["compare", str(load_log_file), str(load_log_after_file)]
    )
    assert "Application started" in result.output
    assert "+1" in result.output
    assert result.exit_code == 0


def test_compare_displays_table_headers(
    load_log_file: Path, load_log_after_file: Path
) -> None:
    result = runner.invoke(
        app, ["compare", str(load_log_file), str(load_log_after_file)]
    )
    assert result.exit_code == 0

    assert "Template" in result.output
    assert "Before" in result.output
    assert "After" in result.output
    assert "Delta" in result.output


def test_compare_displays_msg_for_empty_files(tmp_path: Path) -> None:
    log_file1 = tmp_path / "empty1.log"
    log_file2 = tmp_path / "empty2.log"

    log_file1.touch()
    log_file2.touch()

    result = runner.invoke(app, ["compare", str(log_file1), str(log_file2)])

    assert result.exit_code == 0
    assert "No log templates to compare" in result.output


def test_compare_displays_templates_alphabetically(tmp_path: Path) -> None:
    before = tmp_path / "before.log"
    after = tmp_path / "after.log"

    before.touch()
    after.touch()

    comparisons = [
        TemplateComparison(
            template="Request timeout exceeded",
            before_count=0,
            after_count=2,
            delta=2,
        ),
        TemplateComparison(
            template="Application started",
            before_count=2,
            after_count=3,
            delta=1,
        ),
        TemplateComparison(
            template="Database connection failed",
            before_count=2,
            after_count=0,
            delta=-2,
        ),
    ]

    with patch(
        "logdelta.cli.main.compare_templates",
        return_value=comparisons,
    ):
        result = runner.invoke(
            app,
            ["compare", str(before), str(after)],
        )

    assert result.exit_code == 0, result.exception

    output = result.output

    assert (
        output.index("Application started")
        < output.index("Database connection failed")
        < output.index("Request timeout exceeded")
    )
