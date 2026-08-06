import importlib
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import tomllib
import typer
import yaml
from packaging.version import Version, InvalidVersion
from pydantic import ValidationError
from rich.console import Console
from rich.padding import Padding
from rich.text import Text

from hop import __version__

_INSTALLER_URL = "https://raw.githubusercontent.com/task-hopper/task-hopper/main/install.sh"


class Status(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class Check:
    label: str
    status: Status
    detail: str = ""
    fix: str = ""


@dataclass
class Group:
    title: str
    checks: list[Check] = field(default_factory=list)


@dataclass
class Section:
    title: str
    checks: list[Check] = field(default_factory=list)
    groups: list[Group] = field(default_factory=list)


def _check_install() -> Section:
    s = Section("Install")
    expected_venv = Path.home() / ".hop" / "venv"

    has_invocation = bool(os.environ.get("HOP_SHELL_INVOCATION"))
    s.checks.append(Check(
        "Shell wrapper invocation",
        Status.PASS if has_invocation else Status.FAIL,
        fix=f"Add `source ~/.hop/hop.sh` to your ~/.bashrc or ~/.zshrc and reload your shell.",
    ))

    in_correct_venv = Path(sys.prefix).resolve() == expected_venv.resolve()
    s.checks.append(Check(
        "Isolated venv",
        Status.PASS if in_correct_venv else Status.FAIL,
        detail=f"Running from {sys.prefix}" if not in_correct_venv else "",
        fix=f"Reinstall with: curl -fsSL {_INSTALLER_URL} | bash",
    ))

    venv_bin = expected_venv / "bin" / "hop"
    s.checks.append(Check(
        "Venv binary",
        Status.PASS if venv_bin.exists() else Status.FAIL,
        detail="" if venv_bin.exists() else str(venv_bin),
        fix=f"Reinstall with: curl -fsSL {_INSTALLER_URL} | bash",
    ))

    wrapper = Path.home() / ".hop" / "hop.sh"
    s.checks.append(Check(
        "Shell wrapper file",
        Status.PASS if wrapper.exists() else Status.FAIL,
        detail="" if wrapper.exists() else str(wrapper),
        fix=f"Reinstall with: curl -fsSL {_INSTALLER_URL} | bash",
    ))

    shim = Path.home() / ".local" / "bin" / "hop"
    s.checks.append(Check(
        "Shim",
        Status.PASS if shim.exists() else Status.WARN,
        detail="" if shim.exists() else str(shim),
        fix="Reinstall or ensure ~/.local/bin/hop exists and is executable.",
    ))

    return s


def _check_config() -> Section:
    s = Section("Config")
    hoprc = Path.home() / ".hoprc"

    if not hoprc.exists():
        s.checks.append(Check(
            "~/.hoprc exists",
            Status.WARN,
            fix="Run `hop init` to create one.",
        ))
        return s

    s.checks.append(Check("~/.hoprc exists", Status.PASS))

    try:
        from hop.core.config import _load_yaml as _load_hop_yaml
        _load_hop_yaml(hoprc)
        s.checks.append(Check("~/.hoprc is valid YAML", Status.PASS))
    except Exception as e:
        s.checks.append(Check(
            "~/.hoprc is valid YAML",
            Status.FAIL,
            detail=str(e),
            fix="Fix the YAML syntax in ~/.hoprc.",
        ))

    local_hop = Path.cwd() / ".hop"
    if local_hop.is_file():
        try:
            from hop.core.config import _load_yaml as _load_hop_yaml
            _load_hop_yaml(local_hop)
            s.checks.append(Check(".hop (cwd) is valid YAML", Status.PASS))
        except Exception as e:
            s.checks.append(Check(
                ".hop (cwd) is valid YAML",
                Status.FAIL,
                detail=str(e),
                fix=f"Fix the YAML syntax in {local_hop}.",
            ))

    return s


def _carrot_dirs() -> list[Path]:
    from hop.carrot.resolver import CarrotSourceType, parse
    from hop.config import configs

    dirs = []
    carrots_home = Path.home() / ".hop" / "carrots"
    if carrots_home.exists():
        dirs.extend(p for p in carrots_home.iterdir() if p.is_dir())

    try:
        cfg = configs.get()
    except Exception:
        return dirs

    for raw in cfg.get("carrots", []):
        source = parse(raw)
        if source.source_type == CarrotSourceType.LOCAL:
            p = Path(source.raw).expanduser()
            if p.is_dir():
                dirs.append(p)
    for path_str in cfg.get("carrot_paths", []):
        p = Path(path_str).expanduser()
        if p.is_dir():
            dirs.append(p)

    return dirs


def _check_carrots() -> Section:
    from hop.carrot.manifest import CarrotManifest

    s = Section("Carrots")
    dirs = _carrot_dirs()

    if not dirs:
        s.checks.append(Check("No carrots configured.", Status.WARN))
        return s

    seen_commands: dict[str, str] = {}

    for carrot_dir in dirs:
        name = carrot_dir.name
        g = Group(name)

        manifest_path = carrot_dir / "carrot.toml"
        if not manifest_path.exists():
            g.checks.append(Check(
                "carrot.toml present",
                Status.FAIL,
                fix=f"Add a carrot.toml to {carrot_dir}.",
            ))
            s.groups.append(g)
            continue

        g.checks.append(Check("carrot.toml present", Status.PASS))

        try:
            with manifest_path.open("rb") as f:
                data = tomllib.load(f)
        except Exception as e:
            g.checks.append(Check(
                "carrot.toml valid TOML",
                Status.FAIL,
                detail=str(e),
                fix=f"Fix the TOML syntax in {manifest_path}.",
            ))
            s.groups.append(g)
            continue

        try:
            manifest = CarrotManifest(**data)
            g.checks.append(Check("carrot.toml schema valid", Status.PASS))
        except ValidationError as e:
            errors = "; ".join(
                f"{'.'.join(str(x) for x in err['loc'])}: {err['msg']}"
                for err in e.errors()
            )
            g.checks.append(Check(
                "carrot.toml schema valid",
                Status.FAIL,
                detail=errors,
                fix=f"Fix the fields in {manifest_path}.",
            ))
            s.groups.append(g)
            continue

        try:
            if Version(__version__) < Version(manifest.carrot.min_hop_version):
                g.checks.append(Check(
                    "version compatible",
                    Status.FAIL,
                    detail=f"requires hop >={manifest.carrot.min_hop_version}, have {__version__}",
                    fix=f"Upgrade task-hopper: curl -fsSL {_INSTALLER_URL} | bash",
                ))
            else:
                g.checks.append(Check("version compatible", Status.PASS))
        except InvalidVersion as e:
            g.checks.append(Check(
                "version compatible",
                Status.FAIL,
                detail=str(e),
                fix=f"Fix min_hop_version in {manifest_path}.",
            ))

        if str(carrot_dir) not in sys.path:
            sys.path.insert(0, str(carrot_dir))

        for cmd_name, module_path in manifest.commands.items():
            if cmd_name in seen_commands:
                g.checks.append(Check(
                    f"command '{cmd_name}' unique",
                    Status.FAIL,
                    detail=f"already registered by '{seen_commands[cmd_name]}'",
                    fix="Rename the conflicting command in one of the carrot.toml files.",
                ))
            else:
                seen_commands[cmd_name] = name

            try:
                module = importlib.import_module(module_path)
                if not hasattr(module, "register"):
                    g.checks.append(Check(
                        f"{module_path} has register()",
                        Status.FAIL,
                        fix=f"Add a register(app) function to {module_path}.",
                    ))
                else:
                    g.checks.append(Check(f"{module_path} importable", Status.PASS))
            except Exception as e:
                g.checks.append(Check(
                    f"{module_path} importable",
                    Status.FAIL,
                    detail=str(e),
                    fix=f"Ensure {module_path} exists and has no import errors.",
                ))

        s.groups.append(g)

    return s


def _render(sections: list[Section]) -> bool:
    console = Console()
    any_fail = False

    icons = {
        Status.PASS: Text("✓", style="bold green"),
        Status.WARN: Text("!", style="bold yellow"),
        Status.FAIL: Text("✗", style="bold red"),
    }

    def render_check(check: Check, indent: int) -> None:
        nonlocal any_fail
        if check.status == Status.FAIL:
            any_fail = True
        icon = icons[check.status]
        pad = " " * indent
        line = Text(pad) + icon + Text(f"  {check.label}")
        if check.detail:
            line += Text(f" — {check.detail}", style="dim")
        console.print(line)
        if check.fix and check.status != Status.PASS:
            console.print(Padding(f"[dim]Fix: {check.fix}[/dim]", (0, 0, 0, indent + 4)))

    for section in sections:
        console.print(f"\n[bold]{section.title}[/bold]")
        for check in section.checks:
            render_check(check, indent=2)
        for group in section.groups:
            console.print(f"  [dim]{group.title}[/dim]")
            for check in group.checks:
                render_check(check, indent=4)

    console.print()
    return any_fail


def doctor() -> None:
    """Diagnose your hop installation."""
    sections = [
        _check_install(),
        _check_config(),
        _check_carrots(),
    ]
    any_fail = _render(sections)
    raise typer.Exit(1 if any_fail else 0)
