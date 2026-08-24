# marcelonicchio.github.io

Official personal hub for Marcelo Nicchio.

The public site is served from the `main` branch at:

https://marcelonicchio.github.io

## Current development workflow

- `main` — public, stable site
- `site-v1` — active development branch
- Pull Request #1 — review surface before publication

## Site architecture

- `/` — language entry / canonical hub root
- `/pt/` — Portuguese hub
- `/en/` — English hub
- thematic sections — biography, music, communication, internet/digital culture, audiovisual, Search/Performance, AI/HAI, publications, projects and archive

## Machine-readable authority layer

- `/data/person.json` — canonical person/entity record
- `/data/experience.json` — canonical experience record with editorial evidence status
- `/data/timeline.json` — selected lifetime chronology with source/evidence status
- `/data/publications.json` — canonical research/publication record with work/version distinction
- `/data/public-sources.json` — selected public external/source records
- `/llms.txt` — experimental machine-readable navigation guide; not treated as a search-ranking mechanism or replacement for HTML/Schema.org
- `/sitemap.xml` — currently exposes only pages intended to be indexable at launch

## Search and editorial rules

- unfinished thematic pages remain `noindex,follow`
- canonical URLs and `hreflang` are defined for PT/EN equivalents
- the root profile uses Schema.org `WebSite` + `ProfilePage` / `Person`
- evidence is linked where it adds historical context or verification
- autobiographical facts are not silently removed merely because pre-web documentation did not survive
- WIP projects are labeled explicitly
- repository copies of one research work/version are not counted as separate publications
- future DOIs, repository deposits or publication outcomes are never asserted before they exist
- founder/ownership claims remain distinct from roles directly supported by surviving public records

## Quality-control tooling

- `tools/audit_site.py` — dependency-free structural audit for HTML titles/H1s, canonicals, hreflang, internal links, JSON validity and sitemap/noindex consistency
- `.github/workflows/site-audit.yml` — runs the static audit in the development workflow when GitHub Actions executes it
- `styles.css` — includes visible keyboard focus, reduced-motion handling, coarse-pointer touch targets and horizontally scrollable mobile navigation
- `404.html` — explicit `noindex,follow` recovery page with PT/EN routes

## Internal review notes

- `docs/launch-checklist.md` — pre-publication checklist
- `docs/editorial-fact-audit.md` — factual precision rules and cross-language checks
- `docs/visual-archive-plan.md` — first-wave archive-image curation and rights strategy
- `docs/indexation-plan.md` — staged plan for moving thematic PT/EN pairs from `noindex` to public indexing
- `docs/parity-status.md` — current PT/EN factual-parity status by section
- `docs/external-profile-alignment.md` — post-launch reconciliation plan for HAL, ORCID, GitHub and other authority nodes

`index.html` is the website entry point. `README.md` documents the repository and development process.
