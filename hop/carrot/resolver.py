from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class CarrotSourceType(Enum):
    OFFICIAL = "official"
    GITHUB = "github"
    URL = "url"
    LOCAL = "local"


@dataclass
class CarrotSource:
    raw: str
    source_type: CarrotSourceType
    ref: str | None = None

    @property
    def display(self) -> str:
        if self.source_type == CarrotSourceType.OFFICIAL:
            return "official"
        if self.source_type == CarrotSourceType.LOCAL:
            return self.raw
        return self.raw


def parse(raw: str) -> CarrotSource:
    """Parse a carrot declaration string into a CarrotSource."""
    ref = None

    if raw.startswith("path:"):
        path = raw.removeprefix("path:")
        return CarrotSource(raw=path, source_type=CarrotSourceType.LOCAL)

    if raw.startswith("https://"):
        if "@" in raw.split("/")[-1]:
            raw, ref = raw.rsplit("@", 1)
        return CarrotSource(raw=raw, source_type=CarrotSourceType.URL, ref=ref)

    if "/" in raw:
        if "@" in raw.split("/")[-1]:
            raw, ref = raw.rsplit("@", 1)
        return CarrotSource(raw=raw, source_type=CarrotSourceType.GITHUB, ref=ref)

    return CarrotSource(raw=raw, source_type=CarrotSourceType.OFFICIAL)
