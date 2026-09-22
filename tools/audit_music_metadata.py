#!/usr/bin/env python3
"""Guard Music vertical metadata around Marcelo Nicchio as the page entity."""

from __future__ import annotations

import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "pt/musica/index.html": {
        "title": "Música | Marcelo Nicchio",
        "description": "Vida musical de Marcelo Nicchio: formação, composição e bateria, com destaque para o Coitado do Próximo, álbuns, shows, TV e arquivo de 1989 a 2023.",
        "h1": "Música",
    },
    "en/music/index.html": {
        "title": "Music | Marcelo Nicchio",
        "description": "Marcelo Nicchio’s musical life: training, songwriting and drums, with Coitado do Próximo, albums, live shows, television and archive records from 1989 to 2023.",
        "h1": "Music",
    },
}


def meta_content(soup: BeautifulSoup, *, name: str | None = None, prop: str | None = None) -> str:
    attrs = {"name": name} if name else {"property": prop}
    tag = soup.find("meta", attrs=attrs)
    return str(tag.get("content", "")).strip() if tag else ""


def main() -> int:
    errors: list[str] = []

    for rel, expected in EXPECTED.items():
        soup = BeautifulSoup((ROOT / rel).read_text(encoding="utf-8"), "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        h1 = soup.h1.get_text(" ", strip=True) if soup.h1 else ""
        description = meta_content(soup, name="description")
        og_title = meta_content(soup, prop="og:title")
        og_description = meta_content(soup, prop="og:description")
        twitter_title = meta_content(soup, name="twitter:title")
        twitter_description = meta_content(soup, name="twitter:description")
        schema_tag = soup.find("script", attrs={"data-authority-vertical-schema": True})

        if title != expected["title"]:
            errors.append(f"{rel}: title mismatch: {title!r}")
        if h1 != expected["h1"]:
            errors.append(f"{rel}: H1 mismatch: {h1!r}")
        if description != expected["description"]:
            errors.append(f"{rel}: meta description mismatch")
        if og_title != expected["title"] or twitter_title != expected["title"]:
            errors.append(f"{rel}: social titles must match vertical title")
        if og_description != expected["description"] or twitter_description != expected["description"]:
            errors.append(f"{rel}: social descriptions must match canonical description")
        if "Coitado do Próximo (CDP)" in title:
            errors.append(f"{rel}: band name must not replace Music as page title")

        if schema_tag is None:
            errors.append(f"{rel}: authority schema missing")
            continue
        try:
            schema = json.loads(schema_tag.string or schema_tag.get_text())
        except Exception as exc:
            errors.append(f"{rel}: invalid authority schema: {exc}")
            continue
        if schema.get("name") != expected["title"]:
            errors.append(f"{rel}: CollectionPage name mismatch")
        if schema.get("description") != expected["description"]:
            errors.append(f"{rel}: CollectionPage description mismatch")

    if errors:
        print(f"Music metadata audit failed with {len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        return 1

    print("Music metadata OK: PT/EN vertical identity centered on Marcelo Nicchio; CDP remains a subject, not the page title.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
