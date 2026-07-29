from pathlib import Path

import typer
from rich.console import Console

from hop.core.logo import LOGO
from hop.core.prompt import ask, confirm, path

console = Console()

CARROT_TOML_TEMPLATE = """\
[carrot]
name = "{name}"
version = "0.1.0"
description = "{description}"
min_hop_version = "2.0.0"
author = "{author}"

[commands]
{command_name} = "commands.{command_name}"
"""

HELLO_COMMAND_TEMPLATE = '''\
import typer
from hop.sdk import composer, directives

LOGO = r"""{logo}"""


def register(app: typer.Typer) -> None:
    @app.command()
    def {command_name}(
        name: str = typer.Argument("doc"),
    ) -> None:
        """Eh, what\'s up?"""
        composer.add(directives.MESSAGE, LOGO)
        composer.add(directives.MESSAGE, f"Eh, what\'s up, {{name}}?")
'''


def scaffold() -> None:
    """Interactively scaffold a new hop carrot."""
    console.print(LOGO)
    console.print("[bold]hop carrot scaffold[/bold] — let's grow a carrot.\n")

    name = ask("Carrot name:", instruction="(e.g. hop-carrot-warren)")
    if not name:
        raise typer.Exit(0)

    description = ask("Description:")
    if description is None:
        raise typer.Exit(0)

    author = ask("Author:", instruction="(your GitHub username)")
    if author is None:
        raise typer.Exit(0)

    default_location = str(Path.home() / "Repos" / name)
    location = path("Where should we create it?", default=default_location)
    if location is None:
        raise typer.Exit(0)

    dest = Path(location).expanduser().resolve()

    if dest.exists():
        overwrite = confirm(f"{dest} already exists. Overwrite?", default=False)
        if not overwrite:
            raise typer.Exit(0)

    command_name = ask("Name your first command:", default="hello")
    if command_name is None:
        raise typer.Exit(0)

    add_to_hoprc = confirm("Add to ~/.hoprc automatically?", default=True)
    if add_to_hoprc is None:
        raise typer.Exit(0)

    # Write files
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "commands").mkdir(exist_ok=True)
    (dest / "carrot.toml").write_text(
        CARROT_TOML_TEMPLATE.format(name=name, description=description, author=author, command_name=command_name)
    )
    (dest / "commands" / f"{command_name}.py").write_text(
        HELLO_COMMAND_TEMPLATE.format(command_name=command_name, logo=LOGO)
    )

    if add_to_hoprc:
        from hop.carrot import manager
        try:
            manager.add_to_config(f"path:{dest}")
        except ValueError:
            pass

    console.print(f"\n[green]✓[/green] Created [bold]{name}[/bold] at {dest}\n")
    console.print(f"  {name}/")
    console.print(f"  ├── carrot.toml")
    console.print(f"  └── commands/")
    console.print(f"      └── {command_name}.py")
    console.print(f"\nTest it out:")
    console.print(f"  hop carrot install")
    console.print(f"  hop {command_name}")
    console.print(f"\nWhen ready to publish:")
    console.print(f"  cd {dest}")
    console.print(f"  git init && git add . && git commit -m 'Initial scaffold'")
    console.print(f"  gh repo create {name} --public")
    console.print()
