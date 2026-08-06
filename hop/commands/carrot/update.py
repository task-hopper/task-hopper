from typing import Optional

import typer

from hop.carrot import manager


def update(
    name: Optional[str] = typer.Argument(None, help="Carrot name to update (e.g. warren). Omit to update all."),
) -> None:
    """Update installed carrots. Pinned carrots update only if not already at the pinned version."""
    try:
        results = manager.update_one(name) if name else manager.update_all()
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    if not results:
        typer.echo("No installed GitHub carrots to update.")
        return

    for r in results:
        if r["status"] == "updated":
            typer.echo(f"  ✓  {r['name']} → {r['ref']}")
        elif r["status"] in ("already_up_to_date", "already_at_version"):
            typer.echo(f"  ·  {r['name']} (already up to date)")
        else:
            typer.echo(f"  ✗  {r['name']}: {r['error']}", err=True)

    if any(r["status"] == "failed" for r in results):
        raise typer.Exit(1)
