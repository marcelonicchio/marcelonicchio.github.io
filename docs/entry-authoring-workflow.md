# Entry authoring workflow — Reader Pages, Full Biography and Chapter Pages

Status: **operational workflow**  
Reference: 2026-08-29 BRT

This document explains how new autobiographical material enters the HUB after the entry-architecture pilot. It exists so future authoring sessions can focus on Marcelo Nicchio's memory and narrative rather than reconstructing the site pipeline.

## 1. The content model has two valid source states

There is no requirement to migrate every existing chapter at once.

### State A — Reader-section source

Most entries may continue to be authored directly in the thematic vertical.

```text
PT/EN thematic vertical
        │
        └─ sync_full_biography.py → Full Biography
```

Use this state when:

- the autobiographical chapter is still being written or revised;
- there is no standalone Chapter Page yet;
- forcing a neutral fragment would add machinery without reuse.

`data/entries.json` may still register a mature Reader-section entry for reusable metadata such as curated summary, topics, media associations and future Chapter Page candidacy.

### State B — neutral fragment source

Promote an entry to a neutral source when the same complete body must feed more than one independently generated surface, especially a Chapter Page.

```text
content/entries/<lang>/<entry>.inc
        │
        ├─ sync_entries.py → thematic vertical
        │                      │
        │                      └─ sync_full_biography.py → Full Biography
        │
        └─ build_chapter_pages.py → selective Chapter Page
```

The migration is **per entry**, not a repository-wide rewrite.

## 2. Authoring a new autobiographical block

Human narrative still comes first.

For a new chapter or expanded period:

1. preserve Marcelo's raw autobiographical account outside the final public prose while shaping it;
2. edit the canonical PT thematic vertical entry;
3. create/review the deliberate EN equivalent;
4. run/accept PT↔EN editorial parity for the affected entry;
5. synchronize Full Biography;
6. add or update the `data/entries.json` record **only when the chapter is mature enough for a useful summary/taxonomy**;
7. associate existing galleries/videos/documents through the registry when useful;
8. run all site/entry audits.

Do **not** create registry filler merely because an entry exists. A shallow placeholder summary can become accidental interface copy later.

## 3. Registering an entry

A normal chapter record may contain:

- stable `id` matching the existing Full Biography/editorial identity where possible;
- `kind: chapter`;
- thematic `domain`;
- PT/EN date/period;
- PT/EN title;
- PT/EN curated summary;
- controlled `topic_ids` from `data/tags.json`;
- useful media associations/count invariants;
- PT/EN Reader Page targets;
- source mode;
- Chapter Page status and future path.

The curated summary is interface/editorial metadata. It should explain **why the episode matters**, not mechanically clip the first paragraph.

## 4. Topic taxonomy

`data/tags.json` is a controlled vocabulary for:

- compact Reader Page chips;
- semantic relationships;
- future filtering/internal linking;
- later thematic analysis.

It is **not**:

- `meta keywords`;
- an instruction to create a tag page;
- a ranking trick;
- a substitute for prose.

Add a new topic only if it is likely to remain meaningful across the HUB. Prefer an existing stable concept over near-duplicate labels.

## 5. Composite subjects that cross chronology

Not every concept deserves a Chapter Page or a new chronological entry.

Use a `landmark-set` when one semantic subject legitimately spans more than one Reader chapter.

Pilot example:

- Goobec training belongs chronologically in the Search-professionalization chapter;
- GAP certifications belong chronologically in the CookieWEB chapter;
- the registry relates both under `internet-goobec-gap` without moving either piece or inventing a standalone page.

This pattern is useful for certifications, recurring tools, collaborations or themes that cross chapter boundaries.

## 6. Promoting an entry to a Chapter Page

Promotion is selective.

A Chapter Page should be genuinely autonomous for some combination of:

- reading;
- citation;
- sharing;
- search intent;
- social preview;
- contextual linking;
- a concentrated archive/record set.

There is no fixed word-count rule.

Promotion procedure:

1. extract the existing PT and EN chapter bodies — **not their `<h2>` headings** — into:
   - `content/entries/pt/<entry>.inc`
   - `content/entries/en/<entry>.inc`;
2. change `source.kind` in `data/entries.json` from `reader-section` to `fragment`;
3. set the exact PT/EN fragment paths;
4. change `chapter_page.status` to `pilot`;
5. keep `chapter_page.indexing` as `noindex,follow` during structural validation unless an indexing experiment has been explicitly approved;
6. run `python tools/sync_entries.py`;
7. review the verticals for semantic/content identity;
8. refresh affected parity checkpoints because management comments/serialization may change even when prose does not;
9. run `python tools/sync_full_biography.py`;
10. run `python tools/build_chapter_pages.py`;
11. run the full Site Audit.

The generator adds page framing from registry metadata while the neutral fragment remains the unique complete editorial body.

## 7. Chapter Page indexing states

### `candidate`

A future URL/path may be reserved in the registry, but the page must not exist on disk yet. It cannot be `index,follow`.

### `pilot`

The page exists and is generated. Default structural-test policy is `noindex,follow`.

A noindex pilot must not be inserted into the sitemap.

### future `index,follow` pilot

An indexable Chapter Page requires an explicit editorial/SEO decision. When enabled:

- the page keeps a self-canonical;
- PT/EN hreflang remains reciprocal;
- the page must have normal static HTML links from its Reader Page occurrences — a query-mode JavaScript link is not enough;
- sitemap treatment is reviewed deliberately;
- Search Console observation follows.

No status change authorizes mass indexation of other Chapter Pages.

## 8. Reader Page disclosure

The current implementation is a **query-flag laboratory**:

```text
?ux=disclosure
```

Normal URLs remain visually unchanged.

The lab uses `data/entries.json` for curated summaries/topics and derives media-count badges from rendered content where possible.

The complete autobiographical body remains in page HTML. Disclosure is presentation, not content retrieval.

The query lab exists to validate:

- information hierarchy;
- card density;
- summary quality;
- topic usefulness;
- content indicators;
- deep links;
- keyboard behavior;
- mobile behavior;
- continuous-reading controls;
- Chapter Page discoverability.

Do not switch disclosure on by default before human visual/reading validation.

## 9. Required checks

The permanent CI should protect:

- navigation sync;
- gallery derivatives/rendering;
- PT/EN parity;
- neutral fragment → vertical sync;
- vertical → Full Biography sync;
- Full Biography coverage;
- Reader disclosure loader presence;
- Chapter Page generation drift;
- entry registry/taxonomy/path/indexing invariants;
- browser-level Reader UX behavior;
- page-weight reporting;
- HTML/JSON/sitemap validity;
- presence and analytics.

The purpose is not bureaucracy. It is to make future autobiographical authoring safe: one changed entry should not silently break another surface.

## 10. Block 4 handoff

For the upcoming Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto authoring batch:

- Petlove, Clickland, BEST and Ad.Dialetto already have chronological entry slots in the current system;
- BEST is already the compact neutral-source/Chapter Page pilot in this architecture;
- do not pre-register final summaries for Petlove/Clickland/Dialetto before Marcelo rewrites those chapters;
- after the PT/EN narrative is mature, register/update each case and let the same pipeline distribute it;
- sensitive private/reputational material remains an editorial decision, not a technical-source problem.

This keeps the next session focused on the autobiography rather than site plumbing.
