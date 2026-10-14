"""Tests for the JSON output (AC-07)."""

import json

from csvstat.json_render import render_json
from csvstat.models import ColumnStats


def _numeric(name: str = "amount") -> ColumnStats:
    return ColumnStats(
        name=name,
        type="numeric",
        count=3,
        missing=1,
        min=1.5,
        max=9.25,
        mean=5.125,
        unique=None,
    )


def _text(name: str = "city") -> ColumnStats:
    return ColumnStats(
        name=name,
        type="text",
        count=4,
        missing=2,
        min=None,
        max=None,
        mean=None,
        unique=3,
    )


def test_result_parses_with_json_loads() -> None:
    parsed = json.loads(render_json([_numeric(), _text()]))
    assert set(parsed) == {"columns"}
    assert isinstance(parsed["columns"], list)


def test_columns_hold_every_column_in_order() -> None:
    stats = [_numeric("a"), _text("b"), _numeric("c")]
    parsed = json.loads(render_json(stats))
    assert [column["name"] for column in parsed["columns"]] == ["a", "b", "c"]


def test_numeric_column_has_the_numeric_key_set() -> None:
    parsed = json.loads(render_json([_numeric()]))
    column = parsed["columns"][0]
    assert set(column) == {"name", "type", "count", "min", "max", "mean", "missing"}
    assert column["type"] == "numeric"


def test_text_column_has_the_text_key_set() -> None:
    parsed = json.loads(render_json([_text()]))
    column = parsed["columns"][0]
    assert set(column) == {"name", "type", "unique", "missing"}
    assert column["type"] == "text"


def test_metrics_are_json_numbers_not_strings() -> None:
    numeric = json.loads(render_json([_numeric()]))["columns"][0]
    for key in ("count", "min", "max", "mean", "missing"):
        assert isinstance(numeric[key], (int, float))
        assert not isinstance(numeric[key], str)

    text = json.loads(render_json([_text()]))["columns"][0]
    for key in ("unique", "missing"):
        assert isinstance(text[key], int)
        assert not isinstance(text[key], str)


def test_mean_carries_the_rounded_value() -> None:
    stat = _numeric()
    stat.mean = 1.2346
    parsed = json.loads(render_json([stat]))
    assert parsed["columns"][0]["mean"] == 1.2346


def test_empty_stats_render_empty_columns_list() -> None:
    assert json.loads(render_json([])) == {"columns": []}
