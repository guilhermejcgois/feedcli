
from typer.testing import CliRunner

from feedcli.cli import app
from feedcli.models import Cache, Item

runner = CliRunner()


def test_today_lists_only_items_added_after_prev_ts(monkeypatch):
    # Simula cache com prev_ts=100, ts=200:
    # - item 0: added_ts=50 (antigo)
    # - item 1: added_ts=150 (novo)
    # - item 2: added_ts=200 (também novo)
    fake_cache = Cache(
        prev_ts=100,
        ts=200,
        new_count=2,
        items=[
            Item(
                source="S1",
                title="Old post",
                link="L1",
                published="2025-01-01",
                seen=False,
                added_ts=50,
            ),
            Item(
                source="S2",
                title="New post A",
                link="L2",
                published="2025-01-02",
                seen=False,
                added_ts=150,
            ),
            Item(
                source="S3",
                title="New post B",
                link="L3",
                published="2025-01-03",
                seen=True,
                added_ts=200,
            ),
        ],
    )

    def fake_load_cache() -> Cache:
        return fake_cache

    monkeypatch.setattr("feedcli.cli.load_cache", fake_load_cache)

    result = runner.invoke(app, ["today"])

    assert result.exit_code == 0
    # Não deve aparecer o post antigo
    assert "Old post" not in result.stdout
    # Os novos devem aparecer
    assert "New post A" in result.stdout
    assert "New post B" in result.stdout
    # E o índice deve bater (idx 0 e 1, porque a tabela é só dos recentes)
    assert "Idx" in result.stdout
    assert "0" in result.stdout
    assert "1" in result.stdout


def test_today_prints_message_when_no_recent_items(monkeypatch):
    fake_cache = Cache(
        prev_ts=200,
        ts=300,
        new_count=0,
        items=[
            Item(
                source="S1",
                title="Old post",
                link="L1",
                published="2025-01-01",
                seen=False,
                added_ts=100,
            )
        ],
    )

    def fake_load_cache() -> Cache:
        return fake_cache

    monkeypatch.setattr("feedcli.cli.load_cache", fake_load_cache)

    result = runner.invoke(app, ["today"])

    assert result.exit_code == 0
    assert "Nenhum item novo desde o último update." in result.stdout
