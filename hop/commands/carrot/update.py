import typer

from hop.carrot import manager


def update(
    name: str = typer.Argument(..., help="Name of the carrot to update"),
) -> None:
    """Update an installed carrot to the latest version."""
    carrots = manager.list_installed()
    entry = next((c for c in carrots if c["name"] == name), None)
    if not entry:
        typer.echo(f"Error: carrot '{name}' is not installed.", err=True)
        raise typer.Exit(1)
    source = entry["source"]
    try:
        if source == "official":
            manager.install_named(name)
        elif source.startswith("github:"):
            manager.install_github(source)
        else:
            typer.echo(f"Error: cannot auto-update carrot '{name}' with source '{source}'.", err=True)
            raise typer.Exit(1)
        typer.echo(f"Updated carrot '{name}'.")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
