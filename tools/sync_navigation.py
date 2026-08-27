#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalize_nav_block(block: str, lang: str) -> str:
    if lang == "pt":
        block = block.replace('href="/pt/internet/">Internet</a>', 'href="/pt/internet/">Internet &amp; Performance</a>')
        block = block.replace('href="/pt/internet/">Internet & Cultura Digital</a>', 'href="/pt/internet/">Internet &amp; Performance</a>')
        block = re.sub(r'<a href="/pt/search-performance/">[^<]*</a>', '', block)
    else:
        block = block.replace('href="/en/internet/">Internet</a>', 'href="/en/internet/">Internet &amp; Performance</a>')
        block = block.replace('href="/en/internet/">Internet & Digital Culture</a>', 'href="/en/internet/">Internet &amp; Performance</a>')
        block = re.sub(r'<a href="/en/search-performance/">[^<]*</a>', '', block)
    return block


def normalize_other_links(text: str, lang: str) -> str:
    if lang == "pt":
        pattern = r'<a([^>]*?)href="/pt/search-performance/"([^>]*)>([^<]*)</a>'
        target = '/pt/internet/'
    else:
        pattern = r'<a([^>]*?)href="/en/search-performance/"([^>]*)>([^<]*)</a>'
        target = '/en/internet/'

    def repl(match: re.Match[str]) -> str:
        before, after, label = match.groups()
        clean = label.strip()
        if clean in {"Search", "Search & Performance", "Search &amp; Performance"}:
            label = "Internet &amp; Performance"
        return f'<a{before}href="{target}"{after}>{label}</a>'

    return re.sub(pattern, repl, text)


def normalize(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    rel = path.relative_to(ROOT).as_posix()
    lang = "pt" if rel.startswith("pt/") else "en" if rel.startswith("en/") else ""
    if not lang:
        return False

    def nav_repl(match: re.Match[str]) -> str:
        return normalize_nav_block(match.group(0), lang)

    text = re.sub(r'<nav class="nav-links"[^>]*>.*?</nav>', nav_repl, text, flags=re.S)
    text = normalize_other_links(text, lang)

    if text == original:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    changed = []
    for path in sorted([*ROOT.glob("pt/**/*.html"), *ROOT.glob("en/**/*.html"), ROOT / "pt/index.html", ROOT / "en/index.html"]):
        if path.exists() and normalize(path):
            changed.append(path.relative_to(ROOT).as_posix())

    if args.check:
        if changed:
            print("Navigation is not synchronized:")
            for item in changed:
                print(" -", item)
            return 1
        print("Navigation synchronization check passed.")
        return 0

    if changed:
        print("Updated navigation in:")
        for item in changed:
            print(" -", item)
    else:
        print("Navigation already synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
