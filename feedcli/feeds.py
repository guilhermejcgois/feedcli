from __future__ import annotations

from pathlib import Path

from .config import DEFAULT_FEEDS_FILE


def load_feeds(path: Path | None = None) -> list[str]:
    """Lê o arquivo de feeds (um URL por linha). Linhas com # são ignoradas."""
    p = path or DEFAULT_FEEDS_FILE
    if not p.exists():
        raise FileNotFoundError(
            f"Arquivo de feeds não encontrado: {p}. Crie um feeds.txt com um URL por linha."
        )
    feeds: list[str] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        feeds.append(s)
    if not feeds:
        raise ValueError("feeds.txt está vazio.")
    return feeds
