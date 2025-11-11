from __future__ import annotations

from collections.abc import Iterable

from .models import Item


def dedup_by_link(items: Iterable[Item]) -> list[Item]:
    seen: dict[str, Item] = {}
    for it in items:
        seen[it.link] = it
    return list(seen.values())


def sort_items(items: list[Item]) -> list[Item]:
    # Ordena por (published, title) decrescente; published None vai para o fim
    def key(it: Item):
        pub = it.published or ""
        return (pub, it.title or "")

    return sorted(items, key=key, reverse=True)
