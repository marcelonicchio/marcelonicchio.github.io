#!/usr/bin/env python3
"""Guard the explicit PT/EN indexing constitution for main authority surfaces.

Chapter Page pairs already have registry/generator audits. This check focuses on
hand-authored top-level language surfaces and encodes the site's current authority
model so future edits cannot silently change index/follow state, sitemap membership,
or reciprocal hreflang/canonical relationships.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://marcelonicchio.github.io"
X_DEFAULT = BASE + "/"

# Constitutional policy for the hand-authored PT/EN authority surfaces.
# Format: (PT path, EN path, index disposition, link-follow disposition)
PAIRS = [
    ("pt/index.html", "en/index.html", "index", "follow"),
    ("pt/biografia/index.html", "en/biography/index.html", "noindex", "follow"),
    ("pt/musica/index.html", "en/music/index.html", "index", "follow"),
    ("pt/comunicacao/index.html", "en/communication/index.html", "index", "follow"),
    ("pt/internet/index.html", "en/internet/index.html", "index", "follow"),
    ("pt/ia-hai/index.html", "en/ai-hai/index.html", "index", "follow"),
    ("pt/projetos/index.html", "en/projects/index.html", "noindex", "nofollow"),
    ("pt/publicacoes/index.html", "en/publications/index.html", "index", "follow"),
    ("pt/arquivo/index.html", "en/archive/index.html", "index", "follow"),
]


def page_url(rel: str) -> str:
    if rel.endswith("index.html"):
        rel = rel[:-10]
    return BASE + "/" + rel.lstrip("/")


def page_state(rel: str) -> dict[str, object]:
    soup = BeautifulSoup((ROOT / rel).read_text(encoding="utf-8"), "html.parser")
    robots = soup.find("meta", attrs={"name": "robots"})
    canonical = soup.find("link", attrs={"rel": "canonical"})
    alternates: dict[str, list[str]] = {}
    for link in soup.find_all("link", attrs={"rel": "alternate"}):
        lang = link.get("hreflang")
        href = link.get("href")
        if lang and href:
            alternates.setdefault(str(lang), []).append(str(href))
    return {
        "robots": str(robots.get("content", "")).lower() if robots else "",
        "canonical": str(canonical.get("href", "")) if canonical else "",
        "alternates": alternates,
    }


def disposition(robots: str) -> str:
    tokens = {token.strip() for token in robots.split(",") if token.strip()}
    if "noindex" in tokens:
        return "noindex"
    if "index" in tokens:
        return "index"
    return "unspecified"


def follow_disposition(robots: str) -> str:
    tokens = {token.strip() for token in robots.split(",") if token.strip()}
    if "nofollow" in tokens:
        return "nofollow"
    if "follow" in tokens:
        return "follow"
    return "unspecified"


def sitemap_urls() -> set[str]:
    tree = ET.parse(ROOT / "sitemap.xml")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return {
        node.text.strip()
        for node in tree.findall(".//s:loc", ns)
        if node.text and node.text.strip()
    }


def exact_alternate(
    rel: str,
    state: dict[str, object],
    lang: str,
    expected: str,
    errors: list[str],
) -> None:
    values = dict(state["alternates"]).get(lang, [])
    if values != [expected]:
        errors.append(
            f"{rel}: hreflang {lang!r} must be exactly {expected!r}; found {values!r}"
        )


def main() -> int:
    sitemap = sitemap_urls()
    errors: list[str] = []

    for pt_rel, en_rel, expected_indexing, expected_follow in PAIRS:
        pt_url = page_url(pt_rel)
        en_url = page_url(en_rel)
        pt = page_state(pt_rel)
        en = page_state(en_rel)

        pt_disposition = disposition(str(pt["robots"]))
        en_disposition = disposition(str(en["robots"]))
        pt_follow = follow_disposition(str(pt["robots"]))
        en_follow = follow_disposition(str(en["robots"]))

        if pt_disposition != expected_indexing:
            errors.append(
                f"{pt_rel}: indexing constitution requires {expected_indexing!r}; "
                f"found {pt_disposition!r}"
            )
        if en_disposition != expected_indexing:
            errors.append(
                f"{en_rel}: indexing constitution requires {expected_indexing!r}; "
                f"found {en_disposition!r}"
            )
        if pt_follow != expected_follow:
            errors.append(
                f"{pt_rel}: indexing constitution requires {expected_follow!r}; "
                f"found {pt_follow!r}"
            )
        if en_follow != expected_follow:
            errors.append(
                f"{en_rel}: indexing constitution requires {expected_follow!r}; "
                f"found {en_follow!r}"
            )

        pt_in_sitemap = pt_url in sitemap
        en_in_sitemap = en_url in sitemap
        if pt_in_sitemap != en_in_sitemap:
            errors.append(
                f"{pt_rel} / {en_rel}: sitemap membership must be atomic PT/EN"
            )

        if pt_disposition == "index" and not pt_in_sitemap:
            errors.append(f"{pt_rel}: indexable main surface must be present in sitemap")
        if en_disposition == "index" and not en_in_sitemap:
            errors.append(f"{en_rel}: indexable main surface must be present in sitemap")
        if pt_disposition == "noindex" and pt_in_sitemap:
            errors.append(f"{pt_rel}: noindex main surface must not be present in sitemap")
        if en_disposition == "noindex" and en_in_sitemap:
            errors.append(f"{en_rel}: noindex main surface must not be present in sitemap")

        if pt["canonical"] != pt_url:
            errors.append(
                f"{pt_rel}: canonical must be self {pt_url!r}; found {pt['canonical']!r}"
            )
        if en["canonical"] != en_url:
            errors.append(
                f"{en_rel}: canonical must be self {en_url!r}; found {en['canonical']!r}"
            )

        exact_alternate(pt_rel, pt, "pt-BR", pt_url, errors)
        exact_alternate(pt_rel, pt, "en", en_url, errors)
        exact_alternate(pt_rel, pt, "x-default", X_DEFAULT, errors)
        exact_alternate(en_rel, en, "pt-BR", pt_url, errors)
        exact_alternate(en_rel, en, "en", en_url, errors)
        exact_alternate(en_rel, en, "x-default", X_DEFAULT, errors)

    if errors:
        print(f"PT/EN main-surface authority audit failed with {len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        return 1

    print(
        f"PT/EN indexing constitution passed: {len(PAIRS)} pairs match their explicit "
        "index/follow policy, sitemap state, self-canonical URLs and reciprocal hreflang."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
