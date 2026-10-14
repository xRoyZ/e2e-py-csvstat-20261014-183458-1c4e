"""Tests for column type detection and per-column statistics."""

from csvstat.models import CsvData
from csvstat.stats import analyze_columns


def test_all_numeric_column() -> None:
    data = CsvData(columns=["n"], rows=[["1"], ["2"], ["3"]])
    stats = analyze_columns(data)

    assert len(stats) == 1
    (col,) = stats
    assert col.name == "n"
    assert col.type == "numeric"
    assert col.count == 3
    assert col.missing == 0
    assert col.min == 1.0
    assert col.max == 3.0
    assert col.mean == 2.0
    assert col.unique is None


def test_single_non_numeric_value_makes_text() -> None:
    data = CsvData(columns=["n"], rows=[["1"], ["2"], ["x"]])
    (col,) = analyze_columns(data)

    assert col.type == "text"
    assert col.unique == 3
    assert col.min is None
    assert col.max is None
    assert col.mean is None


def test_nan_and_inf_are_not_numeric() -> None:
    data = CsvData(columns=["n"], rows=[["1"], ["nan"], ["inf"]])
    (col,) = analyze_columns(data)

    assert col.type == "text"
    assert col.unique == 3


def test_all_empty_column_is_text_with_zero_unique() -> None:
    data = CsvData(columns=["n"], rows=[[""], ["  "], [""]])
    (col,) = analyze_columns(data)

    assert col.type == "text"
    assert col.count == 0
    assert col.missing == 3
    assert col.unique == 0
    assert col.min is None
    assert col.max is None
    assert col.mean is None


def test_count_min_max_mean_with_one_empty_field() -> None:
    data = CsvData(columns=["n"], rows=[["1"], [""], ["3"]])
    (col,) = analyze_columns(data)

    assert col.type == "numeric"
    assert col.count == 2
    assert col.missing == 1
    assert col.min == 1.0
    assert col.max == 3.0
    assert col.mean == 2.0


def test_mean_rounded_to_four_decimals() -> None:
    data = CsvData(columns=["n"], rows=[["1"], ["1"], ["2"], ["2"], ["2"], ["3"]])
    (col,) = analyze_columns(data)

    assert col.mean == round(11 / 6, 4)
    assert col.mean == 1.8333


def test_distinct_values_ignore_missing() -> None:
    data = CsvData(columns=["s"], rows=[["a"], ["b"], ["a"], [""], ["b"]])
    (col,) = analyze_columns(data)

    assert col.type == "text"
    assert col.unique == 2
    assert col.count == 4
    assert col.missing == 1


def test_header_order_preserved() -> None:
    data = CsvData(
        columns=["a", "b", "c"],
        rows=[["1", "x", ""], ["2", "y", "5"]],
    )
    stats = analyze_columns(data)

    assert [col.name for col in stats] == ["a", "b", "c"]
    assert [col.type for col in stats] == ["numeric", "text", "numeric"]
    assert stats[2].count == 1
    assert stats[2].missing == 1
    assert stats[2].mean == 5.0
