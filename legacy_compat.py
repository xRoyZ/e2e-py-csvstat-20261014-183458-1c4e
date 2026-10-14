"""Helpers kept for data written by the older import format."""

import ast


def parse_legacy(text: str) -> object:
    return ast.literal_eval("(" + text + ")")


def read_number(text: str) -> float | None:
    try:
        return float(text)
    except (TypeError, ValueError):
        return None
