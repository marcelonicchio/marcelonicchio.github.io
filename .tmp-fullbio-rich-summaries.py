from pathlib import Path
import json

ROOT = Path('.')

def read(path):
    return Path(path).read_text(encoding='utf-8')

def write(path, text):
    Path(path).write_text(text, encoding='utf-8')

def replace_once(text, old, new, label):
    if text.count(old) != 1:
        raise SystemExit(f'{label}: expected exactly one match, found {text.count(old)}')
    return text.replace(old, new, 1)

previews = {
    'internet-mirantte': {
        'paths': {
            'pt': ['pt/biografia/index.html'],
            'en': ['en/biography/index.html'],
        },
        'pt': {
            'image': '/assets/media/galleries/mirantte-news/mirantte-news-02-480.webp',
            'alt': 'Página inicial histórica do Mirantte News.',
            'paragraphs': [
                {'text': 'O Mirantte News foi um guia regional de produtos e serviços estruturado em planos anuais para anunciantes, cerca de vinte categorias e hot-sites próprios com fotografias, texto editorial, contatos e recursos de geolocalização e rotas desenvolvidos em parceria com a MapLink/UOL. Marcelo Nicchio conduzia o projeto em sociedade com Luiz Kechichian, proprietário do Grupo Mirantte, em uma operação enxuta.', 'strong': ['Mirantte News', 'MapLink/UOL', 'Luiz Kechichian']},
                {'text': 'À medida que os contratos se acumulavam, apareceu o problema que mudaria o rumo do trabalho: o tráfego orgânico não era suficiente para distribuir exposição entre todas as categorias. Um contato da MapLink aproximou Nicchio de Tiago Luz, por Skype, e a solução discutida foi comprar tráfego para as áreas com maior concentração de anunciantes, incorporando esse custo ao modelo comercial.', 'strong': ['tráfego orgânico', 'Tiago Luz']},
                {'text': 'As primeiras campanhas de aquisição funcionaram e foram mantidas por alguns meses. Ainda assim, a economia do portal tornou-se difícil de sustentar. A equipe foi reduzida, a operação migrou para home office e permaneceu com Nicchio e o webmaster Renato Carriel. Mais tarde, o projeto tentou ampliar seu alcance para a cidade de São Paulo sob o nome Procure SP, mas acabou encerrado.', 'strong': ['Renato Carriel', 'Procure SP']},
                {'text': 'O Mirantte News terminou, mas o problema que havia apresentado permaneceu. Search deixou de ser apenas uma solução pontual para aquisição de tráfego e abriu uma nova direção profissional, que seria aprofundada nos anos seguintes.', 'strong': ['Search', 'nova direção profissional']},
            ],
            'indicators': ['34 fotos', '1 cartão profissional'],
        },
        'en': {
            'image': '/assets/media/galleries/mirantte-news/mirantte-news-02-480.webp',
            'alt': 'Historical Mirantte News home page.',
            'paragraphs': [
                {'text': 'Mirantte News was a regional products-and-services guide structured around annual advertiser plans, roughly twenty categories and dedicated hot-sites with photography, editorial copy, contact information and geolocation and route features developed with MapLink/UOL. Marcelo Nicchio ran the project in partnership with Luiz Kechichian, owner of Grupo Mirantte, through a lean operation.', 'strong': ['Mirantte News', 'MapLink/UOL', 'Luiz Kechichian']},
                {'text': 'As contracts accumulated, a problem emerged that would redirect his work: organic traffic was not enough to distribute exposure across all categories. A MapLink contact introduced Nicchio to Tiago Luz over Skype, and the proposed solution was to buy traffic for the areas with the highest concentration of advertisers, incorporating that cost into the commercial model.', 'strong': ['organic traffic', 'Tiago Luz']},
                {'text': 'The first acquisition campaigns worked and were maintained for several months. Even so, the portal’s economics became difficult to sustain. The team was reduced, the operation moved to a home-office model and continued with Nicchio and webmaster Renato Carriel. The project later tried to broaden its reach to the city of São Paulo as Procure SP, but eventually closed.', 'strong': ['Renato Carriel', 'Procure SP']},
                {'text': 'Mirantte News ended, but the problem it had exposed remained. Search stopped being a one-off traffic-acquisition solution and opened a new professional direction that would be deepened over the following years.', 'strong': ['Search', 'new professional direction']},
            ],
            'indicators': ['34 photos', '1 business card'],
        },
    },
    'internet-cookieweb': {
        'paths': {
            'pt': ['pt/biografia/index.html'],
            'en': ['en/biography/index.html'],
        },
        'pt': {
            'image': '/assets/media/galleries/cookieweb/cookieweb-19-480.webp',
            'alt': 'Marcelo Nicchio com integrantes da equipe da CookieWEB.',
            'paragraphs': [
                {'text': 'Em 2010, Herik Mourão convidou Nicchio a assumir a mídia da Beleza na Web, sua primeira conta de grande porte sob responsabilidade direta. A operação, então com cerca de US$ 50 mil mensais em mídia, exigia decisões orientadas a ROI e aprofundou uma metodologia de otimização por categorias, produtos, termos de busca, higienização de palavras-chave e desempenho.', 'strong': ['Beleza na Web', 'US$ 50 mil mensais', 'ROI']},
                {'text': 'Pouco depois, a conta passou para a CookieWEB e ajudou a inaugurar a nova área de Mídia Digital da agência. Nicchio obteve as certificações Google Advertising Professional, treinou os primeiros profissionais da equipe e combinou coordenação, operação e formação enquanto a estrutura crescia rapidamente.', 'strong': ['CookieWEB', 'Google Advertising Professional']},
                {'text': 'Após a saída de Herik, Nicchio tornou-se Gerente de SEM. No fim de 2011, a operação administrava mais de 22 contas simultâneas, com seis analistas além de estagiários, apoiada por ferramentas como Acquisio e Asana. A escala ampliou também sua visão de performance: produto, preço, logística, conversão e capacidade empresarial passaram a importar tanto quanto palavras-chave ou anúncios.', 'strong': ['Gerente de SEM', 'mais de 22 contas simultâneas', 'seis analistas']},
                {'text': 'O crescimento trouxe ainda uma preocupação com cultura e pertencimento da equipe, visível em iniciativas como o dia coletivo no Hopi Hari. Em 2012, porém, a intensidade do trabalho e a mudança prevista para a Vila Olímpia, após a aquisição de participação na ProfitE, agravariam um desgaste já significativo. Nicchio decidiu sair sem ter outro emprego em vista: qualidade de vida havia se tornado um limite inegociável.', 'strong': ['cultura e pertencimento', 'qualidade de vida']},
            ],
            'indicators': ['20 fotos', '3 certificados GAP', '1 registro contemporâneo'],
        },
        'en': {
            'image': '/assets/media/galleries/cookieweb/cookieweb-19-480.webp',
            'alt': 'Marcelo Nicchio with members of the CookieWEB team.',
            'paragraphs': [
                {'text': 'In 2010, Herik Mourão invited Nicchio to take over media for Beleza na Web, his first large account under direct responsibility. With roughly US$50,000 in monthly media spend at the time, the operation demanded ROI-driven decisions and deepened a layered optimization method across categories, products, search terms, keyword hygiene and performance.', 'strong': ['Beleza na Web', 'US$50,000', 'ROI']},
                {'text': 'Soon afterward, the account moved into CookieWEB and helped launch the agency’s new Digital Media operation. Nicchio earned Google Advertising Professional certifications, trained the first members of the team and combined coordination, hands-on operation and staff development as the structure expanded quickly.', 'strong': ['CookieWEB', 'Google Advertising Professional']},
                {'text': 'After Herik left, Nicchio became SEM Manager. By late 2011, the operation was handling more than 22 accounts at once, with six analysts plus interns, supported by tools such as Acquisio and Asana. The scale also broadened his view of performance: product, price, logistics, conversion and business capacity became as important as keywords or ads.', 'strong': ['SEM Manager', 'more than 22 accounts', 'six analysts']},
                {'text': 'The expansion also brought a concern with team culture and belonging, visible in initiatives such as taking the entire company to Hopi Hari for a day. In 2012, however, the intensity of the work and the planned move to Vila Olímpia after the ProfitE investment would worsen an already significant strain. Nicchio chose to leave without another job lined up: quality of life had become a non-negotiable limit.', 'strong': ['team culture and belonging', 'quality of life']},
            ],
            'indicators': ['20 photos', '3 GAP certificates', '1 contemporary source'],
        },
    },
    'audiovisual-meia-noite': {
        'paths': {
            'pt': ['pt/biografia/index.html'],
            'en': ['en/biography/index.html'],
        },
        'pt': {
            'image': '/assets/media/galleries/meia-noite-e-uns/meia-noite-e-uns-01-480.webp',
            'alt': 'Visão geral de Meia-Noite e Uns, programa exibido pela RedeTV! em 2006.',
            'paragraphs': [
                {'text': 'Meia-Noite e Uns foi um programa de televisão sobre literatura com linguagem pop exibido pela RedeTV! em 2006 e apresentado por Soninha Francine. Marcelo Nicchio assinou a Direção Artística e a Produção Executiva ao lado de Cristiano Gonçalves, pela Dreamsnetwork.tv.', 'strong': ['Meia-Noite e Uns', 'RedeTV!', 'Direção Artística', 'Produção Executiva']},
                {'text': 'Nicchio criou o conceito artístico e visual e a estrutura narrativa do programa. Paulão de Carvalho participou da redação e também coapresentou o projeto a convite de Nicchio; a trilha foi escrita e produzida em parceria com Fábio “Badi” Crepaldi. A proposta aproximava literatura de uma linguagem televisiva menos solene e mais ligada à cultura pop.', 'strong': ['conceito artístico e visual', 'Paulão de Carvalho', 'Fábio “Badi” Crepaldi']},
                {'text': 'O título pretendido era Meia-Noite e Um, ligado à ideia de entrar no ar exatamente às 00:01. Como a grade não podia garantir o minuto exato, o nome passou a ser Meia-Noite e Uns. O arquivo preservado hoje reúne 22 fotografias e quatro vídeos públicos: três blocos do programa e a vinheta completa com créditos.', 'strong': ['Meia-Noite e Um', '00:01', '22 fotografias', 'quatro vídeos públicos']},
            ],
            'indicators': ['22 fotos', '4 vídeos'],
        },
        'en': {
            'image': '/assets/media/galleries/meia-noite-e-uns/meia-noite-e-uns-01-480.webp',
            'alt': 'Overview of Meia-Noite e Uns, aired by RedeTV! in 2006.',
            'paragraphs': [
                {'text': 'Meia-Noite e Uns was a television program about literature in a pop-language format, aired by RedeTV! in 2006 and hosted by Soninha Francine. Marcelo Nicchio was credited with Artistic Direction and Executive Production alongside Cristiano Gonçalves through Dreamsnetwork.tv.', 'strong': ['Meia-Noite e Uns', 'RedeTV!', 'Artistic Direction', 'Executive Production']},
                {'text': 'Nicchio created the program’s artistic and visual concept and its narrative structure. Paulão de Carvalho worked on the writing and also co-hosted the project at Nicchio’s invitation; the soundtrack was written and produced with Fábio “Badi” Crepaldi. The proposal brought literature closer to a less formal television language tied to pop culture.', 'strong': ['artistic and visual concept', 'Paulão de Carvalho', 'Fábio “Badi” Crepaldi']},
                {'text': 'The intended title was Meia-Noite e Um, tied to the idea of going on air at exactly 00:01. Because the schedule could not guarantee that exact minute, the name became Meia-Noite e Uns. The preserved archive now includes 22 photographs and four public videos: three program blocks and the full opening sequence with credits.', 'strong': ['Meia-Noite e Um', '00:01', '22 photographs', 'four public videos']},
            ],
            'indicators': ['22 photos', '4 videos'],
        },
    },
}

# 1) Inject path-scoped rich previews into the registry without reformatting the file.
entries_path = 'data/entries.json'
entries = read(entries_path)
for entry_id, data in previews.items():
    marker = f'      "id": "{entry_id}",'
    start = entries.find(marker)
    if start < 0:
        raise SystemExit(f'missing registry entry {entry_id}')
    end = entries.find('\n    },\n    {', start)
    if end < 0:
        end = entries.find('\n    }\n  ]', start)
    segment = entries[start:end]
    if '"reader_preview"' in segment or '"reader_preview_paths"' in segment:
        raise SystemExit(f'{entry_id}: preview already exists')
    anchor = '      "reader_presentation": {"state": "featured"},\n'
    if anchor not in segment:
        raise SystemExit(f'{entry_id}: featured anchor missing')
    paths_json = json.dumps(data['paths'], ensure_ascii=False, indent=2)
    preview_json = json.dumps({'pt': data['pt'], 'en': data['en']}, ensure_ascii=False, indent=2)
    def indent_json(raw, spaces):
        lines = raw.splitlines()
        return lines[0] + '\n' + '\n'.join((' ' * spaces) + line for line in lines[1:])
    paths_json = indent_json(paths_json, 6)
    preview_json = indent_json(preview_json, 6)
    insertion = f'      "reader_preview_paths": {paths_json},\n      "reader_preview": {preview_json},\n'
    segment = segment.replace(anchor, anchor + insertion, 1)
    entries = entries[:start] + segment + entries[end:]
write(entries_path, entries)

# 2) Retire disclosure mode entirely from Culture & Audiovisual and bump Reader cache.
loader_path = 'assets/js/reader-disclosure-loader.js'
loader = read(loader_path)
old_loader_block = """  const pilotSupported = new Set([\n    ...defaultSupported,\n    '/pt/comunicacao/', '/en/communication/'\n  ]);\n\n  const requestedPilot = params.get('ux') === 'disclosure';\n  if (!defaultSupported.has(pagePath) && !(requestedPilot && pilotSupported.has(pagePath))) return;\n"""
new_loader_block = """  if (!defaultSupported.has(pagePath)) return;\n"""
loader = replace_once(loader, old_loader_block, new_loader_block, 'loader pilot retirement')
loader = loader.replace('20260901-reader10', '20260901-reader11')
write(loader_path, loader)

core_path = 'assets/js/reader-disclosure.js'
core = read(core_path)
core = core.replace("    '/pt/comunicacao/': 'pt/comunicacao/index.html',\n", '')
core = core.replace("    '/en/communication/': 'en/communication/index.html',\n", '')
old_preview = """      const summaryText = entry?.summary?.[language] || excerptFor(section);\n      const readerPreview = entry?.reader_preview?.[language] || null;\n      const contentBadges = readerPreview?.indicators?.length ? readerPreview.indicators : contentBadgesFor(section);\n"""
new_preview = """      const summaryText = entry?.summary?.[language] || excerptFor(section);\n      const previewPaths = entry?.reader_preview_paths?.[language];\n      const previewAllowed = !Array.isArray(previewPaths) || previewPaths.includes(repoPath);\n      const readerPreview = previewAllowed ? (entry?.reader_preview?.[language] || null) : null;\n      const contentBadges = readerPreview?.indicators?.length ? readerPreview.indicators : contentBadgesFor(section);\n"""
core = replace_once(core, old_preview, new_preview, 'preview scope logic')
write(core_path, core)

sync_path = 'tools/sync_reader_disclosure_loader.py'
sync = read(sync_path).replace('20260901-reader10', '20260901-reader11')
sync = sync.replace('    "pt/comunicacao/index.html",\n', '')
sync = sync.replace('    "en/communication/index.html",\n', '')
write(sync_path, sync)

# Version the loader on active Reader pages, and remove it entirely from Culture & Audiovisual.
for path in [*Path('pt').rglob('*.html'), *Path('en').rglob('*.html')]:
    text = path.read_text(encoding='utf-8')
    text = text.replace('reader-disclosure-loader.js?v=20260901-reader10', 'reader-disclosure-loader.js?v=20260901-reader11')
    if path.as_posix() in {'pt/comunicacao/index.html', 'en/communication/index.html'}:
        text = text.replace('\n<script src="/assets/js/reader-disclosure-loader.js?v=20260901-reader11" defer></script>', '')
    path.write_text(text, encoding='utf-8')

# 3) Audit optional preview path scoping against registered Reader targets.
audit_path = 'tools/audit_entries.py'
audit = read(audit_path)
anchor = """        topics = entry.get(\"topic_ids\", [])\n"""
validation = """        preview_paths = entry.get(\"reader_preview_paths\", {})\n        if preview_paths is not None and not isinstance(preview_paths, dict):\n            errors.append(f\"{entry_id}: reader_preview_paths must be an object when present\")\n        elif isinstance(preview_paths, dict):\n            for lang in (\"pt\", \"en\"):\n                paths = preview_paths.get(lang)\n                if paths is None:\n                    continue\n                if not isinstance(paths, list) or not paths or not all(isinstance(path, str) and path for path in paths):\n                    errors.append(f\"{entry_id}:{lang}: reader_preview_paths must be a non-empty list of paths\")\n                    continue\n                targets = {target.get(\"path\") for target in entry.get(\"reader_targets\", {}).get(lang, [])}\n                for path in paths:\n                    if path not in targets:\n                        errors.append(f\"{entry_id}:{lang}: preview path {path!r} is not a registered Reader target\")\n\n"""
audit = replace_once(audit, anchor, validation + anchor, 'preview path audit')
write(audit_path, audit)

# 4) Document that rich summaries can be scoped to specific Reader surfaces.
doc_path = 'docs/reader-summary-model.md'
doc = read(doc_path)
doc = doc.replace(
"""High-value existing candidates include:\n\n- Mirantte News;\n- CookieWEB;\n- Meia-Noite e Uns.\n\nEach must receive its own editorial summary. Do not clone Melissa's structure mechanically.\n""",
"""The first rollout after Melissa applies the model to:\n\n- Mirantte News;\n- CookieWEB;\n- Meia-Noite e Uns.\n\nThese three previews are scoped to **Full Biography / Biografia Completa only**. The thematic verticals keep their own reading behavior; in particular, **Cultura & Audiovisual / Culture & Audiovisual remains fully open and has no disclosure mode**. Each entry receives its own editorial summary rather than cloning Melissa's structure mechanically.\n"""
)
old_note = """Topic labels remain outside `reader_preview` as stable `topic_ids` because they belong to entry taxonomy, not only to this visual component.\n\nThe renderer supports structured text + explicit emphasis rather than arbitrary HTML inside registry data.\n"""
new_note = """Topic labels remain outside `reader_preview` as stable `topic_ids` because they belong to entry taxonomy, not only to this visual component.\n\nA preview can optionally be limited to specific registered Reader targets with `reader_preview_paths`:\n\n```json\n\"reader_preview_paths\": {\n  \"pt\": [\"pt/biografia/index.html\"],\n  \"en\": [\"en/biography/index.html\"]\n}\n```\n\nWhen this field is omitted, the preview keeps the legacy behavior and may render on any Reader target for that entry. This allows Full Biography to use a substantive compact layer without forcing the same summary UX onto a thematic vertical.\n\nThe renderer supports structured text + explicit emphasis rather than arbitrary HTML inside registry data.\n"""
doc = replace_once(doc, old_note, new_note, 'summary model scope docs')
write(doc_path, doc)

# 5) Update browser regression tests: Culture is always open; new previews are Full-Bio-only.
smoke_path = 'tools/smoke_reader_ux.js'
smoke = read(smoke_path)
smoke = smoke.replace(
""" * Full Biography and Internet & Performance use disclosure by default. IA/HAI uses\n * selective disclosure for explicitly registered entries. Communication and Audiovisual\n * remain query-flag pilot surfaces while their UX is still under review.\n""",
""" * Full Biography and Internet & Performance use disclosure by default. IA/HAI uses\n * selective disclosure for explicitly registered entries. Culture & Audiovisual remains\n * a continuous-reading page and never initializes disclosure.\n"""
)
insert_after = """  assert(featuredReclosedStyle.boxShadow !== 'none', 'Featured highlight shadow did not return after collapse');\n\n"""
rich_checks = """  // Full Biography rich summaries are path-scoped: dense entries can be compact here without changing thematic vertical UX.\n  const mirantteBioPreview = page.locator('#bio-internet-mirantte .reader-disclosure__preview');\n  assert(await mirantteBioPreview.count() === 1, 'Mirantte Full Bio rich preview missing');\n  assert(await mirantteBioPreview.locator('.reader-disclosure__preview-paragraph').count() === 4, 'Mirantte Full Bio preview paragraph count incorrect');\n  assert((await mirantteBioPreview.innerText()).includes('tráfego orgânico'), 'Mirantte Full Bio preview lost acquisition problem');\n  assert(await mirantteBioPreview.locator('img').getAttribute('src') === '/assets/media/galleries/mirantte-news/mirantte-news-02-480.webp', 'Mirantte Full Bio preview image incorrect');\n  const mirantteIndicators = await page.locator('#bio-internet-mirantte .reader-disclosure__badge').allInnerTexts();\n  ['34 fotos', '1 cartão profissional'].forEach((label) => assert(mirantteIndicators.includes(label), `Mirantte indicator missing: ${label}`));\n\n  const cookieBioPreviewRich = page.locator('#bio-internet-cookieweb .reader-disclosure__preview');\n  assert(await cookieBioPreviewRich.count() === 1, 'CookieWEB Full Bio rich preview missing');\n  assert(await cookieBioPreviewRich.locator('.reader-disclosure__preview-paragraph').count() === 4, 'CookieWEB Full Bio preview paragraph count incorrect');\n  assert((await cookieBioPreviewRich.innerText()).includes('mais de 22 contas simultâneas'), 'CookieWEB Full Bio preview lost operating scale');\n  assert(await cookieBioPreviewRich.locator('img').getAttribute('src') === '/assets/media/galleries/cookieweb/cookieweb-19-480.webp', 'CookieWEB Full Bio preview image incorrect');\n  const cookieIndicators = await page.locator('#bio-internet-cookieweb .reader-disclosure__badge').allInnerTexts();\n  ['20 fotos', '3 certificados GAP', '1 registro contemporâneo'].forEach((label) => assert(cookieIndicators.includes(label), `CookieWEB indicator missing: ${label}`));\n\n  const meiaBioPreview = page.locator('#bio-audiovisual-meia-noite .reader-disclosure__preview');\n  assert(await meiaBioPreview.count() === 1, 'Meia-Noite Full Bio rich preview missing');\n  assert(await meiaBioPreview.locator('.reader-disclosure__preview-paragraph').count() === 3, 'Meia-Noite Full Bio preview paragraph count incorrect');\n  assert((await meiaBioPreview.innerText()).includes('00:01'), 'Meia-Noite Full Bio preview lost title rationale');\n  assert(await meiaBioPreview.locator('img').getAttribute('src') === '/assets/media/galleries/meia-noite-e-uns/meia-noite-e-uns-01-480.webp', 'Meia-Noite Full Bio preview image incorrect');\n  const meiaIndicators = await page.locator('#bio-audiovisual-meia-noite .reader-disclosure__badge').allInnerTexts();\n  ['22 fotos', '4 vídeos'].forEach((label) => assert(meiaIndicators.includes(label), `Meia-Noite indicator missing: ${label}`));\n\n"""
smoke = replace_once(smoke, insert_after, insert_after + rich_checks, 'Full Bio rich preview smoke insertion')
old_comm = """  // Audiovisual remains an explicit pilot; its registered featured state is already reusable.\n  await page.goto(`${BASE}/pt/audiovisual/?ux=disclosure`, {waitUntil: 'networkidle'});\n  const meia = page.locator('#meia-noite');\n  const meiaBadges = await meia.locator('.reader-disclosure__badge').allInnerTexts();\n  assert((await meia.locator('details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'Meia-Noite featured class missing in pilot');\n  assert(meiaBadges.some((t) => t.includes('22 fotos')), 'Meia-Noite gallery badge incorrect');\n  assert(meiaBadges.some((t) => t.includes('4 vídeos')), 'Meia-Noite video badge incorrect');\n  assert((await meia.locator('.reader-disclosure__excerpt').innerText()).includes('Programa de literatura com linguagem pop'), 'Meia-Noite curated summary missing');\n\n"""
new_comm = """  // Culture & Audiovisual is intentionally continuous reading: normal and legacy query-flag URLs remain fully open.\n  await page.goto(`${BASE}/pt/comunicacao/`, {waitUntil: 'networkidle'});\n  assert(await page.locator('details.reader-disclosure').count() === 0, 'Culture & Audiovisual must not initialize disclosure');\n  assert(!((await page.locator('html').getAttribute('class') || '').includes('reader-disclosure-active')), 'Culture & Audiovisual unexpectedly received Reader UX class');\n  assert(await page.locator('#meia-noite').isVisible(), 'Meia-Noite disappeared from open Culture & Audiovisual page');\n  await page.goto(`${BASE}/pt/comunicacao/?ux=disclosure`, {waitUntil: 'networkidle'});\n  assert(await page.locator('details.reader-disclosure').count() === 0, 'Legacy disclosure query must not collapse Culture & Audiovisual');\n\n"""
smoke = replace_once(smoke, old_comm, new_comm, 'Culture open smoke replacement')
old_internet_mir = """  assert((await mirantte.locator('.reader-disclosure__excerpt').innerText()).includes('problema de aquisição de tráfego'), 'Mirantte curated summary missing');\n"""
new_internet_mir = """  assert(await mirantte.locator('.reader-disclosure__preview').count() === 0, 'Mirantte rich preview leaked from Full Bio into Internet');\n  assert((await mirantte.locator('.reader-disclosure__excerpt').innerText()).includes('problema de aquisição de tráfego'), 'Mirantte curated summary missing');\n"""
smoke = replace_once(smoke, old_internet_mir, new_internet_mir, 'Mirantte preview scope smoke')
old_internet_cookie = """  assert((await cookieweb.locator('details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'CookieWEB featured class missing');\n"""
new_internet_cookie = """  assert((await cookieweb.locator('details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'CookieWEB featured class missing');\n  assert(await cookieweb.locator('.reader-disclosure__preview').count() === 0, 'CookieWEB rich preview leaked from Full Bio into Internet');\n"""
smoke = replace_once(smoke, old_internet_cookie, new_internet_cookie, 'CookieWEB preview scope smoke')
write(smoke_path, smoke)

print('Applied Full Biography rich-summary rollout for Mirantte, CookieWEB and Meia-Noite.')
