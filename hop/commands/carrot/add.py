import typer

from hop.carrot import manager


def add(
    target: str = typer.Argument(..., help="Carrot to add: name, user/repo, https://..., or path:~/..."),
    install: bool = typer.Option(True, "--install/--no-install", help="Install immediately after adding"),
) -> None:
    """Add a carrot to ~/.hoprc and optionally install it."""
    try:
        manager.add_to_config(target)
        typer.echo(f"Added '{target}' to ~/.hoprc.")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    if install:
        try:
            name = manager.install_one(target)
            typer.echo(f"Installed carrot '{name}'.")
        except Exception as e:
            typer.echo(f"Error installing '{target}': {e}", err=True)
            raise typer.Exit(1)
