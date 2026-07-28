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

CARROTS_DIR = Path.home() / ".hop" / "carrots"
SOURCE_FILE = ".carrot-source.json"
DEFAULT_INDEX_URL = (
    "https://raw.githubusercontent.com/task-hopper/task-hopper-carrots/main/carrot-index.toml"
)


def _index_url() -> str:
    from hop.config import configs
    return configs.global_configs().get("index_url", DEFAULT_INDEX_URL)


def _fetch_index() -> dict:
    url = _index_url()
    try:
        with urllib.request.urlopen(url) as response:
            return tomllib.loads(response.read().decode())
    except Exception as e:
        raise RuntimeError(f"Failed to fetch carrot index from {url}: {e}") from e


def _download_tarball(repo: str, dest: Path, subpath: str | None = None) -> None:
    url = f"https://api.github.com/repos/{repo}/tarball/main"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        tarball = tmp_path / "carrot.tar.gz"
        urllib.request.urlretrieve(url, tarball)
        with tarfile.open(tarball, "r:gz") as tar:
            tar.extractall(tmp_path)
        extracted = next(p for p in tmp_path.iterdir() if p.is_dir())
        source = extracted / subpath if subpath else extracted
        if not source.exists():
            raise FileNotFoundError(f"Path '{subpath}' not found in {repo}")
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(source, dest)


def _write_source(carrot_dir: Path, source: str) -> None:
    (carrot_dir / SOURCE_FILE).write_text(json.dumps({"source": source}))


def _read_source(carrot_dir: Path) -> str:
    source_file = carrot_dir / SOURCE_FILE
    if not source_file.exists():
        return "unknown"
    return json.loads(source_file.read_text()).get("source", "unknown")


def _validate_and_install(tmp_dir: Path, dest: Path, source: str) -> str:
    manifest = load_manifest(tmp_dir)
    if Version(__version__) < Version(manifest.carrot.min_hop_version):
        raise RuntimeError(
            f"Carrot '{manifest.carrot.name}' requires hop >={manifest.carrot.min_hop_version} "
            f"but you have {__version__}."
        )
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(tmp_dir, dest)
    _write_source(dest, source)
    return manifest.carrot.name


def install_named(name: str) -> str:
    """Install a carrot by name from the official index. Returns the installed carrot name."""
    index = _fetch_index()
    entry = index.get("carrots", {}).get(name)
    if not entry:
        raise ValueError(f"Carrot '{name}' not found in the official index.")
    repo = entry["repo"]
    subpath = entry.get("path")
    dest = CARROTS_DIR / name
    CARROTS_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / name
        _download_tarball(repo, tmp_path, subpath)
        return _validate_and_install(tmp_path, dest, source="official")


def install_github(target: str) -> str:
    """Install a carrot from a GitHub repo (format: github:owner/repo). Returns carrot name."""
    repo = target.removeprefix("github:")
    name = repo.split("/")[-1]
    dest = CARROTS_DIR / name
    CARROTS_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / name
        _download_tarball(repo, tmp_path)
        return _validate_and_install(tmp_path, dest, source=target)


def remove(name: str) -> None:
    """Remove an installed carrot by name."""
    carrot_dir = CARROTS_DIR / name
    if not carrot_dir.exists():
        raise ValueError(f"Carrot '{name}' is not installed.")
    shutil.rmtree(carrot_dir)


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
