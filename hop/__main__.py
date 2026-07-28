import typer

from hop.carrot.loader import load_carrots
from hop.commands.carrot import app as carrot_app
from hop.commands.init import init

app = typer.Typer(
    name="hop",
    help="Task Hopper — extensible shell session manager.",
    no_args_is_help=True,
)

app.add_typer(carrot_app, name="carrot")
app.command()(init)


def _load_configured_commands() -> None:
    from hop.config import configs
    from hop.composer import composer
    from hop.core.directives import TASK

    commands = configs.local_configs().get("commands", {})
    for alias, shell_cmd in commands.items():
        def make_command(cmd: str):
            def command(args: list[str] = typer.Argument(None)) -> None:
                full_cmd = cmd if not args else f"{cmd} {' '.join(args)}"
                composer.add(TASK, full_cmd)
            command.__name__ = alias
            command.__doc__ = f"Run: {cmd}"
            return command
        app.command(name=alias)(make_command(shell_cmd))


def main() -> None:
    load_carrots(app)
    _load_configured_commands()
    app()


if __name__ == "__main__":
    main()
