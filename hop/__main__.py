import typer

from hop.carrot.loader import load_carrots
from hop.commands.carrot import app as carrot_app
from hop.commands.init import init

app = typer.Typer(
    name="hop",
    help="Task Hopper — extensible shell session manager.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

app.add_typer(carrot_app, name="carrot")
app.command()(init)


def _load_configured_commands() -> None:
    from hop.config import configs
    from hop.core.commands import register_command

    commands = configs.get().get("commands", {})
    for alias, shell_cmd in commands.items():
        register_command(app, alias, shell_cmd)


def main() -> None:
    _load_configured_commands()
    load_carrots(app)
    app()


if __name__ == "__main__":
    main()
