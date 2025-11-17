from __future__ import annotations

import json
import time

from .config import CACHE_PATH
from .models import Cache, Item


def load_cache() -> Cache:
    if CACHE_PATH.exists():
        cached = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        return Cache(
            items=[Item(
                added_ts=it.get("added_ts"),
                link=it.get("link", ""),
                published=it.get("published"),
                seen=bool(it.get("seen", False)),
                source=it.get("source", ""),
                title=it.get("title", ""),
            ) for it in cached.get("items", [])],
            new_count=cached.get("new_count", 0),
            ts=cached.get("ts", 0),
            prev_ts=cached.get("prev_ts", 0),
        )
    return Cache(items=[], ts=0, prev_ts=0, new_count=0)


def _index_existing_by_link(existing: Cache) -> dict[str, Item]:
    m: dict[str, Item] = {}
    for d in existing.items:
        link = d.link
        if link is not None:
            m[str(link)] = d
    return m


def save_cache(items: list[Item]) -> None:
    existing = load_cache()
    prev_ts = existing.ts
    now = int(time.time())
    existing_map = _index_existing_by_link(existing)

    merged: list[Item] = []
    new_count = 0
    for it in items:
        prev = existing_map.get(it.link)
        if prev is None:
            new_count += 1
            added_ts = now
            seen = it.seen
        else:
            added_ts = int(prev.added_ts) if prev.added_ts is not None else now
            seen = bool(prev.seen or it.seen)
        merged.append(
            Item(
                source=it.source,
                title=it.title,
                link=it.link,
                published=it.published,
                seen=seen,
                added_ts=added_ts,
            )
        )

    data = Cache(prev_ts=prev_ts, ts=now, items=merged, new_count=new_count)
    json_data = json.dumps(data.to_dict(), ensure_ascii=False, indent=2)
    CACHE_PATH.write_text(json_data, encoding="utf-8")
