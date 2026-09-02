# Staged indexation plan — current state

**Updated:** 2 Sep 2026 (BRT)

The HUB does not equate page count with authority. Indexation is staged by editorial maturity and search intent, and experiments should remain attributable rather than changing several URL families at once.

## 1. Current indexable core

Current indexable PT/EN surfaces include:

- root/language/entity hub surfaces;
- Full Biography / Biografia Completa;
- Publications / Publicações;
- Archive / Arquivo;
- AI/HAI / IA/HAI;
- **BEST/Kenshoo Chapter Page pair** — first controlled standalone-entry indexing pilot.

PT/EN counterparts must remain materially aligned when indexing state changes.

## 2. Historical verticals still `noindex,follow`

- Music / Música;
- Mídia & Cultura / Media & Culture at canonical Communication paths;
- Internet & Performance;
- Selected Projects / Projetos.

Legacy Search and Audiovisual URLs are compatibility surfaces, not independent authority pages.

These verticals are publicly readable. `noindex` is staging, not a statement that autobiographical material is unreliable.

### Entity-page gate before vertical promotion

Before historical/thematic verticals are promoted to `index,follow`, root `/` should first become a useful human-readable entity page while preserving its canonical Person identity. Marcelo will supply that prose separately.

C4/Home may be skipped operationally while unrelated work continues. Skipping it does **not** remove the gate for the later mass vertical promotion.

Full Biography remains `index,follow` unless Marcelo explicitly decides otherwise after later review.

## 3. Chapter Page state

Generated Chapter Page pairs now include:

- Folhateen;
- Mirantte News;
- CookieWEB;
- Meia-Noite e Uns;
- Melissa 1.0;
- BEST/Kenshoo.

Current robots/sitemap policy:

- **BEST/Kenshoo:** `index,follow`, self-canonical, reciprocal hreflang, visible breadcrumbs, in sitemap;
- **all other current Chapter Page pairs:** `noindex,follow`, self-canonical, reciprocal hreflang, visible breadcrumbs, outside sitemap.

Creating an autonomous URL does not automatically authorize indexation.

## 4. BEST/Kenshoo is the active controlled experiment

The prior “future experiment” has now been executed.

BEST/Kenshoo was chosen because it is fragment-backed, mature enough to stand alone, has a clear Search/Performance topic, has stable internal links and a preserved workshop/media archive, and is isolated from the broader vertical-indexation question.

Do not immediately promote another Chapter Page merely to create symmetry. Observe indexing/canonical/query behavior before expanding the experiment set.

Do not combine this pilot with mass tag-page creation.

## 5. Topic tags are not indexation instructions

`data/tags.json` supports controlled vocabulary, Reader chips, relationships and future planning.

A topic tag does not imply a public URL. It is not a `meta keywords` system.

## 6. Reader summaries and SEO

Rich compact summaries are human UX first. Their concise framing can later support standalone-page metadata/internal linking, but they must not become hidden keyword copy.

Current rule:

- hard preview ceiling = 1,650 visible-copy characters per language;
- preferred design center ≈1,300 characters when justified;
- preview must remain a useful human-readable concise version of the entry.

See `docs/reader-summary-model.md`.

## 7. Promotion procedure for a pair

Before changing a PT/EN pair from `noindex,follow` to `index,follow`:

1. confirm factual/editorial parity;
2. confirm distinct reader/search value;
3. test external/internal links;
4. review title, description, canonical and hreflang;
5. review rights/privacy for prominent visual material;
6. ensure normal static internal links can reach it;
7. change both robots states deliberately;
8. update sitemap treatment in the same release;
9. update the site audit indexable set in the same release;
10. deploy and observe Search Console rather than inferring success immediately.

## 8. Future thematic vertical promotion

Marcelo has already chosen the destination state: mature thematic verticals should eventually become `index,follow`.

That rollout should occur only after the substantive root entity page exists, and should be atomic by PT/EN pair: robots + sitemap + audit whitelist + canonical/hreflang/internal-link verification.

## 9. AI/HAI semantic follow-up

AI/HAI is already indexable. When PRO v2 stabilizes, structured data can be revisited for richer representation of scholarly works/DOIs where useful.

Do not sediment a large schema redesign while the v2 editorial/methodological object is still moving.

## 10. Principle

Authority comes from coherent identity, useful original content, stable URLs, legitimate persistent identifiers/links, strong navigation and external corroboration where it exists — not from exposing the maximum possible number of URLs to crawlers.
