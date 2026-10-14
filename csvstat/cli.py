"""Command-line entry point for csvstat.

The parser and the pipeline are written once and complete. Every feature module
is imported and called here, so a feature ticket fills its own stub and never
touches this entry point.
"""

import argparse
import sys

from csvstat.errors import CsvstatError
from csvstat.json_render import render_json
from csvstat.reader import read_csv
from csvstat.selection import filter_stats, select_columns
from csvstat.stats import analyze_columns
from csvstat.table_render import render_table


def build_parser() -> argparse.ArgumentParser:
    """Build the csvstat argument parser."""
    parser = argparse.ArgumentParser(
        prog="csvstat",
        description="Print per-column statistics for a CSV file.",
    )
    parser.add_argument("file", help="Path to the CSV file to analyze.")
    parser.add_argument(
        "--delimiter",
        default=None,
        help="Field delimiter character; auto-detected when omitted.",
    )
    parser.add_argument(
        "--columns",
        default=None,
        help="Comma-separated list of columns to report, in header order.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of a text table.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the csvstat pipeline and return the process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    selected_names = args.columns.split(",") if args.columns is not None else None

    try:
        data = read_csv(args.file, args.delimiter)
        stats = analyze_columns(data)
        selected = select_columns(data.columns, selected_names)
        filtered = filter_stats(stats, selected)
        output = render_json(filtered) if args.json else render_table(filtered)
    except CsvstatError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
