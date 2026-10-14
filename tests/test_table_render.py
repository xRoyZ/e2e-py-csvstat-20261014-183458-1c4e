"""Tests for the aligned text table output."""

from csvstat.models import ColumnStats
from csvstat.table_render import render_table


def test_numeric_block_has_labelled_metrics() -> None:
    stats = ColumnStats(
        name="value",
        type="numeric",
        count=3,
        missing=0,
        min=1.0,
        max=3.5,
        mean=2.25,
        unique=None,
    )
    out = render_table([stats])
    assert "(numeric)" in out
    for label in ("count", "min", "max", "mean", "missing"):
        assert label in out


def test_text_block_has_labelled_metrics() -> None:
    stats = ColumnStats(
        name="label",
        type="text",
        count=3,
        missing=1,
        min=None,
        max=None,
        mean=None,
        unique=2,
    )
    out = render_table([stats])
    assert "(text)" in out
    assert "unique" in out
    assert "missing" in out
    assert "mean" not in out


def test_blocks_keep_the_given_order() -> None:
    first = ColumnStats(
        name="first",
        type="numeric",
        count=1,
        missing=0,
        min=1.0,
        max=1.0,
        mean=1.0,
        unique=None,
    )
    second = ColumnStats(
        name="second",
        type="text",
        count=1,
        missing=0,
        min=None,
        max=None,
        mean=None,
        unique=1,
    )
    out = render_table([first, second])
    assert out.index("first") < out.index("second")


def test_numbers_have_at_most_four_decimals_without_trailing_zeros() -> None:
    stats = ColumnStats(
        name="value",
        type="numeric",
        count=3,
        missing=0,
        min=1.0,
        max=3.5,
        mean=42.3333,
        unique=None,
    )
    out = render_table([stats])
    assert "1\n" in out
    assert "3.5\n" in out
    assert "42.3333" in out
    assert "1.0000" not in out


def test_escape_sequence_in_column_name_is_escaped() -> None:
    stats = ColumnStats(
        name="\x1b[31mred\x1b[0m",
        type="numeric",
        count=1,
        missing=0,
        min=1.0,
        max=1.0,
        mean=1.0,
        unique=None,
    )
    out = render_table([stats])
    assert "\\x1b[31mred\\x1b[0m" in out
    assert "\x1b" not in out


def test_newline_in_column_name_is_escaped() -> None:
    stats = ColumnStats(
        name="a\nb",
        type="text",
        count=1,
        missing=0,
        min=None,
        max=None,
        mean=None,
        unique=1,
    )
    out = render_table([stats])
    assert "a\\nb (text)" in out
