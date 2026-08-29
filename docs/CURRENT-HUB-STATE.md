# CURRENT HUB STATE — Marcelo Nicchio

**Read this first in a new editing/architecture session.**  
**Snapshot:** 29 Aug 2026 (BRT)  
**Production `main`:** `09546426f96affc3b8988b6ddf731bfae6d78ad7`  
**Latest architecture merge:** PR #34 — *Add entry registry, Reader UX pilot and Chapter Page architecture*

This file is a current-state handoff. It does not erase older continuity, triangulation or architecture documents; when an older document describes a pre-PR-34 implementation state, this file wins for current implementation status.

---

## 1. HUB constitution

The HUB is Marcelo Nicchio's public, canonical, multidisciplinary autobiography and authority/identity hub.

It is **not** a CV, forensic proof site, defensive biography or current-job landing page.

Permanent editorial priority:

> **Humans first; semantics second.**

Documentation, sources, schema, SEO/GEO/AEO and archive material are structural support. They must not become the protagonist of the reading experience.

Canonical identity: **Marcelo Nicchio**. Historical variants include Marcelo Henrique Nicchio, Marcelo H. Nicchio and Marcelo Minduim.

---

## 2. Permanent autobiographical source rule

This is the current publication rule and it overrides older language that accidentally treated external corroboration as a gate:

> **Information with a useful source → publish the information and the source.**  
> **Autobiographical information without an external source → publish the information normally, without the source.**

The absence of an external source is **not** a criterion for excluding routine autobiographical facts and does not require public disclaimers such as “according to Nicchio”, “not independently verified” or “no documentation was found”.

Privacy, legal/reputational risk and third-party sensitivity are separate editorial questions. A detail can be excluded or anonymized because naming it would be inappropriate even when Marcelo considers the event factual. That is not a source-availability rule.

Examples of current treatment:

- remembered operational scale, team size, workflows and budgets may be narrated autobiographically without a documentary gate;
- private employment documents may remain backstage rather than being published in full;
- sensitive accusations involving named third parties require editorial/legal caution and should not be published casually.

---

## 3. Full Biography constitution

Permanent rule:

> **Full Biography = totality. Verticals = thematic cuts through the same life.**

Do not turn the Full Biography into a short summary merely because Chapter Pages now exist.

Do not concatenate entire verticals one after another. The Full Biography remains a single integrated chronology in which music, communication, internet/performance, audiovisual work and AI/HAI can alternate or overlap.

Canonical Full Biography infrastructure:

- `data/full_biography.json`
- `tools/sync_full_biography.py`
- `tools/audit_full_biography.py`
- `pt/biografia/index.html`
- `en/biography/index.html`

Vertical PT/EN remains the canonical editorial authoring surface unless an entry has deliberately been migrated to a neutral shared fragment as described below.

Do not hand-edit the managed Full Biography region.

---

## 4. PT/EN parity workflow

The bilingual workflow remains deliberate, not automatic translation by checkpoint:

1. edit/review PT source;
2. produce/review equivalent EN;
3. compare PT↔EN editorial meaning;
4. run `python tools/editorial_parity.py --check`;
5. after editorial review, accept the relevant entry revision;
6. regenerate Full Biography;
7. run the full audit suite.

A parity checkpoint records an accepted pair; it does not replace human/editorial review.

---

## 5. Entry architecture introduced by PR #34

PR #34 added a reusable layer between raw chapter HTML and future standalone entry URLs.

Core files:

- `data/entries.json`
- `data/tags.json`
- `tools/sync_entries.py`
- `tools/audit_entries.py`
- `tools/build_chapter_pages.py`
- `tools/sync_reader_disclosure_loader.py`
- `tools/smoke_reader_ux.js`
- `assets/js/reader-disclosure-loader.js`
- `assets/js/reader-disclosure.js`
- `assets/reader-disclosure.css`
- `assets/chapter-page.css`
- `docs/entry-architecture-pilot.md`
- `docs/entry-authoring-workflow.md`

The architecture is **incremental**. It does not require migrating every existing chapter into a new source format.

### Three useful source states

**A. Existing vertical HTML / registered entry**  
The chapter remains authored in the vertical, while `data/entries.json` supplies stable metadata such as summary, topics, media associations and Chapter Page status.

**B. Neutral shared fragment**  
When one body genuinely needs to feed more than one public surface, it may move to:

`content/entries/<lang>/<entry>.inc`

Then:

```text
neutral fragment
      ↓
 thematic vertical
      ↓
 Full Biography

and the same fragment
      ↓
 selective Chapter Page
```

Only migrate deliberately. No mass `.inc` conversion.

**C. Landmark set**  
Some semantic subjects span more than one chronological chapter. They can be registered as relationships/landmarks without physically moving those records together.

Goobec/GAP is the current example: training and certification records stay in their chronological places while the Reader UX can surface the relationship.

---

## 6. Current stress-test registry

The initial registry deliberately covers different content shapes:

- **Mirantte News** — long narrative + 34-image gallery;
- **CookieWEB** — long operational arc + gallery + multiple subphases;
- **Folhateen / Folha de S.Paulo** — press record + restored image + external official sources;
- **Meia-Noite e Uns** — audiovisual narrative + 22 photos + four public video records;
- **Goobec / GAP** — distributed semantic landmarks across training/certification chapters;
- **BEST / Kenshoo** — professional entry + one workshop preserved in four video fragments.

If a future architectural change cannot handle this matrix cleanly, it is probably not ready for site-wide use.

---

## 7. Taxonomy policy

`data/tags.json` is a controlled vocabulary used for internal consistency, semantic relationships and Reader UX chips.

Tags are **not** `meta keywords`.

Do not automatically create public/tag pages from this vocabulary.

A future thematic/tag URL only becomes reasonable when the grouping itself deserves a useful editorial destination. There is no fixed minimum-entry or word-count law.

---

## 8. Reader UX — current production state

Progressive disclosure is now deployed in production **only as an opt-in UX laboratory**.

Normal URLs remain structurally and visually unchanged.

Activation requires `?ux=disclosure`.

Current supported PT surfaces:

- `/pt/biografia/?ux=disclosure`
- `/pt/internet/?ux=disclosure`
- `/pt/comunicacao/?ux=disclosure`
- `/pt/audiovisual/?ux=disclosure`

Equivalent EN surfaces are also supported.

The Reader UX:

- uses native `<details>/<summary>` semantics;
- preserves all autobiographical content in delivered source HTML;
- permits multiple entries to remain open;
- supports Open all / Collapse all;
- auto-opens the containing chapter for a deep link/hash;
- uses registry-backed summaries/topics where registered;
- derives media indicators from actual rendered content;
- can show semantic relations such as Goobec/GAP;
- exposes a standalone-page link only when an entry has a pilot Chapter Page;
- opens all content for print and restores prior state afterward;
- keeps the untransformed source readable when JavaScript is disabled.

The previous branch-only prototype PR #31 has been closed as superseded by PR #34.

### Important

Do not mistake the normal URL for the Reader UX. Without `?ux=disclosure`, the page is intentionally the same long-form reader used before PR #34.

---

## 9. Reader UX regression coverage

Reader UX is no longer tested by memory/manual inspection alone.

`tools/smoke_reader_ux.js` runs in Chrome inside the permanent Site Audit and currently checks, among other things:

- normal URL remains untransformed;
- Full Biography disclosure count and deep-link auto-open;
- curated CookieWEB summary/topics;
- Mirantte 34-photo indicator;
- Goobec/GAP semantic relation;
- BEST four-video indicator and Chapter Page link;
- Folhateen Chapter Page link;
- Meia-Noite 22-photo + four-video indicators;
- independent multiple-open behavior;
- keyboard operation;
- Open all / Collapse all;
- print-state behavior;
- English controls and English topic metadata;
- mobile horizontal overflow;
- no-JavaScript fallback;
- pilot Chapter Page canonical/robots/basic structure.

Do not weaken these checks merely to make CI green. If a test is brittle, replace it with a stronger behavioral assertion rather than deleting meaningful coverage.

---

## 10. Chapter Pages — current policy and pilots

Chapter Pages are **selective**, not a new requirement for every autobiographical entry.

Current pilot pairs:

### Folhateen

- PT: `/pt/comunicacao/folhateen-orfaos-do-rock/`
- EN: `/en/communication/folhateen-orphans-of-rock/`

### BEST / Kenshoo

- PT: `/pt/internet/best-kenshoo/`
- EN: `/en/internet/best-kenshoo/`

Current pilot properties:

- `noindex,follow`;
- self-canonical;
- reciprocal PT/EN hreflang;
- visible breadcrumbs;
- `BreadcrumbList` structured data;
- page-specific title/description;
- normal links back to thematic vertical and exact Full Biography anchor;
- body generated from the same neutral fragment used by the vertical.

They are intentionally **not** in a mass-indexation rollout.

### Promotion rule

Changing a pilot to `index,follow` is a deliberate product/SEO decision, not a string edit.

The entry auditor is designed to prevent an indexable Chapter Page from silently existing as an orphan. A promoted page should have normal static internal linking and appropriate sitemap/index handling.

---

## 11. SEO/indexation constitution after PR #34

No mass indexation was authorized by the architecture merge.

Current strategy remains staged:

- Full Biography and AI/HAI are already indexable surfaces;
- building verticals can remain `noindex,follow` until they are editorially mature and intentionally promoted;
- Chapter Page pilots remain `noindex,follow` until explicit review;
- duplicate internal autobiographical content is a canonical/landing-page strategy question, not an automatic “Google penalty” claim;
- Full Biography and verticals should gradually differentiate by reader intent, not by amputating autobiography;
- Search Console evidence should inform later indexing decisions;
- do not create tag pages and Chapter Pages en masse in the same experiment.

Potential future differentiation remains a hypothesis:

- Full Biography → integrated chronology and cross-domain bridges;
- verticals → topical depth and field-specific organization;
- selective Chapter Pages → autonomous episodes that genuinely work as destinations.

Do not reverse the Full Biography=totality constitution merely because standalone entry URLs now exist.

---

## 12. Schema/metadata rules

Adopted direction:

- stable human-readable URLs;
- self-canonical when a page is genuinely autonomous;
- PT/EN hreflang;
- page-specific title/description;
- visible breadcrumbs + `BreadcrumbList` when useful;
- stable Person identity through Marcelo Nicchio's existing canonical `@id` where the person entity is referenced;
- structured data selected according to the actual object represented.

Explicitly not adopted as automatic rules:

- `meta keywords`;
- `Article` schema on every entry;
- forcing Marcelo as `mainEntity` when he is not the page's actual main entity;
- mass tag-page generation;
- mass Chapter Page generation;
- fixed word-count thresholds;
- `llms.txt` treated as a ranking promise.

---

## 13. Performance guardrails

Pre-Reader-UX browser baseline is preserved in:

`docs/lighthouse-baseline-2026-08-29.md`

Static page/image reporting is handled separately by `tools/audit_page_weight.py`.

Interpretation rules:

- static full-scroll potential is not initial network transfer;
- lazy-loaded archive/media totals do not equal first-load cost;
- the 4 MiB value used by the page-weight auditor is a review warning, not an editorial law;
- Lighthouse values are lab data, not CrUX field data;
- if one metric appears large enough to drive a product decision, repeat runs/compare medians before treating it as meaningful.

A normal-vs-`?ux=disclosure` Lighthouse follow-up remains useful, but it is measurement work, not a blocker for the already-green Reader UX browser regression suite.

---

## 14. Media architecture that remains in force

Raw historical masters stay preserved under archive paths.

Responsive/rendering derivatives remain separate delivery assets when appropriate.

Gallery infrastructure remains registered and audited through:

- `data/galleries.json`
- `tools/build_gallery_media.py`
- `tools/sync_galleries.py`
- `tools/audit_galleries.py`

Do not replace raw historical material merely to reduce delivery weight. Optimize the delivery representation instead.

Important semantic distinction:

- restored historical photograph → still a historical photograph, with restoration disclosure where editorially useful;
- AI-assisted reconstruction from memory → reconstruction/illustration, never evidence or an original historical photograph.

Goobec is the former. Minduim BBS is the latter.

---

## 15. Immediate authorial arc after architecture work

The next main autobiographical batch remains:

### Block 4 — 2012–2015

**Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto**

The architecture should reduce, not increase, the user's authoring burden.

When Block 4 prose arrives:

1. preserve the raw autobiographical account privately/editorially, including context that may not belong on the public site;
2. shape the PT vertical narrative human-first;
3. decide media function only after the narrative is clear;
4. create/review the deliberate EN equivalent;
5. run PT/EN parity review;
6. register stable entry metadata where useful;
7. migrate a chapter to a neutral fragment only if multiple public surfaces genuinely need the same body;
8. regenerate Full Biography;
9. run audits/browser regression;
10. branch → PR → green CI → merge → post-merge audit → Pages.

Do **not** make Marcelo rewrite a chapter separately for vertical, Full Biography and Chapter Page.

### Sensitive Block 4 reminder

For Ad.Dialetto, operational facts such as entering an operation with almost no retained team and rebuilding it from zero can be narrated autobiographically.

Do not casually publish a named accusation of moral harassment involving a third party. If context about a high-friction client environment is needed, handle it at an appropriate level of abstraction unless a later editorial/legal decision explicitly changes that treatment.

This is a privacy/reputational rule, not a source rule.

---

## 16. Later autobiographical batches

After Block 4, current working sequence remains:

- **Block 5 — 2016–2020:** independent work + *O Arquiteto da Apoteose*;
- **Block 6 — 2021–2024:** *Autópsia* + Driven.cx + Coitado reunion;
- **Block 7 — 2025–2026:** AI/HAI/HCI cycle.

These block numbers are workflow labels, not public site architecture.

Do not mix writing these blocks with a major simultaneous SEO/indexation redesign unless a concrete dependency requires it.

---

## 17. Current production validation

PR #34 merged as:

`09546426f96affc3b8988b6ddf731bfae6d78ad7`

Post-merge validation:

- Site Audit run #183 — success;
- GitHub Pages deployment #58 — success.

The permanent Site Audit now covers legacy audits plus entry-source synchronization, generated Chapter Pages, entry registry rules and Reader UX browser behavior.

If a future session changes architecture, keep the sequence:

1. start from current `main` HEAD;
2. use a dedicated branch;
3. keep diff scoped;
4. run existing sync/parity/media/entry/full-bio audits;
5. let Site Audit run the browser regression;
6. merge only green;
7. verify post-merge Site Audit;
8. verify Pages success;
9. only then call the change published.

---

## 18. What is still hypothesis, not constitution

Do not present these as settled requirements:

- converting every vertical into a short index page;
- making every important entry a standalone URL;
- making Chapter Pages the canonical source while Full Biography becomes only a summary;
- automatic topic/tag pages;
- fixed entry-length thresholds;
- permanent disclosure UX on normal URLs;
- automatic indexation of all mature-looking pages;
- removing historical media to chase an arbitrary page-weight number.

The current architecture exists precisely so these questions can be tested incrementally instead of answered ideologically.

---

## 19. Human-validation frontier

The next genuine human/UX decision is not “does the code work?” — CI already answers that.

The useful human questions are:

- does compact reading make a long biography easier to understand and continue reading?
- do the closed cards expose enough context without feeling like a dashboard?
- are topics/media indicators helpful or noisy?
- should the compact mode eventually become default, remain optional, or be redesigned?
- which individual episodes are truly worth autonomous Chapter Pages?

Until those questions are answered, preserve the opt-in flag and `noindex` pilot policy.

---

## 20. Document precedence for current implementation

For architecture/current-state conflicts, use this order:

1. explicit later decision by Marcelo;
2. current `main` implementation and green CI invariants;
3. this `CURRENT-HUB-STATE.md` snapshot;
4. `docs/entry-authoring-workflow.md` and `docs/entry-architecture-pilot.md` for PR-34 mechanics;
5. `docs/ux-seo-architecture-v1.md` for the design rationale that led to the implementation;
6. `docs/full-biography-workflow.md` for Full Biography/parity mechanics;
7. `docs/hub-continuity-guide.md` and older triangulation documents for broader historical context.

An older document does not regain authority merely because its wording is more confident or more detailed.
