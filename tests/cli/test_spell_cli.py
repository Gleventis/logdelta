"""Integration tests for the Spell CLI option."""

from pathlib import Path

from typer.testing import CliRunner

from logdelta.cli.main import app

runner = CliRunner()


def test_summary_with_spell_algorithm(tmp_path: Path) -> None:
    log_file = tmp_path / "spell.log"

    _ = log_file.write_text(
        "2026-11-19T10:00:00+00:00 INFO Application started on server 1\n"
        + "2026-11-19T10:00:01+00:00 INFO Application started on server 2\n"
    )

    result = runner.invoke(
        app,
        [
            "summary",
            str(log_file),
            "--algorithm",
            "spell",
        ],
    )

    assert result.exit_code == 0
    assert "Application started on server <*>" in result.stdout


def test_summary_rejects_unknown_algorithm(tmp_path: Path) -> None:
    log_file = tmp_path / "application.log"

    _ = log_file.write_text("2026-11-19T10:00:00+00:00 INFO Application started\n")

    result = runner.invoke(
        app,
        [
            "summary",
            str(log_file),
            "--algorithm",
            "unknown",
        ],
    )

    assert result.exit_code != 0
