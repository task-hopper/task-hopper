import json
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

import tomllib
from packaging.version import Version

from hop import __version__
from hop.carrot.manifest import load_manifest
from hop.carrot.resolver import CarrotSource, CarrotSourceType, parse

CARROTS_DIR = Path.home() / ".hop" / "carrots"
SOURCE_FILE = ".carrot-source.json"
DEFAULT_INDEX_URL = (
    "https://raw.githubusercontent.com/task-hopper/task-hopper-carrots/main/carrot-index.toml"
)


def _index_url() -> str:
    from hop.config import configs
    return configs.get().get("index_url", DEFAULT_INDEX_URL)


def _fetch_index() -> dict:
    url = _index_url()
    try:
        with urllib.request.urlopen(url) as response:
            return tomllib.loads(response.read().decode())
    except Exception as e:
        raise RuntimeError(f"Failed to fetch carrot index from {url}: {e}") from e


def _github_tarball_url(repo: str, ref: str | None) -> str:
    if ref:
        return f"https://github.com/{repo}/archive/refs/tags/{ref}.tar.gz"
    return f"https://api.github.com/repos/{repo}/tarball"


def _download_tarball(url: str, dest: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        tarball = tmp_path / "carrot.tar.gz"
        urllib.request.urlretrieve(url, tarball)
        with tarfile.open(tarball, "r:gz") as tar:
            tar.extractall(tmp_path)
        extracted = next(p for p in tmp_path.iterdir() if p.is_dir())
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(extracted, dest)


def _write_source(carrot_dir: Path, source: str) -> None:
    (carrot_dir / SOURCE_FILE).write_text(json.dumps({"source": source}))


def _read_source(carrot_dir: Path) -> str:
    source_file = carrot_dir / SOURCE_FILE
    if not source_file.exists():
        return "unknown"
    return json.loads(source_file.read_text()).get("source", "unknown")


def _validate_version(manifest_path: Path, carrot_name: str) -> None:
    manifest = load_manifest(manifest_path)
    if Version(__version__) < Version(manifest.carrot.min_hop_version):
        raise RuntimeError(
            f"Carrot '{carrot_name}' requires hop >={manifest.carrot.min_hop_version} "
            f"but you have {__version__}."
        )


def _install_from_source(source: CarrotSource) -> str:
    CARROTS_DIR.mkdir(parents=True, exist_ok=True)

    if source.source_type == CarrotSourceType.LOCAL:
        local_path = Path(source.raw).expanduser().resolve()
        if not local_path.exists():
            raise FileNotFoundError(f"Local carrot path not found: {local_path}")
        manifest = load_manifest(local_path)
        name = manifest.carrot.name
        dest = CARROTS_DIR / name
        _validate_version(local_path, name)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(local_path, dest)
        _write_source(dest, source.raw)
        return name

    if source.source_type == CarrotSourceType.OFFICIAL:
        index = _fetch_index()
        entry = index.get("carrots", {}).get(source.raw)
        if not entry:
            raise ValueError(f"Carrot '{source.raw}' not found in the official index.")
        repo = entry["repo"]
        url = _github_tarball_url(repo, source.ref)
        name = source.raw
    elif source.source_type == CarrotSourceType.GITHUB:
        url = _github_tarball_url(source.raw, source.ref)
        name = source.raw.split("/")[-1]
    elif source.source_type == CarrotSourceType.URL:
        url = source.raw
        name = source.raw.rstrip("/").split("/")[-1]
    else:
        raise ValueError(f"Unknown carrot source type: {source.source_type}")

    dest = CARROTS_DIR / name
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dest = Path(tmp) / name
        _download_tarball(url, tmp_dest)
        _validate_version(tmp_dest, name)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(tmp_dest, dest)

    _write_source(dest, source.display)
    return name


def install_all() -> list[dict]:
    """Install all uninstalled carrots declared in ~/.hoprc. Returns per-carrot results."""
    from hop.config import configs
    declared = configs.get().get("carrots", [])
    results = []
    for raw in declared:
        source = parse(raw)
        name = source.raw.split("/")[-1] if "/" in source.raw else source.raw
        dest = CARROTS_DIR / name
        if dest.exists():
            results.append({"raw": raw, "name": name, "status": "already installed"})
            continue
        try:
            installed_name = _install_from_source(source)
            results.append({"raw": raw, "name": installed_name, "status": "installed"})
        except Exception as e:
            results.append({"raw": raw, "name": name, "status": "failed", "error": str(e)})
    return results


def install_one(raw: str) -> str:
    """Install a single carrot by its declaration string. Returns the installed carrot name."""
    return _install_from_source(parse(raw))


def add_to_config(raw: str) -> None:
    """Append a carrot declaration to ~/.hoprc carrots list."""
    from hop.config import configs
    hoprc = Path.home() / ".hoprc"
    carrots = configs.get().get("carrots", [])
    if raw in carrots:
        raise ValueError(f"'{raw}' is already in your carrots list.")
    with hoprc.open("a") as f:
        if not carrots:
            f.write("\ncarrots:\n")
        f.write(f"  - {raw}\n")


def remove_from_config(raw: str) -> None:
    """Remove a carrot declaration from ~/.hoprc without deleting installed files."""
    hoprc = Path.home() / ".hoprc"
    lines = hoprc.read_text().splitlines(keepends=True)
    new_lines = [l for l in lines if l.strip() != f"- {raw}"]
    if len(new_lines) == len(lines):
        raise ValueError(f"'{raw}' not found in your carrots list.")
    hoprc.write_text("".join(new_lines))


def uninstall(raw: str) -> None:
    """Remove a carrot from ~/.hoprc and delete its installed files."""
    remove_from_config(raw)
    source = parse(raw)
    name = source.raw.split("/")[-1] if "/" in source.raw else source.raw
    carrot_dir = CARROTS_DIR / name
    if carrot_dir.exists():
        shutil.rmtree(carrot_dir)


def list_official() -> list[dict]:
    """Fetch and return all carrots available in the official index."""
    index = _fetch_index()
    installed = {p.name for p in CARROTS_DIR.iterdir()} if CARROTS_DIR.exists() else set()
    results = []
    for name, entry in index.get("carrots", {}).items():
        results.append({
            "name": name,
            "description": entry.get("description", ""),
            "installed": name in installed,
        })
    return results


def list_installed() -> list[dict]:
    """Return a list of installed carrots with name, version, source, and description."""
    if not CARROTS_DIR.exists():
        return []
    results = []
    for carrot_dir in sorted(CARROTS_DIR.iterdir()):
        if not carrot_dir.is_dir():
            continue
        try:
            manifest = load_manifest(carrot_dir)
            results.append({
                "name": manifest.carrot.name,
                "version": manifest.carrot.version,
                "source": _read_source(carrot_dir),
                "description": manifest.carrot.description,
            })
        except (FileNotFoundError, ValueError):
            results.append({
                "name": carrot_dir.name,
                "version": "?",
                "source": _read_source(carrot_dir),
                "description": "(invalid carrot — missing or broken carrot.toml)",
            })
    return results
