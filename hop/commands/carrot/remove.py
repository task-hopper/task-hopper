import typer

from hop.carrot import manager


def remove(
    target: str = typer.Argument(..., help="Carrot declaration to remove from ~/.hoprc"),
) -> None:
    """Remove a carrot from ~/.hoprc (keeps installed files on disk)."""
    try:
        manager.remove_from_config(target)
        typer.echo(f"Removed '{target}' from ~/.hoprc. Files remain at ~/.hop/carrots/.")
        typer.echo(f"To fully delete files, run: hop carrot uninstall {target}")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
