"""Column type detection and per-column statistics.

One ``ColumnStats`` is produced per header column, in header order. A value that
is empty after stripping whitespace is missing: it counts into ``missing`` and is
never parsed. A column is numeric when it has at least one non-missing value and
every non-missing value parses via ``float()`` to a finite number; otherwise it is
text.
"""

import math

from csvstat.models import ColumnStats, CsvData


def analyze_columns(data: CsvData) -> list[ColumnStats]:
    """Return one ``ColumnStats`` per header column, in header order."""
    return [_analyze_column(data, index) for index in range(len(data.columns))]


def _analyze_column(data: CsvData, index: int) -> ColumnStats:
    name = data.columns[index]
    missing = 0
    values: list[str] = []

    for row in data.rows:
        raw = row[index] if index < len(row) else ""
        value = raw.strip()
        if value == "":
            missing += 1
        else:
            values.append(value)

    parsed = _parse_all(values)
    if parsed is not None:
        total = math.fsum(parsed)
        return ColumnStats(
            name=name,
            type="numeric",
            count=len(parsed),
            missing=missing,
            min=min(parsed),
            max=max(parsed),
            mean=round(total / len(parsed), 4),
            unique=None,
        )

    return ColumnStats(
        name=name,
        type="text",
        count=len(values),
        missing=missing,
        min=None,
        max=None,
        mean=None,
        unique=len(set(values)),
    )


def _parse_all(values: list[str]) -> list[float] | None:
    """Return every value parsed as a finite float, or ``None`` on the first failure.

    An empty ``values`` list yields ``None``: a column without any non-missing
    value is text, never numeric.
    """
    if not values:
        return None

    parsed: list[float] = []
    for value in values:
        try:
            number = float(value)
        except ValueError:
            return None
        if not math.isfinite(number):
            return None
        parsed.append(number)
    return parsed
