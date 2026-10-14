"""Column selection and stats filtering."""

from csvstat.errors import CsvstatError
from csvstat.models import ColumnStats


def select_columns(columns: list[str], names: list[str] | None) -> list[str]:
    """Return the selected column names in header order.

    ``names=None`` selects every column. Otherwise the requested names are
    matched by exact name and returned in header order. Every requested name
    that is missing from ``columns`` is collected and raised together in one
    ``CsvstatError`` naming the unknown names comma-separated.
    """
    if names is None:
        return list(columns)

    unknown = [name for name in names if name not in columns]
    if unknown:
        raise CsvstatError(f"unknown column(s): {', '.join(unknown)}")

    requested = set(names)
    return [column for column in columns if column in requested]


def filter_stats(stats: list[ColumnStats], selected: list[str]) -> list[ColumnStats]:
    """Return the stats entries named in ``selected``, in that order."""
    by_name = {stat.name: stat for stat in stats}
    return [by_name[name] for name in selected]
