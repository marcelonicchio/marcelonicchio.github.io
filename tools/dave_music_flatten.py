#!/usr/bin/env python3
"""Temporary one-shot migration for the Music thread hierarchy.

Promotes the 15 entries currently nested under #palcos/#stages to first-level
chapters, applies Marcelo's 2026-09-16 title/order decisions, adds the MP3-era
entry, updates biography/entry registries and can accept the resulting PT/EN
editorial parity checkpoint.

Delete this file after the migration PR is validated.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PT_PATH = ROOT / "pt/musica/index.html"
EN_PATH = ROOT / "en/music/index.html"
MANIFEST_PATH = ROOT / "data/full_biography.json"
ENTRIES_PATH = ROOT / "data/entries.json"
PARITY_PATH = ROOT / "data/editorial_parity.json"
STYLES_PATH = ROOT / "styles.css"

PT_TITLES = {
    "destemidos": "Destemidos Limonadas & Punkecas (Roberto Limonada)",
    "kid": "Show Kid Vinil & Verminose - Café Piu Piu",
    "studios": "Ensaios em Estúdios e Primeiros Shows",
    "demo": "Gravação Primeira Demo-Tape - Estúdio Anonimato",
    "radio": "Entrevistas para Kid Vinil na 97FM Rock",
    "circuit": "Circuito paulistano - Shows e Aberturas para banda 365",
    "album1": "Primeiro Álbum: Meu Querido Diário",
    "festival": "Show Café Piu Piu (1998) e outros",
    "album2": "Segundo Álbum: Eu Não Tô Nem Aí",
    "etesp": "Shows ETESP / FATEC - Av. Tiradentes",
    "olympia": "Show no Olympia",
    "reunion": "Reencontro - 20 anos depois",
}

EN_TITLES = {
    "destemidos": "Destemidos Limonadas & Punkecas (Roberto Limonada)",
    "kid": "Kid Vinil & Verminose Show - Café Piu Piu",
    "studios": "Studio Rehearsals and First Shows",
    "demo": "First Demo Tape Recording - Estúdio Anonimato",
    "radio": "Interviews with Kid Vinil on 97FM Rock",
    "circuit": "São Paulo Circuit - Shows and Opening Sets for 365",
    "album1": "First Album: Meu Querido Diário",
    "festival": "Café Piu Piu Show (1998) and others",
    "album2": "Second Album: Eu Não Tô Nem Aí",
    "etesp": "ETESP / FATEC Shows - Avenida Tiradentes",
    "olympia": "Show at Olympia",
    "reunion": "Reunion - 20 years later",
}

# PT heading fragments identify the existing entries without relying on guessed keys.
PT_MATCHERS = {
    "destemidos": "Destemidos Limonadas & Punkecas",
    "kid": "Kid Vinil & Verminose",
    "studios": "Estúdios e Shows",
    "demo": "Gravação Primeira Demo-Tape",
    "radio": "Entrevista para Kid Vinil",
    "circuit": "Circuito paulistano",
    "album1": "Meu Querido Diário",
    "festival": "Divulgação e festival",
    "album2": "Eu Não Tô Nem Aí",
    "etesp": "ETESP / FATEC",
    "olympia": "Olympia",
    "reunion": "Reunião pontual",
}

MP3_KEY = "music-mp3-era-2000"
MP3_PT_TITLE = "A Era do MP3"
MP3_EN_TITLE = "The MP3 Era"
MP3_PT = (
    "No mesmo período do lançamento do segundo trabalho, serviços de distribuição gratuita, "
    "como o Napster, entraram em plena atividade. Com isso, portais como o Submarino abriram, "
    "em parceria com a gravadora Trama, áreas de downloads de artistas brasileiros em formato MP3. "
    "Durante um período, uma das músicas de trabalho, “Estava Comigo”, esteve entre as primeiras "
    "colocações em número de downloads."
)
MP3_EN = (
    "During the same period as the release of the second record, free-distribution services such as "
    "Napster entered full operation. In that context, portals such as Submarino opened, in partnership "
    "with the Trama record label, download areas for Brazilian artists in MP3 format. For a period, "
    "one of the tracks being promoted, “Estava Comigo”, ranked among the leading songs by number of downloads."
)


def heading_text(fragment: str) -> str:
    m = re.search(r"<h[23]\b[^>]*>(.*?)</h[23]>", fragment, flags=re.S | re.I)
    if not m:
        raise RuntimeError("entry has no h2/h3 heading")
    text = re.sub(r"<[^>]+>", "", m.group(1))
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def key_of(fragment: str) -> str:
    m = re.search(r'data-bio-key=["\']([^"\']+)["\']', fragment)
    if not m:
        raise RuntimeError("Music entry has no data-bio-key")
    return m.group(1)


def id_of(fragment: str) -> str | None:
    opening = re.match(r"\s*<(?:div|section)\b([^>]*)>", fragment, flags=re.S | re.I)
    if not opening:
        return None
    m = re.search(r'\bid=["\']([^"\']+)["\']', opening.group(1))
    return m.group(1) if m else None


def find_balanced_tag_end(text: str, start: int, tag: str) -> int:
    token = re.compile(rf"</?{re.escape(tag)}\b[^>]*>", re.I)
    depth = 0
    for m in token.finditer(text, start):
        if m.start() < start:
            continue
        if m.group(0).lower().startswith(f"</{tag.lower()}"):
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            depth += 1
    raise RuntimeError(f"unbalanced <{tag}> starting at {start}")


def find_section_by_id(text: str, section_id: str) -> tuple[int, int, str]:
    pat = re.compile(rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])[^>]*>', re.I)
    m = pat.search(text)
    if not m:
        raise RuntimeError(f"missing section #{section_id}")
    end = find_balanced_tag_end(text, m.start(), "section")
    return m.start(), end, text[m.start():end]


def phase_list_inner(block: str) -> tuple[str, str, str]:
    m = re.search(r'<div\s+class=["\']phase-list["\']\s*>', block, re.I)
    if not m:
        raise RuntimeError("phase-list wrapper not found")
    end = find_balanced_tag_end(block, m.start(), "div")
    close = block.rfind("</div>", m.end(), end)
    if close < 0:
        raise RuntimeError("phase-list closing div not found")
    return block[:m.end()], block[m.end():close], block[close:end]


def direct_phase_children(inner: str) -> tuple[list[str], str]:
    token = re.compile(r"</?(?:div|section)\b[^>]*>", re.I)
    depth = 0
    child_start = None
    child_tag = None
    children: list[str] = []
    consumed: list[tuple[int, int]] = []
    for m in token.finditer(inner):
        raw = m.group(0)
        closing = raw.startswith("</")
        tag = "section" if re.match(r"</?section\b", raw, re.I) else "div"
        if not closing:
            if depth == 0:
                if re.search(r'class=["\'][^"\']*\bphase(?:\s|["\'])', raw, re.I):
                    child_start = m.start()
                    child_tag = tag
                else:
                    # phase-list should contain only whitespace plus phase children.
                    raise RuntimeError(f"unexpected top-level element in phase-list: {raw[:80]}")
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                raise RuntimeError("phase-list child nesting underflow")
            if depth == 0 and child_start is not None:
                if tag != child_tag:
                    raise RuntimeError("phase-list child closes with a different tag")
                children.append(inner[child_start:m.end()])
                consumed.append((child_start, m.end()))
                child_start = None
                child_tag = None
    if depth != 0 or child_start is not None:
        raise RuntimeError("unbalanced phase-list children")
    residue = inner
    for start, end in reversed(consumed):
        residue = residue[:start] + residue[end:]
    return children, residue


def unwrap_phase_body(fragment: str) -> str:
    # Legacy phase shape: <div class=phase-year>...</div><div><h3>...</h3>...</div>
    year = re.search(r'<div\s+class=["\']phase-year["\'][^>]*>.*?</div>', fragment, flags=re.S | re.I)
    if not year:
        return fragment
    body = re.match(r"\s*<div\s*>", fragment[year.end():], flags=re.I)
    if not body:
        return fragment
    body_start = year.end() + body.start()
    body_open_end = year.end() + body.end()
    body_end = find_balanced_tag_end(fragment, body_start, "div")
    close_start = fragment.rfind("</div>", body_open_end, body_end)
    if close_start < 0:
        raise RuntimeError("legacy phase body close not found")
    return fragment[:body_start] + fragment[body_open_end:close_start] + fragment[body_end:]


def promote(fragment: str) -> str:
    if re.match(r"\s*<section\b", fragment, re.I):
        fragment = re.sub(
            r'^(\s*<section\b[^>]*\bclass=["\'])[^"\']*\bphase\b[^"\']*(["\'][^>]*>)',
            lambda m: m.group(1) + "chapter music-entry" + m.group(2),
            fragment,
            count=1,
            flags=re.I,
        )
    elif re.match(r"\s*<div\b", fragment, re.I):
        fragment = re.sub(
            r'^(\s*)<div\b([^>]*\bclass=["\'])[^"\']*\bphase\b[^"\']*(["\'][^>]*)>',
            lambda m: m.group(1) + '<section' + m.group(2) + "chapter music-entry" + m.group(3) + '>',
            fragment,
            count=1,
            flags=re.I,
        )
        last = fragment.rfind("</div>")
        if last < 0:
            raise RuntimeError("legacy phase outer close not found")
        fragment = fragment[:last] + "</section>" + fragment[last + len("</div>"):]
    else:
        raise RuntimeError("unknown phase child root element")

    fragment = unwrap_phase_body(fragment)
    # Every promoted entry now gets an h2, not the old nested h3.
    fragment = re.sub(r"<h3\b([^>]*)>", r"<h2\1>", fragment, count=1, flags=re.I)
    fragment = re.sub(r"</h3>", r"</h2>", fragment, count=1, flags=re.I)
    return fragment


def replace_title(fragment: str, new_title: str) -> str:
    escaped = html.escape(new_title, quote=False)
    m = re.search(r"<h2\b[^>]*>(.*?)</h2>", fragment, flags=re.S | re.I)
    if not m:
        raise RuntimeError(f"cannot rename entry without h2: {new_title}")
    inner = m.group(1)
    am = re.search(r"(<a\b[^>]*>)(.*?)(</a>)", inner, flags=re.S | re.I)
    if am:
        new_inner = inner[:am.start()] + am.group(1) + escaped + am.group(3) + inner[am.end():]
    else:
        new_inner = escaped
    return fragment[:m.start(1)] + new_inner + fragment[m.end(1):]


def identify_pt_labels(entries: list[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for frag in entries:
        title = heading_text(frag)
        for label, needle in PT_MATCHERS.items():
            if needle.casefold() in title.casefold():
                if label in found:
                    raise RuntimeError(f"duplicate PT matcher {label}: {title}")
                found[label] = key_of(frag)
    missing = sorted(set(PT_MATCHERS) - set(found))
    if missing:
        raise RuntimeError(f"could not identify PT Music entries: {missing}")
    return found


def mp3_section(lang: str) -> str:
    if lang == "pt":
        title, body = MP3_PT_TITLE, MP3_PT
    else:
        title, body = MP3_EN_TITLE, MP3_EN
    return (
        f'<section class="chapter music-entry" data-bio-key="{MP3_KEY}">'
        f'<div class="phase-year">2000</div><h2>{html.escape(title, quote=False)}</h2>'
        f'<p>{html.escape(body, quote=False)}</p></section>'
    )


def rewrite_music_page(path: Path, lang: str, label_to_key: dict[str, str] | None = None) -> tuple[dict[str, dict[str, str | None]], dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    section_id = "palcos" if lang == "pt" else "stages"
    start, end, block = find_section_by_id(text, section_id)
    _, inner, _ = phase_list_inner(block)
    children, residue = direct_phase_children(inner)
    if residue.strip():
        raise RuntimeError(f"unexpected non-whitespace residue inside #{section_id}: {residue[:120]!r}")
    if len(children) != 15:
        raise RuntimeError(f"expected 15 Music entries under #{section_id}, found {len(children)}")

    promoted = [promote(child) for child in children]
    if lang == "pt":
        label_to_key = identify_pt_labels(promoted)
    if not label_to_key:
        raise RuntimeError("label_to_key missing for EN rewrite")

    titles = PT_TITLES if lang == "pt" else EN_TITLES
    key_to_title: dict[str, str] = {}
    for label, new_title in titles.items():
        key = label_to_key[label]
        matched = False
        for i, frag in enumerate(promoted):
            if key_of(frag) == key:
                promoted[i] = replace_title(frag, new_title)
                key_to_title[key] = new_title
                matched = True
                break
        if not matched:
            raise RuntimeError(f"{lang}: key {key} for {label} not found")

    # Swap only the two requested 1993 entries: studios becomes #2, Kid becomes #3.
    kid_key = label_to_key["kid"]
    studios_key = label_to_key["studios"]
    kid_i = next(i for i, frag in enumerate(promoted) if key_of(frag) == kid_key)
    studios_i = next(i for i, frag in enumerate(promoted) if key_of(frag) == studios_key)
    promoted[kid_i], promoted[studios_i] = promoted[studios_i], promoted[kid_i]

    # Insert the new MP3-era entry after ETESP/FATEC and before Olympia, per Marcelo's list.
    etesp_key = label_to_key["etesp"]
    etesp_i = next(i for i, frag in enumerate(promoted) if key_of(frag) == etesp_key)
    promoted.insert(etesp_i + 1, mp3_section(lang))
    key_to_title[MP3_KEY] = MP3_PT_TITLE if lang == "pt" else MP3_EN_TITLE

    # Capture stable identifiers for manifest/entries registry updates.
    meta: dict[str, dict[str, str | None]] = {}
    for frag in promoted:
        key = key_of(frag)
        meta[key] = {"id": id_of(frag), "title": heading_text(frag)}

    replacement = "\n".join(promoted)
    text = text[:start] + replacement + text[end:]

    # The old aside anchor would become broken after removing #palcos/#stages.
    first_id = meta[label_to_key["destemidos"]]["id"]
    if not first_id:
        raise RuntimeError("Destemidos entry unexpectedly has no id")
    if lang == "pt":
        text = text.replace('<a href="#palcos">Palcos &amp; discos</a>', f'<a href="#{first_id}">Cronologia do Coitado</a>')
        text = text.replace('<a href="#palcos">Palcos & discos</a>', f'<a href="#{first_id}">Cronologia do Coitado</a>')
    else:
        text = text.replace('<a href="#stages">Stages &amp; records</a>', f'<a href="#{first_id}">Coitado chronology</a>')
        text = text.replace('<a href="#stages">Stages & records</a>', f'<a href="#{first_id}">Coitado chronology</a>')

    path.write_text(text, encoding="utf-8")
    return meta, label_to_key


def update_styles() -> None:
    text = STYLES_PATH.read_text(encoding="utf-8")
    start_marker = "/* Music / Coitado do Próximo: major-entry hierarchy — 2026-09-11 */"
    next_marker = "/* Music promoted-entry permalinks — 2026-09-13 */"
    start = text.find(start_marker)
    end = text.find(next_marker)
    if start < 0 or end < 0 or end <= start:
        raise RuntimeError("could not locate legacy Music hierarchy CSS block")
    block = """/* Music / Coitado do Próximo: flat top-level entry hierarchy — 2026-09-16 */
.article-body > .music-entry{padding-top:1px;border-top:1px solid var(--line);scroll-margin-top:100px}
.article-body > .music-entry > .phase-year{margin:46px 0 .55rem;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--accent-soft);font-size:.76rem;line-height:1.2;letter-spacing:.12em;text-transform:uppercase;font-weight:800}
.article-body > .music-entry > .phase-year + h2{margin-top:0}
@media(max-width:580px){.article-body > .music-entry > .phase-year{margin-top:38px;font-size:.72rem}}

"""
    text = text[:start] + block + text[end:]
    text = text.replace(
        "#palcos .music-entry h2 a.entry-title-permalink,\n#stages .music-entry h2 a.entry-title-permalink",
        ".article-body > .music-entry h2 a.entry-title-permalink",
    )
    text = text.replace(
        "#palcos .music-entry h2 a.entry-title-permalink:hover,\n#stages .music-entry h2 a.entry-title-permalink:hover",
        ".article-body > .music-entry h2 a.entry-title-permalink:hover",
    )
    STYLES_PATH.write_text(text, encoding="utf-8")


def selector_matches_meta(selector: str | None, key: str, element_id: str | None) -> bool:
    if not selector:
        return False
    if key in selector:
        return True
    return bool(element_id and selector == f"#{element_id}")


def update_manifest(pt_meta: dict[str, dict[str, str | None]], en_meta: dict[str, dict[str, str | None]]) -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    # Convert every Music vertical phase source into a genuine top-level section source.
    for entry in manifest.get("entries", []):
        for lang, target_path in (("pt", "pt/musica/index.html"), ("en", "en/music/index.html")):
            spec = entry.get("source", {}).get(lang)
            if spec and spec.get("path") == target_path and spec.get("kind") == "phase":
                spec["kind"] = "section"
                spec.pop("parent_selector", None)

    # Update title metadata where the manifest already tracks the entry.
    for entry in manifest.get("entries", []):
        for key, meta in pt_meta.items():
            if key == MP3_KEY:
                continue
            pt_sel = entry.get("source", {}).get("pt", {}).get("selector")
            if entry.get("id") == key or selector_matches_meta(pt_sel, key, meta.get("id")):
                entry["title"] = {
                    "pt": str(pt_meta[key]["title"]),
                    "en": str(en_meta[key]["title"]),
                }
                break

    if any(entry.get("id") == MP3_KEY for entry in manifest.get("entries", [])):
        raise RuntimeError(f"{MP3_KEY} already exists in Full Biography manifest")
    mp3_entry = {
        "id": MP3_KEY,
        "era": "cruzamentos-1992-2000",
        "date": "2000",
        "domain": "music",
        "title": {"pt": MP3_PT_TITLE, "en": MP3_EN_TITLE},
        "source": {
            "pt": {"path": "pt/musica/index.html", "kind": "section", "selector": f"[data-bio-key='{MP3_KEY}']"},
            "en": {"path": "en/music/index.html", "kind": "section", "selector": f"[data-bio-key='{MP3_KEY}']"},
        },
    }

    # Mirror the vertical insertion: after ETESP/FATEC and before Olympia.
    etesp_idx = None
    for i, entry in enumerate(manifest["entries"]):
        sel = entry.get("source", {}).get("pt", {}).get("selector", "")
        if "music-etesp-fatec-2000" in sel or entry.get("id") == "music-etesp-fatec-2000":
            etesp_idx = i
            break
    if etesp_idx is None:
        raise RuntimeError("ETESP/FATEC entry not found in Full Biography manifest")
    manifest["entries"].insert(etesp_idx + 1, mp3_entry)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_entries_registry(pt_meta: dict[str, dict[str, str | None]], en_meta: dict[str, dict[str, str | None]]) -> None:
    registry = json.loads(ENTRIES_PATH.read_text(encoding="utf-8"))
    changed = 0
    for entry in registry.get("entries", []):
        entry_id = entry.get("id")
        if entry_id in pt_meta and entry_id != MP3_KEY:
            entry["title"] = {
                "pt": str(pt_meta[entry_id]["title"]),
                "en": str(en_meta[entry_id]["title"]),
            }
            changed += 1
            continue
        # Some registry ids/selectors may differ from data-bio-key; match reader target id selectors too.
        for key, meta in pt_meta.items():
            if key == MP3_KEY:
                continue
            targets = entry.get("reader_targets", {}).get("pt", [])
            if any(selector_matches_meta(t.get("selector"), key, meta.get("id")) for t in targets):
                entry["title"] = {
                    "pt": str(pt_meta[key]["title"]),
                    "en": str(en_meta[key]["title"]),
                }
                changed += 1
                break
    ENTRIES_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated title metadata for {changed} registered chapter entries.")


def normalized_html_for_hash(raw: str) -> str:
    raw = re.sub(r">\s+<", "><", raw)
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw


def source_fragment_for_hash(entry: dict, lang: str) -> str:
    spec = entry["source"][lang]
    path = ROOT / spec["path"]
    text = path.read_text(encoding="utf-8")
    selector = spec.get("selector")
    if spec["kind"] == "fragment":
        start = text.find("<section")
        if start < 0:
            raise RuntimeError(f"{entry['id']}:{lang}: fragment has no section")
        end = find_balanced_tag_end(text, start, "section")
        return text[start:end]
    if selector and selector.startswith("#"):
        _, _, block = find_section_by_id(text, selector[1:])
        return block
    key_match = re.fullmatch(r"\[data-bio-key=['\"]([^'\"]+)['\"]\]", selector or "")
    if key_match:
        key = key_match.group(1)
        pat = re.compile(rf'<section\b(?=[^>]*\bdata-bio-key=["\']{re.escape(key)}["\'])[^>]*>', re.I)
        m = pat.search(text)
        if not m:
            raise RuntimeError(f"{entry['id']}:{lang}: selector {selector} not found")
        end = find_balanced_tag_end(text, m.start(), "section")
        return text[m.start():end]
    raise RuntimeError(f"unsupported parity selector in temporary migration: {selector}")


def accept_music_parity() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    registry = json.loads(PARITY_PATH.read_text(encoding="utf-8"))
    states = registry.setdefault("entries", {})
    today = date.today().isoformat()
    accepted = []
    for entry in manifest.get("entries", []) + manifest.get("context_entries", []):
        if entry.get("domain") != "music":
            continue
        hashes = {}
        for lang in ("pt", "en"):
            raw = normalized_html_for_hash(source_fragment_for_hash(entry, lang)).encode("utf-8")
            hashes[lang] = hashlib.sha256(raw).hexdigest()
        state = states.get(entry["id"])
        if state is None:
            states[entry["id"]] = {
                "revision": 1,
                "pt_hash": hashes["pt"],
                "en_hash": hashes["en"],
                "accepted_on": today,
                "changed_languages": ["pt", "en"],
            }
            accepted.append(f"{entry['id']}:new")
            continue
        changed = [lang for lang in ("pt", "en") if hashes[lang] != state.get(f"{lang}_hash")]
        if not changed:
            continue
        state["revision"] = int(state.get("revision", 0)) + 1
        state["pt_hash"] = hashes["pt"]
        state["en_hash"] = hashes["en"]
        state["accepted_on"] = today
        state["changed_languages"] = changed
        accepted.append(f"{entry['id']}:{','.join(changed)}")
    PARITY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Accepted Music PT/EN parity checkpoints:")
    for item in accepted:
        print(" -", item)


def migrate() -> None:
    pt_meta, labels = rewrite_music_page(PT_PATH, "pt")
    en_meta, _ = rewrite_music_page(EN_PATH, "en", labels)
    update_styles()
    update_manifest(pt_meta, en_meta)
    update_entries_registry(pt_meta, en_meta)
    print("Music hierarchy migration prepared: 15 entries promoted + MP3 entry inserted.")
    print("PT key map:")
    for label, key in labels.items():
        print(f" - {label}: {key}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--accept-parity", action="store_true")
    args = parser.parse_args()
    if args.accept_parity:
        accept_music_parity()
    else:
        migrate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
