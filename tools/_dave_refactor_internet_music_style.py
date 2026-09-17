#!/usr/bin/env python3
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDS = {
    'bbs', 'internet', 'psinet', 'mirantte', 'sem', 'cookieweb',
    'clickland', 'petlove', 'best', 'dialetto', 'independente', 'driven',
}
SECTION_RE = re.compile(
    r'(<section\b(?=[^>]*\bid="[^"]+")(?=[^>]*\bclass="chapter")[^>]*>)(<h2>.*?</h2>)',
    re.S,
)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f'Missing replacement anchor: {label}')
    return text.replace(old, new, 1)


def transform_page(rel: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    transformed = []

    def repl(match: re.Match) -> str:
        open_tag, h2 = match.groups()
        sid_match = re.search(r'\bid="([^"]+)"', open_tag)
        sid = sid_match.group(1) if sid_match else ''
        if 'internet-entry' in open_tag:
            transformed.append(sid)
            return match.group(0)
        inner_match = re.search(r'<h2>(.*?)</h2>', h2, re.S)
        if not inner_match:
            return match.group(0)
        plain = html.unescape(re.sub(r'<[^>]+>', '', inner_match.group(1))).strip()
        if ' — ' not in plain:
            return match.group(0)
        date_text, _ = plain.split(' — ', 1)
        if not re.search(r'(?:19|20)\d{2}', date_text):
            return match.group(0)
        needle = date_text + ' — '
        if needle not in h2:
            raise RuntimeError(f'{rel}#{sid}: date prefix not found verbatim: {date_text!r}')
        new_open = open_tag.replace('class="chapter"', 'class="chapter internet-entry"', 1)
        new_h2 = h2.replace(needle, '', 1)
        transformed.append(sid)
        return f'{new_open}<div class="phase-year">{html.escape(date_text, quote=False)}</div>{new_h2}'

    updated = SECTION_RE.sub(repl, text)
    found = set(transformed)
    if found != EXPECTED_IDS:
        raise RuntimeError(f'{rel}: expected {sorted(EXPECTED_IDS)}, got {sorted(found)}')
    path.write_text(updated, encoding='utf-8')
    print(f'{rel}: transformed {len(transformed)} dated chapters')


def update_reader_js() -> None:
    path = ROOT / 'assets/js/reader-disclosure.js'
    text = path.read_text(encoding='utf-8')
    changes = [
        ("    mode: 'Leitura compacta',\n", "    mode: 'Leitura compacta',\n    controls: 'Controles de leitura',\n", 'PT controls label'),
        ("    mode: 'Compact reading',\n", "    mode: 'Compact reading',\n    controls: 'Reading controls',\n", 'EN controls label'),
        (
            "      const meta = [...section.children].find((node) => node.classList?.contains('bio-entry-meta')) || null;\n      const entry = metadataFor(section);",
            "      const meta = [...section.children].find((node) => node.classList?.contains('bio-entry-meta')) || null;\n      const phaseYear = [...section.children].find((node) => node.classList?.contains('phase-year')) || null;\n      const entry = metadataFor(section);",
            'phase-year capture',
        ),
        (
            "    document.documentElement.classList.add('reader-disclosure-active');\n",
            "    document.documentElement.classList.add('reader-disclosure-active');\n    if (internetOpenByDefault) document.documentElement.classList.add('reader-internet-open-default');\n",
            'Internet root class',
        ),
        (
            "      if (meta) summary.appendChild(meta);\n      summary.appendChild(heading);",
            "      if (meta) summary.appendChild(meta);\n      if (phaseYear) summary.appendChild(phaseYear);\n      summary.appendChild(heading);",
            'phase-year summary placement',
        ),
        (
            "          body.insertBefore(pageLink, body.firstChild);",
            "          if (internetOpenByDefault) body.appendChild(pageLink);\n          else body.insertBefore(pageLink, body.firstChild);",
            'Internet chapter-page link placement',
        ),
        (
            "    controlLabel.textContent = labels.mode;",
            "    controlLabel.textContent = internetOpenByDefault ? labels.controls : labels.mode;",
            'Internet controls label selection',
        ),
    ]
    for old, new, label in changes:
        text = replace_once(text, old, new, label)
    path.write_text(text, encoding='utf-8')


def update_reader_css() -> None:
    path = ROOT / 'assets/reader-disclosure.css'
    text = path.read_text(encoding='utf-8')
    marker = '/* Internet & Performance: Music-style open editorial rhythm — 2026-09-17 */'
    if marker in text:
        return
    block = r'''

/* Internet & Performance: Music-style open editorial rhythm — 2026-09-17 */
.article-body > .internet-entry{padding-top:1px;border-top:1px solid var(--line);scroll-margin-top:100px}
.article-body > .internet-entry > .phase-year{margin:46px 0 .55rem;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--accent-soft);font-size:.76rem;line-height:1.2;letter-spacing:.12em;text-transform:uppercase;font-weight:800}
.article-body > .internet-entry > .phase-year + h2{margin-top:0}
html.reader-disclosure-active.reader-internet-open-default .reader-disclosure-controls{margin:4px 0 30px;padding:10px 0 14px;border-top:0}
html.reader-disclosure-active.reader-internet-open-default section.chapter.internet-entry.reader-disclosure-chapter{margin:0 0 18px}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure > summary > .phase-year{margin:0 0 .48rem;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--accent-soft);font-size:.76rem;line-height:1.2;letter-spacing:.12em;text-transform:uppercase;font-weight:800}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open]{border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] > summary{padding:1px 0 0;background:transparent}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] > summary:hover{background:transparent}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] > summary::after{display:none}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] > summary > .phase-year{margin:46px 0 .55rem}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] > summary h2{margin:0 0 .55em!important;font-size:clamp(2rem,4vw,3.2rem)!important;line-height:1.05!important;letter-spacing:-.05em!important}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] .reader-disclosure__excerpt,
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] .reader-disclosure__topics,
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] .reader-disclosure__badges,
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] .reader-disclosure__related,
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] .reader-disclosure__toggle{display:none!important}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] .reader-disclosure__body{padding:0;border-top:0}
html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] .reader-disclosure__body > :first-child{margin-top:0}
@media(max-width:580px){
  .article-body > .internet-entry > .phase-year{margin-top:38px;font-size:.72rem}
  html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure > summary > .phase-year{font-size:.72rem}
  html.reader-disclosure-active.reader-internet-open-default .internet-entry > .reader-disclosure[open] > summary > .phase-year{margin-top:38px}
}
'''
    path.write_text(text + block, encoding='utf-8')


def update_loader_versions() -> None:
    loader_path = ROOT / 'assets/js/reader-disclosure-loader.js'
    loader = loader_path.read_text(encoding='utf-8')
    loader = replace_once(loader, 'reader-disclosure.css?v=20260903-reader12', 'reader-disclosure.css?v=20260917-reader13', 'Reader CSS cache version')
    loader = replace_once(loader, 'reader-disclosure.js?v=20260916-reader13', 'reader-disclosure.js?v=20260917-reader14', 'Reader JS cache version')
    loader_path.write_text(loader, encoding='utf-8')

    sync_path = ROOT / 'tools/sync_reader_disclosure_loader.py'
    sync = sync_path.read_text(encoding='utf-8')
    sync = replace_once(sync, 'reader-disclosure-loader.js?v=20260916-reader13', 'reader-disclosure-loader.js?v=20260917-reader14', 'Reader loader cache version')
    sync_path.write_text(sync, encoding='utf-8')


def update_smoke_test() -> None:
    path = ROOT / 'tools/smoke_reader_ux.js'
    text = path.read_text(encoding='utf-8')
    changes = [
        (
            "  assert(await page.locator('details.reader-disclosure[open]').count() === internetDisclosureCount, 'Internet disclosures must start open by default');\n",
            "  assert(await page.locator('details.reader-disclosure[open]').count() === internetDisclosureCount, 'Internet disclosures must start open by default');\n  assert((await page.locator('html').getAttribute('class') || '').includes('reader-internet-open-default'), 'Internet root lost open-editorial Reader class');\n  assert((await page.getByText('Controles de leitura', {exact: true}).count()) === 1, 'Internet reading-controls label missing');\n",
            'PT Internet root smoke',
        ),
        (
            "  assert(await bbs.locator('.reader-disclosure__toggle').count() === 0, 'Minduim/BBS unexpectedly exposes Reader toggle in Internet');\n",
            "  assert(await bbs.locator('.reader-disclosure__toggle').count() === 0, 'Minduim/BBS unexpectedly exposes Reader toggle in Internet');\n  assert(await bbs.locator(':scope > .phase-year').innerText() === '1992–1996', 'BBS date was not separated from its title');\n  assert(await bbs.locator(':scope > h2').innerText() === 'cultura BBS', 'BBS title still carries its date');\n",
            'BBS date/title smoke',
        ),
        (
            "  assert((await cookieweb.locator('.reader-disclosure__related').innerText()).includes('Goobec'), 'GAP landmark missing from CookieWEB');\n",
            "  assert((await cookieweb.locator('.reader-disclosure__related').innerText()).includes('Goobec'), 'GAP landmark missing from CookieWEB');\n  assert(await cookieweb.locator('summary > .phase-year').innerText() === '2010–2012', 'CookieWEB date was not separated from its title');\n  assert(await cookieweb.locator('summary h2').innerText() === 'Beleza na Web e CookieWEB: Search em escala', 'CookieWEB title still carries its date');\n  const cookieOpenStyle = await cookieweb.locator('details.reader-disclosure').evaluate((el) => ({borderTopWidth: getComputedStyle(el).borderTopWidth, backgroundImage: getComputedStyle(el).backgroundImage, borderRadius: getComputedStyle(el).borderRadius}));\n  assert(cookieOpenStyle.borderTopWidth === '0px', `Open CookieWEB still looks boxed: ${cookieOpenStyle.borderTopWidth}`);\n  assert(cookieOpenStyle.backgroundImage === 'none', `Open CookieWEB still has card background: ${cookieOpenStyle.backgroundImage}`);\n  assert(await cookieweb.locator('.reader-disclosure__toggle').isHidden(), 'Open CookieWEB still exposes accordion CTA');\n",
            'CookieWEB open-editorial smoke',
        ),
        (
            "  if (await mirantteDetails.getAttribute('open') !== null) await mirantte.locator('summary').click();\n  await mirantte.locator('summary').focus();",
            "  if (await mirantteDetails.getAttribute('open') !== null) await mirantte.locator('summary').click();\n  const mirantteClosedBorder = await mirantteDetails.evaluate((el) => getComputedStyle(el).borderTopWidth);\n  assert(mirantteClosedBorder !== '0px', 'Collapsed Mirantte did not return to compact card presentation');\n  await mirantte.locator('summary').focus();",
            'collapsed card restoration smoke',
        ),
        (
            "  assert(await page.locator('details.reader-disclosure[open]').count() === internetDisclosureCountEn, 'English Internet disclosures must start open by default');\n",
            "  assert(await page.locator('details.reader-disclosure[open]').count() === internetDisclosureCountEn, 'English Internet disclosures must start open by default');\n  assert((await page.locator('html').getAttribute('class') || '').includes('reader-internet-open-default'), 'English Internet root lost open-editorial Reader class');\n  assert((await page.getByText('Reading controls', {exact: true}).count()) === 1, 'English Internet reading-controls label missing');\n  assert(await page.locator('#cookieweb summary > .phase-year').innerText() === '2010–2012', 'English CookieWEB date was not separated from its title');\n",
            'EN Internet root smoke',
        ),
    ]
    for old, new, label in changes:
        text = replace_once(text, old, new, label)
    path.write_text(text, encoding='utf-8')


def main() -> int:
    transform_page('pt/internet/index.html')
    transform_page('en/internet/index.html')
    update_reader_js()
    update_reader_css()
    update_loader_versions()
    update_smoke_test()
    print('Internet Music-style structural migration staged.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
