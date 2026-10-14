"""Tests for csvstat.reader: delimiter handling and input errors."""

from pathlib import Path

import pytest

from csvstat.errors import CsvstatError
from csvstat.reader import read_csv


def _write(tmp_path: Path, name: str, content: str, encoding: str = "utf-8") -> Path:
    path = tmp_path / name
    path.write_text(content, encoding=encoding)
    return path


def test_reads_comma_separated(tmp_path: Path) -> None:
    path = _write(tmp_path, "comma.csv", "a,b,c\n1,2,3\n4,5,6\n")

    data = read_csv(str(path))

    assert data.columns == ["a", "b", "c"]
    assert data.rows == [["1", "2", "3"], ["4", "5", "6"]]


def test_reads_semicolon_separated(tmp_path: Path) -> None:
    path = _write(tmp_path, "semi.csv", "a;b;c\n1;2;3\n")

    data = read_csv(str(path))

    assert data.columns == ["a", "b", "c"]
    assert data.rows == [["1", "2", "3"]]


def test_reads_tab_separated(tmp_path: Path) -> None:
    path = _write(tmp_path, "tab.csv", "a\tb\tc\n1\t2\t3\n")

    data = read_csv(str(path))

    assert data.columns == ["a", "b", "c"]
    assert data.rows == [["1", "2", "3"]]


def test_auto_detects_delimiter(tmp_path: Path) -> None:
    path = _write(tmp_path, "auto.csv", "name;value\nx;1\ny;2\n")

    data = read_csv(str(path))

    assert data.columns == ["name", "value"]
    assert data.rows == [["x", "1"], ["y", "2"]]


def test_explicit_delimiter_is_used(tmp_path: Path) -> None:
    path = _write(tmp_path, "explicit.csv", "a|b\n1|2\n")

    data = read_csv(str(path), delimiter="|")

    assert data.columns == ["a", "b"]
    assert data.rows == [["1", "2"]]


def test_rejects_multi_character_delimiter(tmp_path: Path) -> None:
    path = _write(tmp_path, "d.csv", "a,b\n1,2\n")

    with pytest.raises(CsvstatError):
        read_csv(str(path), delimiter=",;")


def test_drops_utf8_bom(tmp_path: Path) -> None:
    path = _write(tmp_path, "bom.csv", "a,b\n1,2\n", encoding="utf-8-sig")

    data = read_csv(str(path))

    assert data.columns == ["a", "b"]
    assert data.rows == [["1", "2"]]


def test_pads_short_rows(tmp_path: Path) -> None:
    path = _write(tmp_path, "short.csv", "a,b,c\n1,2\n")

    data = read_csv(str(path))

    assert data.rows == [["1", "2", ""]]


def test_header_only_raises(tmp_path: Path) -> None:
    path = _write(tmp_path, "header_only.csv", "a,b,c\n")

    with pytest.raises(CsvstatError) as excinfo:
        read_csv(str(path))

    assert str(excinfo.value)


def test_empty_file_raises(tmp_path: Path) -> None:
    path = _write(tmp_path, "empty.csv", "")

    with pytest.raises(CsvstatError) as excinfo:
        read_csv(str(path))

    assert str(excinfo.value)


def test_no_columns_raises(tmp_path: Path) -> None:
    path = _write(tmp_path, "no_columns.csv", ",\n1,2\n")

    with pytest.raises(CsvstatError) as excinfo:
        read_csv(str(path))

    assert str(excinfo.value)


def test_missing_path_raises(tmp_path: Path) -> None:
    with pytest.raises(CsvstatError) as excinfo:
        read_csv(str(tmp_path / "does_not_exist.csv"))

    assert str(excinfo.value)


def test_directory_raises(tmp_path: Path) -> None:
    with pytest.raises(CsvstatError) as excinfo:
        read_csv(str(tmp_path))

    assert str(excinfo.value)


def test_non_utf8_raises(tmp_path: Path) -> None:
    path = tmp_path / "latin1.csv"
    path.write_bytes(b"a,b\n\xff\xfe,2\n")

    with pytest.raises(CsvstatError) as excinfo:
        read_csv(str(path))

    assert str(excinfo.value)
