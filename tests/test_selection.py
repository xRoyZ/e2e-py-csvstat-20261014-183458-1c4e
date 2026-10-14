"""Tests for csvstat.selection."""

import pytest

from csvstat.errors import CsvstatError
from csvstat.models import ColumnStats
from csvstat.selection import filter_stats, select_columns


def make_stats(names: list[str]) -> list[ColumnStats]:
    return [
        ColumnStats(
            name=name,
            type="numeric",
            count=1,
            missing=0,
            min=1.0,
            max=1.0,
            mean=1.0,
            unique=None,
        )
        for name in names
    ]


def test_none_returns_all_columns_in_header_order() -> None:
    assert select_columns(["a", "b", "c"], None) == ["a", "b", "c"]


def test_subset_keeps_header_order() -> None:
    assert select_columns(["a", "b", "c"], ["c", "a"]) == ["a", "c"]


def test_unknown_name_raises_and_names_it() -> None:
    with pytest.raises(CsvstatError) as excinfo:
        select_columns(["a", "b"], ["nope"])
    assert "nope" in str(excinfo.value)


def test_several_unknown_names_are_all_named() -> None:
    with pytest.raises(CsvstatError) as excinfo:
        select_columns(["a"], ["x", "y"])
    message = str(excinfo.value)
    assert "x" in message and "y" in message


def test_filter_stats_drops_and_orders() -> None:
    stats = make_stats(["a", "b", "c"])
    assert [s.name for s in filter_stats(stats, ["c", "a"])] == ["c", "a"]
