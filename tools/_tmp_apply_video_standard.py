#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str, label: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: {label}: expected 1 exact match, got {count}")
    write(path, text.replace(old, new, 1))


def replace_segment(path: str, start: str, end: str, new: str, label: str) -> None:
    text = read(path)
    i = text.find(start)
    if i < 0:
        raise RuntimeError(f"{path}: {label}: start marker not found")
    j = text.find(end, i)
    if j < 0:
        raise RuntimeError(f"{path}: {label}: end marker not found")
    write(path, text[:i] + new + text[j:])


def replace_evidence_div(path: str, href: str, new: str, label: str) -> None:
    text = read(path)
    pattern = re.compile(
        r'<div class="evidence-links inline-links">(?:(?!</div>).)*?href="'
        + re.escape(href)
        + r'"(?:(?!</div>).)*?</div>',
        flags=re.S,
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{path}: {label}: expected 1 media div for {href}, got {len(matches)}")
    m = matches[0]
    write(path, text[:m.start()] + new + text[m.end():])


def video_block(lang: str, block_id: str, context: str, groups: list[dict], count: int | None = None) -> str:
    total = count if count is not None else sum(len(g["links"]) for g in groups)
    header = "Vídeos &amp; Mídia" if lang == "pt" else "Videos &amp; Media"
    aria = "Vídeos e mídia" if lang == "pt" else "Videos and media"
    lines = [
        f'<div class="video-library" aria-label="{aria}" aria-labelledby="{block_id}">',
        '  <div class="video-library__head">',
        f'    <strong id="{block_id}">{header} · {total}</strong>',
        f'    <span>{escape(context)}</span>',
        '  </div>',
    ]
    for g in groups:
        cls = "video-library__group video-library__group--primary" if g.get("primary") else "video-library__group"
        lines.append(f'  <div class="{cls}">')
        lines.append(f'    <div class="video-library__label"><strong>{escape(g["title"])}</strong></div>')
        lines.append(f'    <p class="video-library__description">{escape(g["description"])}</p>')
        lines.append('    <div class="video-library__actions">')
        anchors = []
        for idx, (href, label) in enumerate(g["links"]):
            primary = ' video-pill--primary' if g.get("primary") and idx == 0 else ''
            anchors.append(
                f'<a class="video-pill{primary}" href="{escape(href, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)}</a>'
            )
        lines.append('      ' + ''.join(anchors))
        lines.append('    </div>')
        lines.append('  </div>')
    lines.append('</div>')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CSS: keep the approved Jô component, add description copy, remove URL-based
# white-pill styling. No layout/chapter/grid selectors are changed here.
# ---------------------------------------------------------------------------
css_path = "styles.css"
css = read(css_path)
old_pattern = re.compile(
    r'\n/\* High-contrast video action buttons \*/.*?(?=\n/\* Music / Coitado do Próximo: major-entry hierarchy)',
    flags=re.S,
)
css, removed = old_pattern.subn("\n", css, count=1)
if removed != 1:
    raise RuntimeError(f"{css_path}: expected to remove exactly one legacy high-contrast video block, got {removed}")
needle = '.video-library__label strong{font-size:.69rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent-soft);font-weight:820}\n'
if needle not in css:
    raise RuntimeError("styles.css: video-library label rule not found")
description_rule = (
    '.video-library .video-library__description{margin:6px 0 9px!important;max-width:72ch;'
    'color:var(--muted)!important;font-size:.84rem!important;line-height:1.48!important}\n'
    '.evidence-list>.video-library{margin:0}\n'
)
css = css.replace(needle, needle + description_rule, 1)
write(css_path, css)

# ---------------------------------------------------------------------------
# Fragment-backed entries: edit the neutral source, then sync downstream.
# ---------------------------------------------------------------------------
pt_limonada = "content/entries/pt/music-limonada-1992.inc"
en_limonada = "content/entries/en/music-limonada-1992.inc"

replace_evidence_div(
    pt_limonada,
    "https://www.youtube.com/watch?v=_LBHqq8xF1c",
    video_block("pt", "limonada-posto-videos", "TV Cultura · São Paulo", [{
        "title": "O Posto",
        "description": "Registro dos Destemidos Limonadas & Punkecas apresentando “O Posto” na TV Cultura.",
        "links": [("https://www.youtube.com/watch?v=_LBHqq8xF1c", "O Posto")],
    }]),
    "Destemidos O Posto",
)
replace_evidence_div(
    en_limonada,
    "https://www.youtube.com/watch?v=_LBHqq8xF1c",
    video_block("en", "limonada-posto-videos", "TV Cultura · São Paulo", [{
        "title": "O Posto",
        "description": "Record of Destemidos Limonadas & Punkecas performing “O Posto” on TV Cultura.",
        "links": [("https://www.youtube.com/watch?v=_LBHqq8xF1c", "O Posto")],
    }]),
    "Destemidos O Posto EN",
)
replace_evidence_div(
    pt_limonada,
    "https://www.youtube.com/watch?v=giklH5greAc",
    video_block("pt", "limonada-jo-pizza-videos", "Jô Soares Onze e Meia · SBT · jun. 1992", [{
        "title": "Apresentação no Jô",
        "description": "Registro ao vivo de “Ela Só Gosta de Pizza” durante a passagem dos Destemidos pelo programa.",
        "links": [("https://www.youtube.com/watch?v=giklH5greAc", "Ela Só Gosta de Pizza")],
    }]),
    "Destemidos Pizza",
)
replace_evidence_div(
    en_limonada,
    "https://www.youtube.com/watch?v=giklH5greAc",
    video_block("en", "limonada-jo-pizza-videos", "Jô Soares Onze e Meia · SBT · Jun. 1992", [{
        "title": "Performance on Jô",
        "description": "Live record of “Ela Só Gosta de Pizza” during the Destemidos appearance on the program.",
        "links": [("https://www.youtube.com/watch?v=giklH5greAc", "Ela Só Gosta de Pizza")],
    }]),
    "Destemidos Pizza EN",
)
replace_evidence_div(
    pt_limonada,
    "https://www.youtube.com/watch?v=OUBzN8HYuVA",
    video_block("pt", "limonada-jo-archive-videos", "Jô Soares Onze e Meia · SBT · jun. 1992", [
        {
            "title": "Entrevista",
            "description": "Entrevista dos Destemidos preservada em duas partes.",
            "links": [
                ("https://www.youtube.com/watch?v=OUBzN8HYuVA", "Parte 1"),
                ("https://www.youtube.com/watch?v=PyTBtNAU3RE", "Parte 2"),
            ],
        },
        {
            "title": "Participação de Kid Vinil",
            "description": "Registro de “Herói do Brasil” com participação especial de Kid Vinil.",
            "links": [("https://www.youtube.com/watch?v=wzsS-G6ywqc", "Herói do Brasil")],
        },
    ]),
    "Destemidos final archive",
)
replace_evidence_div(
    en_limonada,
    "https://www.youtube.com/watch?v=OUBzN8HYuVA",
    video_block("en", "limonada-jo-archive-videos", "Jô Soares Onze e Meia · SBT · Jun. 1992", [
        {
            "title": "Interview",
            "description": "The Destemidos interview preserved in two parts.",
            "links": [
                ("https://www.youtube.com/watch?v=OUBzN8HYuVA", "Part 1"),
                ("https://www.youtube.com/watch?v=PyTBtNAU3RE", "Part 2"),
            ],
        },
        {
            "title": "Featuring Kid Vinil",
            "description": "Record of “Herói do Brasil” featuring Kid Vinil.",
            "links": [("https://www.youtube.com/watch?v=wzsS-G6ywqc", "Herói do Brasil")],
        },
    ]),
    "Destemidos final archive EN",
)

# Meia-Noite e Uns: replace only the existing media component, not the post.
pt_meia = "content/entries/pt/communication-meia-noite.inc"
en_meia = "content/entries/en/communication-meia-noite.inc"
pt_meia_block = video_block("pt", "meia-noite-video-title", "Meia-Noite e Uns · RedeTV! · 2006", [
    {
        "title": "Programa preservado",
        "description": "Três blocos preservados do programa exibido pela RedeTV!.",
        "links": [
            ("https://www.youtube.com/watch?v=kLQAlzgwmy0", "Bloco 1"),
            ("https://www.youtube.com/watch?v=f-JZfMoHh1I", "Bloco 2"),
            ("https://www.youtube.com/watch?v=6s6843Mq5MA", "Bloco 3"),
        ],
    },
    {
        "title": "Vinheta e créditos",
        "description": "Vinheta completa com os créditos de Direção Artística e Produção Executiva.",
        "links": [("https://www.youtube.com/watch?v=tIGlLDpzQ7E", "Vinheta e créditos")],
    },
])
en_meia_block = video_block("en", "meia-noite-video-title", "Meia-Noite e Uns · RedeTV! · 2006", [
    {
        "title": "Preserved program",
        "description": "Three preserved blocks from the program broadcast by RedeTV!.",
        "links": [
            ("https://www.youtube.com/watch?v=kLQAlzgwmy0", "Block 1"),
            ("https://www.youtube.com/watch?v=f-JZfMoHh1I", "Block 2"),
            ("https://www.youtube.com/watch?v=6s6843Mq5MA", "Block 3"),
        ],
    },
    {
        "title": "Title sequence & credits",
        "description": "Complete title sequence with Artistic Direction and Executive Production credits.",
        "links": [("https://www.youtube.com/watch?v=tIGlLDpzQ7E", "Title sequence & credits")],
    },
])
replace_segment(pt_meia, '<div aria-label="Vídeos preservados de Meia-Noite e Uns" class="record-media-block">', '<!-- gallery:meia-noite-e-uns:start -->', pt_meia_block, "Meia-Noite media block")
replace_segment(en_meia, '<div aria-label="Preserved Meia-Noite e Uns videos" class="record-media-block">', '<!-- gallery:meia-noite-e-uns:start -->', en_meia_block, "Meia-Noite media block EN")

# BEST/Kenshoo: consolidate four repeated evidence cards into one audiovisual library.
pt_best = "content/entries/pt/internet-best.inc"
en_best = "content/entries/en/internet-best.inc"
pt_best_block = video_block("pt", "best-workshop-video-title", "E-Commerce Brasil · 11 nov. 2014", [{
    "title": "Segmentações Avançadas em Search",
    "description": "Gravação integral do workshop preservada em quatro partes.",
    "links": [
        ("https://youtu.be/p-1Uc-zD4TE", "Parte 1"),
        ("https://youtu.be/hOKqH6yxQ4g", "Parte 2"),
        ("https://youtu.be/C1Z3wD8t03A", "Parte 3"),
        ("https://youtu.be/3h-z53IN6AI", "Parte 4"),
    ],
}])
en_best_block = video_block("en", "best-workshop-video-title", "E-Commerce Brasil · Nov. 11, 2014", [{
    "title": "Advanced Segmentation in Search",
    "description": "The complete workshop recording preserved in four parts.",
    "links": [
        ("https://youtu.be/p-1Uc-zD4TE", "Part 1"),
        ("https://youtu.be/hOKqH6yxQ4g", "Part 2"),
        ("https://youtu.be/C1Z3wD8t03A", "Part 3"),
        ("https://youtu.be/3h-z53IN6AI", "Part 4"),
    ],
}])
replace_segment(pt_best, '<div class="evidence-list">\n<div class="evidence"><div class="evidence-top"><strong>Workshop Search', '<p>No dia seguinte', pt_best_block + '\n', "BEST workshop media")
replace_segment(en_best, '<div class="evidence-list">\n<div class="evidence"><div class="evidence-top"><strong>Search workshop', '<p>The following day', en_best_block + '\n', "BEST workshop media EN")

# ---------------------------------------------------------------------------
# Music vertical: only non-fragment legacy audiovisual links + descriptions in
# the already-approved Programa do Jô component. Fragment-backed sections are
# populated by sync_entries after this script.
# ---------------------------------------------------------------------------
pt_music = "pt/musica/index.html"
en_music = "en/music/index.html"

music_replacements = [
    (
        "https://www.youtube.com/watch?v=ZOukRoPC87I",
        video_block("pt", "music-origins-video-title", "Mocidade Alegre · 4 fev. 1989", [{
            "title": "Primeiro desfile preservado",
            "description": "Registro audiovisual do desfile na Avenida Tiradentes, em São Paulo.",
            "links": [("https://www.youtube.com/watch?v=ZOukRoPC87I", "Assistir desfile")],
        }]),
        video_block("en", "music-origins-video-title", "Mocidade Alegre · Feb. 4, 1989", [{
            "title": "First preserved parade",
            "description": "Audiovisual record of the parade on Avenida Tiradentes in São Paulo.",
            "links": [("https://www.youtube.com/watch?v=ZOukRoPC87I", "Watch parade")],
        }]),
        "Mocidade Alegre",
    ),
    (
        "https://www.youtube.com/watch?v=7yjYTV1L0b0",
        video_block("pt", "music-first-show-video-title", "Coitado do Próximo · 5 jul. 1992", [{
            "title": "Primeiro show",
            "description": "Registro original em vídeo do primeiro show preservado da banda.",
            "links": [("https://www.youtube.com/watch?v=7yjYTV1L0b0", "Vídeo original")],
        }]),
        video_block("en", "music-first-show-video-title", "Coitado do Próximo · Jul. 5, 1992", [{
            "title": "First show",
            "description": "Original video record of the band's earliest preserved show.",
            "links": [("https://www.youtube.com/watch?v=7yjYTV1L0b0", "Original video")],
        }]),
        "first show",
    ),
    (
        "https://youtu.be/He7KvTtB-lg?si=8EAdyPQRLOETE_y6",
        video_block("pt", "music-demo-video-title", "Estúdio Anonimato · 1994", [{
            "title": "Sessões da primeira demo",
            "description": "Trecho remanescente em vídeo das gravações da primeira demo-tape.",
            "links": [("https://youtu.be/He7KvTtB-lg?si=8EAdyPQRLOETE_y6", "Filmagem remanescente")],
        }]),
        video_block("en", "music-demo-video-title", "Estúdio Anonimato · 1994", [{
            "title": "First demo sessions",
            "description": "Surviving video excerpt from the recording sessions for the first demo tape.",
            "links": [("https://youtu.be/He7KvTtB-lg?si=8EAdyPQRLOETE_y6", "Surviving footage")],
        }]),
        "demo tape",
    ),
    (
        "https://youtu.be/ps1XJkvd4Qo?si=ckbe6fUHM0s4q5Kw",
        video_block("pt", "music-etesp-video-title", "São Paulo · jun. 2000", [{
            "title": "Apresentação ao vivo",
            "description": "Passagem de som e duas músicas ao vivo preservadas no mesmo registro.",
            "links": [("https://youtu.be/ps1XJkvd4Qo?si=ckbe6fUHM0s4q5Kw", "Assistir registro")],
        }]),
        video_block("en", "music-etesp-video-title", "São Paulo · Jun. 2000", [{
            "title": "Live performance",
            "description": "Soundcheck and two live songs preserved in the same recording.",
            "links": [("https://youtu.be/ps1XJkvd4Qo?si=ckbe6fUHM0s4q5Kw", "Watch record")],
        }]),
        "ETESP/FATEC",
    ),
    (
        "https://www.youtube.com/watch?v=V624sY_rl8I",
        video_block("pt", "music-olympia-video-title", "Olympia · 25 jun. 2000", [{
            "title": "Abertura dos Paralamas do Sucesso",
            "description": "Dois registros preservados da apresentação do Coitado do Próximo no Olympia.",
            "links": [
                ("https://www.youtube.com/watch?v=V624sY_rl8I", "Estava Comigo"),
                ("https://youtu.be/0-RXucDYMfk", "Ciúmes"),
            ],
        }]),
        video_block("en", "music-olympia-video-title", "Olympia · Jun. 25, 2000", [{
            "title": "Opening for Os Paralamas do Sucesso",
            "description": "Two surviving records of Coitado do Próximo's performance at Olympia.",
            "links": [
                ("https://www.youtube.com/watch?v=V624sY_rl8I", "Estava Comigo"),
                ("https://youtu.be/0-RXucDYMfk", "Ciúmes"),
            ],
        }]),
        "Olympia",
    ),
]
for href, pt_block, en_block, label in music_replacements:
    replace_evidence_div(pt_music, href, pt_block, f"Music PT {label}")
    # Olympia never had the second link in EN before; match only if the first link exists.
    replace_evidence_div(en_music, href, en_block, f"Music EN {label}")

# Add descriptions to the Jô component without changing its established structure.
jo_pt = {
    "Apresentação exibida na Globo": "Registro principal da participação, com “Estava Comigo”, exibido pela Rede Globo.",
    "Bastidores": "Cinco registros dos bastidores do Programa do Jô.",
    "Passagem de som": "Três músicas registradas durante a passagem de som.",
}
jo_en = {
    "Broadcast performance": "Main record of the appearance, featuring “Estava Comigo”, broadcast by Rede Globo.",
    "Behind the scenes": "Five preserved behind-the-scenes records from Programa do Jô.",
    "Soundcheck": "Three songs recorded during the soundcheck.",
}
for title, desc in jo_pt.items():
    old = f'<div class="video-library__label"><strong>{title}</strong></div>\n    <div class="video-library__actions">'
    new = f'<div class="video-library__label"><strong>{title}</strong></div>\n    <p class="video-library__description">{desc}</p>\n    <div class="video-library__actions">'
    replace_once(pt_music, old, new, f"Jô description {title}")
for title, desc in jo_en.items():
    old = f'<div class="video-library__label"><strong>{title}</strong></div>\n    <div class="video-library__actions">'
    new = f'<div class="video-library__label"><strong>{title}</strong></div>\n    <p class="video-library__description">{desc}</p>\n    <div class="video-library__actions">'
    replace_once(en_music, old, new, f"Jô EN description {title}")

# ---------------------------------------------------------------------------
# Archive: replace the four audiovisual evidence cards with the same visual
# language. Non-video evidence cards remain untouched.
# ---------------------------------------------------------------------------
pt_archive = "pt/arquivo/index.html"
en_archive = "en/archive/index.html"
archive_pt = [
    (
        '<div class="evidence"><div class="evidence-top"><strong>Coitado do Próximo — Olympia, 2000</strong><span class="status">vídeo</span></div><p>Dois registros da apresentação: “Estava Comigo” e “Ciúmes”.</p><div class="evidence-links"><a href="https://www.youtube.com/watch?v=V624sY_rl8I" target="_blank" rel="noopener noreferrer">Estava Comigo</a><a href="https://youtu.be/0-RXucDYMfk" target="_blank" rel="noopener noreferrer">Ciúmes</a></div></div>',
        video_block("pt", "archive-olympia-video-title", "Coitado do Próximo · Olympia · 2000", [{
            "title": "Apresentação ao vivo",
            "description": "Dois registros preservados da apresentação: “Estava Comigo” e “Ciúmes”.",
            "links": [("https://www.youtube.com/watch?v=V624sY_rl8I", "Estava Comigo"), ("https://youtu.be/0-RXucDYMfk", "Ciúmes")],
        }]),
    ),
    (
        '<div class="evidence"><div class="evidence-top"><strong>Programa do Jô — 21 jun. 2001</strong><span class="status">vídeo</span></div><p>Coitado do Próximo apresenta “Estava Comigo” na Rede Globo.</p><div class="evidence-links"><a href="https://www.youtube.com/watch?v=4NKHy_C8wsI&t=8s" target="_blank" rel="noopener noreferrer">YouTube</a></div></div>',
        video_block("pt", "archive-jo-video-title", "Programa do Jô · 21 jun. 2001", [{
            "title": "Apresentação na Rede Globo",
            "description": "Coitado do Próximo apresenta “Estava Comigo” no programa.",
            "links": [("https://www.youtube.com/watch?v=4NKHy_C8wsI&t=8s", "Estava Comigo")],
        }]),
    ),
    (
        '<div class="evidence"><div class="evidence-top"><strong>Meia-Noite e Uns — RedeTV!, 2006</strong><span class="status">vídeo/créditos</span></div><p>Três blocos do programa e vinheta completa com créditos de Direção Artística e Produção Executiva.</p><div class="evidence-links"><a href="https://www.youtube.com/watch?v=kLQAlzgwmy0" target="_blank" rel="noopener noreferrer">Bloco 1</a><a href="https://www.youtube.com/watch?v=f-JZfMoHh1I" target="_blank" rel="noopener noreferrer">Bloco 2</a><a href="https://www.youtube.com/watch?v=6s6843Mq5MA" target="_blank" rel="noopener noreferrer">Bloco 3</a><a href="https://www.youtube.com/watch?v=tIGlLDpzQ7E" target="_blank" rel="noopener noreferrer">Créditos</a></div></div>',
        video_block("pt", "archive-meia-noite-video-title", "Meia-Noite e Uns · RedeTV! · 2006", [
            {"title": "Programa preservado", "description": "Três blocos preservados do programa.", "links": [("https://www.youtube.com/watch?v=kLQAlzgwmy0", "Bloco 1"), ("https://www.youtube.com/watch?v=f-JZfMoHh1I", "Bloco 2"), ("https://www.youtube.com/watch?v=6s6843Mq5MA", "Bloco 3")]},
            {"title": "Vinheta e créditos", "description": "Vinheta completa com créditos de Direção Artística e Produção Executiva.", "links": [("https://www.youtube.com/watch?v=tIGlLDpzQ7E", "Vinheta e créditos")]},
        ]),
    ),
    (
        '<div class="evidence"><div class="evidence-top"><strong>Workshop Search & Social — E-Commerce Brasil</strong><span class="status">vídeo</span></div><p>Série em quatro partes com Marcelo Nicchio ministrando conteúdo de segmentação avançada.</p><div class="evidence-links"><a href="https://youtu.be/p-1Uc-zD4TE" target="_blank" rel="noopener noreferrer">1/4</a><a href="https://youtu.be/hOKqH6yxQ4g" target="_blank" rel="noopener noreferrer">2/4</a><a href="https://youtu.be/C1Z3wD8t03A" target="_blank" rel="noopener noreferrer">3/4</a><a href="https://youtu.be/3h-z53IN6AI" target="_blank" rel="noopener noreferrer">4/4</a></div></div>',
        video_block("pt", "archive-best-video-title", "E-Commerce Brasil · 2014", [{"title": "Workshop Search & Social", "description": "Série em quatro partes com Marcelo Nicchio ministrando conteúdo de segmentação avançada.", "links": [("https://youtu.be/p-1Uc-zD4TE", "Parte 1"), ("https://youtu.be/hOKqH6yxQ4g", "Parte 2"), ("https://youtu.be/C1Z3wD8t03A", "Parte 3"), ("https://youtu.be/3h-z53IN6AI", "Parte 4")]}]),
    ),
]
archive_en = [
    (
        '<div class="evidence"><div class="evidence-top"><strong>Coitado do Próximo — Olympia, 2000</strong><span class="status">video</span></div><p>Two surviving records of the performance: “Estava Comigo” and “Ciúmes”.</p><div class="evidence-links"><a href="https://www.youtube.com/watch?v=V624sY_rl8I" target="_blank" rel="noopener noreferrer">Estava Comigo</a><a href="https://youtu.be/0-RXucDYMfk" target="_blank" rel="noopener noreferrer">Ciúmes</a></div></div>',
        video_block("en", "archive-olympia-video-title", "Coitado do Próximo · Olympia · 2000", [{"title": "Live performance", "description": "Two surviving records of the performance: “Estava Comigo” and “Ciúmes”.", "links": [("https://www.youtube.com/watch?v=V624sY_rl8I", "Estava Comigo"), ("https://youtu.be/0-RXucDYMfk", "Ciúmes")]}]),
    ),
    (
        '<div class="evidence"><div class="evidence-top"><strong>Programa do Jô — Jun. 21, 2001</strong><span class="status">video</span></div><p>Coitado do Próximo performs “Estava Comigo” on Rede Globo.</p><div class="evidence-links"><a href="https://www.youtube.com/watch?v=4NKHy_C8wsI&t=8s" target="_blank" rel="noopener noreferrer">YouTube</a></div></div>',
        video_block("en", "archive-jo-video-title", "Programa do Jô · Jun. 21, 2001", [{"title": "Rede Globo performance", "description": "Coitado do Próximo performs “Estava Comigo” on the program.", "links": [("https://www.youtube.com/watch?v=4NKHy_C8wsI&t=8s", "Estava Comigo")]}]),
    ),
    (
        '<div class="evidence"><div class="evidence-top"><strong>Meia-Noite e Uns — RedeTV!, 2006</strong><span class="status">video/credits</span></div><p>Three program blocks and the full title sequence with Artistic Direction and Executive Production credits.</p><div class="evidence-links"><a href="https://www.youtube.com/watch?v=kLQAlzgwmy0" target="_blank" rel="noopener noreferrer">Block 1</a><a href="https://www.youtube.com/watch?v=f-JZfMoHh1I" target="_blank" rel="noopener noreferrer">Block 2</a><a href="https://www.youtube.com/watch?v=6s6843Mq5MA" target="_blank" rel="noopener noreferrer">Block 3</a><a href="https://www.youtube.com/watch?v=tIGlLDpzQ7E" target="_blank" rel="noopener noreferrer">Credits</a></div></div>',
        video_block("en", "archive-meia-noite-video-title", "Meia-Noite e Uns · RedeTV! · 2006", [
            {"title": "Preserved program", "description": "Three preserved blocks from the program.", "links": [("https://www.youtube.com/watch?v=kLQAlzgwmy0", "Block 1"), ("https://www.youtube.com/watch?v=f-JZfMoHh1I", "Block 2"), ("https://www.youtube.com/watch?v=6s6843Mq5MA", "Block 3")]},
            {"title": "Title sequence & credits", "description": "Full title sequence with Artistic Direction and Executive Production credits.", "links": [("https://www.youtube.com/watch?v=tIGlLDpzQ7E", "Title sequence & credits")]},
        ]),
    ),
    (
        '<div class="evidence"><div class="evidence-top"><strong>Search & Social Workshop — E-Commerce Brasil</strong><span class="status">video</span></div><p>Four-part series documenting Marcelo Nicchio teaching advanced segmentation content.</p><div class="evidence-links"><a href="https://youtu.be/p-1Uc-zD4TE" target="_blank" rel="noopener noreferrer">1/4</a><a href="https://youtu.be/hOKqH6yxQ4g" target="_blank" rel="noopener noreferrer">2/4</a><a href="https://youtu.be/C1Z3wD8t03A" target="_blank" rel="noopener noreferrer">3/4</a><a href="https://youtu.be/3h-z53IN6AI" target="_blank" rel="noopener noreferrer">4/4</a></div></div>',
        video_block("en", "archive-best-video-title", "E-Commerce Brasil · 2014", [{"title": "Search & Social workshop", "description": "Four-part series documenting Marcelo Nicchio teaching advanced segmentation content.", "links": [("https://youtu.be/p-1Uc-zD4TE", "Part 1"), ("https://youtu.be/hOKqH6yxQ4g", "Part 2"), ("https://youtu.be/C1Z3wD8t03A", "Part 3"), ("https://youtu.be/3h-z53IN6AI", "Part 4")]}]),
    ),
]
for i, (old, new) in enumerate(archive_pt, 1):
    replace_once(pt_archive, old, new, f"archive PT video block {i}")
for i, (old, new) in enumerate(archive_en, 1):
    replace_once(en_archive, old, new, f"archive EN video block {i}")

# Safety guard: this migration must never introduce vertical layout classes in Bio.
for path in ("pt/biografia/index.html", "en/biography/index.html"):
    before = read(path)
    if 'class="phase music-entry chapter bio-entry"' in before:
        raise RuntimeError(f"{path}: unsafe vertical classes already present before synchronization")

print("Video/media standard source migration applied successfully.")
