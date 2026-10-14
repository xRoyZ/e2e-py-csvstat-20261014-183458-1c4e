"""Column type detection and per-column statistics.

Full signature and inert stub: the real implementation is delivered by its own
ticket. One entry per header column, in header order.
"""

from csvstat.models import ColumnStats, CsvData


def analyze_columns(data: CsvData) -> list[ColumnStats]:
    """Return one ``ColumnStats`` per header column, in header order."""
    return []
