from io import StringIO

from rich.console import Console


def render(markup: str) -> str:
    """Render Rich markup to a plain ANSI string for use with composer.add()."""
    buf = StringIO()
    Console(file=buf, highlight=False).print(markup, end="")
    return buf.getvalue()
