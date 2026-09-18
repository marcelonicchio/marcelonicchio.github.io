# Staged indexation plan — current state and operator policy

**Updated:** 18 Sep 2026 (BRT)

The HUB does not equate page count with authority. Indexation follows reader value, content maturity, stable architecture and deliberate rollout.

## 1. Current implementation on `main`

Current top-level indexable authority surfaces include:

- canonical root/language hub surfaces;
- Music / Música;
- Internet & Performance;
- AI/HCI/HAI / IA/HCI/HAI;
- Mídia & Cultura / Media & Culture;
- Publications / Publicações;
- Archive / Arquivo.

Full Biography / Biografia Completa is now `noindex,follow` and is absent from the sitemap. It remains fully readable and crawlable so its ordinary links continue to support human navigation and discovery.

Some autonomous Chapter Pages promoted in earlier rollout phases remain indexable. Their continued indexation is **not** an automatic template for new pages: standalone URLs are now reviewed one by one.

Selected Projects / Projetos and most autonomous Chapter Pages remain staged `noindex,follow`.

## 2. Marcelo's authority hierarchy — 18 Sep 2026

The working priority is intentionally narrower than “index everything”:

| Priority | Surface | Policy |
|---|---|---|
| 1 | Canonical Home `/` | primary name/entity authority surface; `index,follow` |
| 2 | Thematic verticals | current strategic focus: AI/HCI/HAI, Music and Internet & Performance; `index,follow` |
| 3 | Standalone URLs | decide one by one after content/metadata review; no mass promotion |
| 4 | Full Biography / Biografia Completa | navigation/continuity only; `noindex,follow` |

Other already-indexable top-level surfaces are not automatically removed merely because they are outside the current priority trio; any deindexation is a separate deliberate decision.

HCI is explicit in titles, H1, descriptions, navigation and semantics. The established paths remain `/pt/ia-hai/` and `/en/ai-hai/`; do not migrate URLs merely to insert HCI into the slug without a separate migration decision.

## 3. Staging still matters

The broader destination does **not** authorize mass robots flipping.

Before a PT/EN pair or autonomous URL becomes indexable:

1. confirm it has distinct human reader value;
2. finish material content gaps relevant to the page;
3. confirm factual/editorial parity where there is a PT/EN pair;
4. review title/description/canonical/hreflang;
5. confirm ordinary static human-visible internal inlinks;
6. review schema where useful;
7. change robots state deliberately;
8. update sitemap membership in the same release;
9. update audit indexable sets/allowlists in the same release;
10. deploy and measure rather than assuming immediate Search behavior.

## 4. Full Biography cutover — completed 18 Sep 2026

Full Biography PT/EN moved atomically to `noindex,follow` only after Music and Internet & Performance were made indexable and added to the sitemap. The cutover guard remains in CI to prevent future asymmetric or incomplete reversals.

A future indexable Chapter Page must not depend exclusively on Full Biography for its only meaningful internal link.

A future indexable Chapter Page must not depend exclusively on Full Biography for its only meaningful internal link.

Acceptable discovery paths include:

- Home trajectory highlights;
- `/pt/` or `/en/` language hubs;
- a relevant thematic vertical;
- Archive/Publications where contextually appropriate;
- a human-useful chapter/index surface if one is later justified.

Do not create a fake vertical only to satisfy crawler architecture.

## 5. Biography-only example — O Buscador

Espiritualidade — “O Buscador” / Spirituality — “The Seeker” established the biography-only model.

Rules:

- it does not create a Spirituality vertical;
- current implementation is `noindex,follow`;
- Marcelo has explicitly included its autonomous PT/EN URLs in the future indexable set;
- Home already provides one human-visible internal path;
- before promotion, verify PT/EN parity, canonical/hreflang, sitemap/audit treatment and page-level schema.

## 6. Content maturity before promotion

Current priority editorial work includes:

1. Music / Música — Coitado do Próximo and its archive;
2. Internet & Performance — incomplete/refinable passages;
3. Mídia & Cultura / Media & Culture — selected entry adjustments;
4. substantive root entity prose.

A prior “structurally ready” assessment does not mean a vertical is content-complete. Marcelo's later content direction overrides old sequencing assumptions.

## 7. BEST/Kenshoo pilot

BEST/Kenshoo remains useful as the first controlled autonomous indexation pilot and as evidence that the Chapter Page pipeline can support indexed URLs.

It is no longer the permanent ceiling on standalone indexation. Do not preserve old pilot scarcity merely for symmetry once the new destination policy is implemented deliberately.

## 8. Topic tags and page generation

`data/tags.json` remains controlled vocabulary, not a `meta keywords` system and not automatic URL generation.

Broader indexation of legitimate autonomous pages does **not** imply mass tag pages, mass fragments or mass Chapter Page generation.

## 9. Sitemap / hreflang

`tools/build_sitemap.py` remains the canonical sitemap generator and each `<lastmod>` remains derived from real Git history.

Current pages already carry HTML hreflang. Do not add a second sitemap hreflang implementation merely for duplication; Google treats HTML and sitemap hreflang methods as equivalent. Revisit only if there is a concrete maintenance/coverage reason.

## 10. Root entity gate

Root `/` should become a substantive canonical entity page before broad promotion.

Current root already has embedded `WebSite` + `ProfilePage` + `Person` JSON-LD and the 15-profile `sameAs` set. The remaining work is primarily substantive entity content, semantic enrichment and language/hreflang review after the new page is written.

## 11. Principle

Authority comes from coherent identity, useful original content, stable URLs, legitimate identifiers/links, strong internal discovery and external corroboration where it exists — not from exposing the maximum possible number of crawler URLs or deploying search-only pages.
