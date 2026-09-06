#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
GALLERIES = ROOT / "data/galleries.json"
ENTRIES = ROOT / "data/entries.json"
PT = ROOT / "content/entries/pt/internet-best.inc"
EN = ROOT / "content/entries/en/internet-best.inc"

GALLERY_ID = "best-kenshoo"
SOURCE_ROOT = ROOT / "assets/archive/internet/best-kenshoo"
DERIV_ROOT = ROOT / "assets/media/galleries/best-kenshoo"
PDF_HREF = "/assets/archive/internet/best-kenshoo/best08_workshop-facebook-ads-2014.pdf"


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add_gallery_items() -> None:
    data = json.loads(GALLERIES.read_text(encoding="utf-8"))
    gallery = next((g for g in data["galleries"] if g["id"] == GALLERY_ID), None)
    ensure(gallery is not None, "BEST/Kenshoo gallery not found")
    existing = {str(item["id"]) for item in gallery["items"]}
    additions = [
        {
            "id": "12",
            "source": "best07_postblog-facebook-ads-2014.jpg",
            "caption": {
                "pt": "BEST Blog — post de 14/11/2014 sobre o workshop ‘Facebook Ads: Melhores Práticas, Melhor Conversão’, realizado em 12/11/2014 no E-Commerce Brasil.",
                "en": "BEST Blog — November 14, 2014 post about the ‘Facebook Ads: Best Practices, Better Conversion’ workshop held on November 12, 2014 at E-Commerce Brasil."
            },
        },
        {
            "id": "13",
            "source": "best09_postblog-glossario-midia-online-2014.jpg",
            "caption": {
                "pt": "BEST Blog — ‘Conheça o Glossário da Mídia Online (ROI, CPC, CTR...) Parte 1’, publicado em 08/12/2014 e atribuído a Marcelo Nicchio, Gerente de Performance da BEST.",
                "en": "BEST Blog — ‘Online Media Glossary (ROI, CPC, CTR...) Part 1’, published on December 8, 2014 and attributed to Marcelo Nicchio, Performance Manager at BEST."
            },
        },
    ]
    for item in additions:
        if item["id"] not in existing:
            gallery["items"].append(item)
    DERIV_ROOT.mkdir(parents=True, exist_ok=True)
    for item in gallery["items"]:
        if str(item["id"]) not in {"12", "13"}:
            continue
        source = SOURCE_ROOT / item["source"]
        ensure(source.exists(), f"missing source {source}")
        with Image.open(source) as opened:
            image = ImageOps.exif_transpose(opened)
            sw, sh = image.size
            working = image.convert("RGB")
        item["width"] = sw
        item["height"] = sh
        item["derivatives"] = {}
        for profile in (480, 768):
            tw = min(sw, profile)
            th = max(1, round(sh * tw / sw))
            out = DERIV_ROOT / f"best-kenshoo-{item['id']}-{profile}.webp"
            resized = working if (tw, th) == (sw, sh) else working.resize((tw, th), Image.Resampling.LANCZOS)
            resized.save(out, "WEBP", quality=78, method=6, optimize=True)
            item["derivatives"][str(profile)] = {
                "path": out.relative_to(ROOT).as_posix(),
                "width": tw,
                "height": th,
            }
    GALLERIES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_entries_registry() -> None:
    data = json.loads(ENTRIES.read_text(encoding="utf-8"))
    entry = next((e for e in data["entries"] if e["id"] == "internet-best"), None)
    ensure(entry is not None, "internet-best registry entry not found")
    entry["summary"]["pt"] = (
        "Em 2014, Marcelo Nicchio atuou como Gerente de Performance na BEST/Kenshoo, combinando onboarding e otimização para grandes varejistas, dois workshops consecutivos no E-Commerce Brasil — Search e Facebook Ads — e produção técnica no BEST Blog."
    )
    entry["summary"]["en"] = (
        "In 2014, Marcelo Nicchio worked as Performance Manager at BEST/Kenshoo, combining platform onboarding and optimization for major retailers, two consecutive E-Commerce Brasil workshops — Search and Facebook Ads — and technical writing for the BEST Blog."
    )
    media = entry.setdefault("media", {})
    media["known_video_count"] = 4
    galleries = media.setdefault("galleries", [])
    if GALLERY_ID not in galleries:
        galleries.append(GALLERY_ID)
    page = entry.get("chapter_page", {})
    if page:
        page.setdefault("description", {})["pt"] = (
            "BEST/Kenshoo em 2014: performance, tecnologia, dois workshops no E-Commerce Brasil — Search e Facebook Ads —, vídeos, deck e registros do BEST Blog."
        )
        page.setdefault("description", {})["en"] = (
            "BEST/Kenshoo in 2014: performance, technology, two E-Commerce Brasil workshops — Search and Facebook Ads —, videos, deck and BEST Blog records."
        )
    ENTRIES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_fragment(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    if lang == "pt":
        old = '<p>Nesse período ministrou para o E-Commerce Brasil um workshop sobre <strong>Segmentação Avançada em Search e Social</strong>. O registro preserva uma amostra direta do repertório profissional daquele ciclo — segmentação, Search, Social e tecnologia aplicada à operação de mídia — e a gravação está dividida em quatro partes.</p>'
        new = '<p>Em <strong>11 de novembro de 2014, das 9h às 12h</strong>, ministrou no E-Commerce Brasil o workshop <strong>“Segmentações Avançadas em Search”</strong>. A gravação preservada está dividida em quatro partes e documenta diretamente o repertório profissional daquele ciclo em segmentação, Search, tecnologia e operação de mídia.</p>'
        ensure(old in text or new in text, "PT workshop paragraph anchor missing")
        text = text.replace(old, new)
        text = text.replace('<strong>Workshop — Parte 1/4</strong>', '<strong>Workshop Search · 11/11/2014 — Parte 1/4</strong>')
        text = text.replace('<strong>Parte 2/4 — Segmentação Avançada em Search e Social</strong>', '<strong>Parte 2/4 — Segmentações Avançadas em Search</strong>')
        insert_anchor = '</div>\n<p>Além dos vídeos, o arquivo visual reúne 11 registros do período, incluindo fotografias do workshop, cartão profissional, imagens do escritório e outros registros da operação. O conjunto ajuda a situar visualmente uma etapa curta, mas representativa, da trajetória em Performance.</p>'
        inserted = '</div>\n<p>No dia seguinte, <strong>12 de novembro de 2014, também das 9h às 12h</strong>, Nicchio ministrou no E-Commerce Brasil um segundo workshop, <strong>“Facebook Ads: Melhores Práticas, Melhor Conversão”</strong>. Um post contemporâneo recuperado do BEST Blog, publicado em 14/11/2014, registra o evento e o identifica como Gerente de Performance da BEST. A apresentação original preservada cobre objetivos de campanha, métricas, segmentação, Custom Audiences, Lookalike Audiences, Website Custom Audiences e pixel de conversão.</p>\n<p>O arquivo do BEST Blog preserva ainda <strong>“Conheça o Glossário da Mídia Online (ROI, CPC, CTR...) Parte 1”</strong>, publicado em 08/12/2014 e atribuído a Marcelo Nicchio. O registro acrescenta uma frente editorial/técnica ao período, documentando conteúdo sobre métricas, conversão e conceitos de mídia online.</p>\n<p>Além dos vídeos, o arquivo visual reúne <strong>13 registros</strong> do período, incluindo fotografias do workshop, cartão profissional, imagens do escritório e os dois posts recuperados via Web Archive. O conjunto ajuda a situar visualmente uma etapa curta, mas representativa, da trajetória em Performance.</p>'
        if insert_anchor in text:
            text = text.replace(insert_anchor, inserted)
        ensure('13 registros' in text, "PT 13-record narrative missing")
        pdf_block = '\n<div class="inline-records"><a class="inline-record" href="' + PDF_HREF + '" rel="noopener noreferrer" target="_blank" type="application/pdf"><img alt="BEST Blog anunciando o workshop Facebook Ads: Melhores Práticas, Melhor Conversão." decoding="async" loading="lazy" src="/assets/archive/internet/best-kenshoo/best07_postblog-facebook-ads-2014.jpg" width="1029" height="867"/><span><strong>Facebook Ads: Melhores Práticas, Melhor Conversão</strong><small>Apresentação original do workshop · PDF · 46 páginas ↗</small></span></a></div>'
    else:
        old = '<p>During this period he taught an E-Commerce Brasil workshop on <strong>Advanced Segmentation in Search and Social</strong>. The surviving record provides a direct sample of the professional repertoire of that period — segmentation, Search, Social and technology applied to media operations — and the recording is divided into four parts.</p>'
        new = '<p>On <strong>November 11, 2014, from 9 a.m. to noon</strong>, he taught the E-Commerce Brasil workshop <strong>“Advanced Segmentation in Search”</strong>. The surviving recording is divided into four parts and directly documents the professional repertoire of that period in segmentation, Search, technology and media operations.</p>'
        ensure(old in text or new in text, "EN workshop paragraph anchor missing")
        text = text.replace(old, new)
        text = text.replace('<strong>Workshop — Part 1/4</strong>', '<strong>Search workshop · Nov. 11, 2014 — Part 1/4</strong>')
        text = text.replace('<strong>Part 2/4 — Advanced Segmentation in Search and Social</strong>', '<strong>Part 2/4 — Advanced Segmentation in Search</strong>')
        insert_anchor = '</div>\n<p>Beyond the videos, the visual archive contains 11 records from the period, including workshop photographs, a business card, office images and other records from the operation. Together they provide visual context for a short but representative stage in the Performance trajectory.</p>'
        inserted = '</div>\n<p>The following day, <strong>November 12, 2014, also from 9 a.m. to noon</strong>, Nicchio taught a second E-Commerce Brasil workshop, <strong>“Facebook Ads: Best Practices, Better Conversion”</strong>. A contemporaneous BEST Blog post recovered from the Web Archive, published on November 14, 2014, records the event and identifies him as BEST Performance Manager. The surviving original presentation covers campaign objectives, metrics, segmentation, Custom Audiences, Lookalike Audiences, Website Custom Audiences and conversion pixels.</p>\n<p>The BEST Blog archive also preserves <strong>“Online Media Glossary (ROI, CPC, CTR...) Part 1”</strong>, published on December 8, 2014 and attributed to Marcelo Nicchio. This adds a technical/editorial layer to the period, documenting content on metrics, conversion and online-media concepts.</p>\n<p>Beyond the videos, the visual archive now contains <strong>13 records</strong> from the period, including workshop photographs, a business card, office images and the two BEST Blog posts recovered through the Web Archive. Together they provide visual context for a short but representative stage in the Performance trajectory.</p>'
        if insert_anchor in text:
            text = text.replace(insert_anchor, inserted)
        ensure('13 records' in text, "EN 13-record narrative missing")
        pdf_block = '\n<div class="inline-records"><a class="inline-record" href="' + PDF_HREF + '" rel="noopener noreferrer" target="_blank" type="application/pdf"><img alt="BEST Blog post announcing the Facebook Ads: Best Practices, Better Conversion workshop." decoding="async" loading="lazy" src="/assets/archive/internet/best-kenshoo/best07_postblog-facebook-ads-2014.jpg" width="1029" height="867"/><span><strong>Facebook Ads: Best Practices, Better Conversion</strong><small>Original workshop presentation · PDF · 46 pages ↗</small></span></a></div>'

    # Make the thread caption explicit about the first workshop.
    if lang == "pt":
        text = text.replace('<figcaption><strong>Workshop do E-Commerce Brasil durante o ciclo BEST/Kenshoo, 2014.</strong>', '<figcaption><strong>“Segmentações Avançadas em Search” — E-Commerce Brasil, 11 nov. 2014.</strong>')
    else:
        text = text.replace('<figcaption><strong>E-Commerce Brasil workshop during the BEST/Kenshoo period, 2014.</strong>', '<figcaption><strong>“Advanced Segmentation in Search” — E-Commerce Brasil, Nov. 11, 2014.</strong>')

    if PDF_HREF not in text:
        marker = '<!-- gallery:best-kenshoo:end -->'
        ensure(marker in text, f"{lang}: gallery end marker missing")
        text = text.replace(marker, marker + pdf_block, 1)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    add_gallery_items()
    update_entries_registry()
    update_fragment(PT, "pt")
    update_fragment(EN, "en")
    print("BEST/Kenshoo source migration applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
