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

    ramones = soup.find("article", id="ramones-2003")
    if ramones is None:
        raise AssertionError("Ramones transcription missing")
    folhateen_link = ramones.find(
        "a",
        href="/pt/comunicacao/folhateen-orfaos-do-rock/",
    )
    if folhateen_link is None or "Órfãos do Rock" not in folhateen_link.get_text(" ", strip=True):
        raise AssertionError("Ramones transcription must cross-link to the Folhateen standalone page")

    archive_intro = soup.select_one(".prateleira-archive-intro")
    if archive_intro is None:
        raise AssertionError("Prateleira archive intro missing")
    intro_text = archive_intro.get_text(" ", strip=True)
    if "serão normalizados" in intro_text:
        raise AssertionError("Prateleira archive note still uses future-tense normalization wording")
    if "foram normalizados" not in intro_text:
        raise AssertionError("Prateleira archive note must describe normalization as completed")

    archive_gallery = soup.select_one('[data-gallery="prateleira-cultural"]')
    if archive_gallery is None:
        raise AssertionError("Top Prateleira archive carousel missing")
    if len(archive_gallery.select("a.record-gallery__item")) != EXPECTED_SCANS:
        raise AssertionError("Top Prateleira archive carousel no longer contains 24 scans")


    # Chronology: author-confirmed publication month/year must match page order,
    # both navigation indexes, visible article dates and facsimile captions.
    chronology = mapping.get("chronology", [])
    if len(chronology) != EXPECTED_TRANSCRIPTIONS:
        raise AssertionError(f"Expected 22 publication dates, found {len(chronology)}")
    chronological_ids = [row["article_id"] for row in chronology]
    if len(set(chronological_ids)) != EXPECTED_TRANSCRIPTIONS or set(chronological_ids) != set(article_ids):
        raise AssertionError("Publication chronology and facsimile article ids disagree")
    if chronological_ids != [article["id"] for article in page_articles]:
        raise AssertionError("Transcriptions are not rendered in confirmed publication order")
    dates = [row["start"] for row in chronology]
    if dates != sorted(dates):
        raise AssertionError("Publication chronology must follow ascending month/year")
    for row in chronology:
        if len(row["start"]) != 7 or row["start"][4] != "-" or row["start"][5:] not in [f"{m:02d}" for m in range(1, 13)]:
            raise AssertionError(f"Invalid year/month for {row['article_id']}")
        if row.get("end") and row["end"] < row["start"]:
            raise AssertionError(f"Invalid issue range for {row['article_id']}")
        article = soup.find("article", id=row["article_id"])
        meta = article.select_one(".prateleira-column__meta")
        if meta is None or not meta.get_text(" ", strip=True).startswith(row["label"] + " ·"):
            raise AssertionError(f"{row['article_id']}: publication date in article differs from registry")
        caption = article.select_one(".prateleira-facsimile figcaption")
        if caption is None or row["label"] not in caption.get_text(" ", strip=True):
            raise AssertionError(f"{row['article_id']}: facsimile caption missing publication date")
    expected_years = ["2003", "2004", "2005", "2006"]
    rendered_years = [year.find("h2").get_text(" ", strip=True) for year in soup.select("section.prateleira-year")]
    if rendered_years != expected_years:
        raise AssertionError(f"Unexpected year sections: {rendered_years}")
    for selector in (".prateleira-mobile-toc", "aside.prateleira-toc"):
        nav = soup.select_one(selector)
        nav_ids = [a["href"].lstrip("#") for a in nav.select('a[href^="#"]') if a["href"] != "#arquivo-colunas"]
        if nav_ids != chronological_ids:
            raise AssertionError(f"{selector}: navigation not in confirmed chronological order")
        nav_years = [tag.get_text(" ", strip=True) for tag in nav.select(".prateleira-toc__year")]
        if nav_years != expected_years:
            raise AssertionError(f"{selector}: has obsolete inferred year groups")
    carousel_items = archive_gallery.select("a.record-gallery__item")
    by_date_id = {row["article_id"]: row for row in chronology}
    for scan, row in zip(carousel_items, mapping["items"]):
        expected = by_date_id.get(row["article_id"])
        visible = scan.get("data-caption", "")
        if expected and expected["caption_date"] not in visible:
            raise AssertionError(f"Gallery photo {row['photo']}: confirmed date absent from lightbox caption")
        if not expected and "sem data identificada" not in visible:
            raise AssertionError(f"Archive-only gallery photo {row['photo']}: must not assert a publication date")
    scripts = [json.loads(script.string) for script in soup.select('script[type="application/ld+json"]') if script.string]
    lists = [node["mainEntity"]["itemListElement"]
             for graph in scripts for node in (graph.get("@graph", [graph]))
             if isinstance(node, dict) and isinstance(node.get("mainEntity"), dict)
             and node["mainEntity"].get("@type") == "ItemList"]
    if len(lists) != 1:
        raise AssertionError("Expected exactly one Prateleira Article ItemList in structured data")
    schema_ids = [entry["item"]["url"].split("#")[-1] for entry in lists[0]]
    if schema_ids != chronological_ids:
        raise AssertionError("Article structured data not in confirmed chronological order")

    print(
        "Prateleira facsimile mapping OK: "
        "22 dated transcriptions in verified chronology, 23 paired scan pages, 1 archive-only page, 24-page carousel preserved."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
