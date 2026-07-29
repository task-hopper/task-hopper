import importlib
import sys
from pathlib import Path

import typer
from packaging.version import Version

from hop import __version__
from hop.carrot.manifest import load_manifest
from hop.carrot.registry import registry
from hop.config import configs

CARROTS_DIR = Path.home() / ".hop" / "carrots"


def _carrots_dirs() -> list[Path]:
    from hop.carrot.resolver import CarrotSourceType, parse
    dirs = []
    if CARROTS_DIR.exists():
        dirs.extend(p for p in CARROTS_DIR.iterdir() if p.is_dir())
    for raw in configs.get().get("carrots", []):
        source = parse(raw)
        if source.source_type == CarrotSourceType.LOCAL:
            p = Path(source.raw).expanduser()
            if p.is_dir():
                dirs.append(p)
    for path_str in configs.get().get("carrot_paths", []):
        p = Path(path_str).expanduser()
        if p.is_dir():
            dirs.append(p)
    return dirs


def _check_version(min_hop_version: str, carrot_name: str) -> None:
    if Version(__version__) < Version(min_hop_version):
        raise RuntimeError(
            f"Carrot '{carrot_name}' requires hop >={min_hop_version} "
            f"but you have {__version__}. Run 'hop update' or upgrade task-hopper."
        )


def _import_module(module_path: str, carrot_name: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"Carrot '{carrot_name}': could not import '{module_path}' — {e}"
        ) from e


def load_carrots(app: typer.Typer) -> None:
    """Discover installed carrots, validate manifests, and register their commands."""
    for carrot_dir in _carrots_dirs():
        try:
            manifest = load_manifest(carrot_dir)
        except (FileNotFoundError, ValueError) as e:
            typer.echo(f"Warning: skipping {carrot_dir.name} — {e}", err=True)
            continue

        _check_version(manifest.carrot.min_hop_version, manifest.carrot.name)

        for command_name in manifest.commands:
            registry.register(command_name, manifest.carrot.name)

        if str(carrot_dir) not in sys.path:
            sys.path.insert(0, str(carrot_dir))

        for command_name, module_path in manifest.commands.items():
            module = _import_module(module_path, manifest.carrot.name)
            if not hasattr(module, "register"):
                raise AttributeError(
                    f"Carrot '{manifest.carrot.name}': module '{module_path}' "
                    f"has no register(app) function"
                )
            module.register(app)
