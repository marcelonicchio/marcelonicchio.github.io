# Staged indexation plan — current state

**Updated:** 1 Sep 2026 (BRT)

The HUB does not equate page count with authority. Indexation is staged by editorial maturity and search intent, and experiments should remain attributable rather than changing several URL families at once.

## 1. Current indexable core

Verified current PT/EN core surfaces include:

- language/entity hub and home surfaces;
- Full Biography / Biografia Completa;
- Publications / Publicações;
- Archive / Arquivo;
- AI/HAI / IA/HAI.

The Full Biography is the entity-wide chronological authority surface. Publications carries persistent identifiers and research records. Archive provides historical/documentary navigation. AI/HAI is the mature contemporary research vertical.

PT/EN counterparts should remain materially aligned when indexation state changes.

## 2. Current historical verticals still `noindex,follow`

Verified current PT examples:

- Music / Música;
- **Cultura & Audiovisual / Culture & Audiovisual** (canonical paths remain Communication);
- **Internet & Performance**;
- Selected Projects / Projetos.

The old separate “Internet & Digital Culture” / “Search & Performance” staging model is obsolete. Search is now structurally part of **Internet & Performance**. Communication & Culture and Audiovisual are likewise one **Cultura & Audiovisual / Culture & Audiovisual** vertical at the established Communication paths. Legacy Search and Audiovisual paths are compatibility/redirect surfaces, not independent authority pages.

These verticals remain publicly readable while editorial/UX differentiation matures. `noindex` is not a statement that autobiographical material is untrustworthy.


### Entity-page gate before vertical promotion

Before historical/thematic verticals are changed from `noindex,follow` to `index,follow`, the root `/` must first be expanded into a useful human-readable entity page while preserving its canonical `Person` node. The operator will supply that prose separately.

Do not remove the Full Biography from the index in the same step. Any future Full Biography `noindex,follow` decision remains explicitly operator-gated and should occur only after the root and selected verticals have been published and observed.

## 3. Chapter Page pilots

Current generated pilot pairs:

- Folhateen PT/EN;
- BEST/Kenshoo PT/EN.

They remain:

- `noindex,follow`;
- self-canonical;
- reciprocal hreflang;
- visible breadcrumbs;
- outside the sitemap while noindex.

Creating an autonomous URL does not automatically authorize indexation.

## 4. Next controlled SEO experiment

An all-noindex Chapter Page set cannot produce meaningful evidence about indexation, canonical selection or query behavior.

Therefore a reasonable future experiment is:

> promote **one** mature Chapter Page pair to `index,follow`, with normal static internal links and sitemap review, then observe Search Console before promoting more.

**BEST/Kenshoo PT/EN is now the approved first Chapter Page pair for this isolated experiment.** It is mature, already generated from a neutral fragment and unaffected by the Communication + Audiovisual fusion. Execute its robots/sitemap change in a dedicated PR so Search Console effects remain attributable.

Do **not** combine the first Chapter Page indexation experiment with mass tag-page creation.

## 5. Topic tags are not indexation instructions

`data/tags.json` supports controlled vocabulary, Reader chips, relationships and future planning.

A topic tag does not imply a public URL.

For example, the Melissa rich summary uses:

- AI;
- HAI;
- HCI;
- Prompt Engineering;
- Melissa 1.0.

These may later help standalone-page metadata/internal linking, but they do not become pages just because they exist as labels.

## 6. Reader summaries and SEO

The rich collapsed summary model is primarily human UX, but its topic labels and concise entry framing are intentionally reusable if/when a thread becomes a standalone URL.

Do not treat the compact preview as hidden SEO copy or stuff it with keywords.

Current rule:

- rich preview ceiling = 1,650 visible-copy characters per language;
- preferred design center ≈1,300–1,320;
- summary must remain a useful human-readable concise version of the entry.

See `docs/reader-summary-model.md`.

## 7. Promotion procedure for a thematic pair

Before changing a pair from `noindex,follow` to `index,follow`:

1. confirm factual/editorial PT/EN parity;
2. confirm the page has distinct reader/search value;
3. test external/internal links;
4. review title, meta description, canonical and hreflang;
5. review rights/privacy for prominent visual material;
6. ensure normal static navigation can reach the page;
7. change both language robots states deliberately;
8. update sitemap treatment in the same release when appropriate;
9. deploy with normal audit/Pages verification;
10. observe Search Console rather than inferring success immediately.

## 8. AI/HAI semantic follow-up

AI/HAI is already indexable. When PRO v2 stabilizes, structured data can be revisited so the research works are represented more specifically (for example an `ItemList` containing scholarly works with DOI identifiers where appropriate).

Do not sediment a large schema redesign while the v2 editorial/methodological object is still moving.

## 9. Principle

Authority comes from coherent identity, useful original content, stable URLs, legitimate persistent identifiers/links, strong navigation and external corroboration where it exists — not from exposing the maximum possible number of URLs to crawlers.
