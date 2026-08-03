import os
import sys
from pathlib import Path

import typer

from hop.carrot.loader import load_carrots
from hop.commands.carrot import app as carrot_app
from hop.commands.doctor import doctor
from hop.commands.init import init

_INSTALLER_URL = "https://raw.githubusercontent.com/task-hopper/task-hopper/main/install.sh"

app = typer.Typer(
    name="hop",
    add_completion=False,
    help="Task Hopper — extensible shell session manager.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

app.add_typer(carrot_app, name="carrot")
app.command()(init)
app.command()(doctor)


def _load_configured_commands() -> None:
    from hop.config import configs
    from hop.core.commands import register_command

    commands = configs.get().get("commands", {})
    for alias, shell_cmd in commands.items():
        register_command(app, alias, shell_cmd)


def _check_setup() -> None:
    expected_venv = Path.home() / ".hop" / "venv"
    in_correct_venv = Path(sys.prefix).resolve() == expected_venv.resolve()
    has_shell_invocation = bool(os.environ.get("HOP_SHELL_INVOCATION"))

    if in_correct_venv and has_shell_invocation:
        return

    if has_shell_invocation and not in_correct_venv:
        print(
            "hop is running outside its isolated venv.\n"
            "\n"
            "You may have installed it with pip or pipx directly.\n"
            "Reinstall using the official installer:\n"
            "\n"
            f"  curl -fsSL {_INSTALLER_URL} | bash\n",
            file=sys.stderr,
        )
    elif in_correct_venv and not has_shell_invocation:
        print(
            "hop must be run through the shell wrapper, not called directly.\n"
            "\n"
            "Add this to your ~/.bashrc or ~/.zshrc and reload your shell:\n"
            "\n"
            "  source ~/.hop/hop.sh\n",
            file=sys.stderr,
        )
    else:
        print(
            "hop is not set up correctly.\n"
            "\n"
            "Install it with:\n"
            "\n"
            f"  curl -fsSL {_INSTALLER_URL} | bash\n",
            file=sys.stderr,
        )

    sys.exit(1)


def main() -> None:
    _check_setup()
    _load_configured_commands()
    load_carrots(app)
    app()


if __name__ == "__main__":
    main()
