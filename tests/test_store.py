from feedcli.models import Item


def test_save_and_load_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("FEEDCLI_CACHE_DIR", str(tmp_path))
    # Recarregar módulo para pegar novo caminho
    from importlib import reload

    import feedcli.config as cfg
    reload(cfg)
    import feedcli.store as store
    reload(store)

    items = [Item("S", "T", "L", None)]
    store.save_cache(items)
    data = store.load_cache()
    assert data["items"][0]["link"] == "L"
