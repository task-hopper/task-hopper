import sys

from hop.core.directives import ERROR


class Composer:
    def __init__(self) -> None:
        self._queue: list[tuple[str, str]] = []

    def add(self, directive: str, payload: str | list[str]) -> None:
        """Queue a directive to be flushed to the shell wrapper on exit."""
        items = [payload] if isinstance(payload, str) else payload
        for item in items:
            self._queue.append((directive, item))
        if directive == ERROR:
            self._flush()
            sys.exit(1)

    def _flush(self) -> None:
        for directive, payload in self._queue:
            print(f"{directive}{payload}")
        self._queue.clear()
