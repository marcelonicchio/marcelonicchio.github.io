#!/usr/bin/env python3
"""Audit Prateleira Cultural transcription ↔ facsimile mapping and rendering."""

from pathlib import Path
import json
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data" / "prateleira-cultural-facsimiles.json"
GALLERIES_PATH = ROOT / "data" / "galleries.json"
PAGE_PATH = ROOT / "pt" / "comunicacao" / "prateleira-cultural-revista-sinal-verde" / "index.html"

EXPECTED_TRANSCRIPTIONS = 22
EXPECTED_SCANS = 24
EXPECTED_ARCHIVE_ONLY = 1


def main() -> int:
    mapping = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    galleries = json.loads(GALLERIES_PATH.read_text(encoding="utf-8"))
    soup = BeautifulSoup(PAGE_PATH.read_text(encoding="utf-8"), "html.parser")

    gallery = next((g for g in galleries["galleries"] if g["id"] == mapping["gallery_id"]), None)
    if gallery is None:
        raise AssertionError("Prateleira gallery registry entry missing")

    gallery_by_id = {item["id"]: item for item in gallery["items"]}
    if len(gallery_by_id) != EXPECTED_SCANS:
        raise AssertionError(f"Expected {EXPECTED_SCANS} registered scans, found {len(gallery_by_id)}")

    map_items = mapping["items"]
    if len(map_items) != EXPECTED_SCANS:
        raise AssertionError(f"Expected {EXPECTED_SCANS} mapping rows, found {len(map_items)}")

    mapped_gallery_ids = [item["gallery_item"] for item in map_items]
    if len(mapped_gallery_ids) != len(set(mapped_gallery_ids)):
        raise AssertionError("Duplicate gallery item in Prateleira facsimile map")
    if set(mapped_gallery_ids) != set(gallery_by_id):
        raise AssertionError("Prateleira facsimile map does not cover the exact 24-item gallery registry")

    archive_only = [item for item in map_items if not item.get("article_id")]
    if len(archive_only) != EXPECTED_ARCHIVE_ONLY:
        raise AssertionError(
            f"Expected {EXPECTED_ARCHIVE_ONLY} archive-only scan, found {len(archive_only)}"
        )

    article_rows = [item for item in map_items if item.get("article_id")]
    article_ids = sorted(set(item["article_id"] for item in article_rows))
    if len(article_ids) != EXPECTED_TRANSCRIPTIONS:
        raise AssertionError(
            f"Expected {EXPECTED_TRANSCRIPTIONS} mapped transcriptions, found {len(article_ids)}"
        )

    page_articles = soup.select("article.prateleira-column[id]")
    page_article_ids = sorted(article["id"] for article in page_articles)
    if page_article_ids != article_ids:
        raise AssertionError(
            "Mapped transcription ids differ from rendered Prateleira article ids"
        )

    grouped: dict[str, list[dict]] = {}
    for row in article_rows:
        grouped.setdefault(row["article_id"], []).append(row)

    multi = {article_id: rows for article_id, rows in grouped.items() if len(rows) > 1}
    if list(multi) != ["planeta-google-2005"] or len(multi["planeta-google-2005"]) != 2:
        raise AssertionError("Only O Planeta Google should map to two scanned pages")

    for article_id, rows in grouped.items():
        article = soup.find("article", id=article_id)
        if article is None:
            raise AssertionError(f"Missing article #{article_id}")

        figure = next(
            (
                child for child in article.children
                if getattr(child, "name", None) == "figure"
                and "prateleira-facsimile" in (child.get("class") or [])
            ),
            None,
        )
        if figure is None:
            raise AssertionError(f"#{article_id}: facsimile figure missing")

        anchors = figure.select("a.prateleira-facsimile__item")
        if len(anchors) != len(rows):
            raise AssertionError(
                f"#{article_id}: expected {len(rows)} facsimile link(s), found {len(anchors)}"
            )

        expected = []
        for row in rows:
            item = gallery_by_id[row["gallery_item"]]
            expected_href = "/" + gallery["sourceRoot"].strip("/") + "/" + item["source"]
            expected_thumb = "/" + item["derivatives"]["480"]["path"].lstrip("/")
            expected.append((expected_href, expected_thumb))

        found = []
        for anchor in anchors:
            image = anchor.find("img")
            if image is None:
                raise AssertionError(f"#{article_id}: facsimile image missing")
            if image.get("loading") != "lazy":
                raise AssertionError(f"#{article_id}: facsimile must remain lazy-loaded")
            if not image.get("width") or not image.get("height"):
                raise AssertionError(f"#{article_id}: facsimile intrinsic dimensions missing")
            found.append((anchor.get("href"), image.get("src")))

        if found != expected:
            raise AssertionError(
                f"#{article_id}: rendered facsimile mapping differs from registry; "
                f"expected={expected!r}, found={found!r}"
            )

    archive_gallery = soup.select_one('[data-gallery="prateleira-cultural"]')
    if archive_gallery is None:
        raise AssertionError("Top Prateleira archive carousel missing")
    if len(archive_gallery.select("a.record-gallery__item")) != EXPECTED_SCANS:
        raise AssertionError("Top Prateleira archive carousel no longer contains 24 scans")

    print(
        "Prateleira facsimile mapping OK: "
        "22 transcriptions, 23 paired scan pages, 1 archive-only page, 24-page carousel preserved."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
