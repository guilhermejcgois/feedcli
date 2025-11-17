from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    source: str
    title: str
    link: str
    published: str | None = None
    seen: bool = False
    added_ts: int | None = None

    def to_dict(self):
        return {
            "source": self.source,
            "title": self.title,
            "link": self.link,
            "published": self.published,
            "seen": self.seen,
            "added_ts": self.added_ts,
        }


@dataclass()
class Cache:
    ts: int
    prev_ts: int
    items: list[Item]
    new_count: int

    def to_dict(self):
        return {
            "ts": self.ts,
            "prev_ts": self.prev_ts,
            "items": [it.__dict__ for it in self.items],
            "new_count": self.new_count,
        }
