from __future__ import annotations

import webbrowser
from typing import Any, cast

import typer
from rich.console import Console
from rich.table import Table

from .config import DEFAULT_PER_FEED
from .core import dedup_by_link, sort_items
from .feeds import load_feeds
from .fetch import fetch_all
from .render import render_article
from .store import load_cache, save_cache

app = typer.Typer(add_completion=False)
console = Console()


def _show_table(items: list[dict], max_rows: int = 30) -> None:
    table = Table(show_header=True, header_style="bold")
    table.add_column("Idx", justify="right", width=4)
    table.add_column("Fonte", style="dim", no_wrap=True)
    table.add_column("Título")
    table.add_column("Publicado", style="dim")
    for i, it in enumerate(items[:max_rows]):
        table.add_row(str(i), it.get("source", ""), it.get("title", ""), it.get("published") or "—")
    console.print(table)


@app.command()
def update(per_feed: int = DEFAULT_PER_FEED):
    """Atualiza o cache com os feeds do arquivo feeds.txt."""
    feeds = load_feeds()
    raw = fetch_all(feeds, limit_per_feed=per_feed)
    items = sort_items(dedup_by_link(raw))
    save_cache(items)
    console.print(f"[green]Atualizado {len(items)} itens.[/green]")


@app.command()
def list_cmd(max_rows: int = 30, refresh: bool = False):
    """Lista posts do cache (use --refresh para baixar agora)."""
    if refresh:
        update()
    data = load_cache()
    _show_table(data.get("items", []), max_rows=max_rows)


@app.command()
def open(idx: int):
    """Abre o item no navegador padrão."""
    data = load_cache()
    items: list[dict[str, Any]] = cast(list[dict[str, Any]], data.get("items", []))
    if not (0 <= idx < len(items)):
        console.print("[red]Índice inválido. Rode `feed list` para ver os itens.[/red]")
        raise typer.Exit(1)
    webbrowser.open(items[idx]["link"])


@app.command()
def read(idx: int):
    """Renderiza o item no terminal (modo leitura)."""
    data = load_cache()
    items: list[dict[str, Any]] = cast(list[dict[str, Any]], data.get("items", []))
    if not (0 <= idx < len(items)):
        console.print("[red]Índice inválido. Rode `feed list` para ver os itens.[/red]")
        raise typer.Exit(1)
    render_article(items[idx]["link"])


if __name__ == "__main__":
    app()
