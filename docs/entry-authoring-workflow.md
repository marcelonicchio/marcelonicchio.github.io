# Entry authoring workflow — Reader Pages, Full Biography and Chapter Pages

**Status:** operational workflow  
**Reference:** 1 Sep 2026 (BRT)

This document explains how autobiographical material enters the HUB in the current architecture. Its purpose is to keep future sessions focused on Marcelo Nicchio's memory, narrative and editorial judgment instead of rebuilding the site pipeline from scratch.

For current Reader summary design, also read `docs/reader-summary-model.md`.

---

## 1. Human narrative still comes first

The repository architecture exists to reduce duplicate work, not to make Marcelo write for a data model.

For a new or substantially expanded episode:

1. preserve the raw autobiographical account privately/editorially while shaping it;
2. write/review the canonical PT thematic entry;
3. create/review the deliberate EN equivalent;
4. compare PT↔EN factual/editorial meaning;
5. accept the parity checkpoint for the affected entry;
6. regenerate Full Biography;
7. add/update registry metadata when it is mature enough to be useful;
8. associate media/resources only after their editorial function is clear;
9. run the complete audit suite;
10. branch → PR → green CI → merge → post-merge Site Audit → Pages confirmation.

Do not make Marcelo manually maintain the same complete episode in a vertical, Full Biography and Chapter Page.

---

## 2. Two valid editorial source states

There is no requirement to migrate every existing entry into `.inc` fragments.

### State A — Reader-section source

Most entries can remain authored directly in the thematic vertical.

```text
PT/EN thematic vertical
        │
        └─ sync_full_biography.py → Full Biography
```

Use this when:

- the chapter is still evolving;
- there is no standalone Chapter Page;
- forcing a neutral fragment would create machinery without real reuse.

The entry may still be registered in `data/entries.json` for summaries, taxonomy, presentation state, media/resource metadata and future Chapter Page candidacy.

### State B — neutral fragment source

Promote an entry to a neutral shared source only when the same complete body genuinely needs to feed more than one generated public surface.

```text
content/entries/<lang>/<entry>.inc
        │
        ├─ sync_entries.py → thematic vertical
        │                      │
        │                      └─ sync_full_biography.py → Full Biography
        │
        └─ build_chapter_pages.py → selective Chapter Page
```

Migration is **per entry**, never a repository-wide architectural purity exercise.

Current examples: Folhateen and BEST/Kenshoo.

---

## 3. Registering an entry

A normal chapter record may include:

- stable `id`;
- `kind`;
- thematic `domain`;
- PT/EN date/period;
- PT/EN title;
- PT/EN compact `summary`;
- controlled `topic_ids`;
- `reader_presentation` state;
- optional structured `reader_preview` for rich collapsed summaries;
- media/resource associations;
- PT/EN Reader targets;
- source mode;
- Chapter Page status/path/indexing policy.

Do not create registry filler simply because a chapter exists. Weak placeholder metadata eventually becomes weak public interface copy.

---

## 4. `summary` and `reader_preview` are different layers

### `summary`

The ordinary `summary` field is concise reusable metadata. It is appropriate for standard Reader excerpts, Chapter Page framing and entry-level description.

It should explain why an episode matters rather than mechanically copying the first sentence.

### `reader_preview`

Use a structured `reader_preview` only for dense entries whose collapsed state needs to work as a **short autonomous version of the complete post**.

A rich preview may contain:

- optional cover/editorial image;
- multiple concise paragraphs;
- selective strong emphasis;
- curated internal-content indicators.

Topic labels remain `topic_ids`, outside the preview, because they belong to the entry itself rather than one visual state.

Melissa 1.0 is the accepted pilot/reference implementation.

### Rich-preview text budget

For paragraph text inside `reader_preview`:

- maximum = **1,650 visible-copy characters per language**;
- normal design target = roughly **1,300–1,320 characters**;
- shorter is fine;
- do not pad copy to reach a quota.

The ceiling reflects the calibrated Melissa mobile/desktop result. It is enforced by `tools/audit_entries.py`.

Title/date/tags/indicators/CTA do not count toward the preview-copy ceiling.

See `docs/reader-summary-model.md` for the complete rationale and visual/semantic rules.

---

## 5. Topic labels versus internal-content indicators

These are separate systems.

### Topic labels

Source: `topic_ids` → `data/tags.json`.

Purpose:

- human scanning;
- vocabulary consistency;
- future relationships/filtering/internal links;
- future standalone-page/SEO planning.

They are **not** meta keywords and do not automatically create tag pages.

Current rich-summary styling uses a neutral light/translucent chip surface.

### Internal-content indicators

Purpose: tell the reader what useful material exists inside the expanded entry.

Examples:

- photos/images;
- videos;
- audio;
- download links;
- DOI documents;
- repository links.

Prefer machine-derived counts when the DOM/media registry can express the content accurately. Use curated indicators when automatic counting cannot describe the resource meaningfully.

Current rich-summary indicators use the red visual family and must remain visually distinguishable from topic taxonomy.

---

## 6. Reader presentation state

`reader_presentation.state` supports:

- `normal`;
- `always-open`;
- `featured`.

The state belongs in data, not in CSS selector hacks.

`always-open` is **Type 1**: the entry remains ordinary open HTML in the Thread and does not participate in `<details>`, top/bottom expand-collapse CTAs, or global Open all / Collapse all controls. It is scroll-only. Topic taxonomy may remain registered as data without requiring extra visible controls.

Current examples:

- Minduim/BBS → `always-open`;
- Folha de S.Paulo / “Órfãos do Rock” → `always-open`;
- Mirantte News → `featured`;
- CookieWEB → `featured`;
- Meia-Noite e Uns → `featured`.

Presentation state and rich preview are independent dimensions: a future featured entry may or may not use a rich `reader_preview`.

---

## 7. Which Reader surfaces transform by default

### Default compact/disclosure

- Full Biography PT/EN;
- Internet & Performance PT/EN.

### Query-flag laboratory

- Communication PT/EN;
- Audiovisual PT/EN.

### Selective AI/HAI mode

AI/HAI remains openly rendered by editorial rule. Only explicitly selected entries are transformed.

Currently only Melissa 1.0 uses the rich collapsed/expanded model on AI/HAI. PRO v2, PRO v1, the research-cycle opener and research identity remain open.

Do not generalize blanket disclosure to IA/HAI unless Marcelo explicitly changes that rule.

---

## 8. Full Biography synchronization

The Full Biography is totality, not a summary layer.

After any editorial change to a registered biographical entry:

```bash
python tools/editorial_parity.py --check
python tools/editorial_parity.py --accept ENTRY_ID   # after actual PT/EN review
python tools/sync_full_biography.py
python tools/audit_full_biography.py
```

Exact command order may vary when other generators are involved, but the invariant does not: Full Bio must end synchronized and parity must be explicitly accepted.

Do not hand-edit its managed chronological region.

---

## 9. Topic taxonomy

`data/tags.json` is controlled vocabulary for:

- Reader chips;
- semantic relationships;
- future filtering/internal linking;
- future standalone-page planning.

Add a topic only when it is a durable concept. Prefer an existing stable term over near-duplicates.

Do not create public tag URLs automatically.

Melissa currently establishes/reuses:

- AI;
- HAI;
- HCI;
- Prompt Engineering;
- Melissa 1.0.

---

## 10. Composite subjects across chronology

Use a `landmark-set` when one semantic subject legitimately spans multiple chronological chapters and does not need to become a new artificial chapter.

Canonical example: Goobec/GAP.

Training stays in the Search-professionalization portion of the Internet chronology; GAP certifications stay in the CookieWEB period; the registry relates them without moving either event.

This pattern also fits recurring tools, certifications, collaborations or themes.

---

## 11. Promoting an entry to a Chapter Page

A Chapter Page is selective and must be genuinely autonomous for some combination of:

- reading;
- citation;
- sharing;
- search intent;
- social preview;
- contextual linking;
- concentrated records/archive.

There is no automatic word-count rule.

Promotion procedure:

1. extract the existing complete PT/EN bodies (not their `<h2>` headings) into neutral fragments;
2. change `source.kind` to `fragment`;
3. register exact PT/EN fragment paths;
4. set Chapter Page status to `pilot`;
5. keep `noindex,follow` unless an explicit indexation experiment has been approved;
6. run `sync_entries.py`;
7. review the verticals;
8. refresh affected parity checkpoints;
9. regenerate Full Biography;
10. build Chapter Pages;
11. run all audits/browser tests.

Current generated pilot pairs: Folhateen and BEST/Kenshoo.

---

## 12. Chapter Page indexing states

### `candidate`

Possible future page. It must not already exist as an indexable public destination.

### `pilot`

Generated structural page. Default remains `noindex,follow`.

### controlled `index,follow`

Requires explicit SEO/editorial approval, static internal links, sitemap review and later Search Console observation.

One controlled indexation pilot is desirable eventually because an all-noindex experiment cannot produce index/canonical observation data. That is not permission for mass promotion.

---

## 13. Media authoring rules

Distinguish:

1. **editorial thread image** — integrated into narrative flow;
2. **associated record gallery** — one to many images below a record, using registered gallery infrastructure.

Preserve originals/masters where justified and serve appropriate delivery derivatives.

AI-assisted historical restoration and AI reconstruction from memory are not the same category:

- restoration of a historical photo remains a historical photo;
- reconstruction from memory is an illustration and must not be described as evidence.

Do not require public evidence-class bureaucracy for ordinary personal/editorial photographs.

---

## 14. Reader/UX checks

The Reader must continue to protect:

- complete text in delivered HTML;
- deep-link auto-open;
- multiple entries open independently;
- keyboard behavior;
- print expansion;
- no-JS fallback;
- mobile layout/no horizontal overflow;
- rich preview hidden after expansion;
- full body preserved;
- topic/indicator rendering;
- rich-preview character ceiling.

Do not weaken a meaningful smoke assertion just to make CI green. If a test is brittle, replace it with a better behavioral assertion.

---

## 15. Known next editorial/UX work

### Summary rollout

Use Melissa as the flexible reference for other dense entries. High-value candidates include Mirantte News, CookieWEB and Meia-Noite e Uns.

Do not clone the same paragraph count or image composition blindly.

### CookieWEB naming

The eventual public thread title should center **CookieWEB**, not “Beleza na Web e CookieWEB”. Beleza na Web remains an important internal subphase/subtitle and narrative element.

### Featured-card color problems

Still unresolved and intentionally separate from the summary model:

1. yellow should become a clearer pale yellow rather than beige;
2. red should become more genuinely red/translucent rather than wine;
3. colored featured treatment should apply to the collapsed invitation state and revert to the normal dark background after expansion.

Button-border removal and further typography changes remain test ideas, not adopted rules.

---

## 16. Required repository discipline

Before writes, refetch current `main` because assets may be uploaded manually between sessions.

Keep the sequence:

1. current main;
2. branch;
3. scoped change;
4. relevant generators/audits;
5. PR;
6. green Site Audit;
7. merge;
8. post-merge Site Audit;
9. Pages build/deploy success;
10. only then call it published.
