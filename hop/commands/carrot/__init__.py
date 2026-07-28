import typer

from hop.commands.carrot.install import install
from hop.commands.carrot.remove import remove
from hop.commands.carrot.list import list_carrots
from hop.commands.carrot.update import update

app = typer.Typer(help="Manage hop carrots (plugins).")
app.command()(install)
app.command()(remove)
app.command("list")(list_carrots)
app.command()(update)
