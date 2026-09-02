#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data/entries.json"
SMOKE_PT = ROOT / "tools/smoke_reader_ux.js"
SMOKE_EN = ROOT / "tools/smoke_reader_en_rich.js"


def patch_registry() -> None:
    data = json.loads(ENTRIES.read_text(encoding="utf-8"))
    entry = next(item for item in data["entries"] if item.get("id") == "internet-best")

    entry["reader_preview_paths"] = {
        "pt": ["pt/biografia/index.html"],
        "en": ["en/biography/index.html"],
    }
    entry["reader_preview"] = {
        "pt": {
            "image": "/assets/media/thread/best-kenshoo-workshop.webp",
            "alt": "Registro do workshop do E-Commerce Brasil durante o ciclo BEST/Kenshoo, em 2014.",
            "paragraphs": [
                {
                    "text": "Em 2014, Marcelo Nicchio atuou como Gerente de Performance na BEST, em uma operação ligada à plataforma Kenshoo no Brasil. O trabalho combinava onboarding da tecnologia com otimização de campanhas de mídia para grandes varejistas, colocando ferramenta e operação de performance no mesmo ciclo profissional.",
                    "strong": ["Gerente de Performance", "BEST", "Kenshoo"],
                },
                {
                    "text": "Na prática, a adoção da Kenshoo acontecia junto ao acompanhamento de Search e Social. Plataforma, mídia e desempenho faziam parte de um único fluxo de trabalho, em uma etapa que aproximou gestão de campanhas e uso cotidiano de tecnologia especializada.",
                    "strong": ["Search e Social", "Plataforma, mídia e desempenho"],
                },
                {
                    "text": "O período também ficou documentado no workshop do E-Commerce Brasil sobre Segmentação Avançada em Search e Social, preservado em quatro partes no YouTube. O acervo do HUB reúne ainda 11 registros visuais, entre fotografias do workshop, cartão profissional, imagens do escritório e outros registros da operação.",
                    "strong": ["E-Commerce Brasil", "quatro partes", "11 registros visuais"],
                },
            ],
            "indicators": ["4 vídeos", "11 registros visuais"],
        },
        "en": {
            "image": "/assets/media/thread/best-kenshoo-workshop.webp",
            "alt": "Record of the E-Commerce Brasil workshop during the BEST/Kenshoo period in 2014.",
            "paragraphs": [
                {
                    "text": "In 2014, Marcelo Nicchio worked as Performance Manager at BEST, in an operation connected to the Kenshoo platform in Brazil. The work combined technology onboarding with media-campaign optimization for major retailers, placing the platform and day-to-day performance operation within the same professional cycle.",
                    "strong": ["Performance Manager", "BEST", "Kenshoo"],
                },
                {
                    "text": "In practice, Kenshoo adoption happened alongside Search and Social campaign management. Platform, media and performance were part of a single operating flow, in a period that brought campaign management and the everyday use of specialized technology closer together.",
                    "strong": ["Search and Social", "Platform, media and performance"],
                },
                {
                    "text": "The period is also documented by an E-Commerce Brasil workshop on Advanced Segmentation in Search and Social, preserved in four parts on YouTube. The HUB archive also contains 11 visual records, including workshop photographs, a business card, office images and other records from the operation.",
                    "strong": ["E-Commerce Brasil", "four parts", "11 visual records"],
                },
            ],
            "indicators": ["4 videos", "11 visual records"],
        },
    }
    ENTRIES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_pt_smoke() -> None:
    text = SMOKE_PT.read_text(encoding="utf-8")
    anchor = "  ['22 fotos', '4 vídeos'].forEach((label) => assert(meiaIndicators.includes(label), `Meia-Noite indicator missing: ${label}`));\n\n"
    block = """  const bestBioPreview = page.locator('#bio-internet-best .reader-disclosure__preview');
  assert(await bestBioPreview.count() === 1, 'BEST Full Bio rich preview missing');
  assert(await bestBioPreview.locator('.reader-disclosure__preview-paragraph').count() === 3, 'BEST Full Bio preview paragraph count incorrect');
  assert((await bestBioPreview.innerText()).includes('Segmentação Avançada em Search e Social'), 'BEST Full Bio preview lost workshop context');
  assert(await bestBioPreview.locator('img').getAttribute('src') === '/assets/media/thread/best-kenshoo-workshop.webp', 'BEST Full Bio preview image incorrect');
  const bestBioIndicators = await page.locator('#bio-internet-best .reader-disclosure__badge').allInnerTexts();
  ['4 vídeos', '11 registros visuais'].forEach((label) => assert(bestBioIndicators.includes(label), `BEST Full Bio indicator missing: ${label}`));
  const bestBioTopics = await page.locator('#bio-internet-best .reader-disclosure__topic').allInnerTexts();
  ['Performance Marketing', 'Search Marketing', 'Social Ads', 'Kenshoo', 'E-commerce'].forEach((label) => assert(bestBioTopics.includes(label), `BEST Full Bio topic missing: ${label}`));

"""
    if anchor not in text:
        raise RuntimeError("PT Meia-Noite rich-summary anchor not found")
    text = text.replace(anchor, anchor + block, 1)

    internet_anchor = "  const best = page.locator('#best');\n  assert((await best.locator('.reader-disclosure__badge').allInnerTexts()).some((t) => t.includes('4 vídeos')), 'BEST video badge incorrect');\n"
    internet_new = internet_anchor + "  assert(await best.locator('.reader-disclosure__preview').count() === 0, 'BEST rich preview leaked from Full Bio into Internet');\n"
    if internet_anchor not in text:
        raise RuntimeError("PT BEST Internet anchor not found")
    text = text.replace(internet_anchor, internet_new, 1)
    SMOKE_PT.write_text(text, encoding="utf-8")


def patch_en_smoke() -> None:
    text = SMOKE_EN.read_text(encoding="utf-8")
    melissa_spec = """      {
        name: 'Melissa 1.0', selector: '#bio-hai-melissa', paragraphs: 4,
        phrase: '63 hours and 518 prompts', image: '/assets/media/thread/melissa1_0_selfportrait300kb.jpg',
        badges: ['2 images', '1 download link', '4 DOI documents', '1 repository link'], permalink: '/en/ai-hai/melissa-1-0/'
      }
"""
    replacement = """      {
        name: 'Melissa 1.0', selector: '#bio-hai-melissa', paragraphs: 4,
        phrase: '63 hours and 518 prompts', image: '/assets/media/thread/melissa1_0_selfportrait300kb.jpg',
        badges: ['2 images', '1 download link', '4 DOI documents', '1 repository link'], permalink: '/en/ai-hai/melissa-1-0/'
      },
      {
        name: 'BEST / Kenshoo', selector: '#bio-internet-best', paragraphs: 3,
        phrase: 'Advanced Segmentation in Search and Social', image: '/assets/media/thread/best-kenshoo-workshop.webp',
        badges: ['4 videos', '11 visual records'], permalink: '/en/internet/best-kenshoo/', robots: 'index,follow'
      }
"""
    if melissa_spec not in text:
        raise RuntimeError("EN Melissa spec anchor not found")
    text = text.replace(melissa_spec, replacement, 1)

    old_assert = """      assert((await page.locator('meta[name=\"robots\"]').getAttribute('content')) === 'noindex,follow',
        `${spec.name}: standalone pilot unexpectedly changed robots`);
"""
    new_assert = """      const expectedRobots = spec.robots || 'noindex,follow';
      assert((await page.locator('meta[name=\"robots\"]').getAttribute('content')) === expectedRobots,
        `${spec.name}: standalone robots mismatch; expected ${expectedRobots}`);
"""
    if old_assert not in text:
        raise RuntimeError("EN standalone robots assertion not found")
    text = text.replace(old_assert, new_assert, 1)
    SMOKE_EN.write_text(text, encoding="utf-8")


def main() -> int:
    patch_registry()
    patch_pt_smoke()
    patch_en_smoke()
    print("C8 applied: BEST rich preview is scoped to Full Biography, with PT/EN browser coverage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
