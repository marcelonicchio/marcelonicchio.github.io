# Site v1 — staged indexation plan

The site should not equate page count with authority. A page moves from `noindex,follow` to `index,follow` only when its narrative, metadata, evidence links and PT/EN counterpart are coherent enough to represent the canonical entity publicly.

## Stage A — launch foundation

Intended to be indexable at the first public merge:

- `/` — canonical language gateway / entity root
- `/pt/` — Portuguese hub
- `/en/` — English hub

These are already listed in `sitemap.xml`.

## Stage B — first authority pages

The first-release indexation set is now defined as:

1. `/pt/biografia/` + `/en/biography/`
2. `/pt/publicacoes/` + `/en/publications/`
3. `/pt/arquivo/` + `/en/archive/`
4. `/pt/ia-hai/` + `/en/ai-hai/`

These eight thematic URLs will remain `noindex,follow` during branch development. Their robots directives and `sitemap.xml` entries should be changed together only in the final launch commit, after the remaining rendered visual check and link QA.

Why these first:

- the Full Biography provides entity-wide context;
- Publications has persistent identifiers and clear work/version structure;
- Archive provides the evidence map and source policy;
- AI/HAI is the most densely documented contemporary thematic axis.

Do not release one language of a pair for indexing while leaving the counterpart materially inconsistent.

## Stage C — historical thematic pages

Keep `noindex,follow` in the first release and revisit progressively after public archive material is added or the final page-level source review is complete:

- Music
- Communication & Culture
- Internet & Digital Culture
- Audiovisual
- Search & Performance

These pages already have substantial content, but they contain a higher mix of public evidence, preserved private material and autobiographical history. Keeping them available to readers while temporarily outside indexing lets the hub launch without pretending every historical section has the same documentary density.

## Stage D — synthesis pages

Keep `noindex,follow` until they add distinct information architecture value rather than mainly summarizing existing sections:

- Selected Projects
- future cross-field continuity / methodological-line page, if created

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
