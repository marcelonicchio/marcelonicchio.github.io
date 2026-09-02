# CURRENT HUB STATE — Marcelo Nicchio

**Authoritative operational snapshot:** 2 Sep 2026 (BRT)  
**Coverage:** Chet C0–C8, with C4/Home intentionally skipped pending Marcelo-authored prose.  
**Precedence:** later explicit instruction from Marcelo → current `main` + green CI → this file → domain-specific current docs → dated historical handoffs/plans.

This file is the shortest path into the live architecture. Older dossiers and continuity documents remain historical rationale, not current implementation contracts.

---

## 1. Constitution

The HUB is Marcelo Nicchio's public, canonical, multidisciplinary autobiography and authority/identity hub.

It is not a conventional CV, proof site or forensic autobiography. Permanent editorial rule:

> **Humans first; semantics second.**

Autobiographical information may be published as autobiography even without an external corroborating source. Sources, archive material, schema, SEO/GEO/AEO and documentation support the narrative; they do not dominate the reader experience.

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

Settled structural decisions:

- Internet + Search/Performance are one vertical: **Internet & Performance**.
- Search remains a specialization inside the continuous digital trajectory, not a separate competing vertical.
- Communication + Audiovisual are one vertical at canonical paths `/pt/comunicacao/` and `/en/communication/`.
- Legacy Search and Audiovisual paths are compatibility surfaces only.
- Livraria Cultura remains in Full Biography only.

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

Current generated Chapter Page pairs:

- Folhateen / “Órfãos do Rock”;
- Mirantte News;
- CookieWEB;
- Meia-Noite e Uns;
- Melissa 1.0;
- BEST / Kenshoo.

All have self-canonical URLs, reciprocal hreflang, visible breadcrumbs, `BreadcrumbList` and registry-backed source relationships.

Current indexation:

- **BEST/Kenshoo PT/EN:** `index,follow`, in sitemap — first controlled Chapter Page indexing pilot;
- **Folhateen, Mirantte, CookieWEB, Meia-Noite, Melissa Chapter Pages:** `noindex,follow`, outside sitemap.

Creating a Chapter Page does not automatically authorize indexing it.

---

## 5. Reader UX

Reader disclosure is progressive enhancement: complete text stays in delivered HTML and no-JS fallback remains readable.

Default disclosure surfaces:

- Full Biography PT/EN;
- Internet & Performance PT/EN.

Continuous/open surfaces:

- Mídia & Cultura / Media & Culture remains fully open;
- AI/HAI remains an open editorial vertical.

### Path-scoped Melissa rule

- **AI/HAI PT/EN:** full Melissa entry remains completely open — no compact preview/card/disclosure;
- **Full Biography PT/EN:** Melissa uses its rich compact summary to reduce chronological-page density.

### Path-scoped BEST rule

- **Internet & Performance PT/EN:** normal Reader treatment remains unchanged;
- **Full Biography PT/EN:** BEST/Kenshoo has a rich three-paragraph summary with the existing workshop image, topic chips and curated indicators for four videos + 11 visual records.

Reader presentation states remain `normal`, `always-open` and `featured`.

Current explicit open entries include Minduim/BBS, Clickland and Folhateen where registered. Featured entries include Mirantte, CookieWEB and Meia-Noite in their disclosure contexts.

Featured color treatment is aesthetically unresolved. Technical behavior is correct: highlight is collapsed-state only and disappears when expanded.

---

## 6. Rich compact summaries

The compact state is an autonomous concise version of the full entry, not a teaser or mechanical excerpt.

Hard ceiling for structured `reader_preview` copy: **1,650 visible characters per language**. Preferred design center is roughly 1,300 characters when justified.

Current rich-summary set in Full Biography:

- Melissa 1.0;
- Mirantte News;
- CookieWEB;
- Meia-Noite e Uns;
- BEST / Kenshoo.

The rollout remains selective. Folhateen and other deliberately open entries should not be collapsed merely for consistency.

Two visible label systems remain distinct:

- neutral topic/taxonomy chips = what the entry is about;
- red content indicators = what resources exist inside.

Current preview image choices for Mirantte/CookieWEB/Meia-Noite are not operator-approved final selections; do not replace them autonomously before visual review. BEST reuses its already established workshop thread image.

---

## 7. Indexation, sitemap and Home

Current indexable core includes root/language surfaces, Full Biography, Publications, Archive, AI/HAI and the BEST/Kenshoo Chapter Page pair.

Historical thematic verticals Music, Mídia & Cultura, Internet & Performance and Projects remain `noindex,follow` for now.

Marcelo has already decided the destination state: mature thematic verticals should eventually become `index,follow`. Sequencing remains:

1. expand `/` into a substantive human-readable entity page for **Marcelo Nicchio**;
2. then promote mature PT/EN vertical pairs atomically with robots + sitemap + audit whitelist.

The root prose is operator-authored and has not yet been supplied. C4/Home was intentionally skipped in the C5–C8 implementation run, not abandoned.

### Sitemap freshness

`tools/build_sitemap.py` is now the canonical generator for `sitemap.xml`.

- URL membership comes from the audited `LAUNCH_INDEXABLE` set;
- each `<lastmod>` is derived from the real Git history of that HTML page;
- CI uses full Git history (`fetch-depth: 0`) and fails if the sitemap becomes stale;
- fabricated global freshness dates are prohibited.

---

## 8. Media and performance rules

Two image roles remain separate:

1. editorial image inside a thread;
2. associated record gallery below a record.

Gallery UX may use thumbnails, lightbox, manual navigation, accessibility and lazy loading. Ordinary personal images do not require public “evidence classes”. Provenance/credit/date/alt/caption remain useful when applicable.

AI reconstruction from memory is illustration, never historical evidence. Scans, video frames, redacted versions and AI reconstructions should be labeled when materially necessary.

### Runtime observability

C7 added `tools/smoke_runtime_performance.js` to Site Audit. It probes local Chrome behavior for Full Biography mobile and Internet & Performance desktop, including:

- local LCP/CLS and long tasks;
- JS heap where available;
- lazy/loaded image behavior before and after full scroll;
- same-origin image decode;
- horizontal overflow;
- a two-`requestAnimationFrame` Reader latency proxy.

These are CI regression signals, **not field Core Web Vitals and not real INP**. See `docs/runtime-performance-observability.md`.

Coitado do Próximo remains a later archive workstream: preserve source frame/timestamp separately from treated derivatives; use AI reconstruction only when appropriate and clearly labeled.

---

## 9. Chet implementation status

- **C0 — sanitation:** complete.
- **C1 — dense Chapter Pages:** complete.
- **C2 + C2.1 — Melissa Chapter Page + IA/HAI always-open rule:** complete.
- **C3 — BEST/Kenshoo copy + first Chapter Page indexation pilot:** complete.
- **C4 — Home entity prose:** intentionally skipped; depends on Marcelo-authored prose.
- **C5 — living documentation consolidation:** complete.
- **C6 — deterministic sitemap + real per-page `lastmod`:** complete.
- **C7 — runtime performance/media observability:** complete.
- **C8 — selective rich-summary rollout to BEST/Kenshoo:** complete.

---

## 10. Next queue after C8

No automatic C9 is implied by completing this run. Remaining known workstreams include:

- Home/entity prose when Marcelo supplies it;
- collaborative featured-card color review and operator-selected replacement preview images;
- Coitado do Próximo archive by era;
- remaining editorial entries and new media lots;
- later whole-site audit and eventual thematic-vertical indexation after Home;
- Full Biography robots only if Marcelo/Xará later explicitly decide to revisit it.

---

## 11. CI invariants

Site Audit now protects:

- navigation;
- gallery derivatives/sync/registry;
- PT/EN editorial parity;
- neutral entry sources;
- Full Biography generation/coverage;
- Reader loader and Chrome Reader behavior;
- Chapter Pages and entry registry;
- Mídia & Cultura fusion;
- Reader/runtime JavaScript syntax;
- runtime performance/media observability;
- static page-image weight reporting;
- generated sitemap freshness;
- HTML/JSON/sitemap integrity;
- external presence;
- analytics installation.

When CI catches a regression, fix the generator/runtime/source model. Do not weaken assertions merely to make the build green.
