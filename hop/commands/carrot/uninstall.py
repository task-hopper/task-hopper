import typer

from hop.carrot import manager


def uninstall(
    target: str = typer.Argument(..., help="Carrot declaration to remove from ~/.hoprc and delete from disk"),
) -> None:
    """Remove a carrot from ~/.hoprc and delete its files from disk."""
    try:
        manager.uninstall(target)
        typer.echo(f"Uninstalled '{target}'.")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
