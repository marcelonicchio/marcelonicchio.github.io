#!/usr/bin/env python3
"""Audit root embedded Person JSON-LD against data/person.json.

`data/person.json` is the canonical machine-readable Person record. The root page
also embeds that Person inside a WebSite/ProfilePage graph for discovery. This
check prevents the two public representations from drifting apart.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
ROOT_HTML = ROOT / "index.html"
PERSON_JSON = ROOT / "data" / "person.json"


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def normalized_identifier(value: Any) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for item in as_list(value):
        if not isinstance(item, dict):
            continue
        out.add((str(item.get("propertyID", "")), str(item.get("value", ""))))
    return out


def normalized_subjects(value: Any) -> set[str]:
    return {
        json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for item in as_list(value)
    }


def find_graph() -> list[dict[str, Any]]:
    soup = BeautifulSoup(ROOT_HTML.read_text(encoding="utf-8"), "html.parser")
    graphs: list[list[dict[str, Any]]] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"index.html: invalid JSON-LD: {exc}") from exc
        if isinstance(payload, dict) and isinstance(payload.get("@graph"), list):
            graphs.append(payload["@graph"])
    if not graphs:
        raise AssertionError("index.html: no JSON-LD @graph found")
    # Root currently has one canonical entity graph. If more graphs are added later,
    # merge them for lookup while still requiring unique entity IDs below.
    return [node for graph in graphs for node in graph if isinstance(node, dict)]


def exactly_one(graph: list[dict[str, Any]], *, entity_id: str | None = None, entity_type: str | None = None) -> dict[str, Any]:
    matches = []
    for node in graph:
        if entity_id is not None and node.get("@id") != entity_id:
            continue
        if entity_type is not None and node.get("@type") != entity_type:
            continue
        matches.append(node)
    label = entity_id or entity_type or "entity"
    if len(matches) != 1:
        raise AssertionError(f"index.html: expected exactly one {label}, found {len(matches)}")
    return matches[0]


def main() -> int:
    canonical = json.loads(PERSON_JSON.read_text(encoding="utf-8"))
    graph = find_graph()
    person_id = canonical["@id"]
    embedded = exactly_one(graph, entity_id=person_id, entity_type="Person")

    errors: list[str] = []

    scalar_fields = [
        "@id",
        "@type",
        "name",
        "url",
        "description",
        "image",
        "mainEntityOfPage",
    ]
    for field in scalar_fields:
        if embedded.get(field) != canonical.get(field):
            errors.append(
                f"Person {field} mismatch: data/person.json={canonical.get(field)!r}, "
                f"root JSON-LD={embedded.get(field)!r}"
            )

    for field in ["alternateName", "sameAs", "knowsAbout"]:
        if set(as_list(embedded.get(field))) != set(as_list(canonical.get(field))):
            errors.append(f"Person {field} set differs between data/person.json and root JSON-LD")

    if normalized_identifier(embedded.get("identifier")) != normalized_identifier(canonical.get("identifier")):
        errors.append("Person identifier set differs between data/person.json and root JSON-LD")

    if normalized_subjects(embedded.get("subjectOf")) != normalized_subjects(canonical.get("subjectOf")):
        errors.append("Person subjectOf set differs between data/person.json and root JSON-LD")

    website = exactly_one(graph, entity_id="https://marcelonicchio.github.io/#website", entity_type="WebSite")
    profile = exactly_one(graph, entity_id="https://marcelonicchio.github.io/#profile", entity_type="ProfilePage")

    if website.get("publisher") != {"@id": person_id}:
        errors.append("WebSite.publisher must point to the canonical Person @id")
    if profile.get("mainEntity") != {"@id": person_id}:
        errors.append("ProfilePage.mainEntity must point to the canonical Person @id")
    if embedded.get("mainEntityOfPage") != {"@id": profile.get("@id")}:
        errors.append("Person.mainEntityOfPage and ProfilePage @id are not reciprocal")
    if profile.get("isPartOf") != {"@id": website.get("@id")}:
        errors.append("ProfilePage.isPartOf must point to the canonical WebSite @id")

    if errors:
        print(f"Canonical Person schema audit failed with {len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        return 1

    print(
        "Canonical Person schema audit passed: root Person matches data/person.json; "
        "WebSite/ProfilePage references are coherent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
