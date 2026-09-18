#!/usr/bin/env python3
"""Guard CollectionPage semantics on the current priority authority verticals."""

from __future__ import annotations

import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PERSON_ID = "https://marcelonicchio.github.io/#marcelo-nicchio"
WEBSITE_ID = "https://marcelonicchio.github.io/#website"

TARGETS = (
    "pt/ia-hai/index.html",
    "en/ai-hai/index.html",
    "pt/musica/index.html",
    "en/music/index.html",
    "pt/internet/index.html",
    "en/internet/index.html",
)


def main() -> int:
    errors: list[str] = []
    for rel in TARGETS:
        soup = BeautifulSoup((ROOT / rel).read_text(encoding="utf-8"), "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        desc = soup.find("meta", attrs={"name": "description"})
        canonical = soup.find("link", rel="canonical")
        html_tag = soup.find("html")
        script = soup.find("script", attrs={"data-authority-vertical-schema": True})
        if not all((title, desc, canonical, html_tag, script)):
            errors.append(f"{rel}: missing title/description/canonical/lang/authority schema")
            continue
        url = str(canonical.get("href", ""))
        language = str(html_tag.get("lang", ""))
        description = str(desc.get("content", ""))
        try:
            data = json.loads(script.string or script.get_text())
        except Exception as exc:
            errors.append(f"{rel}: invalid authority schema JSON: {exc}")
            continue
        expected = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "@id": url + "#page",
            "url": url,
            "name": title,
            "description": description,
            "inLanguage": language,
            "isPartOf": {"@id": WEBSITE_ID},
            "about": {"@id": PERSON_ID},
            "mainEntity": {"@id": PERSON_ID},
        }
        if data != expected:
            errors.append(f"{rel}: CollectionPage schema does not match canonical page metadata")

    if errors:
        print(f"Priority vertical schema audit failed with {len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        return 1

    print(f"Priority vertical schema audit passed: {len(TARGETS)} pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
