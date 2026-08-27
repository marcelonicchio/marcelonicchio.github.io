from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tag_phase(text: str, year: str, title: str, key: str) -> str:
    pattern = (
        r'<div class="phase">'
        r'(?=<div class="phase-year">' + re.escape(year) + r'</div>'
        r'<div><h3>' + re.escape(title) + r'</h3>)'
    )
    replacement = f'<div class="phase" data-bio-key="{key}">'
    updated, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not tag phase {key}: matched {count}")
    return updated


def patch_music_phase_keys() -> None:
    mappings = {
        "pt/musica/index.html": [
            ("1993–1995", "Circuito paulistano", "music-circuit-1993-1995"),
            ("1997", "Meu Querido Diário", "music-album-1997"),
            ("1998–1999", "Divulgação e festival", "music-festival-1998-1999"),
            ("1999–2000", "Eu Não Tô Nem Aí", "music-album-1999-2000"),
            ("jul. 2000", "Olympia", "music-olympia-2000"),
            ("21 jun. 2001", "Programa do Jô", "music-jo-2001"),
            ("2001–2003", "Atividade contínua", "music-active-2001-2003"),
            ("2003", "Encerramento", "music-end-2003"),
            ("2023", "Reunião pontual", "music-reunion-2023"),
        ],
        "en/music/index.html": [
            ("1993–1995", "São Paulo circuit", "music-circuit-1993-1995"),
            ("1997", "Meu Querido Diário", "music-album-1997"),
            ("1998–1999", "Promotion and festival", "music-festival-1998-1999"),
            ("1999–2000", "Eu Não Tô Nem Aí", "music-album-1999-2000"),
            ("Jul. 2000", "Olympia", "music-olympia-2000"),
            ("Jun. 21, 2001", "Programa do Jô", "music-jo-2001"),
            ("2001–2003", "Continuous activity", "music-active-2001-2003"),
            ("2003", "End of the project", "music-end-2003"),
            ("2023", "One-off reunion", "music-reunion-2023"),
        ],
    }
    for rel, phases in mappings.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if "data-bio-key=" in text:
            raise SystemExit(f"{rel} already contains data-bio-key attributes")
        for year, title, key in phases:
            text = tag_phase(text, year, title, key)
        path.write_text(text, encoding="utf-8")


def patch_manifest_metadata() -> None:
    path = ROOT / "data/full_biography.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    # The EN audiovisual vertical uses #architect while PT uses #arquiteto.
    selector_fixed = False
    for entry in data["entries"]:
        if entry["id"] == "audiovisual-arquiteto":
            entry["source"]["en"]["selector"] = "#architect"
            selector_fixed = True
            break
    if not selector_fixed:
        raise SystemExit("audiovisual-arquiteto not found in Full Biography manifest")

    overrides = {
        "music-olympia": "Jul. 2000",
        "livraria-cultura": "Oct. 2000–Jan. 2001",
        "communication-folha": "Apr. 23, 2001",
        "music-programa-jo": "Jun. 21, 2001",
        "internet-clickland": "Sep. 2012–present",
        "music-reunion-2023": "Dec. 2023",
        "hai-melissa": "Jan. 2026",
        "hai-pro1": "May 2026",
        "hai-pro2": "in development",
    }
    found = set()
    for entry in data["entries"]:
        if entry["id"] in overrides:
            entry["date_en"] = overrides[entry["id"]]
            found.add(entry["id"])
    missing = set(overrides) - found
    if missing:
        raise SystemExit(f"Date override ids not found: {sorted(missing)}")

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_styles() -> None:
    path = ROOT / "styles.css"
    text = path.read_text(encoding="utf-8")
    marker = "/* Full Biography integrated chronology */"
    if marker in text:
        raise SystemExit("Full Biography chronology styles already present")
    css = r'''

/* Full Biography integrated chronology */
.bio-chronology-intro{margin:3.25rem 0 2rem;padding:1.15rem 1.25rem;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.025)}
.bio-chronology-intro span,.bio-context-break span,.bio-era-break span{display:block;margin-bottom:.3rem;font-size:.72rem;line-height:1.25;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.bio-chronology-intro strong,.bio-context-break strong,.bio-era-break strong{display:block;font-size:1rem;line-height:1.35;color:var(--text)}
.bio-chronology-intro p{margin:.55rem 0 0;color:var(--muted);max-width:68ch}
.bio-era-break{margin:5.25rem 0 1.6rem;padding-top:1.15rem;border-top:1px solid var(--line)}
.bio-era-break strong{font-size:1.08rem}
.bio-entry-meta{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .65rem;margin:0 0 .55rem;font-size:.72rem;line-height:1.2;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.bio-entry-meta span+span::before{content:"·";margin-right:.65rem;color:var(--line-strong)}
.bio-entry>h2{margin-top:0}
.bio-context-break{margin:5.5rem 0 1.8rem;padding:1.1rem 0 0;border-top:1px solid var(--line-strong)}
@media(max-width:580px){.bio-chronology-intro{margin-top:2.25rem;padding:1rem}.bio-era-break{margin-top:3.75rem}.bio-context-break{margin-top:4rem}.bio-entry-meta{font-size:.68rem}}
'''
    path.write_text(text.rstrip() + css + "\n", encoding="utf-8")


def ensure_lightbox_script() -> None:
    for rel in ["pt/biografia/index.html", "en/biography/index.html"]:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if "/assets/js/archive-lightbox.js" not in text:
            text = text.replace("</body>", '<script src="/assets/js/archive-lightbox.js" defer></script>\n</body>', 1)
            path.write_text(text, encoding="utf-8")


def run_sync() -> None:
    subprocess.run([sys.executable, str(ROOT / "tools/sync_full_biography.py")], cwd=ROOT, check=True)


def self_clean() -> None:
    for rel in ["tools/_bootstrap_full_biography.py", ".github/workflows/bootstrap-full-biography.yml"]:
        path = ROOT / rel
        if path.exists():
            path.unlink()


patch_manifest_metadata()
patch_music_phase_keys()
append_styles()
ensure_lightbox_script()
run_sync()
self_clean()
print("Full Biography bootstrap complete.")
