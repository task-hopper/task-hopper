import typer

from hop.carrot import manager


def install(
    target: str = typer.Argument(..., help="Carrot name (official), or github:owner/repo"),
) -> None:
    """Install a carrot from the official index or a GitHub repo."""
    try:
        if target.startswith("github:"):
            name = manager.install_github(target)
        else:
            name = manager.install_named(target)
        typer.echo(f"Installed carrot '{name}'.")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
