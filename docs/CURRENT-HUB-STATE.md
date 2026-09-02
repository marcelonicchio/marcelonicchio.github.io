# CURRENT HUB STATE — Marcelo Nicchio

**Authoritative operational snapshot:** 2 Sep 2026 (BRT)  
**Baseline:** `main` after PR #68 / C3 (`c3681d3aebb5c137ff0be3546247897e7c1fe39b`)  
**Precedence:** later explicit instruction from Marcelo → current `main` + green CI → this file → domain-specific current docs → dated historical handoffs/plans.

This file is the shortest path into the live architecture. Older dossiers and continuity documents remain historical rationale, not current implementation contracts.

---

## 1. Constitution

The HUB is Marcelo Nicchio's public, canonical, multidisciplinary autobiography and authority/identity hub.

It is not a conventional CV, a proof site or a forensic autobiography. The permanent editorial rule remains:

> **Humans first; semantics second.**

Autobiographical information may be published as autobiography even when no external corroborating source exists. Sources, archive material, schema, SEO/GEO/AEO and documentation support the narrative; they do not dominate the reader experience.

Full Biography is the integral chronology. Thematic verticals are selective cuts through the same life and do not need to contain every professional episode.

---

## 2. Public architecture

Primary PT/EN surfaces:

- Home / entity gateway;
- Full Biography / Biografia Completa;
- Music / Música;
- Mídia & Cultura / Media & Culture, with H1 **Cultura & Audiovisual / Culture & Audiovisual**;
- Internet & Performance;
- AI/HAI / IA/HAI;
- Publications / Publicações;
- Archive / Arquivo;
- Selected Projects / Projetos.

### Settled structural decisions

- Internet + Search/Performance are one vertical: **Internet & Performance**.
- Search remains an important specialization inside that continuous digital trajectory, not a separate competing vertical.
- Communication + Audiovisual are one vertical at canonical paths `/pt/comunicacao/` and `/en/communication/`.
- Legacy Search and Audiovisual paths are compatibility surfaces only.
- Livraria Cultura remains in Full Biography only; chronology alone does not place it in a thematic vertical.

Do not reopen these decisions casually.

---

## 3. Full Biography

Permanent rule:

> **Full Biography = totality. Verticals = thematic cuts.**

The managed chronology must not be hand-edited. Core infrastructure:

- `data/full_biography.json`
- `data/editorial_parity.json`
- `tools/sync_full_biography.py`
- `tools/audit_full_biography.py`
- `tools/editorial_parity.py`
- `pt/biografia/index.html`
- `en/biography/index.html`

PT/EN parity means factual/editorial equivalence, not literal translation.

Full Biography remains `index,follow`. Any future robots change is explicitly operator-gated.

---

## 4. Entry and Chapter Page architecture

`data/entries.json` is the registry for reusable entry metadata, Reader presentation and selective Chapter Pages. `data/tags.json` is controlled taxonomy; a tag does not imply a public URL.

Valid source roles:

1. **reader-section** — thematic vertical remains editorial source;
2. **fragment** — neutral shared `content/entries/<lang>/*.inc` source used when an entry is deliberately reused in a generated Chapter Page;
3. **composite-reader-landmarks** — a semantic subject spans multiple chronological locations without physically merging them.

No mass fragment migration and no mass Chapter Page generation are authorized.

### Current generated Chapter Page pairs

- Folhateen / “Órfãos do Rock”;
- Mirantte News;
- CookieWEB;
- Meia-Noite e Uns;
- Melissa 1.0;
- BEST / Kenshoo.

All have self-canonical URLs, reciprocal hreflang, visible breadcrumbs, `BreadcrumbList` and registry-backed source relationships.

### Current indexation state

- **BEST/Kenshoo PT/EN:** `index,follow`, in sitemap — first controlled Chapter Page indexation pilot.
- **Folhateen, Mirantte, CookieWEB, Meia-Noite, Melissa Chapter Pages:** `noindex,follow`, outside sitemap.

Creating a Chapter Page does not automatically authorize indexing it.

---

## 5. Reader UX

Reader disclosure is progressive enhancement: complete text stays in delivered HTML and no-JS fallback remains readable.

### Default disclosure surfaces

- Full Biography PT/EN;
- Internet & Performance PT/EN.

### Continuous/open surfaces

- Mídia & Cultura / Media & Culture remains fully open; no Reader wrapper is applied there.
- AI/HAI remains an open editorial vertical.

### Path-scoped Melissa rule

Melissa 1.0 is intentionally different by surface:

- **AI/HAI vertical PT/EN:** full Melissa entry stays completely open — no compact preview, no card, no disclosure;
- **Full Biography PT/EN:** Melissa may use its rich compact summary to reduce chronological-page density.

This is implemented through path-scoped `always_open_paths`; it is not a global rule for old/final entries.

### Reader presentation states

- `normal`
- `always-open`
- `featured`

Current explicit open entries include Minduim/BBS, Clickland and Folhateen where registered. Featured entries include Mirantte, CookieWEB and Meia-Noite in their disclosure contexts.

Featured color treatment is still aesthetically unresolved. Technical behavior is correct: highlight is collapsed-state only and disappears when expanded.

---

## 6. Rich compact summaries

The compact state is an autonomous concise version of the full entry, not a teaser or mechanical excerpt.

Hard ceiling for structured `reader_preview` copy: **1,650 visible characters per language**. Preferred design center is roughly 1,300 characters when the subject justifies that density.

Current rich-summary set in Full Biography:

- Melissa 1.0;
- Mirantte News;
- CookieWEB;
- Meia-Noite e Uns.

Rich summaries are selective. Folhateen and other deliberately open entries should not be collapsed merely for consistency.

Two visible label systems remain distinct:

- neutral topic/taxonomy chips = what the entry is about;
- red content indicators = what resources exist inside.

Current rich-summary image choices for Mirantte/CookieWEB/Meia-Noite are not operator-approved final selections; do not replace them autonomously before the visual review.

---

## 7. Indexation and Home

Current indexable core includes root/language surfaces, Full Biography, Publications, Archive, AI/HAI and the BEST/Kenshoo Chapter Page pair.

Historical thematic verticals Music, Mídia & Cultura, Internet & Performance and Projects remain `noindex,follow` for now.

Marcelo has already decided the destination state: mature thematic verticals should eventually become `index,follow`. The sequencing remains:

1. expand `/` into a substantive human-readable entity page for **Marcelo Nicchio**;
2. then promote mature PT/EN vertical pairs atomically with robots + sitemap + audit whitelist.

The root prose is operator-authored and has not yet been supplied. C4/Home is therefore skipped for the current implementation run, not abandoned.

---

## 8. Media rules

Two image roles remain separate:

1. editorial image inside a thread;
2. associated record gallery below a record.

Gallery UX may use thumbnails, lightbox, manual navigation, accessibility and lazy loading. Ordinary personal images do not require public “evidence classes”. Provenance/credit/date/alt/caption are useful when applicable.

AI reconstruction from memory is illustration, never historical evidence. Scans, video frames, redacted versions and AI reconstructions should be labeled when materially necessary.

Coitado do Próximo is a later archive workstream: preserve source frame/timestamp separately from treated derivatives; use AI reconstruction only when appropriate and clearly labeled.

---

## 9. Chet implementation status through C3

### C0 — sanitation — complete

- corrected active Folhateen master filenames to publication date 23 Apr 2001;
- regenerated managed gallery surfaces;
- removed fabricated global sitemap `lastmod` values;
- added regression guard for the Folhateen date;
- added EN rich-summary browser smoke.

### C1 — dense Chapter Pages — complete

- promoted Mirantte, CookieWEB and Meia-Noite to neutral shared fragments;
- generated PT/EN Chapter Pages;
- added generic title permalinks;
- fixed Full Biography generator so title normalization preserves nested permalinks.

### C2 + C2.1 — Melissa — complete

- promoted Melissa to fragment-backed PT/EN Chapter Pages;
- added HAI support to Chapter Page generation;
- kept Melissa fully open on AI/HAI PT/EN while retaining the compact Full Biography presentation.

### C3 — BEST/Kenshoo — complete

- strengthened the entry copy using already documented facts only;
- promoted BEST PT/EN Chapter Pages to `index,follow`;
- added the pair to sitemap and the indexable audit set.

---

## 10. Current implementation queue

- **C4 Home:** intentionally skipped in the current run; blocked only by operator prose.
- **C5 documentation consolidation:** this rewrite.
- **C6 sitemap freshness policy:** close the stale/fabricated `lastmod` problem with a deterministic policy/tooling decision.
- **C7 performance/media observability:** add reproducible runtime checks around Reader/media loading rather than inferring performance from static full-scroll bytes alone.
- **C8 selective rich-summary rollout:** review remaining registered entries and extend only where the compact model improves the Full Biography.
- later: visual color/image review, Coitado archive, remaining editorial entries, final whole-site audit and eventual vertical indexation after Home.

---

## 11. CI invariants

The Site Audit workflow currently protects navigation, gallery derivatives/sync, editorial parity, neutral entry sources, Full Biography generation/coverage, Reader loader, Chapter Pages, entry registry, Media/Culture fusion, JS syntax, Chrome Reader behavior, page-image weight reporting, HTML/JSON/sitemap, external presence and analytics installation.

When CI catches a regression, fix the generator/runtime/source model. Do not weaken assertions merely to make the build green.
