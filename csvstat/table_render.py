"""Aligned text table output.

Full signature and inert stub: the real implementation with aligned columns and
control-character escaping is delivered by its own ticket.
"""

from csvstat.models import ColumnStats


def render_table(stats: list[ColumnStats]) -> str:
    """Render ``stats`` as an aligned plain-text table."""
    return ""
