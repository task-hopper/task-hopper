import typer

from hop.composer import composer
from hop.core.directives import TASK


def register_command(app: typer.Typer, name: str, shell_cmd: str, panel: str | None = None) -> None:
    """Register a shell command alias as a Typer command on app."""
    def make_command(cmd: str, cmd_name: str):
        def command(args: list[str] = typer.Argument(None)) -> None:
            full_cmd = cmd if not args else f"{cmd} {' '.join(args)}"
            composer.add(TASK, full_cmd)
        command.__name__ = cmd_name
        command.__doc__ = f"Run: {cmd}"
        return command
    kwargs = {"name": name}
    if panel:
        kwargs["rich_help_panel"] = panel
    app.command(**kwargs)(make_command(shell_cmd, name))
