from __future__ import annotations

from collections.abc import Iterable

import feedparser  # type: ignore[import-untyped]

from .models import Item


def fetch_all(feeds: Iterable[str], limit_per_feed: int = 10) -> list[Item]:
    items: list[Item] = []
    for url in feeds:
        parsed = feedparser.parse(url)
        source = getattr(parsed.feed, "title", url)
        for e in parsed.entries[:limit_per_feed]:
            link = getattr(e, "link", None)
            if not link:
                continue
            title = getattr(e, "title", "(sem título)")
            published = getattr(e, "published", getattr(e, "updated", None))
            items.append(Item(source=source, title=title, link=link, published=published))
    return items
