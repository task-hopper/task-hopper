import importlib.util
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
    dirs = []
    if CARROTS_DIR.exists():
        dirs.extend(p for p in CARROTS_DIR.iterdir() if p.is_dir())
    for path_str in configs.global_configs().get("carrot_paths", []):
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


def _import_module(module_path: str, carrot_dir: Path, carrot_name: str):
    parts = module_path.split(".")
    file_path = carrot_dir.joinpath(*parts).with_suffix(".py")
    if not file_path.exists():
        raise FileNotFoundError(
            f"Carrot '{carrot_name}': module '{module_path}' not found at {file_path}"
        )
    module_name = f"hop_carrot_{carrot_name}_{module_path.replace('.', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


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

        for command_name, module_path in manifest.commands.items():
            module = _import_module(module_path, carrot_dir, manifest.carrot.name)
            if not hasattr(module, "register"):
                raise AttributeError(
                    f"Carrot '{manifest.carrot.name}': module '{module_path}' "
                    f"has no register(app) function"
                )
            module.register(app)
