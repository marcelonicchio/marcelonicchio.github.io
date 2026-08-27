from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def wrap_coitado(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    if "music-coitado-1992" in text:
        raise SystemExit(f"{path}: Coitado subunits already present")

    if lang == "pt":
        old = '''<section id="coitado" class="chapter"><h2>Coitado do Próximo</h2><p>Em 1992, Marcelo Nicchio fundou o <strong>Coitado do Próximo</strong>, projeto autoral em que atuou como compositor e baterista. Desde o início, Nicchio e o vocalista formaram o núcleo do projeto, enquanto a banda atravessou diferentes formações ao longo dos anos. O grupo permaneceu continuamente ativo até seu encerramento oficial em 2003.</p><p>O primeiro show preservado em vídeo aconteceu ainda em 1992, no <strong>Barão Homem de Mello</strong>, colégio estadual em Santana, São Paulo. A partir de 1993 começaram as apresentações mais estruturadas no circuito de casas noturnas da cidade.</p><p>Em 1994 foi gravada a primeira demo-tape, com <em>Pegue o seu Celular</em> e <em>Mulher SP</em>. O áudio final e vídeos das sessões de gravação sobreviveram e aguardam publicação.</p><p>No mesmo ano, Nicchio foi entrevistado por <strong>Kid Vinil</strong> na 97FM Rock. O áudio dessa entrevista foi preservado diretamente da transmissão de rádio e também deverá integrar o arquivo público.</p></section>'''
        new = '''<section id="coitado" class="chapter"><h2>Coitado do Próximo</h2><div data-bio-key="music-coitado-1992"><p>Em 1992, Marcelo Nicchio fundou o <strong>Coitado do Próximo</strong>, projeto autoral em que atuou como compositor e baterista. Desde o início, Nicchio e o vocalista formaram o núcleo do projeto, enquanto a banda atravessou diferentes formações ao longo dos anos. O grupo permaneceu continuamente ativo até seu encerramento oficial em 2003.</p><p>O primeiro show preservado em vídeo aconteceu ainda em 1992, no <strong>Barão Homem de Mello</strong>, colégio estadual em Santana, São Paulo. A partir de 1993 começaram as apresentações mais estruturadas no circuito de casas noturnas da cidade.</p></div><div data-bio-key="music-coitado-1994"><p>Em 1994 foi gravada a primeira demo-tape, com <em>Pegue o seu Celular</em> e <em>Mulher SP</em>. O áudio final e vídeos das sessões de gravação sobreviveram e aguardam publicação.</p><p>No mesmo ano, Nicchio foi entrevistado por <strong>Kid Vinil</strong> na 97FM Rock. O áudio dessa entrevista foi preservado diretamente da transmissão de rádio e também deverá integrar o arquivo público.</p></div></section>'''
    else:
        old = '''<section id="coitado" class="chapter"><h2>Coitado do Próximo</h2><p>In 1992, Marcelo Nicchio founded <strong>Coitado do Próximo</strong>, an original project in which he worked as composer and drummer. From the beginning, Nicchio and the vocalist formed the core of the project while the band moved through different lineups over the years. The group remained continuously active until its official end in 2003.</p><p>The first performance preserved on video took place in 1992 at <strong>Barão Homem de Mello</strong>, a state school in the Santana district of São Paulo. From 1993 onward, the band began playing more structured shows on the city's club circuit.</p><p>In 1994 it recorded its first demo tape with <em>Pegue o seu Celular</em> and <em>Mulher SP</em>. The final audio and footage from the recording sessions survive and await publication.</p><p>That same year Nicchio was interviewed by <strong>Kid Vinil</strong> on 97FM Rock. A direct recording of the radio broadcast has been preserved and is also expected to become part of the public archive.</p></section>'''
        new = '''<section id="coitado" class="chapter"><h2>Coitado do Próximo</h2><div data-bio-key="music-coitado-1992"><p>In 1992, Marcelo Nicchio founded <strong>Coitado do Próximo</strong>, an original project in which he worked as composer and drummer. From the beginning, Nicchio and the vocalist formed the core of the project while the band moved through different lineups over the years. The group remained continuously active until its official end in 2003.</p><p>The first performance preserved on video took place in 1992 at <strong>Barão Homem de Mello</strong>, a state school in the Santana district of São Paulo. From 1993 onward, the band began playing more structured shows on the city's club circuit.</p></div><div data-bio-key="music-coitado-1994"><p>In 1994 it recorded its first demo tape with <em>Pegue o seu Celular</em> and <em>Mulher SP</em>. The final audio and footage from the recording sessions survive and await publication.</p><p>That same year Nicchio was interviewed by <strong>Kid Vinil</strong> on 97FM Rock. A direct recording of the radio broadcast has been preserved and is also expected to become part of the public archive.</p></div></section>'''
    if old not in text:
        raise SystemExit(f"{path}: expected Coitado section not found")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def refine_manifest() -> None:
    path = ROOT / "data/full_biography.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data["entries"]
    old_index = next((i for i, e in enumerate(entries) if e["id"] == "music-coitado"), None)
    if old_index is None:
        raise SystemExit("music-coitado entry not found in manifest")
    old = entries.pop(old_index)
    base = {
        "era": old["era"],
        "domain": old["domain"],
    }
    foundation = {
        "id": "music-coitado-1992",
        **base,
        "date": "1992",
        "title": {"pt": "Fundação e primeiro show", "en": "Foundation and first show"},
        "source": {
            "pt": {"path": "pt/musica/index.html", "kind": "subunit", "selector": "[data-bio-key='music-coitado-1992']", "parent_selector": "#coitado"},
            "en": {"path": "en/music/index.html", "kind": "subunit", "selector": "[data-bio-key='music-coitado-1992']", "parent_selector": "#coitado"}
        }
    }
    demo = {
        "id": "music-coitado-1994",
        **base,
        "date": "1994",
        "title": {"pt": "Demo-tape e Kid Vinil", "en": "Demo tape and Kid Vinil"},
        "source": {
            "pt": {"path": "pt/musica/index.html", "kind": "subunit", "selector": "[data-bio-key='music-coitado-1994']", "parent_selector": "#coitado"},
            "en": {"path": "en/music/index.html", "kind": "subunit", "selector": "[data-bio-key='music-coitado-1994']", "parent_selector": "#coitado"}
        }
    }
    entries.insert(old_index, foundation)
    # Place the 1994-specific material after the 1993–1995 circuit entry and before Metrópole.
    circuit_index = next(i for i, e in enumerate(entries) if e["id"] == "music-circuit")
    entries.insert(circuit_index + 1, demo)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_sync_script() -> None:
    path = ROOT / "tools/sync_full_biography.py"
    text = path.read_text(encoding="utf-8")

    old = '''    section["data-bio-entry"] = entry["id"]
    section["data-bio-domain"] = entry["domain"]
    meta = BeautifulSoup(meta_html(entry, lang, manifest, context=context), "html.parser").div
    section.insert(0, meta)
    return str(section)
'''
    new = '''    section["data-bio-entry"] = entry["id"]
    section["data-bio-domain"] = entry["domain"]
    heading = section.find("h2", recursive=False)
    if heading is not None:
        clean = re.sub(r"^\\s*\\d{4}(?:[–-](?:\\d{2,4}|presente|present))?\\s+—\\s+", "", heading.get_text(" ", strip=True), flags=re.I)
        if clean != heading.get_text(" ", strip=True):
            heading.clear()
            heading.append(clean)
    meta = BeautifulSoup(meta_html(entry, lang, manifest, context=context), "html.parser").div
    section.insert(0, meta)
    return str(section)
'''
    if old not in text:
        raise SystemExit("render_section patch point not found")
    text = text.replace(old, new, 1)

    phase_block = '''def render_phase(node: Tag, entry: dict[str, Any], lang: str, manifest: dict[str, Any]) -> str:
'''
    subunit_fn = '''def render_subunit(node: Tag, entry: dict[str, Any], lang: str, manifest: dict[str, Any]) -> str:
    title = entry["title"][lang]
    body = node.decode_contents()
    meta = meta_html(entry, lang, manifest, context=False)
    return (
        f'<section id="bio-{entry["id"]}" class="chapter bio-entry" '
        f'data-bio-entry="{entry["id"]}" data-bio-domain="{entry["domain"]}">'
        f'{meta}<h2>{html.escape(title)}</h2>{body}</section>'
    )


'''
    if phase_block not in text:
        raise SystemExit("render_phase insertion point not found")
    text = text.replace(phase_block, subunit_fn + phase_block, 1)

    old_dispatch = '''    if kind == "phase":
        node = select_exactly_one(soup, spec["selector"], f"{entry['id']}:{lang}")
        return render_phase(node, entry, lang, manifest)
    if kind == "fragment":
'''
    new_dispatch = '''    if kind == "phase":
        node = select_exactly_one(soup, spec["selector"], f"{entry['id']}:{lang}")
        return render_phase(node, entry, lang, manifest)
    if kind == "subunit":
        node = select_exactly_one(soup, spec["selector"], f"{entry['id']}:{lang}")
        return render_subunit(node, entry, lang, manifest)
    if kind == "fragment":
'''
    if old_dispatch not in text:
        raise SystemExit("render_entry dispatch patch point not found")
    text = text.replace(old_dispatch, new_dispatch, 1)
    path.write_text(text, encoding="utf-8")


def patch_audit_script() -> None:
    path = ROOT / "tools/audit_full_biography.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('registered_phase_keys: dict[str, set[str]] = defaultdict(set)', 'registered_unit_keys: dict[str, set[str]] = defaultdict(set)')
    text = text.replace('phase_parents: dict[str, set[str]] = defaultdict(set)', 'keyed_parents: dict[str, set[str]] = defaultdict(set)')

    old = '''            elif spec["kind"] == "phase":
                parent = selector_id(spec.get("parent_selector"))
                if not parent:
                    fail(errors, f"{entry['id']}:{lang}: phase has no simple parent selector")
                else:
                    phase_parents[path].add(parent)
                key_match = re.search(r"data-bio-key=['\\\"]([^'\\\"]+)['\\\"]", spec["selector"])
                if not key_match:
                    fail(errors, f"{entry['id']}:{lang}: phase selector must use data-bio-key")
                else:
                    registered_phase_keys[path].add(key_match.group(1))
            else:
'''
    new = '''            elif spec["kind"] in {"phase", "subunit"}:
                parent = selector_id(spec.get("parent_selector"))
                if not parent:
                    fail(errors, f"{entry['id']}:{lang}: keyed unit has no simple parent selector")
                else:
                    keyed_parents[path].add(parent)
                key_match = re.search(r"data-bio-key=['\\\"]([^'\\\"]+)['\\\"]", spec["selector"])
                if not key_match:
                    fail(errors, f"{entry['id']}:{lang}: keyed unit selector must use data-bio-key")
                else:
                    registered_unit_keys[path].add(key_match.group(1))
            else:
'''
    if old not in text:
        raise SystemExit("audit kind block patch point not found")
    text = text.replace(old, new, 1)
    text = text.replace('covered = covered_sections[path] | phase_parents[path]', 'covered = covered_sections[path] | keyed_parents[path]')

    old_loop = '''            for parent_id in phase_parents[path]:
                parent = body.select_one(f"#{parent_id}")
                if parent is None:
                    continue
                phases = parent.select(".phase")
                actual_keys = {phase.get("data-bio-key") for phase in phases}
                if None in actual_keys:
                    fail(errors, f"{lang}: unregistered .phase without data-bio-key inside #{parent_id} in {path}")
                    actual_keys.discard(None)
                expected_keys = registered_phase_keys[path]
                missing_keys = sorted(actual_keys - expected_keys)
                stale_keys = sorted(expected_keys - actual_keys)
                if missing_keys:
                    fail(errors, f"{lang}: phase keys missing from manifest in {path}: {missing_keys}")
                if stale_keys:
                    fail(errors, f"{lang}: manifest phase keys missing from source in {path}: {stale_keys}")
'''
    new_loop = '''            for parent_id in keyed_parents[path]:
                parent = body.select_one(f"#{parent_id}")
                if parent is None:
                    continue
                keyed = parent.select("[data-bio-key]")
                actual_keys = {node.get("data-bio-key") for node in keyed}
                expected_keys = registered_unit_keys[path]
                missing_keys = sorted(actual_keys - expected_keys)
                if missing_keys:
                    fail(errors, f"{lang}: keyed biography units missing from manifest in {path}: {missing_keys}")
                parent_expected = {
                    key for key in expected_keys
                    if parent.select_one(f'[data-bio-key="{key}"]') is not None
                }
                stale_keys = sorted(parent_expected - actual_keys)
                if stale_keys:
                    fail(errors, f"{lang}: manifest biography unit keys missing from source in {path}: {stale_keys}")
'''
    if old_loop not in text:
        raise SystemExit("audit keyed-unit loop patch point not found")
    text = text.replace(old_loop, new_loop, 1)
    path.write_text(text, encoding="utf-8")


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def self_clean() -> None:
    for rel in ["tools/_refine_full_biography.py", ".github/workflows/refine-full-biography.yml"]:
        p = ROOT / rel
        if p.exists():
            p.unlink()


wrap_coitado(ROOT / "pt/musica/index.html", "pt")
wrap_coitado(ROOT / "en/music/index.html", "en")
refine_manifest()
patch_sync_script()
patch_audit_script()
run("tools/sync_full_biography.py")
run("tools/sync_full_biography.py", "--check")
run("tools/audit_full_biography.py")
self_clean()
print("Full Biography chronology refinement complete.")
