"""Error type shared across the csvstat package."""


class CsvstatError(Exception):
    """A user-facing error.

    ``cli.main`` catches this, prints ``str(exc)`` on stderr and returns exit
    code 1, so the message is expected to be understandable on its own.
    """
