#!/usr/bin/env python3
"""Track PT/EN editorial parity checkpoints for Full Biography source units.

The Full Biography is generated from thematic verticals. This tool does not
translate content. Instead it records, per registered biography unit, the exact
PT and EN source hashes that were jointly reviewed. Any later drift is blocked
until the pair is reviewed again and explicitly accepted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "full_biography.json"
REGISTRY = ROOT / "data" / "editorial_parity.json"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def load_registry() -> dict[str, Any]:
    if not REGISTRY.exists():
        raise RuntimeError("editorial parity registry is missing; run --bootstrap once")
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def source_node(entry: dict[str, Any], lang: str) -> Tag:
    spec = entry["source"][lang]
    path = ROOT / spec["path"]
    if not path.exists():
        raise RuntimeError(f"{entry['id']}:{lang}: missing source {spec['path']}")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    if spec["kind"] == "fragment":
        node = soup.find("section")
        if node is None:
            raise RuntimeError(f"{entry['id']}:{lang}: fragment has no section")
        return node
    matches = soup.select(spec["selector"])
    if len(matches) != 1:
        raise RuntimeError(
            f"{entry['id']}:{lang}: selector {spec['selector']!r} matched {len(matches)} nodes"
        )
    node = matches[0]
    if not isinstance(node, Tag):
        raise RuntimeError(f"{entry['id']}:{lang}: selector did not resolve to an element")
    return node


def normalized_html(node: Tag) -> str:
    # Hash semantic markup while ignoring formatting-only whitespace between tags.
    text = str(node)
    text = re.sub(r">\s+<", "><", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def digest(entry: dict[str, Any], lang: str) -> str:
    payload = normalized_html(source_node(entry, lang)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def all_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return manifest["entries"] + manifest["context_entries"]


def current_hashes(entry: dict[str, Any]) -> dict[str, str]:
    return {"pt": digest(entry, "pt"), "en": digest(entry, "en")}


def bootstrap(manifest: dict[str, Any]) -> int:
    if REGISTRY.exists():
        raise RuntimeError("editorial parity registry already exists; refusing to overwrite")
    today = date.today().isoformat()
    entries: dict[str, Any] = {}
    for entry in all_entries(manifest):
        hashes = current_hashes(entry)
        entries[entry["id"]] = {
            "revision": 1,
            "pt_hash": hashes["pt"],
            "en_hash": hashes["en"],
            "accepted_on": today,
        }
    payload = {
        "version": 1,
        "policy": "PT and EN hashes represent a jointly reviewed editorial checkpoint. Source drift requires explicit re-acceptance after both languages are reviewed.",
        "entries": entries,
    }
    REGISTRY.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Bootstrapped editorial parity registry: {len(entries)} entries")
    return 0


def check(manifest: dict[str, Any], registry: dict[str, Any]) -> int:
    expected_ids = {entry["id"] for entry in all_entries(manifest)}
    registered_ids = set(registry.get("entries", {}))
    errors: list[str] = []
    missing = sorted(expected_ids - registered_ids)
    stale = sorted(registered_ids - expected_ids)
    if missing:
        errors.append(f"entries missing from parity registry: {missing}")
    if stale:
        errors.append(f"stale parity registry entries: {stale}")

    by_id = {entry["id"]: entry for entry in all_entries(manifest)}
    for entry_id in sorted(expected_ids & registered_ids):
        entry = by_id[entry_id]
        state = registry["entries"][entry_id]
        current = current_hashes(entry)
        pt_changed = current["pt"] != state.get("pt_hash")
        en_changed = current["en"] != state.get("en_hash")
        if not pt_changed and not en_changed:
            continue
        revision = state.get("revision", "?")
        if pt_changed and not en_changed:
            errors.append(
                f"{entry_id}: PT changed after editorial revision {revision}; review EN and accept a new checkpoint"
            )
        elif en_changed and not pt_changed:
            errors.append(
                f"{entry_id}: EN changed after editorial revision {revision}; review PT and accept a new checkpoint"
            )
        else:
            errors.append(
                f"{entry_id}: PT and EN both changed after editorial revision {revision}; jointly review and accept a new checkpoint"
            )

    if errors:
        print("Editorial parity audit failed:")
        for error in errors:
            print(f" - {error}")
        print("After PT/EN review, run: python tools/editorial_parity.py --accept ENTRY_ID")
        return 1

    print(f"Editorial parity OK: {len(expected_ids)} PT/EN source units match accepted checkpoints.")
    return 0


def accept(manifest: dict[str, Any], registry: dict[str, Any], entry_id: str) -> int:
    by_id = {entry["id"]: entry for entry in all_entries(manifest)}
    if entry_id not in by_id:
        raise RuntimeError(f"unknown Full Biography entry: {entry_id}")
    if entry_id not in registry.get("entries", {}):
        raise RuntimeError(f"{entry_id}: not present in parity registry")
    state = registry["entries"][entry_id]
    current = current_hashes(by_id[entry_id])
    changed = [lang for lang in ("pt", "en") if current[lang] != state.get(f"{lang}_hash")]
    if not changed:
        print(f"{entry_id}: no source drift; checkpoint remains revision {state.get('revision')}")
        return 0
    state["revision"] = int(state.get("revision", 0)) + 1
    state["pt_hash"] = current["pt"]
    state["en_hash"] = current["en"]
    state["accepted_on"] = date.today().isoformat()
    state["changed_languages"] = changed
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Accepted {entry_id} editorial revision {state['revision']} after PT/EN review; "
        f"changed source language(s): {', '.join(changed)}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--bootstrap", action="store_true")
    mode.add_argument("--accept", metavar="ENTRY_ID")
    args = parser.parse_args()

    manifest = load_manifest()
    if args.bootstrap:
        return bootstrap(manifest)
    registry = load_registry()
    if args.check:
        return check(manifest, registry)
    return accept(manifest, registry, args.accept)


if __name__ == "__main__":
    raise SystemExit(main())
