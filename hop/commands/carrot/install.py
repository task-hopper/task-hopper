import typer

from hop.carrot import manager


def install() -> None:
    """Install all uninstalled carrots declared in ~/.hoprc."""
    results = manager.install_all()
    if not results:
        typer.echo("No GitHub carrots declared in ~/.hoprc.")
        return
    for r in results:
        if r["status"] == "installed":
            typer.echo(f"  ✓  {r['name']}")
        elif r["status"] == "already_installed":
            typer.echo(f"  ·  {r['name']} (already installed)")
        else:
            typer.echo(f"  ✗  {r['name']}: {r['error']}", err=True)
    if any(r["status"] == "failed" for r in results):
        raise typer.Exit(1)
