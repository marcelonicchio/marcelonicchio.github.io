#!/usr/bin/env python3
"""Audit canonical Person JSON-LD across root and language hubs.

`data/person.json` is the canonical machine-readable Person record. The root page
embeds that Person inside a WebSite/ProfilePage graph, while PT/EN language hubs
embed a localized ProfilePage with the same Person @id. This check prevents the
identity core from drifting across those public representations while allowing
language-specific subject emphasis such as localized `knowsAbout` values.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
ROOT_HTML = ROOT / "index.html"
PERSON_JSON = ROOT / "data" / "person.json"
LANGUAGE_HUBS = {
    "pt/index.html": {
        "profile_id": "https://marcelonicchio.github.io/pt/#profile",
        "language": "pt-BR",
    },
    "en/index.html": {
        "profile_id": "https://marcelonicchio.github.io/en/#profile",
        "language": "en",
    },
}
WEBSITE_ID = "https://marcelonicchio.github.io/#website"


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


def jsonld_payloads(path: Path) -> list[Any]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    payloads: list[Any] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        try:
            payloads.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path.relative_to(ROOT)}: invalid JSON-LD: {exc}") from exc
    return payloads


def root_graph() -> list[dict[str, Any]]:
    graphs: list[list[dict[str, Any]]] = []
    for payload in jsonld_payloads(ROOT_HTML):
        if isinstance(payload, dict) and isinstance(payload.get("@graph"), list):
            graphs.append(payload["@graph"])
    if not graphs:
        raise AssertionError("index.html: no JSON-LD @graph found")
    return [node for graph in graphs for node in graph if isinstance(node, dict)]


def exactly_one(
    graph: list[dict[str, Any]],
    *,
    entity_id: str | None = None,
    entity_type: str | None = None,
    source: str = "index.html",
) -> dict[str, Any]:
    matches = []
    for node in graph:
        if entity_id is not None and node.get("@id") != entity_id:
            continue
        if entity_type is not None and node.get("@type") != entity_type:
            continue
        matches.append(node)
    label = entity_id or entity_type or "entity"
    if len(matches) != 1:
        raise AssertionError(f"{source}: expected exactly one {label}, found {len(matches)}")
    return matches[0]


def compare_identity_core(
    embedded: dict[str, Any],
    canonical: dict[str, Any],
    source: str,
    errors: list[str],
) -> None:
    for field in ["@id", "@type", "name", "url", "image"]:
        if embedded.get(field) != canonical.get(field):
            errors.append(
                f"{source}: Person {field} mismatch: canonical={canonical.get(field)!r}, "
                f"embedded={embedded.get(field)!r}"
            )

    for field in ["alternateName", "sameAs"]:
        if set(as_list(embedded.get(field))) != set(as_list(canonical.get(field))):
            errors.append(f"{source}: Person {field} set differs from data/person.json")

    if normalized_identifier(embedded.get("identifier")) != normalized_identifier(canonical.get("identifier")):
        errors.append(f"{source}: Person identifier set differs from data/person.json")


def audit_language_hubs(
    canonical: dict[str, Any],
    person_id: str,
    errors: list[str],
) -> None:
    for rel, expected in LANGUAGE_HUBS.items():
        path = ROOT / rel
        payloads = jsonld_payloads(path)
        profiles = [
            payload
            for payload in payloads
            if isinstance(payload, dict) and payload.get("@type") == "ProfilePage"
        ]
        if len(profiles) != 1:
            errors.append(f"{rel}: expected exactly one top-level ProfilePage JSON-LD object")
            continue

        profile = profiles[0]
        if profile.get("@id") != expected["profile_id"]:
            errors.append(f"{rel}: ProfilePage @id differs from expected language-hub profile id")
        if profile.get("inLanguage") != expected["language"]:
            errors.append(f"{rel}: ProfilePage inLanguage differs from expected {expected['language']!r}")
        if profile.get("isPartOf") != {"@id": WEBSITE_ID}:
            errors.append(f"{rel}: ProfilePage.isPartOf must point to the canonical WebSite")

        person = profile.get("mainEntity")
        if not isinstance(person, dict):
            errors.append(f"{rel}: ProfilePage.mainEntity must embed/reference the canonical Person")
            continue
        if person.get("@id") != person_id:
            errors.append(f"{rel}: ProfilePage.mainEntity uses a different Person @id")
            continue

        compare_identity_core(person, canonical, rel, errors)


def main() -> int:
    canonical = json.loads(PERSON_JSON.read_text(encoding="utf-8"))
    graph = root_graph()
    person_id = canonical["@id"]
    embedded = exactly_one(graph, entity_id=person_id, entity_type="Person")

    errors: list[str] = []

    compare_identity_core(embedded, canonical, "index.html", errors)

    for field in ["description", "mainEntityOfPage"]:
        if embedded.get(field) != canonical.get(field):
            errors.append(
                f"index.html: Person {field} mismatch: data/person.json={canonical.get(field)!r}, "
                f"root JSON-LD={embedded.get(field)!r}"
            )

    if set(as_list(embedded.get("knowsAbout"))) != set(as_list(canonical.get("knowsAbout"))):
        errors.append("index.html: Person knowsAbout set differs from data/person.json")

    if normalized_subjects(embedded.get("subjectOf")) != normalized_subjects(canonical.get("subjectOf")):
        errors.append("index.html: Person subjectOf set differs from data/person.json")

    website = exactly_one(graph, entity_id=WEBSITE_ID, entity_type="WebSite")
    profile = exactly_one(
        graph,
        entity_id="https://marcelonicchio.github.io/#profile",
        entity_type="ProfilePage",
    )

    if website.get("publisher") != {"@id": person_id}:
        errors.append("index.html: WebSite.publisher must point to the canonical Person @id")
    if profile.get("mainEntity") != {"@id": person_id}:
        errors.append("index.html: ProfilePage.mainEntity must point to the canonical Person @id")
    if embedded.get("mainEntityOfPage") != {"@id": profile.get("@id")}:
        errors.append("index.html: Person.mainEntityOfPage and ProfilePage @id are not reciprocal")
    if profile.get("isPartOf") != {"@id": website.get("@id")}:
        errors.append("index.html: ProfilePage.isPartOf must point to the canonical WebSite @id")

    audit_language_hubs(canonical, person_id, errors)

    if errors:
        print(f"Canonical Person schema audit failed with {len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        return 1

    print(
        "Canonical Person schema audit passed: root matches data/person.json; "
        "PT/EN hubs preserve the same identity core; WebSite/ProfilePage references are coherent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
