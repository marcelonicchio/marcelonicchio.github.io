#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

POSTS = {
    "music-limonada-1992": {
        "selector_id": "destemidos-limonadas-punkecas-1992",
        "year": {"pt": "1992", "en": "1992"},
        "title": {
            "pt": "Destemidos Limonadas & Punkecas / Roberto Limonada",
            "en": "Destemidos Limonadas & Punkecas / Roberto Limonada",
        },
        "path": {
            "pt": "pt/musica/destemidos-limonadas-punkecas/index.html",
            "en": "en/music/destemidos-limonadas-punkecas/index.html",
        },
        "description": {
            "pt": "Destemidos Limonadas & Punkecas e Roberto Limonada: punk rock, Jô Soares, TV Cultura, Kid Vinil e a formação musical de Marcelo Nicchio a partir de 1992.",
            "en": "Destemidos Limonadas & Punkecas and Roberto Limonada: punk rock, Jô Soares, TV Cultura, Kid Vinil and Marcelo Nicchio's musical formation from 1992 onward.",
        },
    },
    "music-kid-vinil-1993": {
        "selector_id": "kid-vinil-verminose-cafe-piu-piu-1993",
        "year": {"pt": "1993", "en": "1993"},
        "title": {
            "pt": "Kid Vinil & Verminose — Café Piu Piu",
            "en": "Kid Vinil & Verminose — Café Piu Piu",
        },
        "path": {
            "pt": "pt/musica/kid-vinil-verminose-cafe-piu-piu/index.html",
            "en": "en/music/kid-vinil-verminose-cafe-piu-piu/index.html",
        },
        "description": {
            "pt": "Kid Vinil & Verminose no Café Piu Piu em 1993: a noite que marcou a entrada de Marcelo Nicchio no circuito punk rock paulistano.",
            "en": "Kid Vinil & Verminose at Café Piu Piu in 1993: the night that marked Marcelo Nicchio's entry into São Paulo's punk rock circuit.",
        },
    },
    "music-coitado-1994": {
        "selector_id": "kid-vinil-97fm-rock-1994",
        "year": {"pt": "1994", "en": "1994"},
        "title": {
            "pt": "Kid Vinil na 97FM Rock",
            "en": "Kid Vinil on 97FM Rock",
        },
        "path": {
            "pt": "pt/musica/kid-vinil-97fm-rock/index.html",
            "en": "en/music/kid-vinil-97fm-rock/index.html",
        },
        "description": {
            "pt": "Coitado do Próximo e Kid Vinil na 97FM Rock: a primeira demo, “Mulher SP” no rádio e uma segunda passagem improvisada com Mirão/365.",
            "en": "Coitado do Próximo and Kid Vinil on 97FM Rock: the first demo, “Mulher SP” on air and a second improvised appearance with Mirão/365.",
        },
    },
}

MUSIC_FILES = {"pt": ROOT / "pt/musica/index.html", "en": ROOT / "en/music/index.html"}
FRAGMENT_DIR = {"pt": ROOT / "content/entries/pt", "en": ROOT / "content/entries/en"}


def balanced_div(text: str, marker: str) -> tuple[int, int, str]:
    marker_pos = text.find(marker)
    if marker_pos < 0:
        raise RuntimeError(f"marker not found: {marker}")
    start = text.rfind("<div", 0, marker_pos)
    if start < 0:
        raise RuntimeError(f"opening div not found for {marker}")
    token = re.compile(r"</?div\b[^>]*>", re.I)
    depth = 0
    for m in token.finditer(text, start):
        if m.group(0).lower().startswith("</div"):
            depth -= 1
            if depth == 0:
                return start, m.end(), text[start:m.end()]
        else:
            depth += 1
    raise RuntimeError(f"unbalanced div for {marker}")


def phase_parts(block: str, entry_id: str) -> tuple[str, str]:
    pattern = re.compile(
        r'^<div\b[^>]*data-bio-key=["\']' + re.escape(entry_id) +
        r'["\'][^>]*>\s*<div\b[^>]*class=["\']phase-year["\'][^>]*>.*?</div>\s*'
        r'<div>\s*<h3>(?P<title>.*?)</h3>(?P<body>.*)</div>\s*</div>$',
        re.S | re.I,
    )
    m = pattern.match(block.strip())
    if not m:
        raise RuntimeError(f"could not parse phase block for {entry_id}")
    return m.group("title"), m.group("body").strip()


def plain_div_body(block: str, entry_id: str) -> str:
    m = re.match(
        r'^<div\b[^>]*data-bio-key=["\']' + re.escape(entry_id) + r'["\'][^>]*>(?P<body>.*)</div>$',
        block.strip(), re.S | re.I,
    )
    if not m:
        raise RuntimeError(f"could not parse plain block for {entry_id}")
    return m.group("body").strip()


def section_html(entry_id: str, lang: str, body: str) -> str:
    cfg = POSTS[entry_id]
    return (
        f'<section class="phase music-entry" data-bio-key="{entry_id}" id="{cfg["selector_id"]}">'
        f'<div class="phase-year">{cfg["year"][lang]}</div>'
        f'<h2>{cfg["title"][lang]}</h2>'
        f'{body}</section>'
    )


def migrate_music_file(lang: str) -> None:
    path = MUSIC_FILES[lang]
    text = path.read_text(encoding="utf-8")

    # Extract the three canonical bodies before changing their containers.
    bodies: dict[str, str] = {}
    for entry_id in ("music-limonada-1992", "music-kid-vinil-1993"):
        start, end, block = balanced_div(text, f'data-bio-key="{entry_id}"')
        _title, body = phase_parts(block, entry_id)
        bodies[entry_id] = body
        text = text[:start] + section_html(entry_id, lang, body) + text[end:]

    # The 97FM text currently lives inside the Coitado do Próximo parent block.
    start, end, block = balanced_div(text, 'data-bio-key="music-coitado-1994"')
    bodies["music-coitado-1994"] = plain_div_body(block, "music-coitado-1994")
    text = text[:start] + text[end:]

    # Promote 97FM to its own first-class entry, immediately after the 1994 demo entry.
    demo_start, demo_end, _demo = balanced_div(text, 'data-bio-key="music-demo-tape-1994"')
    promoted = "\n" + section_html("music-coitado-1994", lang, bodies["music-coitado-1994"])
    text = text[:demo_end] + promoted + text[demo_end:]

    for entry_id, body in bodies.items():
        FRAGMENT_DIR[lang].mkdir(parents=True, exist_ok=True)
        frag = FRAGMENT_DIR[lang] / f"{entry_id}.inc"
        frag.write_text(body + "\n", encoding="utf-8")

    path.write_text(text, encoding="utf-8")


def update_entries_registry() -> None:
    path = ROOT / "data/entries.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    by_id = {entry["id"]: entry for entry in data["entries"]}
    vertical = {
        "pt": "pt/musica/index.html",
        "en": "en/music/index.html",
    }
    biography = {
        "pt": "pt/biografia/index.html",
        "en": "en/biography/index.html",
    }
    for entry_id, cfg in POSTS.items():
        entry = by_id[entry_id]
        entry.pop("reader_scope", None)
        entry["source"] = {
            "kind": "fragment",
            "pt_path": f"content/entries/pt/{entry_id}.inc",
            "en_path": f"content/entries/en/{entry_id}.inc",
        }
        entry["reader_targets"] = {
            lang: [
                {"path": vertical[lang], "selector": f'#{cfg["selector_id"]}'},
                {"path": biography[lang], "selector": f"#bio-{entry_id}"},
            ]
            for lang in ("pt", "en")
        }
        entry["chapter_page"] = {
            "status": "pilot",
            "indexing": "noindex,follow",
            "pt_path": cfg["path"]["pt"],
            "en_path": cfg["path"]["en"],
            "description": cfg["description"],
        }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_full_bio_manifest() -> None:
    path = ROOT / "data/full_biography.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    by_id = {entry["id"]: entry for entry in data["entries"]}
    for entry_id, cfg in POSTS.items():
        entry = by_id[entry_id]
        entry["source"] = {
            "pt": {
                "path": "pt/musica/index.html",
                "kind": "section",
                "selector": f'#{cfg["selector_id"]}',
            },
            "en": {
                "path": "en/music/index.html",
                "kind": "section",
                "selector": f'#{cfg["selector_id"]}',
            },
        }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_sync_entries() -> None:
    path = ROOT / "tools/sync_entries.py"
    text = path.read_text(encoding="utf-8")
    old = '    fragment = fragment_path(entry, lang).read_text(encoding="utf-8").strip()\n    rendered_heading = render_heading(heading.group(0), entry, lang)\n    managed = (\n        f"{opening}{rendered_heading}"\n'
    new = '    fragment = fragment_path(entry, lang).read_text(encoding="utf-8").strip()\n    prefix = inner[: heading.start()]\n    rendered_heading = render_heading(heading.group(0), entry, lang)\n    managed = (\n        f"{opening}{prefix}{rendered_heading}"\n'
    if old not in text:
        if 'prefix = inner[: heading.start()]' not in text:
            raise RuntimeError("sync_entries patch point not found")
    else:
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")


def patch_full_bio_sync() -> None:
    path = ROOT / "tools/sync_full_biography.py"
    text = path.read_text(encoding="utf-8")
    old = '    section["data-bio-entry"] = entry["id"]\n    section["data-bio-domain"] = entry["domain"]\n    heading = section.find("h2", recursive=False)\n'
    new = '    section["data-bio-entry"] = entry["id"]\n    section["data-bio-domain"] = entry["domain"]\n    phase_year = section.find(class_="phase-year", recursive=False)\n    if phase_year is not None:\n        phase_year.decompose()\n    heading = section.find("h2", recursive=False)\n'
    if old not in text:
        if 'phase_year = section.find(class_="phase-year", recursive=False)' not in text:
            raise RuntimeError("sync_full_biography patch point not found")
    else:
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")


def patch_css() -> None:
    path = ROOT / "styles.css"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '#palcos .phase h3,\n#stages .phase h3{',
        '#palcos .phase h2,\n#stages .phase h2,\n#palcos .phase h3,\n#stages .phase h3{',
    )
    text = text.replace(
        '  #palcos .phase h3,#stages .phase h3{',
        '  #palcos .phase h2,#stages .phase h2,#palcos .phase h3,#stages .phase h3{',
    )
    marker = '/* Music promoted-entry permalinks — 2026-09-13 */'
    if marker not in text:
        text += (
            '\n' + marker + '\n'
            '#palcos .music-entry h2 a.entry-title-permalink,\n'
            '#stages .music-entry h2 a.entry-title-permalink{color:inherit;text-decoration:none}\n'
            '#palcos .music-entry h2 a.entry-title-permalink:hover,\n'
            '#stages .music-entry h2 a.entry-title-permalink:hover{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.16em}\n'
        )
    path.write_text(text, encoding="utf-8")


def main() -> int:
    for lang in ("pt", "en"):
        migrate_music_file(lang)
    update_entries_registry()
    update_full_bio_manifest()
    patch_sync_entries()
    patch_full_bio_sync()
    patch_css()
    print("Promoted three music entries to first-class structural units.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
