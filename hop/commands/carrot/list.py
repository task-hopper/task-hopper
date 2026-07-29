import typer

from hop.carrot import manager


def list_carrots() -> None:
    """List all available official carrots and their install status."""
    try:
        carrots = manager.list_official()
    except Exception as e:
        typer.echo(f"Error fetching carrot index: {e}", err=True)
        raise typer.Exit(1)

    if not carrots:
        typer.echo("No carrots found in the official index.")
        return

    for c in carrots:
        status = "[installed]" if c["installed"] else ""
        typer.echo(f"  {c['name']:<20} {c['description']:<45} {status}")
