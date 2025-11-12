from __future__ import annotations

import webbrowser
from typing import Any, cast

import typer  # type: ignore
from rich.console import Console  # type: ignore
from rich.progress import (  # type: ignore
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table  # type: ignore

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
    table.add_column("Lido", style="dim", justify="center", width=5)
    for i, it in enumerate(items[:max_rows]):
        seen = "•" if bool(it.get("seen")) else ""
        table.add_row(
            str(i),
            str(it.get("source", "")),
            str(it.get("title", "")),
            str(it.get("published") or "—"),
            seen,
        )
    console.print(table)


@app.command()
def update(per_feed: int = DEFAULT_PER_FEED):
    """Atualiza o cache com os feeds do arquivo feeds.txt."""
    feeds = load_feeds()
    # progress UI
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Baixando feeds…", total=len(feeds))
        def on_feed(_url: str, _idx: int, _total: int) -> None:
            progress.advance(task)
        raw = fetch_all(feeds, limit_per_feed=per_feed)
        progress.update(task, completed=len(feeds))
    items = sort_items(dedup_by_link(raw))
    save_cache(items)
    data = load_cache()
    new_count = int(data.get("new_count", 0))
    console.print(f"[green]Atualizado {len(items)} itens[/green] ( +{new_count} novos ).")


@app.command("list")
def list_cmd( max_rows: int = 30,
    refresh: bool = False,
    source: str | None = typer.Option(None, help="Filtra pela fonte (substring/regex simples)"),
    search: str | None = typer.Option(None, help="Filtra pelo título (substring/regex simples)")):
    """Lista posts do cache (use --refresh para baixar agora)."""
    if refresh:
        update()
    data = load_cache()
    items: list[dict[str, Any]] = cast(list[dict[str, Any]], data.get("items", []))
    if source:
        import re
        rx = re.compile(source, re.IGNORECASE)
        items = [it for it in items if rx.search(str(it.get("source","")))]
    if search:
        import re
        rx = re.compile(search, re.IGNORECASE)
        items = [it for it in items if rx.search(str(it.get("title","")))]
    _show_table(items, max_rows=max_rows)


@app.command()
def open(idx: int):
    """Abre o item no navegador padrão."""
    data = load_cache()
    items: list[dict[str, Any]] = cast(list[dict[str, Any]], data.get("items", []))
    if not (0 <= idx < len(items)):
        console.print("[red]Índice inválido. Rode `feed list` para ver os itens.[/red]")
        raise typer.Exit(1)
    webbrowser.open(str(items[idx]["link"]))
    items[idx]["seen"] = True
    from .models import Item
    save_cache([Item(**{
        "source": it.get("source",""),
        "title": it.get("title",""),
        "link": it.get("link",""),
        "published": it.get("published"),
        "seen": bool(it.get("seen", False)),
    }) for it in items])


@app.command()
def read(idx: int):
    """Renderiza o item no terminal (modo leitura)."""
    data = load_cache()
    items: list[dict[str, Any]] = cast(list[dict[str, Any]], data.get("items", []))
    if not (0 <= idx < len(items)):
        console.print("[red]Índice inválido. Rode `feed list` para ver os itens.[/red]")
        raise typer.Exit(1)
    render_article(str(items[idx]["link"]))
    items[idx]["seen"] = True
    from .models import Item
    save_cache([Item(**{
        "source": it.get("source",""),
        "title": it.get("title",""),
        "link": it.get("link",""),
        "published": it.get("published"),
        "seen": bool(it.get("seen", False)),
    }) for it in items])


if __name__ == "__main__":
    app()
