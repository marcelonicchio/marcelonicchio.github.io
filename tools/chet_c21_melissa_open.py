#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data/entries.json"
READER = ROOT / "assets/js/reader-disclosure.js"
SMOKE = ROOT / "tools/smoke_reader_ux.js"


def patch_entries() -> None:
    data = json.loads(ENTRIES.read_text(encoding="utf-8"))
    entry = next(item for item in data["entries"] if item.get("id") == "hai-melissa")
    entry["reader_presentation"] = {
        "state": "normal",
        "always_open_paths": [
            "pt/ia-hai/index.html",
            "en/ai-hai/index.html",
        ],
    }
    entry["reader_preview_paths"] = {
        "pt": ["pt/biografia/index.html"],
        "en": ["en/biography/index.html"],
    }
    ENTRIES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_reader() -> None:
    text = READER.read_text(encoding="utf-8")
    old = "      const presentationState = entry?.reader_presentation?.state || 'normal';\n"
    new = (
        "      const alwaysOpenPaths = entry?.reader_presentation?.always_open_paths || [];\n"
        "      const presentationState = alwaysOpenPaths.includes(repoPath)\n"
        "        ? 'always-open'\n"
        "        : (entry?.reader_presentation?.state || 'normal');\n"
    )
    if old not in text:
        raise RuntimeError("Reader presentation-state line not found")
    READER.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_smoke() -> None:
    text = SMOKE.read_text(encoding="utf-8")
    old = '''  // IA/HAI selective pilot: Melissa alone gets the compact/full two-state treatment.\n  await page.goto(`${BASE}/pt/ia-hai/`, {waitUntil: 'networkidle'});\n  assert(await page.locator('details.reader-disclosure').count() === 1, 'IA/HAI should expose exactly one selective disclosure');\n  assert(await page.locator('.reader-disclosure-controls').count() === 0, 'IA/HAI selective pilot should not show global disclosure controls');\n  assert(await page.locator('#pro2 details.reader-disclosure').count() === 0, 'PRO v2 was unexpectedly collapsed');\n  assert(await page.locator('#pro1 details.reader-disclosure').count() === 0, 'PRO v1 was unexpectedly collapsed');\n  const melissaHai = page.locator('#melissa');\n  const melissaHaiPreview = melissaHai.locator('.reader-disclosure__preview');\n  assert(await melissaHaiPreview.isVisible(), 'Melissa IA/HAI collapsed preview is not visible');\n  assert((await melissaHaiPreview.innerText()).includes('63 horas e 518 prompts'), 'Melissa IA/HAI preview lost core case metrics');\n  assert(await melissaHaiPreview.locator('img').getAttribute('src') === '/assets/media/thread/melissa1_0_selfportrait300kb.jpg', 'Melissa IA/HAI preview cover image incorrect');\n  await melissaHai.locator('details.reader-disclosure > summary').click();\n  assert(await melissaHai.locator('details.reader-disclosure').getAttribute('open') !== null, 'Melissa IA/HAI did not expand');\n  assert(await melissaHaiPreview.isHidden(), 'Melissa IA/HAI compact preview remained visible after expansion');\n  assert((await melissaHai.locator('.reader-disclosure__body').innerText()).includes('O que aconteceu depois não foi planejado.'), 'Melissa IA/HAI full body was not preserved');\n'''
    new = '''  // IA/HAI preserves continuous reading: Melissa is the oldest/final chapter and stays fully open.\n  await page.goto(`${BASE}/pt/ia-hai/`, {waitUntil: 'networkidle'});\n  assert(await page.locator('details.reader-disclosure').count() === 0, 'IA/HAI should preserve a fully open continuous-reading surface');\n  assert(await page.locator('.reader-disclosure-controls').count() === 0, 'IA/HAI should not show global disclosure controls');\n  assert(await page.locator('#pro2 details.reader-disclosure').count() === 0, 'PRO v2 was unexpectedly collapsed');\n  assert(await page.locator('#pro1 details.reader-disclosure').count() === 0, 'PRO v1 was unexpectedly collapsed');\n  const melissaHai = page.locator('#melissa');\n  assert(await melissaHai.getAttribute('data-reader-presentation') === 'always-open', 'Melissa IA/HAI path-scoped always-open state missing');\n  assert(await melissaHai.locator('details.reader-disclosure').count() === 0, 'Melissa IA/HAI must not be wrapped in disclosure');\n  assert(await melissaHai.locator('.reader-disclosure__preview').count() === 0, 'Melissa IA/HAI must not render a compact preview');\n  assert((await melissaHai.innerText()).includes('O que aconteceu depois não foi planejado.'), 'Melissa IA/HAI full body is not visible');\n  assert((await melissaHai.innerText()).includes('Melissa Framework'), 'Melissa IA/HAI lost framework content');\n\n  await page.goto(`${BASE}/en/ai-hai/`, {waitUntil: 'networkidle'});\n  const melissaHaiEn = page.locator('#melissa');\n  assert(await melissaHaiEn.getAttribute('data-reader-presentation') === 'always-open', 'Melissa EN AI/HAI path-scoped always-open state missing');\n  assert(await melissaHaiEn.locator('details.reader-disclosure').count() === 0, 'Melissa EN AI/HAI must not be wrapped in disclosure');\n  assert(await melissaHaiEn.locator('.reader-disclosure__preview').count() === 0, 'Melissa EN AI/HAI must not render a compact preview');\n  assert((await melissaHaiEn.innerText()).includes('What happened afterward was not planned.'), 'Melissa EN AI/HAI full body is not visible');\n'''
    if old not in text:
        raise RuntimeError("Melissa IA/HAI smoke block not found")
    SMOKE.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> int:
    patch_entries()
    patch_reader()
    patch_smoke()
    print("C2.1 applied: Melissa is always-open only on PT/EN AI/HAI verticals; Full Biography preview remains path-scoped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
