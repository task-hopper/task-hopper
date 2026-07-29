import typer

from hop.carrot import manager


def install() -> None:
    """Install all uninstalled carrots declared in ~/.hoprc."""
    results = manager.install_all()
    if not results:
        typer.echo("No carrots declared in ~/.hoprc. Use 'hop carrot add <carrot>' to add one.")
        return
    for r in results:
        if r["status"] == "installed":
            typer.echo(f"  ✓ {r['name']:<20} installed")
        elif r["status"] == "already installed":
            typer.echo(f"  · {r['name']:<20} already installed")
        else:
            typer.echo(f"  ✗ {r['name']:<20} failed: {r['error']}", err=True)
    failed = [r for r in results if r["status"] == "failed"]
    if failed:
        raise typer.Exit(1)
