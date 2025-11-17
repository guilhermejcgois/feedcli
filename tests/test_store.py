from importlib import reload

from feedcli.models import Item


def _reload_with_tmp_cache(tmp_path, monkeypatch):
    """Helper pra redirecionar o cache pro tmp_path e recarregar módulos."""
    monkeypatch.setenv("FEEDCLI_CACHE_DIR", str(tmp_path))
    import feedcli.config as cfg

    reload(cfg)
    import feedcli.store as store

    reload(store)
    return store

def test_save_and_load_cache_basic(tmp_path, monkeypatch):
    store = _reload_with_tmp_cache(tmp_path, monkeypatch)

    items = [Item("S", "T", "L", "2025-01-01")]
    store.save_cache(items)
    data = store.load_cache()

    assert data.ts > 0
    assert data.prev_ts == 0
    assert data.new_count == 1
    assert len(data.items) == 1
    assert data.items[0].link == "L"
    assert data.items[0].added_ts == data.ts
    assert data.items[0].seen is False


def test_save_cache_preserves_seen_and_added_ts_and_counts_new(tmp_path, monkeypatch):
    store = _reload_with_tmp_cache(tmp_path, monkeypatch)

    # 1ª rodada: 2 itens
    first_items = [
        Item("S1", "T1", "L1", "2025-01-01"),
        Item("S1", "T2", "L2", "2025-01-02"),
    ]
    store.save_cache(first_items)
    first_data = store.load_cache()
    first_ts = first_data.ts

    # Força um write de volta pro cache no formato esperado pelo store
    from feedcli.models import Item as MItem

    existing_items = [
        MItem(
            source=it.source,
            title=it.title,
            link=it.link,
            published=it.published,
            seen=i == 0
        )
        for i, it in enumerate(first_data.items)
    ]
    # sobrescreve com seen via save_cache (que vai mesclar com existing)
    store.save_cache(existing_items)
    data_after_seen = store.load_cache()
    assert data_after_seen.items[0].seen is True

    # 2ª rodada: adiciona um item novo (L3)
    second_items = [
        Item("S1", "T1", "L1", "2025-01-01"),
        Item("S1", "T2", "L2", "2025-01-02"),
        Item("S2", "T3", "L3", "2025-01-03"),
    ]
    store.save_cache(second_items)
    second_data = store.load_cache()

    assert second_data.prev_ts == first_ts
    assert second_data.ts >= second_data.prev_ts
    # Apenas L3 é novo em relação ao cache anterior
    assert second_data.new_count == 1

    items_map = {it.link: it for it in second_data.items}
    # L1 e L2 preservam added_ts e seen
    assert items_map["L1"].added_ts == items_map["L2"].added_ts
    assert items_map["L1"].seen is True
    # L3 tem added_ts igual ao ts da 2ª rodada
    assert items_map["L3"].added_ts == second_data.ts