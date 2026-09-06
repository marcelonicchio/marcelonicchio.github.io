#!/usr/bin/env python3
"""Synchronize social + semantic metadata for the six thematic authority verticals.

These pages may remain staged behind noindex while editorial work is unfinished;
metadata readiness is independent from indexation policy. The script deliberately
leaves robots, visible copy and canonical/hreflang untouched.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PERSON_ID = "https://marcelonicchio.github.io/#marcelo-nicchio"
WEBSITE_ID = "https://marcelonicchio.github.io/#website"
START = "<!-- authority-meta:start -->"
END = "<!-- authority-meta:end -->"

TARGETS = (
    "pt/musica/index.html",
    "en/music/index.html",
    "pt/comunicacao/index.html",
    "en/communication/index.html",
    "pt/internet/index.html",
    "en/internet/index.html",
)


def extract(path: Path) -> tuple[str, str, str, str]:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    desc = soup.find("meta", attrs={"name": "description"})
    canonical = soup.find("link", rel="canonical")
    html_tag = soup.find("html")
    language = html_tag.get("lang", "") if html_tag else ""
    description = desc.get("content", "") if desc else ""
    url = canonical.get("href", "") if canonical else ""
    if not title or not description or not url or not language:
        raise RuntimeError(f"{path.relative_to(ROOT)}: missing title/description/canonical/lang")
    return title, description, url, language


def block_for(path: Path) -> str:
    title, description, url, language = extract(path)
    locale = "pt_BR" if language.lower() == "pt-br" else "en_US"
    alternate = "en_US" if locale == "pt_BR" else "pt_BR"
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": f"{url}#page",
        "url": url,
        "name": title,
        "description": description,
        "inLanguage": language,
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": PERSON_ID},
    }
    compact = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
    esc_title = title.replace("&", "&amp;").replace('"', "&quot;")
    esc_desc = description.replace("&", "&amp;").replace('"', "&quot;")
    return "\n".join(
        [
            START,
            '  <meta property="og:type" content="website">',
            f'  <meta property="og:title" content="{esc_title}">',
            f'  <meta property="og:description" content="{esc_desc}">',
            f'  <meta property="og:url" content="{url}">',
            '  <meta property="og:site_name" content="Marcelo Nicchio — Official Hub">',
            f'  <meta property="og:locale" content="{locale}">',
            f'  <meta property="og:locale:alternate" content="{alternate}">',
            '  <meta name="twitter:card" content="summary">',
            f'  <meta name="twitter:title" content="{esc_title}">',
            f'  <meta name="twitter:description" content="{esc_desc}">',
            f'  <script type="application/ld+json" data-authority-page-schema>{compact}</script>',
            END,
        ]
    )


def render(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    block = block_for(path)
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    if "</head>" not in text:
        raise RuntimeError(f"{path.relative_to(ROOT)}: </head> missing")
    return text.replace("</head>", block + "\n</head>", 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed: list[str] = []
    for rel in TARGETS:
        path = ROOT / rel
        expected = render(path)
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            changed.append(rel)
            if not args.check:
                path.write_text(expected, encoding="utf-8")
    if args.check and changed:
        print("Authority vertical metadata is stale:")
        for rel in changed:
            print(" -", rel)
        return 1
    if changed:
        print("Updated authority vertical metadata:")
        for rel in changed:
            print(" -", rel)
    else:
        print("Authority vertical metadata already synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
