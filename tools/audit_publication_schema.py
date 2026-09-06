#!/usr/bin/env python3
"""Audit embedded publication JSON-LD against data/publications.json.

The canonical publication registry remains data/publications.json. This audit makes
sure the PT/EN public pages expose exactly the same five published works without
turning repository instances into separate publications or leaking WIP PRO v2 into
ScholarlyArticle markup.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "publications.json"
PAGE_PATHS = [
    ROOT / "pt" / "publicacoes" / "index.html",
    ROOT / "en" / "publications" / "index.html",
]


def canonical_works() -> dict[str, dict[str, Any]]:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    works: dict[str, dict[str, Any]] = {}
    for work in data["works"]:
        dois: set[str] = set()
        if work.get("doi"):
            dois.add(work["doi"])
        for instance in work.get("instances", []):
            if instance.get("doi"):
                dois.add(instance["doi"])
        works[work["title"]] = {
            "dois": dois,
            "version": work.get("version"),
        }
    return works


def embedded_articles(path: Path) -> dict[str, dict[str, Any]]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    script = soup.select_one('script[type="application/ld+json"][data-publications-schema]')
    if script is None:
        raise AssertionError(f"{path.relative_to(ROOT)}: missing data-publications-schema JSON-LD")
    payload = json.loads(script.string or script.get_text())
    graph = payload.get("@graph")
    if not isinstance(graph, list):
        raise AssertionError(f"{path.relative_to(ROOT)}: JSON-LD @graph missing")

    articles = [node for node in graph if node.get("@type") == "ScholarlyArticle"]
    if len(articles) != 5:
        raise AssertionError(
            f"{path.relative_to(ROOT)}: expected 5 ScholarlyArticle nodes, found {len(articles)}"
        )

    result: dict[str, dict[str, Any]] = {}
    for article in articles:
        name = article.get("name")
        if not name or name in result:
            raise AssertionError(f"{path.relative_to(ROOT)}: missing/duplicate ScholarlyArticle name")
        dois: set[str] = set()
        identifiers = article.get("identifier", [])
        if isinstance(identifiers, dict):
            identifiers = [identifiers]
        for identifier in identifiers:
            if identifier.get("propertyID") == "DOI" and identifier.get("value"):
                dois.add(identifier["value"])
        result[name] = {
            "id": article.get("@id"),
            "dois": dois,
            "version": article.get("version"),
        }
    return result


def main() -> int:
    expected = canonical_works()
    page_results: list[dict[str, dict[str, Any]]] = []

    for path in PAGE_PATHS:
        actual = embedded_articles(path)
        if set(actual) != set(expected):
            missing = sorted(set(expected) - set(actual))
            extra = sorted(set(actual) - set(expected))
            raise AssertionError(
                f"{path.relative_to(ROOT)}: publication title mismatch; missing={missing}, extra={extra}"
            )
        for title, exp in expected.items():
            got = actual[title]
            if got["dois"] != exp["dois"]:
                raise AssertionError(
                    f"{path.relative_to(ROOT)}: DOI mismatch for {title!r}: "
                    f"expected={sorted(exp['dois'])}, got={sorted(got['dois'])}"
                )
            if got["version"] != exp["version"]:
                raise AssertionError(
                    f"{path.relative_to(ROOT)}: version mismatch for {title!r}: "
                    f"expected={exp['version']!r}, got={got['version']!r}"
                )
            if not got["id"]:
                raise AssertionError(f"{path.relative_to(ROOT)}: missing @id for {title!r}")
        page_results.append(actual)

    pt, en = page_results
    for title in expected:
        if pt[title]["id"] != en[title]["id"]:
            raise AssertionError(f"PT/EN work @id mismatch for {title!r}")

    canonical_data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if any(work.get("version") == "v2" for work in canonical_data.get("works", [])):
        raise AssertionError("PRO v2 must remain outside published works until public")
    for result, path in zip(page_results, PAGE_PATHS):
        if any(node.get("version") == "v2" for node in result.values()):
            raise AssertionError(f"{path.relative_to(ROOT)}: WIP PRO v2 leaked into ScholarlyArticle schema")

    print("Publication schema audit passed: 5 works, PT/EN aligned, PRO v1 remains one work.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
