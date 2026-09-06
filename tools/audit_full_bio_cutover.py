#!/usr/bin/env python3
"""Guard the future Full Biography indexation cutover.

Full Biography may remain indexable during the rollout. If either language is ever
changed to noindex, this audit requires the PT/EN pair to move atomically and
requires the Music and Internet top-level authority verticals to be indexable and
present in the sitemap first.
"""

from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
BASE = "https://marcelonicchio.github.io"

BIO = {
    "pt": "pt/biografia/index.html",
    "en": "en/biography/index.html",
}
PREREQUISITES = {
    "pt": ["pt/musica/index.html", "pt/internet/index.html"],
    "en": ["en/music/index.html", "en/internet/index.html"],
}


def robots(rel: str) -> str:
    path = ROOT / rel
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    meta = soup.find("meta", attrs={"name": "robots"})
    if meta is None or not meta.get("content"):
        raise AssertionError(f"{rel}: robots meta missing")
    return str(meta["content"])


def url_for(rel: str) -> str:
    if rel.endswith("index.html"):
        rel = rel[:-10]
    return BASE + "/" + rel.lstrip("/")


def is_indexable(value: str) -> bool:
    return value.startswith("index,follow")


def is_noindex(value: str) -> bool:
    return value.startswith("noindex,follow")


def main() -> int:
    bio_state = {lang: robots(rel) for lang, rel in BIO.items()}

    if is_noindex(bio_state["pt"]) != is_noindex(bio_state["en"]):
        raise AssertionError(
            "Full Biography cutover must be atomic: PT/EN robots states differ"
        )

    cutover_active = all(is_noindex(value) for value in bio_state.values())

    if not cutover_active:
        if not all(is_indexable(value) for value in bio_state.values()):
            raise AssertionError(
                "Full Biography must be either indexable in both languages or noindex in both"
            )
        staged: list[str] = []
        for lang, rels in PREREQUISITES.items():
            for rel in rels:
                if not is_indexable(robots(rel)):
                    staged.append(rel)
        print(
            "Full Biography cutover guard passed: biography remains indexable; "
            f"{len(staged)} prerequisite vertical(s) are still staged."
        )
        return 0

    errors: list[str] = []

    for lang, rels in PREREQUISITES.items():
        for rel in rels:
            state = robots(rel)
            if not is_indexable(state):
                errors.append(
                    f"{rel}: must be index,follow before Full Biography can become noindex"
                )
            if url_for(rel) not in SITEMAP:
                errors.append(
                    f"{rel}: must be in sitemap before Full Biography can become noindex"
                )

    for rel in BIO.values():
        if url_for(rel) in SITEMAP:
            errors.append(
                f"{rel}: noindex Full Biography must be removed from sitemap"
            )

    if errors:
        print("Full Biography cutover guard failed:")
        for error in errors:
            print(" -", error)
        return 1

    print(
        "Full Biography cutover guard passed: PT/EN biographies are noindex only after "
        "Music and Internet authority verticals became indexable."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
