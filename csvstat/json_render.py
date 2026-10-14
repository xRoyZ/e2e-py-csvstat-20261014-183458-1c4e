"""JSON output.

Renders a list of :class:`~csvstat.models.ColumnStats` as a JSON document of the
form ``{"columns": [...]}``. Each column contributes exactly the metrics that
belong to its type: numeric columns carry ``min``/``max``/``mean``, text columns
carry ``unique``. All numeric metrics are emitted as JSON numbers, never as
strings.
"""

import json

from csvstat.models import ColumnStats


def _column_object(stat: ColumnStats) -> dict[str, object]:
    """Build the JSON object for a single column, keyed by its type."""
    if stat.type == "numeric":
        return {
            "name": stat.name,
            "type": "numeric",
            "count": stat.count,
            "min": stat.min,
            "max": stat.max,
            "mean": stat.mean,
            "missing": stat.missing,
        }
    return {
        "name": stat.name,
        "type": "text",
        "unique": stat.unique,
        "missing": stat.missing,
    }


def render_json(stats: list[ColumnStats]) -> str:
    """Render ``stats`` as ``json.dumps`` of ``{"columns": [...]}``."""
    columns = [_column_object(stat) for stat in stats]
    return json.dumps({"columns": columns}, ensure_ascii=False, indent=2)
