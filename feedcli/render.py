from __future__ import annotations

import os
import platform
import shutil
import tempfile
import webbrowser

import trafilatura  # type: ignore
from rich.console import Console  # type: ignore

console = Console()


def render_article(url: str) -> None:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        console.print("[yellow]Não consegui baixar; abrindo no navegador.[/yellow]")
        webbrowser.open(url)
        return
    md = trafilatura.extract(downloaded, output_format="markdown", include_links=False) or ""
    if not md.strip():
        console.print("[yellow]Não consegui extrair; abrindo no navegador.[/yellow]")
        webbrowser.open(url)
        return
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(md)
        tmp = f.name
    pager = os.environ.get("PAGER")
    if not pager:
        if platform.system() == "Windows":
            if shutil.which("glow"):
                pager = "glow -p"
            elif shutil.which("less"):
                pager = "less -R"
            elif shutil.which(r"C:\Program Files\Git\usr\bin\less.exe"):
                pager = r'"C:\Program Files\Git\usr\bin\less.exe" -R'
            else:
                webbrowser.open(url)
                return
        else:
            pager = "less -R"

    os.system(f'{pager} "{tmp}"')
