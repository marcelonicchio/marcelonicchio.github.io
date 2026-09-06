# Billy URL / indexation matrix — 5 Sep 2026

Operational inventory for the sprint ending 10 Sep 2026.

This file distinguishes **deployed state** from **destination state**. No robots/sitemap change is implied merely by appearing here.

## Rules

- Autonomous substantive URLs should converge to `index,follow`.
- Full Biography / Biografia Completa should converge to `noindex,follow` after the authority graph is ready; do not block them in `robots.txt`.
- Legacy compatibility surfaces stay `noindex,follow` and canonicalize to the current vertical.
- PT/EN pairs move atomically whenever they are paired surfaces.
- A Chapter Page may be indexed only when static internal links to it exist from the relevant reader/source surfaces.
- Biography-only does not imply a new vertical. `O Buscador / The Seeker` remains biography-only and autonomous.
- Sitemap membership follows real indexation state and retains Git-derived `lastmod`.

## Root and language/entity surfaces

| URL | Role | Current robots | Destination | Sitemap target | Action |
|---|---|---|---|---|---|
| `/` | canonical entity gateway | `index,follow` | `index,follow` | yes | B1 substantive entity content + schema refinement |
| `/pt/` | PT trajectory/index surface | `index,follow` | `index,follow` | yes | preserve; strengthen internal authority paths |
| `/en/` | EN trajectory/index surface | `index,follow` | `index,follow` | yes | preserve; strengthen internal authority paths |

## Full Biography

| URL | Role | Current robots | Destination | Sitemap target | Action |
|---|---|---|---|---|---|
| `/pt/biografia/` | total chronology | `index,follow` | `noindex,follow` | no | flip only after autonomous URL graph/indexation rollout |
| `/en/biography/` | total chronology | `index,follow` | `noindex,follow` | no | flip atomically with PT |

Full Biography remains a first-class human navigation/Reader surface. `noindex` is intended to prevent it from competing with the entity/vertical/chapter authority pages, not to remove it from the site.

## Main PT surfaces

| URL | Role | Current robots | Destination | Readiness/action |
|---|---|---|---|---|
| `/pt/arquivo/` | Archive | `index,follow` | `index,follow` | preserve; expand archive over time |
| `/pt/comunicacao/` | Mídia & Cultura / Cultura & Audiovisual | `noindex,follow` | `index,follow` | editorial adjustments before flip |
| `/pt/ia-hai/` | IA / Human–AI Interaction | `index,follow` | `index,follow` | preserve; semantic/schema refinement |
| `/pt/internet/` | Internet & Performance | `noindex,follow` | `index,follow` | fill remaining substantive gaps, then flip |
| `/pt/musica/` | Música | `noindex,follow` | `index,follow` | Coitado do Próximo substantive work is priority blocker |
| `/pt/projetos/` | Projetos selecionados | `noindex,follow` | `index,follow` candidate | review authority/search value before final flip |
| `/pt/publicacoes/` | Publicações | `index,follow` | `index,follow` | add scholarly structured-data layer |

## Main EN surfaces

| URL | Role | Current robots | Destination | Readiness/action |
|---|---|---|---|---|
| `/en/archive/` | Archive | `index,follow` | `index,follow` | preserve; expand archive over time |
| `/en/communication/` | Media & Culture / Culture & Audiovisual | `noindex,follow` | `index,follow` | editorial adjustments before flip |
| `/en/ai-hai/` | AI / Human–AI Interaction | `index,follow` | `index,follow` | preserve; semantic/schema refinement |
| `/en/internet/` | Internet & Performance | `noindex,follow` | `index,follow` | fill remaining substantive gaps, then flip |
| `/en/music/` | Music | `noindex,follow` | `index,follow` | Coitado do Próximo substantive work is priority blocker |
| `/en/projects/` | Selected Projects | `noindex,follow` | `index,follow` candidate | review authority/search value before final flip |
| `/en/publications/` | Publications | `index,follow` | `index,follow` | add scholarly structured-data layer |

## Autonomous Chapter Pages — PT

| URL | Current robots | Destination | Parent/source role | Action |
|---|---|---|---|---|
| `/pt/biografia/espiritualidade-o-buscador/` | `noindex,follow` | `index,follow` | biography-only | index; Home already provides a direct static entry point |
| `/pt/comunicacao/folhateen-orfaos-do-rock/` | `noindex,follow` | `index,follow` | Mídia & Cultura | verify source links, then promote |
| `/pt/comunicacao/meia-noite-e-uns/` | `noindex,follow` | `index,follow` | Mídia & Cultura | verify source links, then promote |
| `/pt/ia-hai/melissa-1-0/` | `noindex,follow` | `index,follow` | IA/HAI | verify source links, then promote |
| `/pt/internet/best-kenshoo/` | `index,follow` | `index,follow` | Internet & Performance | preserve current pilot |
| `/pt/internet/cookieweb/` | `noindex,follow` | `index,follow` | Internet & Performance | verify source links, then promote |
| `/pt/internet/mirantte-news/` | `noindex,follow` | `index,follow` | Internet & Performance | verify source links, then promote |

## Autonomous Chapter Pages — EN

| URL | Current robots | Destination | Parent/source role | Action |
|---|---|---|---|---|
| `/en/biography/spirituality-the-seeker/` | `noindex,follow` | `index,follow` | biography-only | index; language Home provides a route through the shared entity architecture |
| `/en/communication/folhateen-orphans-of-rock/` | `noindex,follow` | `index,follow` | Media & Culture | verify source links, then promote |
| `/en/communication/meia-noite-e-uns/` | `noindex,follow` | `index,follow` | Media & Culture | verify source links, then promote |
| `/en/ai-hai/melissa-1-0/` | `noindex,follow` | `index,follow` | AI/HAI | verify source links, then promote |
| `/en/internet/best-kenshoo/` | `index,follow` | `index,follow` | Internet & Performance | preserve current pilot |
| `/en/internet/cookieweb/` | `noindex,follow` | `index,follow` | Internet & Performance | verify source links, then promote |
| `/en/internet/mirantte-news/` | `noindex,follow` | `index,follow` | Internet & Performance | verify source links, then promote |

## Legacy compatibility surfaces

These are real URLs but **not independent authority pages**.

| URL | Canonical destination | Destination robots | Sitemap |
|---|---|---|---|
| `/pt/audiovisual/` | `/pt/comunicacao/` | `noindex,follow` | no |
| `/en/audiovisual/` | `/en/communication/` | `noindex,follow` | no |
| `/pt/search-performance/` | `/pt/internet/` | `noindex,follow` | no |
| `/en/search-performance/` | `/en/internet/` | `noindex,follow` | no |

## Non-authority utility

- `/404.html` — error surface; never sitemap/index authority target.

## Counts

Physical HTML inventory:

- 18 PT HTML surfaces;
- 18 EN HTML surfaces;
- root `/`;
- `404.html`;
- **38 HTML files total**.

Current sitemap/indexable audited set: **13 URLs**.

Destination with all current autonomous authority surfaces indexed, Full Biography pair removed, and legacy compatibility pages excluded: **31 indexable URLs** if Selected Projects is promoted; **29** if Projects remains staged.

## Promotion gates

Before a URL/pair is promoted:

1. substantive human value confirmed;
2. PT/EN parity where applicable;
3. self-canonical and reciprocal hreflang confirmed;
4. normal static internal links confirmed;
5. title/description/H1 reviewed;
6. schema role reviewed where useful;
7. robots + `LAUNCH_INDEXABLE` + sitemap changed atomically;
8. generated Chapter Pages synchronized with registry;
9. CI green;
10. post-deploy Search Console observation.

## Explicit rejected workaround

Do **not** create `/pt/ensaios/` or `/en/essays/` merely to make `O Buscador / The Seeker` indexable. The biography-only architecture is intentional. A direct authority link from Home plus ordinary site navigation/internal references is preferable to inventing a de facto vertical that the editorial model does not need.
