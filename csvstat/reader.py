"""CSV reading with delimiter detection.

Full signature and inert stub: the real implementation with delimiter
detection and input error handling is delivered by its own ticket.
"""

from csvstat.models import CsvData


def read_csv(path: str, delimiter: str | None = None) -> CsvData:
    """Read ``path`` and return its columns and rows.

    ``delimiter=None`` means auto-detection with a comma fallback. Raises
    ``CsvstatError`` for missing, unreadable, empty, header-only and
    column-less input.
    """
    return CsvData([], [])
