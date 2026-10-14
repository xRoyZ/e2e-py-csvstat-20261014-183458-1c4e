"""JSON output.

Full signature and inert stub: the real implementation is delivered by its own
ticket.
"""

from csvstat.models import ColumnStats


def render_json(stats: list[ColumnStats]) -> str:
    """Render ``stats`` as ``json.dumps`` of ``{"columns": [...]}``."""
    return ""
