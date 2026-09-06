# Staged indexation plan — current state and Billy destination

**Updated:** 5 Sep 2026 (BRT)

The HUB does not equate page count with authority. Indexation follows reader value, content maturity, stable architecture and deliberate rollout.

## 1. Current implementation on `main`

Current indexable PT/EN surfaces include:

- root/language/entity hub surfaces;
- Full Biography / Biografia Completa;
- Publications / Publicações;
- Archive / Arquivo;
- AI/HAI / IA/HAI;
- BEST/Kenshoo Chapter Page pair.

Current staged `noindex,follow` surfaces still include:

- Music / Música;
- Mídia & Cultura / Media & Culture;
- Internet & Performance;
- Selected Projects / Projetos;
- most autonomous Chapter Pages, including Espiritualidade — “O Buscador” / Spirituality — “The Seeker”.

This section describes implementation, not the newly decided destination policy.

## 2. Marcelo's destination policy — 5 Sep 2026

The intended end state is now:

| Surface | Destination |
|---|---|
| Home `/` | `index,follow` |
| `/pt/`, `/en/` | `index,follow` |
| Thematic verticals | `index,follow` |
| Legitimate autonomous Chapter Pages / biography-only URLs | `index,follow` |
| Publications / Archive | `index,follow` |
| Full Biography / Biografia Completa | **`noindex,follow`** |

The Full Biography pages must remain crawlable. Do not block them in `robots.txt`, because search crawlers need access to read the `noindex` directive.

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

## 4. Full Biography migration gate

Full Biography PT/EN should move to `noindex,follow` **after**, not before, the intended standalone discovery graph is safe.

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
