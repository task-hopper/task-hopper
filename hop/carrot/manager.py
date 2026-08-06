import subprocess
from pathlib import Path

from hop.carrot.manifest import load_manifest
from hop.carrot.resolver import CarrotSourceType, parse

CARROTS_DIR = Path.home() / ".hop" / "carrots"


def _repo_name(repo: str) -> str:
    return repo.split("/")[-1]


def _clone(repo: str, ref: str | None, dest: Path) -> None:
    CARROTS_DIR.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/{repo}.git"
    cmd = ["git", "clone"]
    if ref:
        cmd += ["--branch", ref, "--depth", "1"]
    cmd += [url, str(dest)]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"git clone failed for {repo}")


def _pull(dest: Path) -> bool:
    """Pull latest. Returns True if updated, False if already up to date."""
    result = subprocess.run(["git", "-C", str(dest), "pull"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return "Already up to date." not in result.stdout


def _checkout_ref(dest: Path, ref: str) -> bool:
    """Fetch and checkout a specific ref. Returns True if HEAD changed."""
    before = subprocess.run(
        ["git", "-C", str(dest), "rev-parse", "HEAD"],
        capture_output=True, text=True
    ).stdout.strip()
    subprocess.run(["git", "-C", str(dest), "fetch", "--tags"], capture_output=True)
    result = subprocess.run(["git", "-C", str(dest), "checkout", ref], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    after = subprocess.run(
        ["git", "-C", str(dest), "rev-parse", "HEAD"],
        capture_output=True, text=True
    ).stdout.strip()
    return before != after


def _current_ref(dest: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(dest), "describe", "--tags", "--always"],
        capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def _github_carrots_from_config() -> list[tuple[str, str | None]]:
    from hop.config import configs
    results = []
    for raw in configs.get().get("carrots", []):
        source = parse(raw)
        if source.source_type == CarrotSourceType.GITHUB:
            results.append((source.raw, source.ref))
    return results


def install_all() -> list[dict]:
    """Clone all GitHub carrots in config that aren't already installed."""
    from hop.config import configs
    declared = configs.get().get("carrots", [])
    results = []
    for raw in declared:
        source = parse(raw)
        if source.source_type != CarrotSourceType.GITHUB:
            continue
        name = _repo_name(source.raw)
        dest = CARROTS_DIR / name
        if dest.exists():
            results.append({"name": name, "status": "already_installed"})
            continue
        try:
            _clone(source.raw, source.ref, dest)
            results.append({"name": name, "status": "installed"})
        except Exception as e:
            results.append({"name": name, "status": "failed", "error": str(e)})
    return results


def update_all() -> list[dict]:
    """Update all installed GitHub carrots. Pinned ones update to their pinned ref."""
    github_carrots = {_repo_name(repo): (repo, ref) for repo, ref in _github_carrots_from_config()}
    results = []
    if not CARROTS_DIR.exists():
        return results
    for carrot_dir in sorted(CARROTS_DIR.iterdir()):
        if not carrot_dir.is_dir():
            continue
        name = carrot_dir.name
        if name not in github_carrots:
            continue
        _, ref = github_carrots[name]
        try:
            if ref:
                changed = _checkout_ref(carrot_dir, ref)
                status = "updated" if changed else "already_at_version"
            else:
                changed = _pull(carrot_dir)
                status = "updated" if changed else "already_up_to_date"
            results.append({"name": name, "status": status, "ref": _current_ref(carrot_dir)})
        except Exception as e:
            results.append({"name": name, "status": "failed", "error": str(e)})
    return results


def update_one(name: str) -> list[dict]:
    """Update a single carrot by repo name."""
    matches = [(repo, ref) for repo, ref in _github_carrots_from_config() if _repo_name(repo) == name]
    if not matches:
        raise ValueError(f"No carrot named '{name}' found in ~/.hoprc.")
    if len(matches) > 1:
        repos = ", ".join(repo for repo, _ in matches)
        raise ValueError(f"Multiple carrots named '{name}': {repos}. Specify the full org/repo.")
    repo, ref = matches[0]
    dest = CARROTS_DIR / name
    if not dest.exists():
        raise ValueError(f"'{name}' is in config but not installed. Run 'hop carrot install' first.")
    try:
        if ref:
            changed = _checkout_ref(dest, ref)
            status = "updated" if changed else "already_at_version"
        else:
            changed = _pull(dest)
            status = "updated" if changed else "already_up_to_date"
        return [{"name": name, "status": status, "ref": _current_ref(dest)}]
    except Exception as e:
        return [{"name": name, "status": "failed", "error": str(e)}]


def list_installed() -> list[dict]:
    """Return all installed carrots: GitHub clones and local path carrots."""
    from hop.config import configs
    results = []
    if CARROTS_DIR.exists():
        for carrot_dir in sorted(CARROTS_DIR.iterdir()):
            if not carrot_dir.is_dir():
                continue
            try:
                manifest = load_manifest(carrot_dir)
                results.append({
                    "name": manifest.carrot.name,
                    "version": _current_ref(carrot_dir),
                    "source": "github",
                    "description": manifest.carrot.description,
                })
            except (FileNotFoundError, ValueError):
                results.append({
                    "name": carrot_dir.name,
                    "version": "?",
                    "source": "github",
                    "description": "(invalid — missing or broken carrot.toml)",
                })
    for raw in configs.get().get("carrots", []):
        source = parse(raw)
        if source.source_type == CarrotSourceType.LOCAL:
            local_path = Path(source.raw).expanduser()
            try:
                manifest = load_manifest(local_path)
                results.append({
                    "name": manifest.carrot.name,
                    "version": "local",
                    "source": str(local_path),
                    "description": manifest.carrot.description,
                })
            except (FileNotFoundError, ValueError):
                results.append({
                    "name": local_path.name,
                    "version": "local",
                    "source": str(local_path),
                    "description": "(invalid — missing or broken carrot.toml)",
                })
    return results
