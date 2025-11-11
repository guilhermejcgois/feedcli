from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Item:
    source: str
    title: str
    link: str
    published: str | None = None

Cache = dict[str, Any]  # {"ts": int, "items": List[Item as dict]}
