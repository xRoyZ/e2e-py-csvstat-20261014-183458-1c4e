"""Tests for the csvstat CLI skeleton.

These assert only what the skeleton itself delivers: the parser exposes the
three documented options, ``main`` runs the wired pipeline and returns 0 on a
valid input, and every feature module is importable. Nothing here asserts what a
feature stub answers today.
"""

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

from csvstat.cli import main

OPTIONS = ("--delimiter", "--columns", "--json")
MODULES = (
    "csvstat",
    "csvstat.__main__",
    "csvstat.cli",
    "csvstat.errors",
    "csvstat.models",
    "csvstat.reader",
    "csvstat.stats",
    "csvstat.selection",
    "csvstat.table_render",
    "csvstat.json_render",
)


def test_help_exits_zero_and_lists_options(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])

    assert excinfo.value.code == 0
    out = capsys.readouterr().out
    for option in OPTIONS:
        assert option in out


def test_main_returns_zero_on_tiny_csv(tmp_path: Path) -> None:
    csv_file = tmp_path / "tiny.csv"
    csv_file.write_text("a,b\n1,2\n", encoding="utf-8")

    assert main([str(csv_file)]) == 0


def test_every_module_imports() -> None:
    for name in MODULES:
        assert importlib.import_module(name) is not None


def test_run_as_module_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "csvstat", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    for option in OPTIONS:
        assert option in result.stdout
