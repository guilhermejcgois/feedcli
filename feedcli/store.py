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

def _index_seen_by_link(existing: Cache) -> dict[str, bool]:
    m: dict[str, bool] = {}
    for d in existing.get("items", []):
        link = d.get("link")
        if link is not None:
            m[str(link)] = bool(d.get("seen", False))
    return m

def save_cache(items: list[Item]) -> None:
    existing = load_cache()
    seen_map = _index_seen_by_link(existing)
    merged: list[dict] = []
    new_count = 0
    for it in items:
        was_seen = seen_map.get(it.link, False)
        if it.link not in seen_map:
            new_count += 1
        merged.append({**it.__dict__, "seen": was_seen or it.seen})
    data: Cache = {"ts": int(time.time()), "items": merged, "new_count": new_count}
    CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return