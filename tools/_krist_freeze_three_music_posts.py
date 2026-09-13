#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "entries.json"

data = json.loads(PATH.read_text(encoding="utf-8"))
entries = data.setdefault("entries", [])
by_id = {entry.get("id"): entry for entry in entries}

specs = [
    {
        "id": "music-limonada-1992",
        "kind": "chapter",
        "domain": "music",
        "date": {"pt": "1992", "en": "1992"},
        "title": {
            "pt": "Destemidos Limonadas & Punkecas",
            "en": "Destemidos Limonadas & Punkecas"
        },
        "summary": {
            "pt": "Em 1992, o encontro de Marcelo Nicchio com Roberto Sassano, o Roberto Limonada, aproximou amizade, punk rock, televisão e repertório: do posto Esso da Brás Leme e dos Destemidos Limonadas & Punkecas ao Jô Soares Onze e Meia, TV Cultura, Kid Vinil e uma relação que continuaria nos anos seguintes.",
            "en": "In 1992, Marcelo Nicchio's encounter with Roberto Sassano, Roberto Limonada, brought friendship, punk rock, television and repertoire together: from the Esso station on Brás Leme and Destemidos Limonadas & Punkecas to Jô Soares Onze e Meia, TV Cultura, Kid Vinil and a relationship that continued in the following years."
        },
        "topic_ids": [],
        "media": {
            "galleries": ["destemidos-limonadas-1992"]
        },
        "reader_scope": "biography-only",
        "reader_presentation": {"state": "always-open"},
        "source": {"kind": "reader-section"},
        "reader_targets": {
            "pt": [{"path": "pt/biografia/index.html", "selector": "#bio-music-limonada-1992"}],
            "en": [{"path": "en/biography/index.html", "selector": "#bio-music-limonada-1992"}]
        },
        "chapter_page": {"status": "none", "indexing": "none"}
    },
    {
        "id": "music-kid-vinil-1993",
        "kind": "chapter",
        "domain": "music",
        "date": {"pt": "1993", "en": "1993"},
        "title": {
            "pt": "Kid Vinil & Verminose — Café Piu Piu",
            "en": "Kid Vinil & Verminose — Café Piu Piu"
        },
        "summary": {
            "pt": "Em 1993, a passagem pelo Café Piu Piu e o contato com Kid Vinil e Verminose marcaram um rito de passagem do Coitado do Próximo no circuito paulistano, conectando palco, camarim, repertório e a circulação daquela cena pela televisão e pelos discos.",
            "en": "In 1993, the Café Piu Piu episode and contact with Kid Vinil and Verminose marked a rite of passage for Coitado do Próximo in São Paulo's circuit, connecting stage, backstage, repertoire and the circulation of that scene through television and records."
        },
        "topic_ids": [],
        "reader_scope": "biography-only",
        "reader_presentation": {"state": "always-open"},
        "source": {"kind": "reader-section"},
        "reader_targets": {
            "pt": [{"path": "pt/biografia/index.html", "selector": "#bio-music-kid-vinil-1993"}],
            "en": [{"path": "en/biography/index.html", "selector": "#bio-music-kid-vinil-1993"}]
        },
        "chapter_page": {"status": "none", "indexing": "none"}
    },
    {
        "id": "music-coitado-1994",
        "kind": "chapter",
        "domain": "music",
        "date": {"pt": "1994", "en": "1994"},
        "title": {
            "pt": "Kid Vinil na 97FM Rock",
            "en": "Kid Vinil on 97FM Rock"
        },
        "summary": {
            "pt": "Em 1994, Roberto Limonada levou Marcelo Nicchio à 97FM Rock e o apresentou a Kid Vinil. O Coitado do Próximo levou sua primeira demo, ouviu “Mulher SP” tocar no rádio e ainda faria uma segunda passagem pelo programa, sem convite, com Mirão/365 e uma versão acústica de “Pegue o Seu Celular”.",
            "en": "In 1994, Roberto Limonada took Marcelo Nicchio to 97FM Rock and introduced him to Kid Vinil. Coitado do Próximo brought its first demo, heard “Mulher SP” played on the radio and would later make a second appearance, uninvited, with Mirão/365 and an acoustic version of “Pegue o Seu Celular”."
        },
        "topic_ids": [],
        "reader_scope": "biography-only",
        "reader_presentation": {"state": "always-open"},
        "source": {"kind": "reader-section"},
        "reader_targets": {
            "pt": [{"path": "pt/biografia/index.html", "selector": "#bio-music-coitado-1994"}],
            "en": [{"path": "en/biography/index.html", "selector": "#bio-music-coitado-1994"}]
        },
        "chapter_page": {"status": "none", "indexing": "none"}
    }
]

for spec in specs:
    existing = by_id.get(spec["id"])
    if existing is None:
        entries.append(spec)
        by_id[spec["id"]] = spec
        continue
    # Preserve unrelated future metadata, but remove preview fields that can become
    # invalid after narrowing this registry entry to the Full Biography surface.
    existing.pop("reader_preview_paths", None)
    existing.pop("reader_preview", None)
    existing.update(spec)

PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Three music posts locked as always-open in Full Biography.")
