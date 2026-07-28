from pathlib import Path

import typer
import yaml

HOPRC = Path.home() / ".hoprc"
HOPRC_TEMPLATE = """\
# hop configuration
# Documentation: https://github.com/task-hopper/task-hopper

# Global command shortcuts — run from anywhere.
# commands:
#   deploy: ./deploy.sh
#   hello: echo "Hello from hop!"

# Paths to local carrots (optional).
# carrot_paths:
#   - ~/my-carrots/my-carrot
"""


def init() -> None:
    """Initialize hop by creating a ~/.hoprc config file."""
    if HOPRC.exists():
        typer.echo(f"~/.hoprc already exists. Edit it with: $EDITOR ~/.hoprc")
        return
    HOPRC.write_text(HOPRC_TEMPLATE)
    typer.echo("Created ~/.hoprc — open it to configure your command shortcuts and carrots.")
    typer.echo("Install carrots with: hop carrot install <name>")
