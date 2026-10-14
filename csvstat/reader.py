"""CSV reading with delimiter detection.

Reads a CSV file into a :class:`CsvData`. The delimiter is either the caller's
explicit choice or sniffed from a sample of the file, falling back to a comma.
All input problems surface as :class:`CsvstatError` with a plain-language
message; the file is read once and never copied to disk or sent anywhere.
"""

import csv

from csvstat.errors import CsvstatError
from csvstat.models import CsvData

_SNIFF_SAMPLE_SIZE = 8192


def _validate_delimiter(delimiter: str) -> str:
    """Return ``delimiter`` if it is a single character, else raise."""
    if len(delimiter) != 1:
        raise CsvstatError(f"Invalid delimiter {delimiter!r}: it must be exactly one character.")
    return delimiter


def _detect_delimiter(sample: str) -> str:
    """Sniff the delimiter from ``sample``, falling back to a comma."""
    if not sample:
        return ","
    try:
        return csv.Sniffer().sniff(sample).delimiter
    except csv.Error:
        return ","


def read_csv(path: str, delimiter: str | None = None) -> CsvData:
    """Read ``path`` and return its columns and rows.

    ``delimiter=None`` means auto-detection with a comma fallback. Raises
    ``CsvstatError`` for missing, unreadable, empty, header-only and
    column-less input.
    """
    if delimiter is not None:
        delimiter = _validate_delimiter(delimiter)

    try:
        with open(path, encoding="utf-8-sig", newline="") as handle:
            sample = handle.read(_SNIFF_SAMPLE_SIZE)
            if delimiter is None:
                delimiter = _detect_delimiter(sample)
            handle.seek(0)
            all_rows = list(csv.reader(handle, delimiter=delimiter))
    except OSError as exc:
        reason = exc.strerror or str(exc)
        raise CsvstatError(f"Could not read '{path}': {reason}.") from exc
    except UnicodeDecodeError as exc:
        raise CsvstatError(f"'{path}' is not a valid UTF-8 file: {exc}.") from exc

    if not all_rows:
        raise CsvstatError(f"'{path}' is empty and has no header row.")

    header = all_rows[0]
    if not header or all(field == "" for field in header):
        raise CsvstatError(f"'{path}' contains no columns.")

    if len(all_rows) < 2:
        raise CsvstatError(f"'{path}' has a header but no data rows.")

    width = len(header)
    rows: list[list[str]] = []
    for row in all_rows[1:]:
        if len(row) < width:
            row = row + [""] * (width - len(row))
        rows.append(row)

    return CsvData(columns=list(header), rows=rows)
