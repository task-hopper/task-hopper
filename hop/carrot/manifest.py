from pathlib import Path

import tomllib
from pydantic import BaseModel, ValidationError


class CarrotMeta(BaseModel):
    name: str
    version: str
    description: str
    min_hop_version: str
    author: str


class CarrotManifest(BaseModel):
    carrot: CarrotMeta
    commands: dict[str, str] = {}


def load_manifest(carrot_dir: Path) -> CarrotManifest:
    """Parse and validate a carrot.toml from the given carrot directory."""
    manifest_path = carrot_dir / "carrot.toml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No carrot.toml found in {carrot_dir}")
    with manifest_path.open("rb") as f:
        data = tomllib.load(f)
    try:
        return CarrotManifest(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid carrot.toml in {carrot_dir}:\n{e}") from e
