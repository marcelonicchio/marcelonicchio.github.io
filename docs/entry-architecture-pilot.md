# Entry architecture pilot — six-case stress matrix

Status: **historical implementation record — the core entry/Reader architecture became a production baseline and later evolved; see `docs/CURRENT-HUB-STATE.md`**  
Reference: 2026-08-29 BRT  
Base: `8ce56f866d2eec058333b2b4e0a8e78f228d110c`

This pilot turns the UX/SEO architecture in `docs/ux-seo-architecture-v1.md` into an inspectable system without waiting for new autobiographical writing.

The six cases were chosen because together they cover most structures already present in the HUB.

## 1. Stress matrix

| Case | What it stresses |
|---|---|
| Mirantte News | long narrative + 34-image gallery + archival card + digital-product/Search bridge |
| CookieWEB | very long mixed narrative + thread image + credentials + 20-image gallery + people/operations/culture |
| Folhateen / Folha de S.Paulo | compact press episode + restored thread image + two authoritative external source links |
| Meia-Noite e Uns | television project + 22-image gallery + four videos + credits + art-direction/production roles |
| Goobec + GAP | one semantic subject split across two chronological chapters, with photo + three credentials |
| BEST / Kenshoo | compact professional episode + four-video workshop + technology/performance context |

The point is not to force the same public page type onto all six. A good architecture must support different roles.

## 2. Implemented data layer

`data/entries.json` is the pilot entry registry.

It owns only metadata that should be reused across surfaces:

- stable entry id;
- date/period;
- title;
- curated PT/EN summary;
- controlled topic ids;
- reader targets;
- media associations when useful;
- source mode;
- Chapter Page status/path/indexing policy.

It does **not** become a second autobiography. Full narrative remains in an editorial source.

`data/tags.json` is the controlled vocabulary. Tags begin as data/chips only. They do not create `meta keywords` and do not automatically create indexable tag pages.

## 3. Three entry roles proved by the matrix

### 3.1 Reader chapter

Mirantte, CookieWEB and Meia-Noite currently remain `reader-section` sources. They are used to stress progressive disclosure and metadata on media-heavy chapters before any source migration.

### 3.2 Shared-source Chapter Page pilot

Folhateen and BEST/Kenshoo are deliberately small enough to prove the neutral-source pipeline first.

Their target architecture is:

```text
content/entries/<lang>/<entry>.inc
        │
        ├─ sync → thematic vertical section
        │             │
        │             └─ existing Full Biography sync
        │
        └─ build → Chapter Page
```

This proves the source-of-truth migration on compact entries before touching the two large galleries or CookieWEB's long mixed body.

### 3.3 Landmark set / composite subject

Goobec + GAP is **not** forced into a Chapter Page in this pilot.

The training appears in the 2008–2009 Search chapter; the GAP certifications belong chronologically inside the CookieWEB chapter. `data/entries.json` therefore represents this as `landmark-set` with explicit content assertions across both sections.

This is intentional. The architecture must be able to say “these two pieces are semantically related” without rewriting chronology or manufacturing a standalone URL prematurely.

## 4. Progressive disclosure rule

The first browser prototype remains progressive enhancement:

- full autobiographical text stays in delivered HTML;
- disclosure changes visual exposure, not content ownership;
- existing hashes remain stable;
- opening one entry never closes another;
- print/PDF must expose the complete text;
- JS failure must leave readable HTML.

The next prototype revision consumes curated summaries/topic labels from `data/entries.json` instead of treating first-paragraph clipping as permanent editorial copy.

## 5. Chapter Page indexing policy

No indexing experiment is enabled merely by creating the architecture.

During this implementation pilot:

- generated Folhateen and BEST Chapter Pages remain `noindex,follow`;
- candidate pages remain ungenerated until their source migration is deliberate;
- Meia-Noite remains the preferred future indexable experiment only if explicitly approved at that later step;
- canonical/hreflang can still be validated on `noindex` pilot pages.

This separates **URL architecture testing** from **Google indexing testing**.

## 6. Acceptance criteria for the pilot

The implementation is acceptable when all of the following are true:

1. registry ids and topic ids are unique;
2. every registered topic exists in `data/tags.json`;
3. reader target files/selectors exist;
4. landmark text assertions remain true;
5. fragment-backed entries are synchronized from one PT source and one EN source;
6. generated Chapter Pages have self-canonical, PT/EN hreflang, breadcrumbs and `noindex,follow` during pilot;
7. Full Biography continues to be generated from the thematic sources and remains complete;
8. query-flag disclosure can use curated summaries/topics on all target Reader Pages;
9. normal URLs without the flag remain visually unchanged during the experiment;
10. existing site/parity/gallery/Full Biography audits remain green.

## 7. Deliberately deferred

- mass `.inc` migration;
- mass Chapter Page generation;
- public tag pages;
- mass indexation;
- dynamic gallery materialization;
- a custom client-side search system;
- rewriting Autópsia or AI/HAI before their content/media pass is complete.

The six mature cases are sufficient to build and test the container first.
