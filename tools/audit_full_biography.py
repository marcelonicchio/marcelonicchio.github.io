#!/usr/bin/env python3
"""Audit Full Biography coverage, source registration and rendered integrity."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "full_biography.json"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def selector_id(selector: str | None) -> str | None:
    if selector and re.fullmatch(r"#[A-Za-z][A-Za-z0-9_-]*", selector):
        return selector[1:]
    return None


def main() -> int:
    manifest: dict[str, Any] = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []

    all_entries = manifest["entries"] + manifest["context_entries"]
    ids = [entry["id"] for entry in all_entries]
    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    if duplicates:
        fail(errors, f"duplicate Full Biography entry ids: {duplicates}")

    era_ids = {era["id"] for era in manifest["eras"]}
    for entry in manifest["entries"]:
        if entry["era"] not in era_ids:
            fail(errors, f"{entry['id']}: unknown era {entry['era']!r}")
        if entry["domain"] not in manifest["domains"]:
            fail(errors, f"{entry['id']}: unknown domain {entry['domain']!r}")

    for lang in ("pt", "en"):
        covered_sections: dict[str, set[str]] = defaultdict(set)
        registered_phase_keys: dict[str, set[str]] = defaultdict(set)
        phase_parents: dict[str, set[str]] = defaultdict(set)
        source_paths: set[str] = set()

        for entry in all_entries:
            spec = entry["source"][lang]
            path = spec["path"]
            if spec["kind"] == "fragment":
                fragment = ROOT / path
                if not fragment.exists():
                    fail(errors, f"{entry['id']}:{lang}: missing fragment {path}")
                continue
            source_paths.add(path)
            source = ROOT / path
            if not source.exists():
                fail(errors, f"{entry['id']}:{lang}: missing source {path}")
                continue
            soup = BeautifulSoup(source.read_text(encoding="utf-8"), "html.parser")
            matches = soup.select(spec["selector"])
            if len(matches) != 1:
                fail(errors, f"{entry['id']}:{lang}: {spec['selector']!r} matched {len(matches)} nodes in {path}")
            if spec["kind"] == "section":
                sid = selector_id(spec["selector"])
                if sid:
                    covered_sections[path].add(sid)
            elif spec["kind"] == "phase":
                parent = selector_id(spec.get("parent_selector"))
                if not parent:
                    fail(errors, f"{entry['id']}:{lang}: phase has no simple parent selector")
                else:
                    phase_parents[path].add(parent)
                key_match = re.search(r"data-bio-key=['\"]([^'\"]+)['\"]", spec["selector"])
                if not key_match:
                    fail(errors, f"{entry['id']}:{lang}: phase selector must use data-bio-key")
                else:
                    registered_phase_keys[path].add(key_match.group(1))
            else:
                fail(errors, f"{entry['id']}:{lang}: unsupported kind {spec['kind']!r}")

        # Every public vertical chapter must be represented either directly or by registered phases.
        for path in sorted(source_paths):
            soup = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
            body = soup.select_one("article.article-body")
            if body is None:
                fail(errors, f"{lang}: {path} has no article.article-body")
                continue
            actual_ids: set[str] = set()
            for section in body.select("section.chapter"):
                sid = section.get("id")
                if not sid:
                    fail(errors, f"{lang}: chapter without id in {path}")
                    continue
                actual_ids.add(sid)
            covered = covered_sections[path] | phase_parents[path]
            missing = sorted(actual_ids - covered)
            stale = sorted(covered - actual_ids)
            if missing:
                fail(errors, f"{lang}: chapters not registered for Full Biography in {path}: {missing}")
            if stale:
                fail(errors, f"{lang}: manifest references missing chapters in {path}: {stale}")

            for parent_id in phase_parents[path]:
                parent = body.select_one(f"#{parent_id}")
                if parent is None:
                    continue
                phases = parent.select(".phase")
                actual_keys = {phase.get("data-bio-key") for phase in phases}
                if None in actual_keys:
                    fail(errors, f"{lang}: unregistered .phase without data-bio-key inside #{parent_id} in {path}")
                    actual_keys.discard(None)
                expected_keys = registered_phase_keys[path]
                missing_keys = sorted(actual_keys - expected_keys)
                stale_keys = sorted(expected_keys - actual_keys)
                if missing_keys:
                    fail(errors, f"{lang}: phase keys missing from manifest in {path}: {missing_keys}")
                if stale_keys:
                    fail(errors, f"{lang}: manifest phase keys missing from source in {path}: {stale_keys}")

        target_path = ROOT / manifest["targets"][lang]["path"]
        if not target_path.exists():
            fail(errors, f"{lang}: missing Full Biography target {target_path.relative_to(ROOT)}")
            continue
        target_text = target_path.read_text(encoding="utf-8")
        if "<!-- full-biography:start -->" not in target_text or "<!-- full-biography:end -->" not in target_text:
            fail(errors, f"{lang}: Full Biography managed markers are missing")
        target_soup = BeautifulSoup(target_text, "html.parser")
        rendered = [node.get("data-bio-entry") for node in target_soup.select("[data-bio-entry]")]
        rendered_counts = Counter(rendered)
        expected_ids = set(ids)
        rendered_ids = set(rendered)
        if rendered_ids != expected_ids:
            fail(errors, f"{lang}: rendered Full Biography ids differ; missing={sorted(expected_ids-rendered_ids)} extra={sorted(rendered_ids-expected_ids)}")
        repeated = sorted(key for key, count in rendered_counts.items() if count != 1)
        if repeated:
            fail(errors, f"{lang}: Full Biography entries must render exactly once: {repeated}")

        html_ids = [node.get("id") for node in target_soup.select("[id]")]
        dupe_html_ids = sorted(key for key, count in Counter(html_ids).items() if key and count > 1)
        if dupe_html_ids:
            fail(errors, f"{lang}: duplicate HTML ids in Full Biography: {dupe_html_ids}")

    if errors:
        print("Full Biography audit failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Full Biography audit OK: {len(manifest['entries'])} chronological entries + {len(manifest['context_entries'])} context entries, PT/EN coverage complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
