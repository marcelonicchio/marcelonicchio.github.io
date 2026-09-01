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
SITEMAP = ROOT / "sitemap.xml"
BASE_URL = "https://marcelonicchio.github.io/"
ALLOWED_SOURCE_KINDS = {"reader-section", "fragment", "composite-reader-landmarks"}
ALLOWED_PAGE_STATUS = {"pilot", "candidate", "none"}
ALLOWED_INDEXING = {"index,follow", "noindex,follow", "none"}
ALLOWED_READER_PRESENTATION = {"normal", "default-open", "featured"}
MAX_READER_PREVIEW_CHARS = 1650


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


def public_path_for(path: str) -> str:
    directory = path[:-10] if path.endswith("index.html") else path
    return "/" + directory.lstrip("/")


def unique_video_urls(node: Tag) -> set[str]:
    urls: set[str] = set()
    for tag in node.select("a[href], iframe[src]"):
        raw = tag.get("href") or tag.get("src") or ""
        if re.search(r"(?:youtube\.com|youtu\.be)", raw, flags=re.I):
            urls.add(raw)
    return urls


def has_jsonld_type(soup: BeautifulSoup, schema_type: str) -> bool:
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue
        nodes: list[Any]
        if isinstance(data, dict) and isinstance(data.get("@graph"), list):
            nodes = data["@graph"]
        else:
            nodes = [data]
        for node in nodes:
            if isinstance(node, dict) and node.get("@type") == schema_type:
                return True
    return False


def main() -> int:
    registry = load(REGISTRY)
    taxonomy = load(TAGS)
    errors: list[str] = []
    warnings: list[str] = []
    cache: dict[str, BeautifulSoup] = {}
    sitemap_text = SITEMAP.read_text(encoding="utf-8") if SITEMAP.exists() else ""

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

    registered_page_paths: list[str] = []
    for entry in entries:
        page = entry.get("chapter_page", {})
        for lang in ("pt", "en"):
            rel = page.get(f"{lang}_path")
            if rel:
                registered_page_paths.append(rel)
    if len(registered_page_paths) != len(set(registered_page_paths)):
        errors.append("data/entries.json contains duplicate Chapter Page paths")

    for entry in entries:
        entry_id = entry.get("id", "<missing-id>")
        kind = entry.get("kind")
        source = entry.get("source", {})
        source_kind = source.get("kind")
        if source_kind not in ALLOWED_SOURCE_KINDS:
            errors.append(f"{entry_id}: unsupported source kind {source_kind!r}")

        presentation_state = entry.get("reader_presentation", {}).get("state", "normal")
        if presentation_state not in ALLOWED_READER_PRESENTATION:
            errors.append(f"{entry_id}: unsupported Reader presentation state {presentation_state!r}")

        for lang in ("pt", "en"):
            if not entry.get("title", {}).get(lang, "").strip():
                errors.append(f"{entry_id}: missing {lang} title")
            if not entry.get("summary", {}).get(lang, "").strip():
                errors.append(f"{entry_id}: missing {lang} summary")

        # Rich collapsed previews are concise autonomous versions of dense entries.
        # Melissa 1.0 established the accepted upper-density reference; keep future
        # preview paragraph copy within that mobile-tested ceiling.
        reader_preview = entry.get("reader_preview", {})
        if reader_preview is not None and not isinstance(reader_preview, dict):
            errors.append(f"{entry_id}: reader_preview must be an object when present")
        elif isinstance(reader_preview, dict):
            for lang in ("pt", "en"):
                preview = reader_preview.get(lang)
                if preview is None:
                    continue
                if not isinstance(preview, dict):
                    errors.append(f"{entry_id}:{lang}: reader_preview must be an object")
                    continue
                paragraphs = preview.get("paragraphs", [])
                if not isinstance(paragraphs, list) or not paragraphs:
                    errors.append(f"{entry_id}:{lang}: reader_preview requires at least one paragraph")
                    continue
                visible_copy = 0
                for idx, paragraph in enumerate(paragraphs, start=1):
                    if not isinstance(paragraph, dict) or not isinstance(paragraph.get("text"), str):
                        errors.append(f"{entry_id}:{lang}: reader_preview paragraph {idx} requires text")
                        continue
                    visible_copy += len(paragraph["text"])
                if visible_copy > MAX_READER_PREVIEW_CHARS:
                    errors.append(
                        f"{entry_id}:{lang}: reader_preview copy has {visible_copy} characters; "
                        f"maximum is {MAX_READER_PREVIEW_CHARS}"
                    )

        topics = entry.get("topic_ids", [])
        if len(topics) != len(set(topics)):
            errors.append(f"{entry_id}: duplicate topic ids")
        for topic in topics:
            if topic not in known_tags:
                errors.append(f"{entry_id}: unknown topic id {topic!r}")

        if kind == "landmark-set":
            if source_kind != "composite-reader-landmarks":
                errors.append(f"{entry_id}: landmark-set must use composite-reader-landmarks source kind")
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

        if source_kind == "fragment":
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
        indexing = page.get("indexing")
        if status not in ALLOWED_PAGE_STATUS:
            errors.append(f"{entry_id}: unsupported Chapter Page status {status!r}")
            continue
        if indexing not in ALLOWED_INDEXING:
            errors.append(f"{entry_id}: unsupported Chapter Page indexing policy {indexing!r}")

        if status == "none":
            if indexing != "none":
                errors.append(f"{entry_id}: Chapter Page status none requires indexing=none")
            continue

        if status == "candidate":
            if indexing == "index,follow":
                errors.append(f"{entry_id}: candidate Chapter Page cannot be index,follow before promotion")
            for lang in ("pt", "en"):
                rel = page.get(f"{lang}_path")
                if rel and (ROOT / rel).exists():
                    errors.append(f"{entry_id}:{lang}: candidate Chapter Page exists on disk before promotion: {rel}")
            continue

        # status == pilot
        if source_kind != "fragment":
            errors.append(f"{entry_id}: pilot Chapter Page requires fragment source")
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
            expected_robots = indexing or "noindex,follow"
            if robots is None or robots.get("content") != expected_robots:
                errors.append(f"{entry_id}:{lang}: Chapter Page robots must be {expected_robots!r}")

            expected_canonical = canonical_for(rel)
            canonical = soup.find("link", rel="canonical")
            if canonical is None or canonical.get("href") != expected_canonical:
                errors.append(f"{entry_id}:{lang}: bad self-canonical")
            self_hreflang = "pt-BR" if lang == "pt" else "en"
            self_alt = soup.find("link", rel="alternate", hreflang=self_hreflang)
            if self_alt is None or self_alt.get("href") != expected_canonical:
                errors.append(f"{entry_id}:{lang}: self hreflang missing or incorrect")
            if soup.select_one(".entry-breadcrumbs") is None:
                errors.append(f"{entry_id}:{lang}: visible breadcrumbs missing")
            if not has_jsonld_type(soup, "BreadcrumbList"):
                errors.append(f"{entry_id}:{lang}: BreadcrumbList JSON-LD missing")
            main = soup.select_one(f'main[data-entry-id="{entry_id}"]')
            if main is None:
                errors.append(f"{entry_id}:{lang}: stable data-entry-id missing")

            other_lang = "en" if lang == "pt" else "pt"
            other_rel = page.get(f"{other_lang}_path")
            expected_alt = canonical_for(other_rel) if other_rel else None
            hreflang = soup.find("link", rel="alternate", hreflang=("en" if other_lang == "en" else "pt-BR"))
            if expected_alt and (hreflang is None or hreflang.get("href") != expected_alt):
                errors.append(f"{entry_id}:{lang}: reciprocal hreflang missing or incorrect")

            x_default = soup.find("link", rel="alternate", hreflang="x-default")
            expected_default = canonical_for(page["pt_path"])
            if x_default is None or x_default.get("href") != expected_default:
                errors.append(f"{entry_id}:{lang}: x-default must point to PT Chapter Page")

            in_sitemap = expected_canonical in sitemap_text
            if expected_robots.startswith("noindex") and in_sitemap:
                errors.append(f"{entry_id}:{lang}: noindex pilot Chapter Page must not be listed in sitemap")

            # Once a Chapter Page becomes indexable, search/crawlers must have normal static links to it.
            if expected_robots == "index,follow":
                expected_href = public_path_for(rel)
                for target in entry.get("reader_targets", {}).get(lang, []):
                    try:
                        node = select_one(target["path"], target["selector"], cache)
                    except (FileNotFoundError, RuntimeError):
                        continue
                    if node.select_one(f'a[href="{expected_href}"]') is None:
                        errors.append(
                            f"{entry_id}:{lang}: indexable Chapter Page lacks static link from {target['path']} {target['selector']}"
                        )

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
