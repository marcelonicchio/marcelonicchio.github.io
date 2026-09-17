#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data" / "entries.json"
FULL = ROOT / "data" / "full_biography.json"

PLAN = {
    "music-demo-tape-1994": {
        "domain": "music", "selector": {"pt":"#music-demo-tape-1994","en":"#music-demo-tape-1994"},
        "title": {"pt":"Gravação Primeira Demo-Tape - Estúdio Anonimato","en":"First Demo Tape Recording - Estúdio Anonimato"},
        "path": {"pt":"pt/musica/primeira-demo-tape-estudio-anonimato/index.html","en":"en/music/first-demo-tape-estudio-anonimato/index.html"},
    },
    "music-album-1997": {
        "domain": "music", "selector": {"pt":"#music-album-1997","en":"#music-album-1997"},
        "title": {"pt":"Primeiro Álbum: Meu Querido Diário","en":"First Album: Meu Querido Diário"},
        "path": {"pt":"pt/musica/meu-querido-diario/index.html","en":"en/music/meu-querido-diario/index.html"},
    },
    "audiovisual-homens": {
        "domain": "communication", "selector": {"pt":"#homens","en":"#homens"},
        "title": {"pt":"Programa \"Homens na Cozinha\"","en":"TV Program \"Homens na Cozinha\""},
        "path": {"pt":"pt/comunicacao/homens-na-cozinha/index.html","en":"en/communication/homens-na-cozinha/index.html"},
    },
    "music-festival-1998-1999": {
        "domain": "music", "selector": {"pt":"#music-festival-1998-1999","en":"#music-festival-1998-1999"},
        "title": {"pt":"Show Café Piu Piu (1998) e outros","en":"Café Piu Piu Show (1998) and others"},
        "path": {"pt":"pt/musica/cafe-piu-piu-1998/index.html","en":"en/music/cafe-piu-piu-1998/index.html"},
    },
    "music-album-1999-2000": {
        "domain": "music", "selector": {"pt":"#music-album-1999-2000","en":"#music-album-1999-2000"},
        "title": {"pt":"Segundo Álbum: Eu Não Tô Nem Aí","en":"Second Album: Eu Não Tô Nem Aí"},
        "path": {"pt":"pt/musica/eu-nao-to-nem-ai/index.html","en":"en/music/eu-nao-to-nem-ai/index.html"},
    },
    "internet-psinet": {
        "domain": "internet", "selector": {"pt":"#psinet","en":"#psinet"},
        "title": {"pt":"PSINet e hosting corporativo","en":"PSINet and corporate hosting"},
        "path": {"pt":"pt/internet/psinet-hosting-corporativo/index.html","en":"en/internet/psinet-corporate-hosting/index.html"},
    },
    "music-programa-jo": {
        "domain": "music", "selector": {"pt":"#music-jo-2001","en":"#music-jo-2001"},
        "title": {"pt":"Programa do Jô","en":"Programa do Jô"},
        "path": {"pt":"pt/musica/programa-do-jo/index.html","en":"en/music/programa-do-jo/index.html"},
    },
    "communication-sinal-verde": {
        "domain": "communication", "selector": {"pt":"#sinal-verde","en":"#sinal-verde"},
        "title": {"pt":"Coluna \"Prateleira Cultural\" - Revista Sinal Verde","en":"Column \"Prateleira Cultural\" - Sinal Verde Magazine"},
        "path": {"pt":"pt/comunicacao/prateleira-cultural-revista-sinal-verde/index.html","en":"en/communication/prateleira-cultural-sinal-verde/index.html"},
    },
    "internet-sem": {
        "domain": "internet", "selector": {"pt":"#sem","en":"#sem"},
        "title": {"pt":"Profissionalização em Search Marketing (2008)","en":"Professionalization in Search Marketing (2008)"},
        "path": {"pt":"pt/internet/search-marketing-2008/index.html","en":"en/internet/search-marketing-2008/index.html"},
    },
    "internet-clickland": {
        "domain": "internet", "selector": {"pt":"#clickland","en":"#clickland"},
        "title": {"pt":"Agência Clickland Digital","en":"Clickland Digital Agency"},
        "path": {"pt":"pt/internet/agencia-clickland-digital/index.html","en":"en/internet/clickland-digital-agency/index.html"},
    },
    "internet-petlove": {
        "domain": "internet", "selector": {"pt":"#petlove","en":"#petlove"},
        "title": {"pt":"Petlove: internalização de mídia (em escala)","en":"Petlove: media internalization (at scale)"},
        "path": {"pt":"pt/internet/petlove-internalizacao-de-midia/index.html","en":"en/internet/petlove-media-internalization/index.html"},
    },
    "hai-pro1": {
        "domain": "hai", "selector": {"pt":"#pro1","en":"#pro1"},
        "title": {"pt":"Metodologia \"Punk Rock Orchestra (PRO)\" v1","en":"Methodology \"Punk Rock Orchestra (PRO)\" v1"},
        "path": {"pt":"pt/ia-hai/punk-rock-orchestra-pro-v1/index.html","en":"en/ai-hai/punk-rock-orchestra-pro-v1/index.html"},
    },
    "hai-pro2": {
        "domain": "hai", "selector": {"pt":"#pro2","en":"#pro2"},
        "title": {"pt":"Metodologia \"Punk Rock Orchestra (PRO)\" 2.0","en":"Methodology \"Punk Rock Orchestra (PRO)\" 2.0"},
        "path": {"pt":"pt/ia-hai/punk-rock-orchestra-pro-2-0/index.html","en":"en/ai-hai/punk-rock-orchestra-pro-2-0/index.html"},
    },
}

VERTICAL = {
    "music": {"pt":"pt/musica/index.html","en":"en/music/index.html"},
    "communication": {"pt":"pt/comunicacao/index.html","en":"en/communication/index.html"},
    "internet": {"pt":"pt/internet/index.html","en":"en/internet/index.html"},
    "hai": {"pt":"pt/ia-hai/index.html","en":"en/ai-hai/index.html"},
}
FULL_PATH = {"pt":"pt/biografia/index.html","en":"en/biography/index.html"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def public(rel: str) -> str:
    return "/" + (rel[:-10] if rel.endswith("index.html") else rel).lstrip("/")


def section_parts(text: str, selector: str):
    assert selector.startswith("#")
    sid = re.escape(selector[1:])
    pat = re.compile(rf'(<section\b(?=[^>]*\bid=["\']{sid}["\'])[^>]*>)(.*?)(</section>)', re.S | re.I)
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{selector}: matched {len(matches)} sections")
    m = matches[0]
    return pat, m, m.group(1), m.group(2), m.group(3)


def first_paragraph(fragment: str) -> str:
    soup = BeautifulSoup(fragment, "html.parser")
    p = soup.find("p")
    if p is None:
        return soup.get_text(" ", strip=True)[:500] or "Registro documental no HUB de Marcelo Nicchio."
    return p.get_text(" ", strip=True)


def strip_managed_markers(body: str, entry_id: str) -> str:
    start = f"<!-- entry-source:{entry_id}:start -->"
    end = f"<!-- entry-source:{entry_id}:end -->"
    if start in body and end in body:
        return body.split(start,1)[1].split(end,1)[0].strip()
    return body.strip()


def replace_heading(text: str, selector: str, title: str, href: str) -> tuple[str, str]:
    pat, m, opening, inner, closing = section_parts(text, selector)
    h = re.search(r'(<h2\b[^>]*>)(.*?)(</h2>)', inner, re.S | re.I)
    if h is None:
        raise RuntimeError(f"{selector}: h2 missing")
    before = inner[:h.start()]
    after = inner[h.end():]
    heading = f'{h.group(1)}<a class="entry-title-permalink" href="{href}">{html.escape(title)}</a>{h.group(3)}'
    new_inner = before + heading + after
    return text[:m.start()] + opening + new_inner + closing + text[m.end():], strip_managed_markers(after, "")


def extract_body(text: str, selector: str, entry_id: str) -> str:
    _, _, _, inner, _ = section_parts(text, selector)
    h = re.search(r'<h2\b[^>]*>.*?</h2>', inner, re.S | re.I)
    if h is None:
        raise RuntimeError(f"{selector}: h2 missing")
    return strip_managed_markers(inner[h.end():], entry_id)


def main() -> int:
    registry = load(ENTRIES)
    full = load(FULL)
    full_by_id = {e["id"]: e for e in full["entries"]}
    entries = registry["entries"]
    by_id = {e["id"]: e for e in entries}

    for entry_id, spec in PLAN.items():
        full_entry = full_by_id.get(entry_id)
        if full_entry is None:
            raise RuntimeError(f"{entry_id}: missing from full biography manifest")

        fragments = {}
        summaries = {}
        for lang in ("pt","en"):
            vertical_rel = VERTICAL[spec["domain"]][lang]
            vertical_path = ROOT / vertical_rel
            text = vertical_path.read_text(encoding="utf-8")
            selector = spec["selector"][lang]
            fragment = extract_body(text, selector, entry_id)
            fragments[lang] = fragment
            summaries[lang] = first_paragraph(fragment)
            new_text, _ = replace_heading(text, selector, spec["title"][lang], public(spec["path"][lang]))
            vertical_path.write_text(new_text, encoding="utf-8")

        existing = by_id.get(entry_id)
        source_paths = {lang: f"content/entries/{lang}/{entry_id}.inc" for lang in ("pt","en")}
        if existing and existing.get("source",{}).get("kind") == "fragment":
            for lang in ("pt","en"):
                current = existing["source"].get(f"{lang}_path")
                if current:
                    source_paths[lang] = current
        for lang in ("pt","en"):
            p = ROOT / source_paths[lang]
            p.parent.mkdir(parents=True, exist_ok=True)
            # Existing fragment sources remain authoritative; new sources are extracted from the current vertical.
            if not p.exists():
                p.write_text(fragments[lang].strip() + "\n", encoding="utf-8")

        date_pt = full_entry.get("date", "")
        date_en = full_entry.get("date_en", date_pt)
        if existing is None:
            existing = {
                "id": entry_id,
                "kind": "chapter",
                "domain": spec["domain"],
                "date": {"pt": date_pt, "en": date_en},
                "title": spec["title"],
                "summary": summaries,
                "topic_ids": [],
                "reader_presentation": {"state": "normal"},
                "source": {},
                "reader_targets": {},
                "chapter_page": {},
            }
            entries.append(existing)
            by_id[entry_id] = existing
        existing["domain"] = spec["domain"]
        existing["date"] = {"pt": date_pt, "en": date_en}
        existing["title"] = spec["title"]
        existing.setdefault("summary", summaries)
        for lang in ("pt","en"):
            if not existing["summary"].get(lang, "").strip():
                existing["summary"][lang] = summaries[lang]
        existing.setdefault("topic_ids", [])
        existing.setdefault("reader_presentation", {"state":"normal"})
        existing["source"] = {
            "kind": "fragment",
            "pt_path": source_paths["pt"],
            "en_path": source_paths["en"],
        }
        existing["reader_targets"] = {
            "pt": [
                {"path": VERTICAL[spec["domain"]]["pt"], "selector": spec["selector"]["pt"]},
                {"path": FULL_PATH["pt"], "selector": f"#bio-{entry_id}"},
            ],
            "en": [
                {"path": VERTICAL[spec["domain"]]["en"], "selector": spec["selector"]["en"]},
                {"path": FULL_PATH["en"], "selector": f"#bio-{entry_id}"},
            ],
        }
        old_page = existing.get("chapter_page", {})
        old_indexing = old_page.get("indexing") if old_page.get("status") == "pilot" else None
        existing["chapter_page"] = {
            "status": "pilot",
            "indexing": old_indexing or "noindex,follow",
            "pt_path": old_page.get("pt_path") or spec["path"]["pt"],
            "en_path": old_page.get("en_path") or spec["path"]["en"],
        }

    ENTRIES.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Phase 2 registry promotion complete: {len(PLAN)} entries.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
