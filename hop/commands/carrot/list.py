import typer

from hop.carrot import manager


def list_carrots() -> None:
    """List all installed carrots."""
    carrots = manager.list_installed()
    if not carrots:
        typer.echo("No carrots installed. Run 'hop carrot install <name>' to get started.")
        return
    for c in carrots:
        typer.echo(f"  {c['name']:<16} {c['version']:<8} {c['source']:<30} {c['description']}")
