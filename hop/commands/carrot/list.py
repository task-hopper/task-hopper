from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from hop.carrot import manager


def list_carrots(
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Show version and source details."),
) -> None:
    """List installed carrots."""
    carrots = manager.list_installed()
    if not carrots:
        typer.echo("No carrots installed. Add one to ~/.hoprc and run 'hop carrot install'.")
        return

    console = Console()
    if verbose:
        table = Table(box=None, pad_edge=False, show_header=True, header_style="bold")
        table.add_column("Name")
        table.add_column("Version")
        table.add_column("Source")
        table.add_column("Description")
        for c in carrots:
            table.add_row(c["name"], c["version"], c["source"], c["description"])
        console.print(table)
    else:
        for c in carrots:
            console.print(f"  {c['name']}")
