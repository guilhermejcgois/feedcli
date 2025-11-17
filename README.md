# feedcli

Feeder de terminal (RSS/Atom) em Python. Lista posts e permite abrir no navegador ou ler no terminal com “readability”.

## Instalação rápida
```bash
# Python 3.11+
python -m venv .venv && source .venv/bin/activate
pip install -e .
# deps runtime
pip install typer[all] rich feedparser trafilatura beautifulsoup4
```

## Uso
```bash
feed update                         # baixa/atualiza cache
feed today                          # mostra apenas itens adicionados desde o último update
feed list --refresh                 # lista itens (já atualiza)
feed list --source "Spotify"        # filtra pela fonte
feed list --search "python|airflow" # filtra pelo título (regex)
feed read 0                         # lê no terminal o item 0
feed open 0                         # abre no navegador o item 0
```

## Configuração
- `feeds.txt`: um URL por linha; linhas iniciadas com `#` são ignoradas.
- `FEEDCLI_FEEDS`: path alternativo para o arquivo de feeds.
- `FEEDCLI_CACHE_DIR`: diretório de cache (default: ~/.feedcli).
- `FEEDCLI_PER_FEED`: limite por feed (default: 10).

## Dev
```bash
ruff check . && ruff format .
mypy feedcli
pytest -q
```

## FZF (opcional)
```bash
feed list --refresh | sed -n '5,$p' | fzf | awk '{print $1}' | xargs -I{} feed read {}
```

## Licença
MIT
