#!/usr/bin/env python3
"""Audit the incremental entry/Reader Page/Chapter Page architecture."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "entries.json"
TAGS = ROOT / "data" / "tags.json"
BASE_URL = "https://marcelonicchio.github.io/"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def soup_for(rel: str, cache: dict[str, BeautifulSoup]) -> BeautifulSoup:
    if rel not in cache:
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(rel)
        cache[rel] = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    return cache[rel]


def select_one(rel: str, selector: str, cache: dict[str, BeautifulSoup]) -> Tag:
    soup = soup_for(rel, cache)
    nodes = soup.select(selector)
    if len(nodes) != 1 or not isinstance(nodes[0], Tag):
        raise RuntimeError(f"{rel}: selector {selector!r} matched {len(nodes)} nodes")
    return nodes[0]


def canonical_for(path: str) -> str:
    directory = path[:-10] if path.endswith("index.html") else path
    return BASE_URL + directory.lstrip("/")


def unique_video_urls(node: Tag) -> set[str]:
    urls: set[str] = set()
    for tag in node.select("a[href], iframe[src]"):
        raw = tag.get("href") or tag.get("src") or ""
        if re.search(r"(?:youtube\.com|youtu\.be)", raw, flags=re.I):
            urls.add(raw)
    return urls


def main() -> int:
    registry = load(REGISTRY)
    taxonomy = load(TAGS)
    errors: list[str] = []
    warnings: list[str] = []
    cache: dict[str, BeautifulSoup] = {}

    tags = taxonomy.get("tags", [])
    tag_ids = [tag.get("id") for tag in tags]
    if len(tag_ids) != len(set(tag_ids)):
        errors.append("data/tags.json contains duplicate tag ids")
    known_tags = set(tag_ids)
    for tag in tags:
        for lang in ("pt", "en"):
            if not tag.get("label", {}).get(lang, "").strip():
                errors.append(f"tag {tag.get('id')}: missing {lang} label")

    entries = registry.get("entries", [])
    entry_ids = [entry.get("id") for entry in entries]
    if len(entry_ids) != len(set(entry_ids)):
        errors.append("data/entries.json contains duplicate entry ids")

    for entry in entries:
        entry_id = entry.get("id", "<missing-id>")
        kind = entry.get("kind")
        for lang in ("pt", "en"):
            if not entry.get("title", {}).get(lang, "").strip():
                errors.append(f"{entry_id}: missing {lang} title")
            if not entry.get("summary", {}).get(lang, "").strip():
                errors.append(f"{entry_id}: missing {lang} summary")

        for topic in entry.get("topic_ids", []):
            if topic not in known_tags:
                errors.append(f"{entry_id}: unknown topic id {topic!r}")

        if kind == "landmark-set":
            for lang in ("pt", "en"):
                landmarks = entry.get("landmarks", {}).get(lang, [])
                if not landmarks:
                    errors.append(f"{entry_id}:{lang}: landmark-set has no landmarks")
                for landmark in landmarks:
                    try:
                        node = select_one(landmark["path"], landmark["selector"], cache)
                    except (FileNotFoundError, RuntimeError) as exc:
                        errors.append(f"{entry_id}:{lang}: {exc}")
                        continue
                    expected = landmark.get("contains", "")
                    if expected and expected not in node.get_text(" ", strip=True):
                        errors.append(
                            f"{entry_id}:{lang}: {landmark['selector']} no longer contains {expected!r}"
                        )
        else:
            targets = entry.get("reader_targets", {})
            for lang in ("pt", "en"):
                lang_targets = targets.get(lang, [])
                if len(lang_targets) < 2:
                    errors.append(f"{entry_id}:{lang}: expected vertical + Full Biography reader targets")
                for target in lang_targets:
                    try:
                        select_one(target["path"], target["selector"], cache)
                    except (FileNotFoundError, RuntimeError) as exc:
                        errors.append(f"{entry_id}:{lang}: {exc}")

        source = entry.get("source", {})
        if source.get("kind") == "fragment":
            for lang in ("pt", "en"):
                src_rel = source.get(f"{lang}_path")
                src = ROOT / (src_rel or "")
                if not src_rel or not src.exists():
                    errors.append(f"{entry_id}:{lang}: missing fragment source {src_rel!r}")
                    continue
                verticals = [
                    t for t in entry.get("reader_targets", {}).get(lang, [])
                    if "/biografia/" not in f"/{t['path']}/" and "/biography/" not in f"/{t['path']}/"
                ]
                if len(verticals) != 1:
                    errors.append(f"{entry_id}:{lang}: expected exactly one thematic vertical target")
                    continue
                vertical_path = ROOT / verticals[0]["path"]
                if not vertical_path.exists():
                    errors.append(f"{entry_id}:{lang}: missing thematic vertical {verticals[0]['path']}")
                    continue
                text = vertical_path.read_text(encoding="utf-8")
                start = f"<!-- entry-source:{entry_id}:start -->"
                end = f"<!-- entry-source:{entry_id}:end -->"
                pattern = re.compile(re.escape(start) + r"\s*(.*?)\s*" + re.escape(end), re.S)
                match = pattern.search(text)
                if match is None:
                    errors.append(f"{entry_id}:{lang}: thematic vertical is not managed by entry-source markers")
                elif match.group(1).strip() != src.read_text(encoding="utf-8").strip():
                    errors.append(f"{entry_id}:{lang}: thematic vertical body differs from neutral fragment")

        # Machine-derived media checks: registry stores associations/known counts, not duplicate DOM counts.
        if kind != "landmark-set":
            for lang in ("pt", "en"):
                vertical = next(
                    (t for t in entry.get("reader_targets", {}).get(lang, [])
                     if "/biografia/" not in f"/{t['path']}/" and "/biography/" not in f"/{t['path']}/"),
                    None,
                )
                if not vertical:
                    continue
                try:
                    node = select_one(vertical["path"], vertical["selector"], cache)
                except (FileNotFoundError, RuntimeError):
                    continue
                for gallery in entry.get("media", {}).get("galleries", []):
                    if node.select_one(f'[data-gallery="{gallery}"]') is None:
                        errors.append(f"{entry_id}:{lang}: registered gallery {gallery!r} missing from vertical")
                expected_videos = entry.get("media", {}).get("known_video_count")
                if expected_videos is not None:
                    actual = len(unique_video_urls(node))
                    if actual != expected_videos:
                        errors.append(
                            f"{entry_id}:{lang}: expected {expected_videos} YouTube URLs, found {actual}"
                        )

        page = entry.get("chapter_page", {})
        status = page.get("status")
        if status == "pilot":
            for lang in ("pt", "en"):
                rel = page.get(f"{lang}_path")
                if not rel:
                    errors.append(f"{entry_id}:{lang}: pilot Chapter Page path missing")
                    continue
                path = ROOT / rel
                if not path.exists():
                    errors.append(f"{entry_id}:{lang}: pilot Chapter Page not generated: {rel}")
                    continue
                soup = soup_for(rel, cache)
                robots = soup.find("meta", attrs={"name": "robots"})
                expected_robots = page.get("indexing", "noindex,follow")
                if robots is None or robots.get("content") != expected_robots:
                    errors.append(f"{entry_id}:{lang}: Chapter Page robots must be {expected_robots!r}")
                canonical = soup.find("link", rel="canonical")
                expected_canonical = canonical_for(rel)
                if canonical is None or canonical.get("href") != expected_canonical:
                    errors.append(f"{entry_id}:{lang}: bad self-canonical")
                if soup.select_one(".entry-breadcrumbs") is None:
                    errors.append(f"{entry_id}:{lang}: visible breadcrumbs missing")
                main = soup.select_one(f'main[data-entry-id="{entry_id}"]')
                if main is None:
                    errors.append(f"{entry_id}:{lang}: stable data-entry-id missing")

                other_lang = "en" if lang == "pt" else "pt"
                other_rel = page.get(f"{other_lang}_path")
                expected_alt = canonical_for(other_rel) if other_rel else None
                hreflang = soup.find("link", rel="alternate", hreflang=("en" if other_lang == "en" else "pt-BR"))
                if expected_alt and (hreflang is None or hreflang.get("href") != expected_alt):
                    errors.append(f"{entry_id}:{lang}: reciprocal hreflang missing or incorrect")
        elif status not in {"candidate", "none"}:
            errors.append(f"{entry_id}: unsupported Chapter Page status {status!r}")

    print(f"Entry architecture audit: {len(entries)} registered case(s), {len(tags)} controlled tag(s).")
    for warning in warnings:
        print("WARN:", warning)
    if errors:
        print(f"Entry architecture audit failed with {len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        return 1
    print("Entry architecture audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
