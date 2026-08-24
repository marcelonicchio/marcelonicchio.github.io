# Site v1 — staged indexation plan

The site should not equate page count with authority. A page moves from `noindex,follow` to `index,follow` only when its narrative, metadata, evidence links and PT/EN counterpart are coherent enough to represent the canonical entity publicly.

## Stage A — launch foundation

Intended to be indexable at the first public merge:

- `/` — canonical language gateway / entity root
- `/pt/` — Portuguese hub
- `/en/` — English hub

These are already listed in `sitemap.xml`.

## Stage B — first authority pages

Best candidates to become indexable immediately after final factual/link review:

1. `/pt/biografia/` + `/en/biography/`
2. `/pt/publicacoes/` + `/en/publications/`
3. `/pt/arquivo/` + `/en/archive/`
4. `/pt/ia-hai/` + `/en/ai-hai/`

Why these first:

- the Full Biography provides entity-wide context;
- Publications has persistent identifiers and clear work/version structure;
- Archive provides the evidence map and source policy;
- AI/HAI is the most densely documented contemporary thematic axis.

Do not release one language of a pair for indexing while leaving the counterpart materially inconsistent.

## Stage C — historical thematic pages

Release after PT/EN parity and archive wording are reviewed:

- Music
- Communication & Culture
- Internet & Digital Culture
- Audiovisual
- Search & Performance

These pages contain a higher mix of public evidence, preserved private material and autobiographical history. That is acceptable, but wording must consistently distinguish those categories.

## Stage D — synthesis pages

- Selected Projects
- future cross-field continuity / methodological-line page, if created

These should be released only when they add information architecture value rather than duplicate existing thematic pages.

## Release procedure for any thematic pair

1. factual cross-check;
2. PT/EN parity check;
3. external-link test;
4. title/meta/canonical/hreflang review;
5. rights/privacy check for any visual asset;
6. change `noindex,follow` to `index,follow`;
7. add both language URLs to `sitemap.xml` in the same release;
8. update `llms.txt` and machine-readable records if canonical facts changed.

## Principle

Authority comes from a coherent entity graph, original source value, stable URLs, useful depth and external corroboration — not from exposing unfinished pages to crawlers early.
