"""Aligned text table output.

Values coming from the CSV (above all the column name) are escaped before they
reach the terminal so a field can never emit a control sequence or break the
alignment. See :func:`escape_text`.
"""

from csvstat.models import ColumnStats

_CONTROL_ESCAPES = {"\n": "\\n", "\r": "\\r"}


def escape_text(value: str) -> str:
    """Return ``value`` with every C0 control character except tab escaped.

    Tab is kept as-is; ``"\\n"`` and ``"\\r"`` become their two-character
    escapes and any other C0 byte becomes ``\\xNN``, so a value can never emit a
    terminal escape sequence.
    """
    escaped: list[str] = []
    for char in value:
        code = ord(char)
        if char == "\t":
            escaped.append(char)
        elif code < 0x20:
            escaped.append(_CONTROL_ESCAPES.get(char, f"\\x{code:02x}"))
        else:
            escaped.append(char)
    return "".join(escaped)


def _format_number(value: float) -> str:
    """Format ``value`` with at most 4 decimals and no trailing zeros."""
    text = f"{value:.4f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _format_optional(value: float | None) -> str:
    """Render an optional numeric metric, using ``-`` when it is absent."""
    return "-" if value is None else _format_number(value)


def _metric_lines(stats: ColumnStats) -> list[tuple[str, str]]:
    """Return the ``(label, value)`` metric lines for one column."""
    if stats.type == "numeric":
        return [
            ("count", str(stats.count)),
            ("min", _format_optional(stats.min)),
            ("max", _format_optional(stats.max)),
            ("mean", _format_optional(stats.mean)),
            ("missing", str(stats.missing)),
        ]
    return [
        ("unique", "-" if stats.unique is None else str(stats.unique)),
        ("missing", str(stats.missing)),
    ]


def render_table(stats: list[ColumnStats]) -> str:
    """Render ``stats`` as an aligned plain-text table, one block per column."""
    blocks: list[str] = []
    for column in stats:
        lines = _metric_lines(column)
        width = max(len(label) for label, _ in lines)
        block = [f"{escape_text(column.name)} ({column.type})"]
        block.extend(f"  {label.ljust(width)}  {value}" for label, value in lines)
        blocks.append("\n".join(block))
    return "\n\n".join(blocks)
