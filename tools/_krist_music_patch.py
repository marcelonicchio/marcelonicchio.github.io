#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PT = ROOT / "pt/musica/index.html"
EN = ROOT / "en/music/index.html"
STYLES = ROOT / "styles.css"
MANIFEST = ROOT / "data/full_biography.json"
PARITY = ROOT / "data/editorial_parity.json"

PT_MARKER = '<section id="palcos" class="chapter"><h2>Palcos, discos e expansão</h2><div class="phase-list">\n'
EN_MARKER = '<section id="stages" class="chapter"><h2>Stages, albums and expansion</h2><div class="phase-list">\n'

PT_ENTRY = '''<div class="phase" data-bio-key="music-limonada-1992" id="destemidos-limonadas-punkecas-1992"><div class="phase-year">1992</div><div><h3>Destemidos Limonadas &amp; Punkecas</h3><p>Em 1992, quando o <strong>Coitado do Próximo</strong> ainda estava no começo, um encontro casual ampliou o horizonte musical de Nicchio. Num dia em que havia cabulado aula e passava o tempo lendo jornal na banca de <strong>Márcio</strong>, amigo e dono da banca, Márcio chamou sua atenção para um homem que passava: <strong>Roberto Sassano</strong>, conhecido na cena como <strong>Roberto Limonada</strong> — ou simplesmente Limonada.</p><p>Roberto era proprietário de um <strong>posto Esso na Avenida Brás Leme</strong>, a mesma avenida onde Nicchio morava, e tocava com os <strong>Destemidos Limonadas &amp; Punkecas</strong>. A banda estava prestes a se apresentar no <strong>Café Piu-Piu</strong>, no Bexiga, e aparecia com foto em uma matéria do extinto <em>Diário de São Paulo</em>. Márcio abriu o jornal e apontou para a imagem: <q>Olha quem é esse cara, olha eles aqui.</q></p><p>Da conversa nasceu uma convivência musical. Nicchio ainda estava muito ligado ao thrash metal — com <strong>Ratos de Porão</strong> entre as referências mais presentes — enquanto Limonada tinha um conhecimento profundo de punk rock. <strong>Ramones</strong>, paixão que Nicchio já carregava, para Roberto era quase uma religião. Nicchio passou a frequentar o escritório do posto Esso para ouvir rádio e conversar sobre bandas, discos e a cena.</p><p>Em uma dessas noites, ao chegar em casa, ouviu da mãe que Roberto havia telefonado: uma entrevista com a banda seria exibida naquela noite no <strong>Jô Soares Onze e Meia</strong>, no SBT. Ver uma banda punk ligada a alguém que ele conhecia pessoalmente chegar à televisão nacional foi um divisor de águas. Um universo que parecia distante ganhou proximidade e possibilidade.</p><p>Essa relação continuaria repercutindo na história do Coitado do Próximo. Mais tarde, Limonada apresentaria Nicchio a <strong>Kid Vinil</strong> e ajudaria a viabilizar sua entrevista na <strong>97FM Rock</strong>, quando a primeira demo-tape, gravada no <strong>Estúdio Anonimato</strong>, pôde ser apresentada no rádio com <strong>“Mulher SP”</strong>.</p></div></div>\n'''

EN_ENTRY = '''<div class="phase" data-bio-key="music-limonada-1992" id="destemidos-limonadas-punkecas-1992"><div class="phase-year">1992</div><div><h3>Destemidos Limonadas &amp; Punkecas</h3><p>In 1992, while <strong>Coitado do Próximo</strong> was still taking shape, a chance encounter widened Nicchio's musical horizon. One day, after skipping class and spending time reading newspapers at the newsstand run by his friend <strong>Márcio</strong>, Márcio called his attention to a man passing by: <strong>Roberto Sassano</strong>, known in the scene as <strong>Roberto Limonada</strong> — or simply Limonada.</p><p>Roberto owned an <strong>Esso gas station on Avenida Brás Leme</strong>, the same avenue where Nicchio lived, and played with <strong>Destemidos Limonadas &amp; Punkecas</strong>. The band was about to perform at <strong>Café Piu-Piu</strong> in Bexiga and had appeared with a photograph in the now-defunct <em>Diário de São Paulo</em>. Márcio opened the paper and pointed at the picture: <q>Look who this guy is — look, they're right here.</q></p><p>A musical friendship grew out of that conversation. Nicchio was still strongly connected to thrash metal — with <strong>Ratos de Porão</strong> among his most immediate references — while Limonada had a deep knowledge of punk rock. <strong>Ramones</strong>, already a passion for Nicchio, were almost a religion to Roberto. Nicchio began spending time in the Esso station office listening to the radio and talking about bands, records and the scene.</p><p>One evening, when he got home, his mother told him Roberto had called: an interview with the band would air that night on <strong>Jô Soares Onze e Meia</strong> on SBT. Seeing a punk band connected to someone he actually knew reach national television became a turning point. A world that had seemed distant suddenly felt close and possible.</p><p>That relationship would continue to shape Coitado do Próximo's story. Later, Limonada would introduce Nicchio to <strong>Kid Vinil</strong> and help make possible his interview on <strong>97FM Rock</strong>, where the first demo tape, recorded at <strong>Estúdio Anonimato</strong>, could be played on the radio with <strong>“Mulher SP”</strong>.</p></div></div>\n'''

CSS = r'''

/* Music / Coitado do Próximo: major-entry hierarchy — 2026-09-11 */
#palcos .phase-list,
#stages .phase-list{display:grid;gap:0;margin:34px 0}
#palcos .phase,
#stages .phase{display:block;padding:34px 0 38px;border-top:1px solid var(--line)}
#palcos .phase:last-child,
#stages .phase:last-child{border-bottom:1px solid var(--line)}
#palcos .phase-year,
#stages .phase-year{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--accent-soft);font-size:.76rem;line-height:1.2;letter-spacing:.12em;text-transform:uppercase;font-weight:800;margin:0 0 .55rem}
#palcos .phase h3,
#stages .phase h3{margin:0 0 .72rem;font-size:clamp(1.55rem,3vw,2.05rem);line-height:1.12;letter-spacing:-.035em;color:var(--text)}
#palcos .phase p,
#stages .phase p{margin:.72rem 0 0;font-size:1.02rem;line-height:1.68;color:#ddd8ce}
#palcos .phase q,
#stages .phase q{color:var(--text);font-style:italic}
@media(max-width:580px){
  #palcos .phase,#stages .phase{padding:28px 0 32px}
  #palcos .phase-year,#stages .phase-year{font-size:.72rem}
  #palcos .phase h3,#stages .phase h3{font-size:clamp(1.45rem,7vw,1.8rem)}
}
'''


def insert_once(path: Path, marker: str, entry: str) -> None:
    text = path.read_text(encoding="utf-8")
    if 'data-bio-key="music-limonada-1992"' in text:
        return
    if marker not in text:
        raise RuntimeError(f"marker not found in {path}")
    path.write_text(text.replace(marker, marker + entry, 1), encoding="utf-8")


def source_hash(path: Path, selector: str) -> str:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    nodes = soup.select(selector)
    if len(nodes) != 1:
        raise RuntimeError(f"{path}: selector {selector!r} matched {len(nodes)} nodes")
    text = str(nodes[0])
    import re
    text = re.sub(r">\s+<", "><", text)
    text = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    insert_once(PT, PT_MARKER, PT_ENTRY)
    insert_once(EN, EN_MARKER, EN_ENTRY)

    css_text = STYLES.read_text(encoding="utf-8")
    if "Music / Coitado do Próximo: major-entry hierarchy" not in css_text:
        STYLES.write_text(css_text.rstrip() + CSS + "\n", encoding="utf-8")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entry_id = "music-limonada-1992"
    if not any(e.get("id") == entry_id for e in manifest["entries"]):
        new_entry = {
            "id": entry_id,
            "era": "cruzamentos-1992-2000",
            "date": "1992",
            "domain": "music",
            "title": {
                "pt": "Destemidos Limonadas & Punkecas",
                "en": "Destemidos Limonadas & Punkecas"
            },
            "source": {
                "pt": {
                    "path": "pt/musica/index.html",
                    "kind": "phase",
                    "selector": "[data-bio-key='music-limonada-1992']",
                    "parent_selector": "#palcos"
                },
                "en": {
                    "path": "en/music/index.html",
                    "kind": "phase",
                    "selector": "[data-bio-key='music-limonada-1992']",
                    "parent_selector": "#stages"
                }
            }
        }
        pos = next(i for i, e in enumerate(manifest["entries"]) if e.get("id") == "music-coitado-1992") + 1
        manifest["entries"].insert(pos, new_entry)
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    registry = json.loads(PARITY.read_text(encoding="utf-8"))
    if entry_id not in registry["entries"]:
        registry["entries"][entry_id] = {
            "revision": 1,
            "pt_hash": source_hash(PT, "[data-bio-key='music-limonada-1992']"),
            "en_hash": source_hash(EN, "[data-bio-key='music-limonada-1992']"),
            "accepted_on": "2026-09-11",
            "changed_languages": ["pt", "en"]
        }
        PARITY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    subprocess.run(["python", "tools/sync_full_biography.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "tools/build_sitemap.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "tools/editorial_parity.py", "--check"], cwd=ROOT, check=True)
    subprocess.run(["python", "tools/sync_full_biography.py", "--check"], cwd=ROOT, check=True)
    subprocess.run(["python", "tools/audit_full_biography.py"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
