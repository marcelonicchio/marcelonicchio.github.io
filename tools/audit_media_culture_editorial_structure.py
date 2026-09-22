#!/usr/bin/env python3
"""Audit the complete Music-style editorial hierarchy on Media & Culture."""

from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "pt": ROOT / "pt/comunicacao/index.html",
    "en": ROOT / "en/communication/index.html",
}
EXPECTED_IDS = {
    "pt": ["bbs","radio","homens","cinema","folha","sinal-verde","meia-noite","arquiteto","autopsia"],
    "en": ["bbs","radio","homens","film","folha","sinal-verde","meia-noite","architect","autopsia"],
}
CONTEXT = {
    "pt": {
        "themes":"temas",
        "names":"nomes",
        "theme_labels":["MÚSICA","CINEMA/TV","DIGITAL","REPORTAGEM"],
    },
    "en": {
        "themes":"themes",
        "names":"names",
        "theme_labels":["MUSIC","FILM/TV","DIGITAL","REPORTING"],
    },
}
CSS = "/assets/media-culture-editorial.css?v=20260922-v1"
YEAR_RE = re.compile(r"(?:19|20)\d{2}")


def direct_child(section, tag=None, cls=None):
    for child in section.children:
        if not getattr(child, "name", None):
            continue
        if tag and child.name != tag:
            continue
        if cls and cls not in (child.get("class") or []):
            continue
        return child
    return None


def audit(lang: str, path: Path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    article = soup.select_one("article.article-body")
    if article is None:
        raise AssertionError(f"{path.relative_to(ROOT)}: article.article-body missing")

    stylesheets = [node.get("href") for node in soup.select('link[rel="stylesheet"][href]')]
    if CSS not in stylesheets:
        raise AssertionError(f"{path.relative_to(ROOT)}: dedicated Media & Culture stylesheet missing")

    entries = []
    for sid in EXPECTED_IDS[lang]:
        section = article.select_one(f"section#{sid}")
        if section is None:
            raise AssertionError(f"{path.relative_to(ROOT)}: #{sid} missing")
        phase = direct_child(section, cls="phase-year")
        heading = direct_child(section, tag="h2")
        if phase is None:
            raise AssertionError(f"{path.relative_to(ROOT)}#{sid}: direct .phase-year missing")
        if heading is None:
            raise AssertionError(f"{path.relative_to(ROOT)}#{sid}: direct h2 missing")
        phase_text = phase.get_text(" ", strip=True)
        if not YEAR_RE.search(phase_text):
            raise AssertionError(f"{path.relative_to(ROOT)}#{sid}: phase-year has no year: {phase_text!r}")
        children = [child for child in section.children if getattr(child, "name", None)]
        if children.index(phase) > children.index(heading):
            raise AssertionError(f"{path.relative_to(ROOT)}#{sid}: date must precede h2")
        entries.append(sid)

    context = CONTEXT[lang]
    themes = article.select_one(f"section#{context['themes']}")
    names = article.select_one(f"section#{context['names']}")
    if themes is None or names is None:
        raise AssertionError(f"{path.relative_to(ROOT)}: contextual sections missing")
    if direct_child(themes, cls="phase-year") is not None:
        raise AssertionError(
            f"{path.relative_to(ROOT)}#{context['themes']}: contextual section must not have a direct chronology date"
        )
    theme_labels = [
        node.get_text(" ", strip=True)
        for node in themes.select(".phase-list > .phase > .phase-year")
    ]
    if theme_labels != context["theme_labels"]:
        raise AssertionError(
            f"{path.relative_to(ROOT)}#{context['themes']}: topical labels drifted; "
            f"expected={context['theme_labels']}, found={theme_labels}"
        )
    if any(YEAR_RE.search(label) for label in theme_labels):
        raise AssertionError(
            f"{path.relative_to(ROOT)}#{context['themes']}: topical labels must remain non-chronological"
        )
    if direct_child(names, cls="phase-year") is not None:
        raise AssertionError(f"{path.relative_to(ROOT)}#{context['names']}: names context must remain undated")

    return entries


def main() -> int:
    results = {lang: audit(lang, path) for lang, path in TARGETS.items()}
    canonical_en = [
        {"film":"cinema","architect":"arquiteto"}.get(item,item)
        for item in results["en"]
    ]
    if results["pt"] != canonical_en:
        raise AssertionError(f"PT/EN Media & Culture chronology differs: {results}")
    print(
        "Media & Culture editorial structure OK: "
        f"{len(results['pt'])} dated episodes in PT/EN; thematic/name context remains separate."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
