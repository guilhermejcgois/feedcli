from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "feedcli"
HOME = Path.home()
CACHE_DIR = Path(os.environ.get("FEEDCLI_CACHE_DIR", HOME / f".{APP_NAME}"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_PATH = CACHE_DIR / "cache.json"
DEFAULT_FEEDS_FILE = Path(os.environ.get("FEEDCLI_FEEDS", "feeds.txt"))
DEFAULT_PER_FEED = int(os.environ.get("FEEDCLI_PER_FEED", "10"))
