#!/usr/bin/env python3
"""Audit the experimental llms.txt authority/navigation map.

The file is not a search-engine standard and does not replace canonical HTML, but
once it is published as a machine navigation aid it should not drift from the
site's real authority graph. This audit checks only objective repository facts:
internal URLs must resolve locally and every indexable pilot Chapter Page must be
represented in llms.txt.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LLMS = ROOT / "llms.txt"
ENTRIES = ROOT / "data" / "entries.json"
HOST = "marcelonicchio.github.io"
BASE = f"https://{HOST}"

URL_RE = re.compile(r"https://marcelonicchio\.github\.io(?:/[^\s)>,;]*)?")


def local_path(url: str) -> Path:
    parsed = urlsplit(url)
    path = parsed.path or "/"
    if path == "/":
        return ROOT / "index.html"
    rel = path.lstrip("/")
    direct = ROOT / rel
    if direct.exists() and direct.is_file():
        return direct
    return ROOT / rel / "index.html"


def canonical_for(rel: str) -> str:
    if rel.endswith("index.html"):
        rel = rel[:-10]
    return BASE + "/" + rel.lstrip("/")


def main() -> int:
    text = LLMS.read_text(encoding="utf-8")
    errors: list[str] = []

    urls = sorted(set(URL_RE.findall(text)))
    if not urls:
        errors.append("llms.txt contains no internal HUB URLs")

    for url in urls:
        parsed = urlsplit(url)
        if parsed.netloc != HOST:
            continue
        path = local_path(url)
        if not path.exists():
            errors.append(f"llms.txt internal URL has no local target: {url}")

    required_core = {
        f"{BASE}/",
        f"{BASE}/data/person.json",
        f"{BASE}/data/timeline.json",
        f"{BASE}/data/publications.json",
        f"{BASE}/data/public-sources.json",
        f"{BASE}/pt/",
        f"{BASE}/en/",
        f"{BASE}/pt/publicacoes/",
        f"{BASE}/en/publications/",
    }
    for url in sorted(required_core):
        if url not in text:
            errors.append(f"llms.txt missing required core reference: {url}")

    registry = json.loads(ENTRIES.read_text(encoding="utf-8"))
    expected_chapters: set[str] = set()
    for entry in registry.get("entries", []):
        page = entry.get("chapter_page", {})
        if page.get("status") != "pilot" or page.get("indexing") != "index,follow":
            continue
        for lang in ("pt", "en"):
            rel = page.get(f"{lang}_path")
            if rel:
                expected_chapters.add(canonical_for(rel))

    for url in sorted(expected_chapters):
        if url not in text:
            errors.append(f"indexable Chapter Page missing from llms.txt authority map: {url}")

    mapped_internal = {url for url in urls if urlsplit(url).netloc == HOST}
    print(
        f"llms.txt audit: {len(mapped_internal)} internal HUB URL(s); "
        f"{len(expected_chapters)} indexable Chapter Page URL(s) required."
    )
    if errors:
        print(f"llms.txt authority-map audit failed with {len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        return 1

    print("llms.txt authority-map audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
