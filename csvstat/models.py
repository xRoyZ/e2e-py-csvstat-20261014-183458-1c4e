"""Data structures shared across the csvstat pipeline."""

from dataclasses import dataclass


@dataclass
class CsvData:
    """The raw contents of a CSV file.

    ``rows[i][j]`` is column ``j`` of data row ``i``. A short row is padded with
    empty strings so every row has ``len(columns)`` entries.
    """

    columns: list[str]
    rows: list[list[str]]


@dataclass
class ColumnStats:
    """Statistics computed for a single column.

    ``type`` is either ``"numeric"`` or ``"text"``. ``count`` is the number of
    non-missing values, ``missing`` the number of empty values. Numeric columns
    set ``min``/``max``/``mean`` (the mean already rounded to 4 decimals) and
    leave ``unique`` as ``None``; text columns set ``unique`` and leave
    ``min``/``max``/``mean`` as ``None``.
    """

    name: str
    type: str
    count: int
    missing: int
    min: float | None
    max: float | None
    mean: float | None
    unique: int | None
