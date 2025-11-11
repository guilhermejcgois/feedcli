from __future__ import annotations

import json
import time
from typing import cast

from .config import CACHE_PATH
from .models import Cache, Item


def load_cache() -> Cache:
    if CACHE_PATH.exists():
        return cast(Cache, json.loads(CACHE_PATH.read_text(encoding="utf-8")))
    return {"items": [], "ts": 0}


def save_cache(items: list[Item]) -> None:
    data: Cache = {
        "ts": int(time.time()),
        "items": [it.__dict__ for it in items],
    }
    CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
