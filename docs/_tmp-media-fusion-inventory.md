# Temporary media fusion inventory

## PT: `pt/comunicacao/index.html`
- `bbs` — Primeiros textos em ambiente digital
- `radio` — Metrópole — Rádio Nova Paulista FM
- `folha` — Folha de S.Paulo — “Órfãos do Rock”
- `sinal-verde` — Prateleira Cultural — Revista Sinal Verde
- `temas` — Temas preservados
- `nomes` — Assinaturas e identidade nominal

## EN: `en/communication/index.html`
- `bbs` — Early writing in digital environments
- `radio` — Metrópole — Rádio Nova Paulista FM
- `folha` — Folha de S.Paulo — “Órfãos do Rock”
- `sinal-verde` — Prateleira Cultural — Sinal Verde magazine
- `themes` — Preserved themes
- `names` — Bylines and name identity

## PT audiovisual: `pt/audiovisual/index.html`
- `homens` — 1998 — Homens na Cozinha
- `cinema` — 1998–2000 — captação para cinema
- `meia-noite` — 2006 — Meia-Noite e Uns
- `arquiteto` — 2019 — O Arquiteto da Apoteose
- `autopsia` — 2021 — Autópsia

## EN audiovisual: `en/audiovisual/index.html`
- `homens` — 1998 — Homens na Cozinha
- `film` — 1998–2000 — film fundraising
- `meia-noite` — 2006 — Meia-Noite e Uns
- `architect` — 2019 — O Arquiteto da Apoteose
- `autopsia` — 2021 — Autópsia

## Registry communication/audiovisual
- `communication-folha` domain=`communication`
  - pt: pt/comunicacao/index.html #folha, pt/biografia/index.html #bio-communication-folha
  - en: en/communication/index.html #folha, en/biography/index.html #bio-communication-folha
  - chapter: {'status': 'pilot', 'indexing': 'noindex,follow', 'description': {'pt': 'Marcelo Nicchio na capa do Folhateen de 23/04/2001, discutindo Joey Ramone, cultura punk, faça-você-mesmo e o underground brasileiro.', 'en': 'Marcelo Nicchio in Folhateen’s Apr. 23, 2001 cover story on Joey Ramone, punk culture, DIY ethics and Brazil’s underground rock scene.'}, 'pt_path': 'pt/comunicacao/folhateen-orfaos-do-rock/index.html', 'en_path': 'en/communication/folhateen-orphans-of-rock/index.html'}
- `audiovisual-meia-noite` domain=`audiovisual`
  - pt: pt/audiovisual/index.html #meia-noite, pt/biografia/index.html #bio-audiovisual-meia-noite
  - en: en/audiovisual/index.html #meia-noite, en/biography/index.html #bio-audiovisual-meia-noite
  - chapter: {'status': 'candidate', 'indexing': 'noindex,follow', 'pt_path': 'pt/audiovisual/meia-noite-e-uns/index.html', 'en_path': 'en/audiovisual/meia-noite-e-uns/index.html'}

## `data/galleries.json` audiovisual/communication references
- L16: `"sourceRoot": "assets/archive/audiovisual/meia-noite-e-uns",`
- L19: `"pt/audiovisual/index.html"`
- L22: `"en/audiovisual/index.html"`
- L2002: `"sourceRoot": "assets/archive/communication/folha-orfaos-do-rock",`
- L2005: `"content/entries/pt/communication-folha.inc"`
- L2008: `"content/entries/en/communication-folha.inc"`
- L2474: `"sourceRoot": "assets/archive/communication/prateleira-cultural",`
- L2477: `"pt/comunicacao/index.html"`
- L2480: `"en/communication/index.html"`

## `data/video-embeds.json` audiovisual/communication references

## `data/media-registry.json` audiovisual/communication references

## `assets/js/reader-disclosure-loader.js` relevant references
- L12: `'/pt/comunicacao/', '/en/communication/',`
- L13: `'/pt/audiovisual/', '/en/audiovisual/'`

## `assets/js/reader-disclosure.js` relevant references
- L12: `'/pt/comunicacao/': 'pt/comunicacao/index.html',`
- L13: `'/en/communication/': 'en/communication/index.html',`
- L14: `'/pt/audiovisual/': 'pt/audiovisual/index.html',`
- L15: `'/en/audiovisual/': 'en/audiovisual/index.html',`

## `tools/sync_navigation.py` relevant references

## `tools/sync_galleries.py` relevant references

## `tools/build_full_biography.py` relevant references

## `tools/build_chapter_pages.py` relevant references
- L25: `"communication": {`
- L26: `"pt": ("Comunicação & Cultura", "/pt/comunicacao/"),`
- L27: `"en": ("Communication & Culture", "/en/communication/"),`
- L33: `"audiovisual": {`
- L34: `"pt": ("Audiovisual", "/pt/audiovisual/"),`
- L35: `"en": ("Audiovisual", "/en/audiovisual/"),`
- L44: `"communication-folha": "/assets/media/thread/folhateen-cover-2001.webp",`
- L62: `("/pt/comunicacao/", "Comunicação"),`
- L64: `("/pt/audiovisual/", "Audiovisual"),`
- L74: `("/en/communication/", "Communication"),`
- L76: `("/en/audiovisual/", "Audiovisual"),`

## `sitemap.xml` relevant references
