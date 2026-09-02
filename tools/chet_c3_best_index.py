#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data/entries.json"
PT = ROOT / "content/entries/pt/internet-best.inc"
EN = ROOT / "content/entries/en/internet-best.inc"
SITEMAP = ROOT / "sitemap.xml"
AUDIT = ROOT / "tools/audit_site.py"


def patch_fragments() -> None:
    pt = PT.read_text(encoding="utf-8")
    old_pt_intro = '<p>Em 2014, Nicchio atuou como <strong>Gerente de Performance</strong> na BEST, em uma operação ligada à plataforma Kenshoo no Brasil. O trabalho envolvia onboarding da ferramenta e otimização de campanhas de mídia para grandes varejistas.</p>\n'
    new_pt_intro = old_pt_intro + '<p>Na prática, esse ciclo aproximava duas frentes que aparecem juntas no trabalho de performance: a adoção da tecnologia e a operação cotidiana das campanhas. O onboarding da Kenshoo fazia parte da mesma rotina em que Search e Social eram acompanhados e otimizados para contas de grande porte, colocando plataforma, mídia e desempenho dentro de um único fluxo de trabalho.</p>\n'
    if old_pt_intro not in pt:
        raise RuntimeError('BEST PT intro not found')
    pt = pt.replace(old_pt_intro, new_pt_intro, 1)
    old_pt_workshop = '<p>Nesse período ministrou para o E-Commerce Brasil um workshop sobre <strong>Segmentação Avançada em Search e Social</strong>. A gravação preservada está dividida em quatro partes.</p>\n'
    new_pt_workshop = '<p>Nesse período ministrou para o E-Commerce Brasil um workshop sobre <strong>Segmentação Avançada em Search e Social</strong>. O registro preserva uma amostra direta do repertório profissional daquele ciclo — segmentação, Search, Social e tecnologia aplicada à operação de mídia — e a gravação está dividida em quatro partes.</p>\n'
    if old_pt_workshop not in pt:
        raise RuntimeError('BEST PT workshop paragraph not found')
    pt = pt.replace(old_pt_workshop, new_pt_workshop, 1)
    marker = '<!-- gallery:best-kenshoo:start -->\n'
    extra_pt = '<p>Além dos vídeos, o arquivo visual reúne 11 registros do período, incluindo fotografias do workshop, cartão profissional, imagens do escritório e outros registros da operação. O conjunto ajuda a situar visualmente uma etapa curta, mas representativa, da trajetória em Performance.</p>\n'
    if marker not in pt:
        raise RuntimeError('BEST PT gallery marker not found')
    pt = pt.replace(marker, extra_pt + marker, 1)
    PT.write_text(pt, encoding="utf-8")

    en = EN.read_text(encoding="utf-8")
    old_en_intro = '<p>In 2014, Nicchio worked as a <strong>Performance Manager</strong> at BEST, in an operation connected to the Kenshoo platform in Brazil. His work involved platform onboarding and media-campaign optimization for major retailers.</p>\n'
    new_en_intro = old_en_intro + '<p>In practice, this period brought together two fronts that operate side by side in performance work: technology adoption and day-to-day campaign management. Kenshoo onboarding was part of the same routine in which Search and Social were monitored and optimized for large accounts, placing platform, media and performance within a single operating flow.</p>\n'
    if old_en_intro not in en:
        raise RuntimeError('BEST EN intro not found')
    en = en.replace(old_en_intro, new_en_intro, 1)
    old_en_workshop = '<p>During this period he taught an E-Commerce Brasil workshop on <strong>Advanced Segmentation in Search and Social</strong>. The surviving recording is divided into four parts.</p>\n'
    new_en_workshop = '<p>During this period he taught an E-Commerce Brasil workshop on <strong>Advanced Segmentation in Search and Social</strong>. The surviving record provides a direct sample of the professional repertoire of that period — segmentation, Search, Social and technology applied to media operations — and the recording is divided into four parts.</p>\n'
    if old_en_workshop not in en:
        raise RuntimeError('BEST EN workshop paragraph not found')
    en = en.replace(old_en_workshop, new_en_workshop, 1)
    extra_en = '<p>Beyond the videos, the visual archive contains 11 records from the period, including workshop photographs, a business card, office images and other records from the operation. Together they provide visual context for a short but representative stage in the Performance trajectory.</p>\n'
    if marker not in en:
        raise RuntimeError('BEST EN gallery marker not found')
    en = en.replace(marker, extra_en + marker, 1)
    EN.write_text(en, encoding="utf-8")


def patch_registry() -> None:
    data = json.loads(ENTRIES.read_text(encoding="utf-8"))
    entry = next(item for item in data["entries"] if item.get("id") == "internet-best")
    page = entry["chapter_page"]
    if page.get("status") != "pilot":
        raise RuntimeError('BEST is not a Chapter Page pilot')
    page["indexing"] = "index,follow"
    ENTRIES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_sitemap() -> None:
    text = SITEMAP.read_text(encoding="utf-8")
    urls = [
        'https://marcelonicchio.github.io/pt/internet/best-kenshoo/',
        'https://marcelonicchio.github.io/en/internet/best-kenshoo/',
    ]
    if any(url in text for url in urls):
        raise RuntimeError('BEST URL already present in sitemap')
    block = ''.join(f'  <url>\n    <loc>{url}</loc>\n  </url>\n' for url in urls)
    SITEMAP.write_text(text.replace('</urlset>\n', block + '</urlset>\n', 1), encoding="utf-8")


def patch_audit() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    old = '    "pt/ia-hai/index.html",\n    "en/ai-hai/index.html",\n}'
    new = '    "pt/ia-hai/index.html",\n    "en/ai-hai/index.html",\n    "pt/internet/best-kenshoo/index.html",\n    "en/internet/best-kenshoo/index.html",\n}'
    if old not in text:
        raise RuntimeError('LAUNCH_INDEXABLE anchor not found')
    AUDIT.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> int:
    patch_fragments()
    patch_registry()
    patch_sitemap()
    patch_audit()
    print('C3 applied: BEST copy strengthened and PT/EN Chapter Pages promoted to index,follow.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
