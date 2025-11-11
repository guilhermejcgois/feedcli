from feedcli.core import dedup_by_link, sort_items
from feedcli.models import Item


def test_dedup_by_link():
    items = [
        Item("A", "t1", "http://x", "2025-10-01"),
        Item("A", "t1-dup", "http://x", "2025-10-02"),
        Item("B", "t2", "http://y", None),
    ]
    out = dedup_by_link(items)
    assert len(out) == 2
    assert {it.link for it in out} == {"http://x", "http://y"}


def test_sort_items():
    items = [
        Item("A", "b", "l1", None),
        Item("A", "a", "l2", "2025-10-02"),
        Item("A", "c", "l3", "2025-09-01"),
    ]
    out = sort_items(items)
    assert [it.link for it in out] == ["l2", "l3", "l1"]

