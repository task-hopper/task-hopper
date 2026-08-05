from pathlib import Path

import yaml
from jinja2 import BaseLoader, Environment


def _mergedicts(base: dict, override: dict) -> dict:
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _mergedicts(result[key], value)
        else:
            result[key] = value
    return result


def _render_config(raw: str, context: dict) -> dict:
    template = Environment(loader=BaseLoader()).from_string(raw)
    rendered = template.render(**context)
    return yaml.safe_load(rendered) or {}


def _extract_scalars(raw: str) -> dict:
    """Parse only top-level scalar key:value pairs for use as template context."""
    context = {}
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or ":" not in stripped or stripped.startswith("-"):
            continue
        if line and line[0] in (" ", "\t"):
            continue
        key, _, value = stripped.partition(":")
        value = value.strip()
        if value and not value.startswith("{") and not value.startswith("["):
            context[key.strip()] = value
    return context


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    raw = path.read_text()
    context = _extract_scalars(raw)
    return _render_config(raw, context)


class ConfigHandler:
    def __init__(self) -> None:
        self._global = _load_yaml(Path.home() / ".hoprc")

    def get(self) -> dict:
        """Return ~/.hoprc deep-merged with the .hop file in the current directory, if present."""
        local = _load_yaml(Path.cwd() / ".hop")
        return _mergedicts(self._global, local)

    def carrot_configs(self, carrot_name: str) -> dict:
        """Return the config namespace for the given carrot."""
        return self.get().get(carrot_name, {})
