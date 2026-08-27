#!/usr/bin/env python3
"""Build the Full Biography from canonical entries in the thematic verticals.

The thematic pages remain the editorial authoring surfaces. This script reads the
registered source sections/phases and composes the PT/EN Full Biography in one
chronological, cross-domain sequence. Do not hand-edit the managed region in the
Full Biography pages.
"""

from __future__ import annotations

import argparse
import copy
import html
import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "full_biography.json"
START = "<!-- full-biography:start -->"
END = "<!-- full-biography:end -->"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def source_soup(path: str) -> BeautifulSoup:
    p = ROOT / path
    if not p.exists():
        raise RuntimeError(f"Full Biography source does not exist: {path}")
    return BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")


def select_exactly_one(soup: BeautifulSoup, selector: str, label: str) -> Tag:
    nodes = soup.select(selector)
    if len(nodes) != 1:
        raise RuntimeError(f"{label}: selector {selector!r} matched {len(nodes)} nodes")
    node = nodes[0]
    if not isinstance(node, Tag):
        raise RuntimeError(f"{label}: selector did not resolve to an element")
    return node


def date_for(entry: dict[str, Any], lang: str) -> str:
    return entry.get(f"date_{lang}", entry.get("date", ""))


def meta_html(entry: dict[str, Any], lang: str, manifest: dict[str, Any], *, context: bool) -> str:
    domain = manifest["domains"][entry["domain"]][lang]
    if context:
        return f'<div class="bio-entry-meta"><span>{html.escape(domain)}</span></div>'
    date = date_for(entry, lang)
    return (
        '<div class="bio-entry-meta">'
        f'<span>{html.escape(date)}</span>'
        f'<span>{html.escape(domain)}</span>'
        '</div>'
    )


def render_section(node: Tag, entry: dict[str, Any], lang: str, manifest: dict[str, Any], *, context: bool) -> str:
    fragment = BeautifulSoup(str(node), "html.parser")
    section = fragment.find("section")
    if section is None:
        raise RuntimeError(f"{entry['id']}: registered section source is not a section")
    section["id"] = f"bio-{entry['id']}"
    classes = list(section.get("class", []))
    if "chapter" not in classes:
        classes.append("chapter")
    if "bio-entry" not in classes:
        classes.append("bio-entry")
    section["class"] = classes
    section["data-bio-entry"] = entry["id"]
    section["data-bio-domain"] = entry["domain"]
    heading = section.find("h2", recursive=False)
    if heading is not None:
        clean = re.sub(r"^\s*\d{4}(?:[–-](?:\d{2,4}|presente|present))?\s+—\s+", "", heading.get_text(" ", strip=True), flags=re.I)
        if clean and clean[0].islower():
            clean = clean[0].upper() + clean[1:]
        if clean != heading.get_text(" ", strip=True):
            heading.clear()
            heading.append(clean)
    meta = BeautifulSoup(meta_html(entry, lang, manifest, context=context), "html.parser").div
    section.insert(0, meta)
    return str(section)


def render_subunit(node: Tag, entry: dict[str, Any], lang: str, manifest: dict[str, Any]) -> str:
    title = entry["title"][lang]
    body = node.decode_contents()
    meta = meta_html(entry, lang, manifest, context=False)
    return (
        f'<section id="bio-{entry["id"]}" class="chapter bio-entry" '
        f'data-bio-entry="{entry["id"]}" data-bio-domain="{entry["domain"]}">'
        f'{meta}<h2>{html.escape(title)}</h2>{body}</section>'
    )


def render_phase(node: Tag, entry: dict[str, Any], lang: str, manifest: dict[str, Any]) -> str:
    year = node.select_one(".phase-year")
    body = None
    direct_divs = [child for child in node.children if isinstance(child, Tag) and child.name == "div"]
    if len(direct_divs) >= 2:
        body = direct_divs[1]
    if year is None or body is None:
        raise RuntimeError(f"{entry['id']}: malformed phase source")
    h3 = body.find("h3", recursive=False)
    if h3 is None:
        raise RuntimeError(f"{entry['id']}: phase has no h3")
    title = h3.decode_contents()
    rest = "".join(str(child) for child in body.contents if child is not h3)
    meta = meta_html(entry, lang, manifest, context=False)
    return (
        f'<section id="bio-{entry["id"]}" class="chapter bio-entry" '
        f'data-bio-entry="{entry["id"]}" data-bio-domain="{entry["domain"]}">'
        f'{meta}<h2>{title}</h2>{rest}</section>'
    )


def render_entry(entry: dict[str, Any], lang: str, manifest: dict[str, Any], *, context: bool = False) -> str:
    spec = entry["source"][lang]
    soup = source_soup(spec["path"])
    kind = spec["kind"]
    if kind == "section":
        node = select_exactly_one(soup, spec["selector"], f"{entry['id']}:{lang}")
        return render_section(node, entry, lang, manifest, context=context)
    if kind == "phase":
        node = select_exactly_one(soup, spec["selector"], f"{entry['id']}:{lang}")
        return render_phase(node, entry, lang, manifest)
    if kind == "subunit":
        node = select_exactly_one(soup, spec["selector"], f"{entry['id']}:{lang}")
        return render_subunit(node, entry, lang, manifest)
    if kind == "fragment":
        node = soup.find("section")
        if node is None:
            raise RuntimeError(f"{entry['id']}:{lang}: fragment has no section")
        return render_section(node, entry, lang, manifest, context=context)
    raise RuntimeError(f"{entry['id']}:{lang}: unsupported source kind {kind!r}")


def era_break(era: dict[str, Any], lang: str) -> str:
    return (
        f'<div class="bio-era-break" id="bio-era-{era["id"]}">'
        f'<span>{html.escape(era["range"])}</span>'
        f'<strong>{html.escape(era[lang])}</strong>'
        '</div>'
    )


def render_managed_block(lang: str, manifest: dict[str, Any]) -> str:
    eras = {era["id"]: era for era in manifest["eras"]}
    if lang == "pt":
        intro = (
            '<div class="bio-chronology-intro" id="cronologia">'
            '<span>1989 → presente</span><strong>Uma única linha do tempo</strong>'
            '<p>Música, comunicação, internet, performance, audiovisual e IA/HAI aparecem aqui na ordem em que atravessaram a trajetória, inclusive quando ocorreram em paralelo.</p>'
            '</div>'
        )
        context_head = (
            '<div class="bio-context-break" id="bio-contexto">'
            '<span>Referências transversais</span><strong>Autoria, identidade e notas de contexto</strong>'
            '</div>'
        )
    else:
        intro = (
            '<div class="bio-chronology-intro" id="chronology">'
            '<span>1989 → present</span><strong>One integrated timeline</strong>'
            '<p>Music, communication, internet, performance, audiovisual work and AI/HAI appear here in the order they crossed the trajectory, including periods in which they happened in parallel.</p>'
            '</div>'
        )
        context_head = (
            '<div class="bio-context-break" id="bio-context">'
            '<span>Cross-cutting references</span><strong>Authorship, identity and context notes</strong>'
            '</div>'
        )

    pieces = [START, intro]
    current_era = None
    for entry in manifest["entries"]:
        if entry["era"] != current_era:
            current_era = entry["era"]
            pieces.append(era_break(eras[current_era], lang))
        pieces.append(render_entry(entry, lang, manifest))
    pieces.append(context_head)
    for entry in manifest["context_entries"]:
        pieces.append(render_entry(entry, lang, manifest, context=True))
    pieces.append(END)
    return "\n".join(pieces)


def render_aside(lang: str, manifest: dict[str, Any]) -> str:
    target = manifest["targets"][lang]
    overview_id = target["overview_id"]
    chronology_id = "cronologia" if lang == "pt" else "chronology"
    context_id = "bio-contexto" if lang == "pt" else "bio-context"
    links = [
        f'<a href="#{overview_id}">{html.escape(target["overview_label"])}</a>',
        f'<a href="#{chronology_id}">{html.escape(target["chronology_label"])}</a>',
    ]
    for era in manifest["eras"]:
        links.append(
            f'<a href="#bio-era-{era["id"]}">{html.escape(era["range"])} · {html.escape(era[lang])}</a>'
        )
    links.append(f'<a href="#{context_id}">{html.escape(target["context_label"])}</a>')
    aria = target["aside_label"]
    return (
        f'<aside class="article-aside" aria-label="{html.escape(aria)}">'
        f'<h3>{html.escape(aria)}</h3>{"".join(links)}</aside>'
    )


def replace_managed_region(text: str, lang: str, manifest: dict[str, Any]) -> str:
    block = render_managed_block(lang, manifest)
    if START in text and END in text:
        pattern = re.escape(START) + r".*?" + re.escape(END)
        text, count = re.subn(pattern, block, text, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError(f"{lang}: failed to replace managed Full Biography region")
    else:
        legacy_id = re.escape(manifest["targets"][lang]["legacy_start_id"])
        pattern = rf'<section id="{legacy_id}" class="chapter">.*?(?=<div class="page-tools">)'
        text, count = re.subn(pattern, block + "\n\n", text, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError(f"{lang}: failed to replace legacy Full Biography body")

    aside = render_aside(lang, manifest)
    text, count = re.subn(r'<aside class="article-aside"[^>]*>.*?</aside>', aside, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{lang}: failed to replace Full Biography aside")
    return text


def build_target(lang: str, manifest: dict[str, Any]) -> tuple[Path, str, str]:
    path = ROOT / manifest["targets"][lang]["path"]
    current = path.read_text(encoding="utf-8")
    expected = replace_managed_region(current, lang, manifest)
    return path, current, expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated Full Biography differs")
    args = parser.parse_args()

    manifest = load_manifest()
    changed = []
    for lang in ("pt", "en"):
        path, current, expected = build_target(lang, manifest)
        if current != expected:
            changed.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(expected, encoding="utf-8")

    if args.check and changed:
        print("Full Biography is out of sync:")
        for path in changed:
            print(f" - {path}")
        print("Run: python tools/sync_full_biography.py")
        return 1
    if changed:
        print("Synchronized Full Biography:")
        for path in changed:
            print(f" - {path}")
    else:
        print("Full Biography is synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
