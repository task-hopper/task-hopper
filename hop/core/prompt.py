from typing import Any

import questionary
from prompt_toolkit.input import create_input
from prompt_toolkit.output import create_output


def _tty():
    try:
        tty_in = create_input(open("/dev/tty", "r"))
        tty_out = create_output(open("/dev/tty", "w"))
        return tty_in, tty_out
    except OSError:
        return None, None


def ask(message: str, default: str | None = None, instruction: str | None = None, **kwargs) -> str | None:
    """Prompt for text input, working correctly through hop's shell pipe."""
    tty_in, tty_out = _tty()
    instr = instruction
    if default and not instr:
        instr = f"(default: {default})"
    elif default and instr:
        instr = f"{instr} (default: {default})"

    result = questionary.text(
        message,
        default="",
        instruction=instr,
        input=tty_in,
        output=tty_out,
        **kwargs,
    ).ask()

    if result is None:
        return None
    return result if result.strip() else (default or "")


def confirm(message: str, default: bool = True, **kwargs) -> bool | None:
    """Prompt for a yes/no confirmation, working correctly through hop's shell pipe."""
    tty_in, tty_out = _tty()
    return questionary.confirm(
        message,
        default=default,
        input=tty_in,
        output=tty_out,
        **kwargs,
    ).ask()


def select(message: str, choices: list[Any], **kwargs) -> Any | None:
    """Prompt for a selection from a list, working correctly through hop's shell pipe."""
    tty_in, tty_out = _tty()
    return questionary.select(
        message,
        choices=choices,
        input=tty_in,
        output=tty_out,
        **kwargs,
    ).ask()


def path(message: str, default: str | None = None, **kwargs) -> str | None:
    """Prompt for a filesystem path with tab completion, working correctly through hop's shell pipe."""
    tty_in, tty_out = _tty()
    prompt = f"{message} (default: {default})" if default else message
    result = questionary.path(
        prompt,
        default="",
        input=tty_in,
        output=tty_out,
        **kwargs,
    ).ask()
    if result is None:
        return None
    return result if result.strip() else (default or "")
