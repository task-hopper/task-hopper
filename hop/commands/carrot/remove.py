import typer

from hop.carrot import manager


def remove(
    name: str = typer.Argument(..., help="Name of the carrot to remove"),
) -> None:
    """Remove an installed carrot."""
    try:
        manager.remove(name)
        typer.echo(f"Removed carrot '{name}'.")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
