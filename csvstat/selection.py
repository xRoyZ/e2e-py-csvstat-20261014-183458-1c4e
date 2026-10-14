"""Column selection and stats filtering.

Full signatures and inert stubs: the real implementation is delivered by its own
ticket.
"""

from csvstat.models import ColumnStats


def select_columns(columns: list[str], names: list[str] | None) -> list[str]:
    """Return the selected column names in header order.

    ``names=None`` selects every column. Raises ``CsvstatError`` naming every
    unknown name.
    """
    return []


def filter_stats(stats: list[ColumnStats], selected: list[str]) -> list[ColumnStats]:
    """Return the stats entries named in ``selected``, in that order."""
    return []
