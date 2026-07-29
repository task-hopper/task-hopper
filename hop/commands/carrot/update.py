import typer

from hop.carrot import manager


def update(
    target: str = typer.Argument(..., help="Carrot declaration to update"),
) -> None:
    """Update an installed carrot to the latest version."""
    try:
        name = manager.install_one(target)
        typer.echo(f"Updated carrot '{name}'.")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
