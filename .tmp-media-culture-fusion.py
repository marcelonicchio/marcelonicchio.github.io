from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path('.')

def read(p):
    return Path(p).read_text(encoding='utf-8')

def write(p, s):
    Path(p).write_text(s, encoding='utf-8')

def sub1(pattern, repl, text, label, flags=0):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 replacement, got {n}')
    return out

def section_from(path, selector):
    soup = BeautifulSoup(read(path), 'html.parser')
    node = soup.select_one(selector)
    if node is None:
        raise SystemExit(f'missing {selector} in {path}')
    return str(node)

configs = {
    'pt': {
        'comm': 'pt/comunicacao/index.html', 'av': 'pt/audiovisual/index.html',
        'early': ['#homens', '#cinema'], 'late': ['#meia-noite', '#arquiteto', '#autopsia'],
        'before_early': '<section id="folha"', 'before_late': '<section id="temas"',
        'title': 'Cultura & Audiovisual — Marcelo Nicchio',
        'desc': 'Trajetória de Marcelo Nicchio em rádio, imprensa, crítica cultural, televisão, direção artística, produção executiva, cinema e projetos autorais.',
        'hero': '<section class="article-hero"><div class="wrap"><div class="eyebrow">Trajetória · cultura & audiovisual</div><h1>Cultura & Audiovisual</h1><p class="hero-lead">Rádio, imprensa, crítica cultural, televisão, cinema e projetos autorais formam um eixo contínuo em que produção cultural, linguagem editorial e audiovisual se cruzam ao longo da trajetória de Marcelo Nicchio.</p><div class="fact-strip"><div class="fact"><span>Rádio</span><strong>Metrópole · 1994–95</strong></div><div class="fact"><span>Imprensa</span><strong>Folha de S.Paulo · 2001</strong></div><div class="fact"><span>TV</span><strong>Meia-Noite e Uns · 2006</strong></div><div class="fact"><span>Audiovisual</span><strong>Autópsia · 2021</strong></div></div></div></section>',
        'tools': '<div class="page-tools"><a href="/pt/biografia/">Biografia completa</a><a href="/pt/musica/">Música</a><a href="/pt/internet/">Internet & Performance</a><a href="/pt/projetos/">Projetos</a><a href="/pt/arquivo/">Arquivo</a></div>',
        'aside': '<aside class="article-aside"><h3>Nesta página</h3><a href="#bbs">Tremonte BBS</a><a href="#radio">Rádio Metrópole</a><a href="#homens">Homens na Cozinha</a><a href="#cinema">Captação para cinema</a><a href="#folha">Folha de S.Paulo</a><a href="#sinal-verde">Sinal Verde</a><a href="#meia-noite">Meia-Noite e Uns</a><a href="#arquiteto">Arquiteto da Apoteose</a><a href="#autopsia">Autópsia</a><a href="#temas">Temas preservados</a><a href="#nomes">Assinaturas</a></aside>',
    },
    'en': {
        'comm': 'en/communication/index.html', 'av': 'en/audiovisual/index.html',
        'early': ['#homens', '#film'], 'late': ['#meia-noite', '#architect', '#autopsia'],
        'before_early': '<section id="folha"', 'before_late': '<section id="themes"',
        'title': 'Culture & Audiovisual — Marcelo Nicchio',
        'desc': 'Marcelo Nicchio’s work across radio, press, cultural criticism, television, art direction, executive production, film and authored audiovisual projects.',
        'hero': '<section class="article-hero"><div class="wrap"><div class="eyebrow">Trajectory · culture & audiovisual</div><h1>Culture & Audiovisual</h1><p class="hero-lead">Radio, press, cultural criticism, television, film and authored projects form a continuous axis where cultural production, editorial language and audiovisual work intersect throughout Marcelo Nicchio’s trajectory.</p><div class="fact-strip"><div class="fact"><span>Radio</span><strong>Metrópole · 1994–95</strong></div><div class="fact"><span>Press</span><strong>Folha de S.Paulo · 2001</strong></div><div class="fact"><span>TV</span><strong>Meia-Noite e Uns · 2006</strong></div><div class="fact"><span>Audiovisual</span><strong>Autópsia · 2021</strong></div></div></div></section>',
        'tools': '<div class="page-tools"><a href="/en/biography/">Full biography</a><a href="/en/music/">Music</a><a href="/en/internet/">Internet & Performance</a><a href="/en/projects/">Projects</a><a href="/en/archive/">Archive</a></div>',
        'aside': '<aside class="article-aside"><h3>On this page</h3><a href="#bbs">Tremonte BBS</a><a href="#radio">Metrópole radio</a><a href="#homens">Homens na Cozinha</a><a href="#film">Film fundraising</a><a href="#folha">Folha de S.Paulo</a><a href="#sinal-verde">Sinal Verde</a><a href="#meia-noite">Meia-Noite e Uns</a><a href="#architect">O Arquiteto da Apoteose</a><a href="#autopsia">Autópsia</a><a href="#themes">Preserved themes</a><a href="#names">Bylines</a></aside>',
    },
}

for lang, c in configs.items():
    text = read(c['comm'])
    if 'id="homens"' not in text:
        early = '\n'.join(section_from(c['av'], s) for s in c['early']) + '\n'
        if c['before_early'] not in text:
            raise SystemExit(f'{lang}: early insertion anchor missing')
        text = text.replace(c['before_early'], early + c['before_early'], 1)
    if 'id="meia-noite"' not in text:
        late = '\n'.join(section_from(c['av'], s) for s in c['late']) + '\n'
        if c['before_late'] not in text:
            raise SystemExit(f'{lang}: late insertion anchor missing')
        text = text.replace(c['before_late'], late + c['before_late'], 1)
    text = sub1(r'<title>.*?</title>', f'<title>{c["title"]}</title>', text, f'{lang} title', re.S)
    text = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{c["desc"]}">', text, f'{lang} desc')
    text = sub1(r'<section class="article-hero">.*?</section>\n<section class="section">', c['hero'] + '\n<section class="section">', text, f'{lang} hero', re.S)
    text = sub1(r'<div class="page-tools">.*?</div>', c['tools'], text, f'{lang} page tools', re.S)
    text = sub1(r'<aside class="article-aside">.*?</aside>', c['aside'], text, f'{lang} aside', re.S)
    write(c['comm'], text)


def make_stub(path, lang):
    text = read(path)
    if lang == 'pt':
        target = '/pt/comunicacao/'; other = '/en/communication/'
        title = 'Cultura & Audiovisual — Marcelo Nicchio'
        desc = 'A antiga página Audiovisual foi incorporada à vertical Cultura & Audiovisual de Marcelo Nicchio.'
        main = '<main><section class="article-hero"><div class="wrap"><div class="eyebrow">Página incorporada</div><h1>Cultura & Audiovisual</h1><p class="hero-lead">Audiovisual agora faz parte de uma única trajetória com rádio, imprensa, crítica cultural, televisão, cinema, direção artística e produção executiva.</p><div class="actions"><a class="button primary" href="/pt/comunicacao/">Ir para Cultura & Audiovisual</a></div></div></section></main>'
    else:
        target = '/en/communication/'; other = '/pt/comunicacao/'
        title = 'Culture & Audiovisual — Marcelo Nicchio'
        desc = 'The former Audiovisual page is now part of Marcelo Nicchio’s unified Culture & Audiovisual vertical.'
        main = '<main><section class="article-hero"><div class="wrap"><div class="eyebrow">Page incorporated</div><h1>Culture & Audiovisual</h1><p class="hero-lead">Audiovisual work now belongs to one trajectory spanning radio, press, cultural criticism, television, film, art direction and executive production.</p><div class="actions"><a class="button primary" href="/en/communication/">Go to Culture & Audiovisual</a></div></div></section></main>'
    text = sub1(r'<title>.*?</title>', f'<title>{title}</title>', text, path + ' title', re.S)
    text = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', text, path + ' desc')
    if 'http-equiv="refresh"' not in text:
        text = text.replace('<meta name="viewport" content="width=device-width,initial-scale=1">', '<meta name="viewport" content="width=device-width,initial-scale=1">\n  <meta http-equiv="refresh" content="0; url=' + target + '">', 1)
    text = sub1(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://marcelonicchio.github.io{target}">', text, path + ' canonical')
    if lang == 'pt':
        text = sub1(r'<link rel="alternate" hreflang="pt-BR" href="[^"]*">', f'<link rel="alternate" hreflang="pt-BR" href="https://marcelonicchio.github.io{target}">', text, path + ' pt alt')
        text = sub1(r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="https://marcelonicchio.github.io{other}">', text, path + ' en alt')
    else:
        text = sub1(r'<link rel="alternate" hreflang="pt-BR" href="[^"]*">', f'<link rel="alternate" hreflang="pt-BR" href="https://marcelonicchio.github.io{other}">', text, path + ' pt alt')
        text = sub1(r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="https://marcelonicchio.github.io{target}">', text, path + ' en alt')
    text = sub1(r'<main>.*?</main>', main, text, path + ' main', re.S)
    text = re.sub(r'\n<script src="/assets/js/(?:archive-lightbox|reader-disclosure-loader)\.js[^\n]*</script>', '', text)
    text = re.sub(r'\n<script>location\.replace\([^<]*</script>', '', text)
    text = text.replace('</body>', f'<script>location.replace(\'{target}\');</script>\n</body>', 1)
    write(path, text)

make_stub('pt/audiovisual/index.html', 'pt')
make_stub('en/audiovisual/index.html', 'en')

# Registry and Full Biography manifest.
p = 'data/entries.json'; text = read(p)
text = text.replace('"domain": "audiovisual"', '"domain": "communication"')
text = text.replace('"path": "pt/audiovisual/index.html"', '"path": "pt/comunicacao/index.html"')
text = text.replace('"path": "en/audiovisual/index.html"', '"path": "en/communication/index.html"')
text = text.replace('"pt_path": "pt/audiovisual/', '"pt_path": "pt/comunicacao/')
text = text.replace('"en_path": "en/audiovisual/', '"en_path": "en/communication/')
write(p, text)

p = 'data/full_biography.json'; text = read(p)
text = text.replace('"pt": "Comunicação & Cultura"', '"pt": "Cultura & Audiovisual"')
text = text.replace('"en": "Communication & Culture"', '"en": "Culture & Audiovisual"')
text = text.replace('"domain": "audiovisual"', '"domain": "communication"')
text = text.replace('"path": "pt/audiovisual/index.html"', '"path": "pt/comunicacao/index.html"')
text = text.replace('"path": "en/audiovisual/index.html"', '"path": "en/communication/index.html"')
text = re.sub(r',\n    "audiovisual": \{\n      "pt": "Audiovisual",\n      "en": "Audiovisual"\n    \}', '', text, count=1)
write(p, text)

p = 'data/galleries.json'; text = read(p)
text = text.replace('"pt/audiovisual/index.html"', '"pt/comunicacao/index.html"')
text = text.replace('"en/audiovisual/index.html"', '"en/communication/index.html"')
write(p, text)

# Reader canonical route only.
p = 'assets/js/reader-disclosure-loader.js'; text = read(p)
text = text.replace("    '/pt/comunicacao/', '/en/communication/',\n    '/pt/audiovisual/', '/en/audiovisual/'", "    '/pt/comunicacao/', '/en/communication/'")
text = text.replace('20260901-reader9', '20260901-reader10')
write(p, text)
p = 'assets/js/reader-disclosure.js'; text = read(p)
text = text.replace("    '/pt/audiovisual/': 'pt/audiovisual/index.html',\n", '')
text = text.replace("    '/en/audiovisual/': 'en/audiovisual/index.html',\n", '')
write(p, text)
p = 'tools/sync_reader_disclosure_loader.py'; text = read(p)
text = text.replace('20260901-reader9', '20260901-reader10')
text = text.replace('    "pt/audiovisual/index.html",\n', '')
text = text.replace('    "en/audiovisual/index.html",\n', '')
write(p, text)
for path in [*Path('pt').rglob('*.html'), *Path('en').rglob('*.html')]:
    t = path.read_text(encoding='utf-8').replace('reader-disclosure-loader.js?v=20260901-reader9', 'reader-disclosure-loader.js?v=20260901-reader10')
    path.write_text(t, encoding='utf-8')

# Chapter Page generator.
p = 'tools/build_chapter_pages.py'; text = read(p)
text = text.replace('"pt": ("Comunicação & Cultura", "/pt/comunicacao/"),', '"pt": ("Cultura & Audiovisual", "/pt/comunicacao/"),')
text = text.replace('"en": ("Communication & Culture", "/en/communication/"),', '"en": ("Culture & Audiovisual", "/en/communication/"),')
text = re.sub(r'    "audiovisual": \{\n        "pt": \("Audiovisual", "/pt/audiovisual/"\),\n        "en": \("Audiovisual", "/en/audiovisual/"\),\n    \},\n', '', text, count=1)
text = text.replace('("/pt/comunicacao/", "Comunicação"),', '("/pt/comunicacao/", "Mídia & Cultura"),')
text = text.replace('            ("/pt/audiovisual/", "Audiovisual"),\n', '')
text = text.replace('("/en/communication/", "Communication"),', '("/en/communication/", "Media & Culture"),')
text = text.replace('            ("/en/audiovisual/", "Audiovisual"),\n', '')
write(p, text)

# Permanent navigation normalizer.
nav_tool = r'''#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def normalize_nav_block(block: str, lang: str) -> str:
    if lang == "pt":
        internet_href = '/pt/internet/'
        search_pattern = r'<a href="/pt/search-performance/">[^<]*</a>'
        internet_anchor = '<a href="/pt/internet/">Internet & Performance</a>'
        media_href = '/pt/comunicacao/'
        av_pattern = r'<a href="/pt/audiovisual/">[^<]*</a>'
        media_anchor = '<a href="/pt/comunicacao/">Mídia & Cultura</a>'
        internet_repl = (
            ('href="/pt/internet/">Internet</a>', 'href="/pt/internet/">Internet & Performance</a>'),
            ('href="/pt/internet/">Internet & Cultura Digital</a>', 'href="/pt/internet/">Internet & Performance</a>'),
        )
        media_repl = (
            ('href="/pt/comunicacao/">Comunicação</a>', 'href="/pt/comunicacao/">Mídia & Cultura</a>'),
            ('href="/pt/comunicacao/">Comunicação & Cultura</a>', 'href="/pt/comunicacao/">Mídia & Cultura</a>'),
            ('href="/pt/comunicacao/">Cultura & Audiovisual</a>', 'href="/pt/comunicacao/">Mídia & Cultura</a>'),
        )
    else:
        internet_href = '/en/internet/'
        search_pattern = r'<a href="/en/search-performance/">[^<]*</a>'
        internet_anchor = '<a href="/en/internet/">Internet & Performance</a>'
        media_href = '/en/communication/'
        av_pattern = r'<a href="/en/audiovisual/">[^<]*</a>'
        media_anchor = '<a href="/en/communication/">Media & Culture</a>'
        internet_repl = (
            ('href="/en/internet/">Internet</a>', 'href="/en/internet/">Internet & Performance</a>'),
            ('href="/en/internet/">Internet & Digital Culture</a>', 'href="/en/internet/">Internet & Performance</a>'),
        )
        media_repl = (
            ('href="/en/communication/">Communication</a>', 'href="/en/communication/">Media & Culture</a>'),
            ('href="/en/communication/">Communication & Culture</a>', 'href="/en/communication/">Media & Culture</a>'),
            ('href="/en/communication/">Culture & Audiovisual</a>', 'href="/en/communication/">Media & Culture</a>'),
        )
    had_internet = f'href="{internet_href}"' in block
    had_search = re.search(search_pattern, block) is not None
    for old, new in internet_repl:
        block = block.replace(old, new)
    if had_search and not had_internet:
        block = re.sub(search_pattern, internet_anchor, block, count=1)
    elif had_search:
        block = re.sub(search_pattern, '', block)
    had_media = f'href="{media_href}"' in block
    had_av = re.search(av_pattern, block) is not None
    for old, new in media_repl:
        block = block.replace(old, new)
    if had_av and not had_media:
        block = re.sub(av_pattern, media_anchor, block, count=1)
    elif had_av:
        block = re.sub(av_pattern, '', block)
    return block

def normalize_other_links(text: str, lang: str) -> str:
    pairs = [
        ('/pt/search-performance/', '/pt/internet/', 'Internet & Performance') if lang == 'pt' else ('/en/search-performance/', '/en/internet/', 'Internet & Performance'),
        ('/pt/audiovisual/', '/pt/comunicacao/', 'Mídia & Cultura') if lang == 'pt' else ('/en/audiovisual/', '/en/communication/', 'Media & Culture'),
    ]
    for old, target, label_out in pairs:
        pattern = rf'<a([^>]*?)href="{re.escape(old)}"([^>]*)>([^<]*)</a>'
        def repl(match):
            before, after, label = match.groups()
            if label.strip() in {'Search', 'Search & Performance', 'Search &amp; Performance', 'Audiovisual'}:
                label = label_out
            return f'<a{before}href="{target}"{after}>{label}</a>'
        text = re.sub(pattern, repl, text)
    return text

def normalize(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text
    rel = path.relative_to(ROOT).as_posix()
    lang = 'pt' if rel.startswith('pt/') else 'en' if rel.startswith('en/') else ''
    if not lang:
        return False
    text = re.sub(r'<nav class="nav-links"[^>]*>.*?</nav>', lambda m: normalize_nav_block(m.group(0), lang), text, flags=re.S)
    text = normalize_other_links(text, lang)
    if text == original:
        return False
    path.write_text(text, encoding='utf-8')
    return True

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = []
    paths = sorted(set([*ROOT.glob('pt/**/*.html'), *ROOT.glob('en/**/*.html'), ROOT / 'pt/index.html', ROOT / 'en/index.html']))
    for path in paths:
        if path.exists() and normalize(path):
            changed.append(path.relative_to(ROOT).as_posix())
    if args.check and changed:
        print('Navigation is not synchronized:')
        for item in changed:
            print(' -', item)
        return 1
    if changed:
        print('Updated navigation in:')
        for item in changed:
            print(' -', item)
    else:
        print('Navigation already synchronized.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
'''
write('tools/sync_navigation.py', nav_tool)

# Home structural consolidation.
def update_home(path, lang):
    t = read(path)
    if lang == 'pt':
        t = t.replace('Hub oficial de Marcelo Nicchio: biografia, música, comunicação, Internet & Performance, audiovisual, publicações e pesquisa em Human–AI Interaction.', 'Hub oficial de Marcelo Nicchio: biografia, música, Cultura & Audiovisual, Internet & Performance, publicações e pesquisa em Human–AI Interaction.')
        t = t.replace('Uma trajetória desde 1989 em música, comunicação, Internet & Performance, audiovisual e pesquisa em Human–AI Interaction.', 'Uma trajetória desde 1989 em música, Cultura & Audiovisual, Internet & Performance e pesquisa em Human–AI Interaction.')
        t = t.replace('Uma trajetória iniciada em 1989 atravessando criação musical, comunicação, Internet & Performance, audiovisual e pesquisa independente em Human–AI Interaction.', 'Uma trajetória iniciada em 1989 atravessando criação musical, Cultura & Audiovisual, Internet & Performance e pesquisa independente em Human–AI Interaction.')
        t = t.replace('<a href="/pt/comunicacao/"><b>02</b>Comunicação</a>', '<a href="/pt/comunicacao/"><b>02</b>Mídia & Cultura</a>')
        t = re.sub(r'\s*<a href="/pt/audiovisual/"><b>04</b>Audiovisual</a>', '', t, count=1)
        t = t.replace('<a href="/pt/ia-hai/"><b>05</b>IA / HAI</a>', '<a href="/pt/ia-hai/"><b>04</b>IA / HAI</a>')
        new = '<article class="card"><span class="card-no">03 / MEDIA</span><h3>Cultura & Audiovisual</h3><p>Rádio, imprensa, crítica cultural, televisão, cinema, direção artística, produção executiva e projetos autorais.</p><a href="/pt/comunicacao/">Explorar</a></article>'
        t = re.sub(r'<article class="card"><span class="card-no">03 / MEDIA</span>.*?<a href="/pt/comunicacao/">Explorar</a></article>', new, t, count=1, flags=re.S)
        t = re.sub(r'\s*<article class="card"><span class="card-no">05 / AV</span>.*?<a href="/pt/audiovisual/">Explorar</a></article>', '', t, count=1, flags=re.S)
        for a, b in [('06 / HAI', '05 / HAI'), ('07 / DOI', '06 / DOI'), ('08 / PROJECTS', '07 / PROJECTS'), ('09 / ARCHIVE', '08 / ARCHIVE')]:
            t = t.replace(a, b)
    else:
        t = t.replace('Hub oficial de Marcelo Nicchio: biography, music, communication, Internet & Performance, audiovisual, publications and Human–AI Interaction research.', 'Marcelo Nicchio’s official hub: biography, music, Culture & Audiovisual, Internet & Performance, publications and Human–AI Interaction research.')
        t = t.replace('A trajectory since 1989 across music, communication, Internet & Performance, audiovisual work and Human–AI Interaction research.', 'A trajectory since 1989 across music, Culture & Audiovisual, Internet & Performance and Human–AI Interaction research.')
        t = t.replace('A trajectory beginning in 1989 across music creation, communication, Internet & Performance, audiovisual work and independent Human–AI Interaction research.', 'A trajectory beginning in 1989 across music creation, Culture & Audiovisual, Internet & Performance and independent Human–AI Interaction research.')
        t = t.replace('<a href="/en/communication/"><b>02</b>Communication</a>', '<a href="/en/communication/"><b>02</b>Media & Culture</a>')
        t = re.sub(r'\s*<a href="/en/audiovisual/"><b>04</b>Audiovisual</a>', '', t, count=1)
        t = t.replace('<a href="/en/ai-hai/"><b>05</b>AI / HAI</a>', '<a href="/en/ai-hai/"><b>04</b>AI / HAI</a>')
        new = '<article class="card"><span class="card-no">03 / MEDIA</span><h3>Culture & Audiovisual</h3><p>Radio, press, cultural criticism, television, film, art direction, executive production and authored projects.</p><a href="/en/communication/">Explore</a></article>'
        t = re.sub(r'<article class="card"><span class="card-no">03 / MEDIA</span>.*?<a href="/en/communication/">Explore</a></article>', new, t, count=1, flags=re.S)
        t = re.sub(r'\s*<article class="card"><span class="card-no">05 / AV</span>.*?<a href="/en/audiovisual/">Explore</a></article>', '', t, count=1, flags=re.S)
        for a, b in [('06 / HAI', '05 / HAI'), ('07 / DOI', '06 / DOI'), ('08 / PROJECTS', '07 / PROJECTS'), ('09 / ARCHIVE', '08 / ARCHIVE')]:
            t = t.replace(a, b)
    write(path, t)

update_home('pt/index.html', 'pt')
update_home('en/index.html', 'en')

# Documentation.
p = 'docs/CURRENT-HUB-STATE.md'; t = read(p)
replacement = '''### Cultura & Audiovisual is one vertical

The former Communication & Culture and Audiovisual axes are structurally merged into one thematic vertical.

Public naming separates navigation economy from editorial precision:

- menu PT: **Mídia & Cultura**;
- menu EN: **Media & Culture**;
- page H1/title PT: **Cultura & Audiovisual**;
- page H1/title EN: **Culture & Audiovisual**.

Canonical paths remain **`/pt/comunicacao/`** and **`/en/communication/`**. The Folhateen Chapter Page remains at its existing Communication path. The old `/pt/audiovisual/` and `/en/audiovisual/` URLs are permanent `noindex,follow` compatibility stubs canonicalized and redirected to the combined vertical.

The merged page follows one thematic chronology; the Full Biography remains the integral cross-domain chronology and continues to be generated from thematic sources rather than hand-edited. See `docs/url-policy.md`.
'''
t = re.sub(r'### Next vertical consolidation — Communication \+ Audiovisual\n.*?\n---\n\n## 3\.', replacement + '\n---\n\n## 3.', t, count=1, flags=re.S)
t = t.replace('Communication and Audiovisual remain accessible as disclosure experiments through `?ux=disclosure` rather than being promoted site-wide by default.', 'The combined Cultura & Audiovisual vertical remains an opt-in Reader experiment through `?ux=disclosure` on `/pt/comunicacao/` and `/en/communication/`; the legacy Audiovisual stubs do not participate in Reader disclosure.')
write(p, t)

p = 'docs/indexation-plan.md'; t = read(p)
t = t.replace('- Communication / Comunicação;\n- **Internet & Performance**;\n- Audiovisual;', '- **Cultura & Audiovisual / Culture & Audiovisual** (canonical paths remain Communication);\n- **Internet & Performance**;')
t = t.replace('The old separate “Internet & Digital Culture” / “Search & Performance” staging model is obsolete. Search is now structurally part of **Internet & Performance**. Legacy Search paths are compatibility/redirect surfaces, not independent authority pages.', 'The old separate “Internet & Digital Culture” / “Search & Performance” staging model is obsolete. Search is now structurally part of **Internet & Performance**. Communication & Culture and Audiovisual are likewise one **Cultura & Audiovisual / Culture & Audiovisual** vertical at the established Communication paths. Legacy Search and Audiovisual paths are compatibility/redirect surfaces, not independent authority pages.')
write(p, t)

p = 'docs/url-policy.md'; t = read(p)
t = t.replace('when the fusion ships', 'after the fusion ships').replace('will become permanent', 'are permanent')
write(p, t)

# Permanent regression audit.
audit = r'''#!/usr/bin/env python3
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
errors = []
def text(p): return (ROOT / p).read_text(encoding='utf-8')
pairs = [
    ('pt/comunicacao/index.html', ['bbs','radio','homens','cinema','folha','sinal-verde','meia-noite','arquiteto','autopsia','temas','nomes'], 'Cultura & Audiovisual'),
    ('en/communication/index.html', ['bbs','radio','homens','film','folha','sinal-verde','meia-noite','architect','autopsia','themes','names'], 'Culture & Audiovisual'),
]
for path, ids, title in pairs:
    t = text(path)
    if f'<h1>{title}</h1>' not in t: errors.append(f'{path}: combined H1 missing')
    pos = []
    for item in ids:
        p = t.find(f'id="{item}"')
        if p < 0: errors.append(f'{path}: missing #{item}')
        pos.append(p)
    if all(p >= 0 for p in pos) and pos != sorted(pos): errors.append(f'{path}: chronology/order drift')
for path, target, title in [
    ('pt/audiovisual/index.html','/pt/comunicacao/','Cultura & Audiovisual'),
    ('en/audiovisual/index.html','/en/communication/','Culture & Audiovisual'),
]:
    t = text(path)
    for token in ['noindex,follow', f'url={target}', f'https://marcelonicchio.github.io{target}', f"location.replace('{target}')"]:
        if token not in t: errors.append(f'{path}: stub missing {token}')
    if f'<h1>{title}</h1>' not in t: errors.append(f'{path}: stub title missing')
entries = text('data/entries.json'); full = text('data/full_biography.json'); galleries = text('data/galleries.json')
for name, t in [('entries',entries),('full biography',full),('galleries',galleries)]:
    if '"path": "pt/audiovisual/index.html"' in t or '"path": "en/audiovisual/index.html"' in t or '"pt/audiovisual/index.html"' in t or '"en/audiovisual/index.html"' in t:
        errors.append(f'{name}: legacy Audiovisual is still an active data target')
if '"domain": "audiovisual"' in entries or '"domain": "audiovisual"' in full:
    errors.append('registry/manifest still exposes audiovisual as independent domain')
for path in [*ROOT.glob('pt/**/*.html'), *ROOT.glob('en/**/*.html'), ROOT/'pt/index.html', ROOT/'en/index.html']:
    if path.as_posix().endswith('/audiovisual/index.html'):
        continue
    t = path.read_text(encoding='utf-8')
    nav = re.search(r'<nav class="nav-links"[^>]*>(.*?)</nav>', t, re.S)
    if nav and ('href="/pt/audiovisual/"' in nav.group(1) or 'href="/en/audiovisual/"' in nav.group(1)):
        errors.append(f'{path.relative_to(ROOT)}: legacy Audiovisual remains in top navigation')
if errors:
    print('Media/Culture fusion audit failed:')
    for e in errors: print(' -', e)
    sys.exit(1)
print('Media/Culture fusion audit passed.')
'''
write('tools/audit_media_culture_fusion.py', audit)

# Add invariant to CI.
p = '.github/workflows/site-audit.yml'; t = read(p)
if 'Audit Media & Culture fusion' not in t:
    anchor = '      - name: Audit synchronized navigation\n        run: python tools/sync_navigation.py --check\n'
    if anchor not in t:
        raise SystemExit('site-audit navigation anchor not found')
    t = t.replace(anchor, anchor + '      - name: Audit Media & Culture fusion\n        run: python tools/audit_media_culture_fusion.py\n', 1)
write(p, t)
