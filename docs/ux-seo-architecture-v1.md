# UX + SEO architecture v1 — progressive biography

Status: **adopted implementation plan, not yet implemented on the live site**  
Reference date: 2026-08-29 (BRT)  
Baseline `main` at planning start: `c959fd2555fca7d39cbca8e8be8e9c9702730713` (PR #29 merged)

This document consolidates the three UX/SEO triangulation rounds and the decisions explicitly adopted by Marcelo Nicchio after review by Charlie (ChatGPT, implementation/Blue Team) and the external reviewer nicknamed Xará.

It exists to prevent a future session from confusing proposals, rejected hypotheses and implemented architecture.

---

## 1. Problem being solved

Two independent readers were asked to navigate first **Internet & Performance** and then the **Full Biography**. Both reported that the amount of continuously exposed material made it difficult to navigate the pages to the end.

The adopted diagnosis is **not** "the autobiography contains too much information". The problem is that the interface currently presents nearly all available depth as if it must be consumed at once.

The response is architectural:

> **Editorial totality does not require simultaneous visual exposure.**

The HUB preserves the complete autobiography while presenting it through progressive disclosure.

The existing constitutional rule remains valid:

> **Full Biography = totality. Verticals = thematic cuts.**

New complementary rule:

> **Totality means that the complete autobiographical content belongs to the work and remains accessible. It does not mean that every chapter, image and gallery must be visually expanded at first paint.**

---

## 2. Adopted UX model

### 2.1 Reader Pages

Reader Pages are broad navigation surfaces:

- Full Biography / Biografia Completa;
- Internet & Performance;
- Music;
- Audiovisual;
- Communication;
- AI/HAI when density eventually justifies it.

Dense Reader Pages will use progressive disclosure. The initial implementation target is:

1. **Full Biography PT/EN**;
2. **Internet & Performance PT/EN**.

Other verticals are evaluated after the pilot; the component must not become a universal visual dogma.

### 2.2 Native disclosure

Use native HTML `<details>` + `<summary>` for the first implementation.

Requirements:

- entries can start closed;
- multiple entries can remain open simultaneously;
- clicking an open entry closes it;
- keyboard operation remains available;
- basic behavior works without JavaScript;
- JavaScript is only an enhancement layer;
- do **not** use a grouping behavior that forces opening one chapter to close another.

The default state (all closed versus first entry open) remains a **UX test variable**, not a permanent rule. The preferred first variant is eras/context visible with entries closed, because the original complaint was excessive simultaneous density.

### 2.3 What remains visible when an entry is closed

Each closed card/disclosure should communicate enough to decide whether to open it:

- period/date;
- chapter title;
- short editorial summary explaining why the chapter matters;
- content indicators where meaningful (photos, videos, audio, documents);
- controlled topic labels;
- expand/collapse affordance;
- later, when a Chapter Page exists, a normal HTML link to that page.

The summary is a **doorway**, not a replacement for the chapter. No fixed word or character count is constitutional.

### 2.4 Content badges versus topic labels

These are separate concepts even if they share visual language.

**Content indicators** should eventually be machine-derived where possible:

- `22 fotos`;
- `4 vídeos`;
- `1 áudio`;
- `3 documentos`.

Do not hand-maintain counts when they can drift.

**Topic labels** are editorial taxonomy:

- `Google Ads`;
- `Search Marketing`;
- `SEM`;
- `CookieWEB`;
- etc.

Topic labels are not `meta keywords` and do not exist as a ranking trick.

---

## 3. Text, media and rendering rule

### 3.1 Text stays in delivered HTML

For indexable Reader Pages, the complete autobiographical text remains in the HTML delivered by the page.

The disclosure is visual. **Do not fetch the autobiographical text only after a user click.**

A previously considered future phase in which chapter text would be fetched on expansion is **explicitly rejected and removed from the roadmap**.

Reasons:

- the text is small relative to media payload;
- HTML-first content is robust for accessibility, search, archival use and non-JavaScript clients;
- there is no performance case strong enough to justify hiding the primary text behind interaction.

### 3.2 Images remain lazy by default

Existing responsive derivatives and `loading="lazy"` remain the baseline.

Dynamic materialization of gallery thumbnails is **not part of the first prototype**. It becomes eligible only if PageSpeed/Lighthouse, DOM behavior or browser testing demonstrates a concrete performance problem after progressive disclosure is implemented.

If later adopted, dynamic materialization applies to media, not the autobiographical text.

### 3.3 Master versus delivery derivative

Repository/archive weight and normal page-delivery weight are different metrics.

- historically important masters may remain preserved when there is an archival reason;
- public page rendering should prefer optimized WebP/JPEG derivatives;
- a master linked only for full-size inspection is not normal initial page payload;
- new ordinary photographs should preferably arrive in JPEG/WebP rather than losslessly bloating Git without archival benefit;
- PNG remains appropriate for transparency, text-heavy screenshots/graphics, or justified archival cases.

Do not rewrite Git history merely to recover a few already-committed megabytes.

---

## 4. Navigation behavior requirements

### 4.1 Open all / collapse all

Dense Reader Pages should provide:

- **Abrir todos / Open all**;
- **Recolher todos / Collapse all**.

This preserves a continuous-reading mode for readers who want the page to behave like a book.

### 4.2 Deep links and legacy hashes

Existing fragment URLs must keep working, including forms such as:

- `/pt/internet/#cookieweb`;
- `/pt/biografia/#bio-internet-cookieweb`.

When a URL targets an entry inside a closed disclosure, the enhancement layer should open the corresponding `<details>` and move focus/scroll appropriately.

Do not break existing IDs merely to implement the new visual component.

### 4.3 Ctrl+F / Find in page

Because browser behavior around matches inside closed `<details>` may vary, explicitly test Find-in-page on current Chrome, Firefox and Safari when available.

Do not build custom search preemptively. If real testing shows that native Find produces friction, then implement a local search that finds text inside a closed chapter and opens the relevant disclosure.

### 4.4 Print / Save as PDF

Printing and PDF export must reveal the complete biography regardless of current disclosure state.

Print behavior is a **prototype acceptance requirement**, not an optional future enhancement.

---

## 5. Chapter Pages

### 5.1 Purpose

A Chapter Page is a stable URL for an episode/project that is genuinely autonomous for:

- reading;
- search;
- citation;
- sharing;
- social preview;
- contextual linking.

A chronological Full Bio entry does **not** automatically deserve a separate URL.

No word-count threshold is constitutional.

### 5.2 Pilot candidates

The first four structural pilots are:

1. Coitado do Próximo;
2. Mirantte News;
3. CookieWEB;
4. Meia-Noite e Uns.

They stress different combinations of chronology, galleries, documents, video, credits and external sources.

### 5.3 URL model

Current preferred family for pilots is semantically nested under the primary vertical, for example:

- `/pt/internet/cookieweb/`;
- `/en/internet/cookieweb/`;
- `/pt/audiovisual/meia-noite-e-uns/`;
- `/pt/musica/coitado-do-proximo/`.

A previous `/pt/registros/.../` proposal is **not adopted**.

Published slugs are presumed stable.

If a chapter later changes thematic vertical, the old URL must remain indefinitely as a compatibility stub using the best redirect/canonical mechanism available rather than silently disappearing.

### 5.4 One indexed pilot

Creating four `noindex` Chapter Pages cannot test canonical selection or Search behavior.

Therefore the proposed experiment is:

- three pilot Chapter Pages initially `noindex,follow`;
- one pilot Chapter Page `index,follow` to create observable Search data.

Current preferred indexed pilot: **Meia-Noite e Uns**, subject to explicit confirmation at implementation time.

Do not use this pilot as permission to mass-index Chapter Pages.

---

## 6. Source-of-truth migration

### 6.1 Current model

Today the vertical HTML is the primary editorial source and Full Biography is synchronized from it.

This remains valid for entries without a Chapter Page.

### 6.2 New model for promoted entries

When an entry gains a Chapter Page, avoid creating a temporary extractor from the vertical that is known to be disposable.

Instead, migrate **that entry only** to a neutral shared source, provisionally:

```text
content/entries/pt/<entry>.inc
content/entries/en/<entry>.inc
```

That source can then feed:

```text
entry source
  ├─ vertical
  ├─ Full Biography
  └─ Chapter Page
```

Adopted migration rule:

> **The unique editorial source migrates by batch, together with the Chapter Pages that require it, and never as a mass rewrite.**

Entries not yet promoted may continue using the existing vertical-source workflow until their turn comes.

---

## 7. Verticals after Chapter Pages

Do **not** transform Internet & Performance or other verticals into thematic indexes before evidence shows that such a change is useful.

Initial state after UX pilot:

- Full Biography remains complete + progressively disclosed;
- Internet & Performance remains complete + progressively disclosed;
- Chapter Pages are added selectively.

A future vertical may become a more differentiated thematic index with original framing and cards, but this is a **post-pilot hypothesis**, not a prerequisite for Chapter Pages or indexing.

Search Console and UX evidence must justify that change.

---

## 8. Taxonomy / tags

### 8.1 Controlled vocabulary

A future `data/tags.json` or equivalent may define stable internal IDs and aliases, for example:

```json
{
  "id": "google-ads",
  "label": "Google Ads",
  "aliases": ["Google AdWords", "AdWords"]
}
```

Purpose:

- consistent visual chips;
- semantic relationships;
- contextual internal linking;
- future filtering;
- possible future thematic pages.

### 8.2 No automatic tag-page factory

Tags begin as data/chips.

A tag only gains an indexable page when the grouping itself provides enough editorial value to justify a destination beyond a mechanical list of links.

Rejected as constitutional rules:

- minimum exactly three entries;
- exactly 2–3 introductory paragraphs;
- fixed word counts.

Do not launch Chapter Pages and a large family of tag pages simultaneously. Preserve the ability to attribute Search effects to one architectural change at a time.

---

## 9. SEO / metadata principles

### Adopted

- stable, human-readable URLs;
- normal `<a href>` links to Chapter Pages;
- self-canonical Chapter Pages where appropriate;
- PT/EN `hreflang` parity;
- page-specific title and description;
- Open Graph / Twitter image and metadata for important Chapter Pages;
- visible breadcrumbs + `BreadcrumbList` where useful;
- stable `Person` `@id` for Marcelo Nicchio when structured data references the same person;
- schema chosen page-by-page according to the actual object represented;
- gradual indexing with Search Console observation.

### Explicitly not adopted

- `meta keywords`;
- automatic `Article` schema on every Chapter Page;
- forcing `mainEntity` to Marcelo when Marcelo is not the page's main entity;
- mass indexation;
- mass tag-page creation;
- using `llms.txt` as a ranking promise;
- rewriting content into arbitrary chunks because "AI requires it";
- numerical thresholds without observed data turning into editorial law.

`llms.txt` may remain as a low-cost experimental/agent-friendly map, but it is not treated as a core SEO invariant.

---

## 10. Performance measurement

### 10.1 Static page-weight auditor

`tools/audit_page_weight.py` reports static image payload and should remain **warning-first**, not a hard quality gate.

The 4 MiB value is a review indicator, not a law.

Its report should distinguish:

- HTML size;
- image count;
- `src` aggregate;
- maximum local `src/srcset` candidate aggregate;
- linked archival masters excluded from normal page-delivery measurement.

The report wording must explicitly state that lazy-loaded image totals represent **full-scroll potential**, not initial-load bytes.

### 10.2 Browser baseline

Before the UX prototype is merged, record baseline measurements for:

- Full Biography PT — mobile and desktop;
- Internet & Performance PT — mobile and desktop.

Prefer repeatable Lighthouse/PageSpeed values, including where available:

- Performance score;
- LCP;
- FCP;
- CLS;
- TBT / INP-related diagnostics as applicable;
- Speed Index;
- DOM diagnostics;
- transfer/resource diagnostics.

Lab data is the primary immediate before/after comparator. Field/CrUX data, when available, has a historical window and should not be interpreted as an instant deployment measurement.

Repeat the same protocol after the UX pilot and later after Block 4 integration.

---

## 11. Analytics

Do not add disclosure telemetry simply because it is possible.

Possible future events include `chapter_open`, `chapter_close`, `chapter_page_click` and `expand_all`, but instrumentation only enters when a clear decision is defined in advance that the resulting data can inform.

---

## 12. Audit strategy for the new architecture

Start with **one** new logical auditor, provisionally `tools/audit_entries.py`, rather than three separate scripts.

Initial responsibilities may include:

- registered entry source exists;
- PT/EN pair exists;
- summary exists;
- slug/path uniqueness;
- Chapter Page canonical/hreflang when applicable;
- Reader Pages still contain the required entry;
- no entry silently disappears during source migration;
- content indicator counts match registered media where automated counts exist.

Split the auditor only if its responsibilities become genuinely independent and large.

Existing Full Biography coverage/parity auditors remain authoritative for their current invariants.

---

## 13. Rollout order

### Phase 0 — documentation and baseline

- [x] consolidate architecture decisions in this document;
- [ ] reconcile stale continuity/media documentation;
- [ ] clarify page-weight report terminology;
- [ ] record reproducible static baseline;
- [ ] record browser/PageSpeed baseline where tooling permits.

### Phase 1 — disclosure UX prototype

Target only Full Biography PT/EN and Internet & Performance PT/EN.

Implement/test:

- `<details>/<summary>`;
- closed-card hierarchy;
- editorial summaries;
- content indicators/topic chips where available;
- open all / collapse all;
- deep-link auto-open;
- keyboard/focus behavior;
- reduced-motion compatibility;
- Ctrl+F behavior;
- print/PDF complete content;
- mobile layout.

No indexation changes in this phase.

### Phase 2 — human validation

Re-test with Marcelo and preferably the same external readers who reported the original density problem.

Do not tell testers what response is expected. Ask them to navigate again and observe whether they can understand the trajectory, choose chapters and continue farther through the page.

### Phase 3 — Chapter Page pilots

- define small entry registry/metadata structure;
- migrate only the four pilot sources to shared `.inc` files;
- create four PT/EN Chapter Page pairs;
- add page metadata, breadcrumbs and stable links;
- keep three pilots `noindex,follow`;
- expose one controlled `index,follow` pilot after explicit review;
- introduce `audit_entries.py`.

### Phase 4 — observe

Use:

- Search Console;
- PageSpeed/Lighthouse;
- manual UX;
- canonical/index observations;
- browser behavior.

Do not infer a site-wide answer from theory alone.

### Phase 5 — decide vertical differentiation

Only now decide whether any vertical should become a more differentiated thematic index rather than a complete thematic Reader Page.

### Phase 6 — later taxonomy/tag pages

Only after Chapter Pages and Search behavior are understood.

---

## 14. Relationship to autobiographical Blocks 4–7

The architecture project freezes **integration into an unstable old/new container**, not autobiographical writing.

Marcelo may write Blocks 4–7 at any time.

The safest project sequence remains:

1. finish/document the UX/SEO container;
2. integrate new autobiographical material using the settled model;
3. avoid writing the same chapter manually into multiple surfaces.

Block 4 remains Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto.

Sensitive third-party conduct is an editorial/privacy/reputational question, not a source-availability question.

---

## 15. Explicit non-goals for this migration

Do **not** use this architecture project to:

- shorten the autobiography merely because it is long;
- rewrite all existing content;
- reopen the publicability/source constitution;
- redesign the whole visual identity;
- index every vertical;
- generate dozens of Chapter Pages;
- generate tag pages;
- migrate every entry to `.inc` in one operation;
- rework Git history to reduce archived image weight;
- remove historical media because performance might become a problem;
- invent fixed word-count rules;
- treat SEO hypotheses as editorial commands.

---

## 16. Tonight / next-agent safe worklist (no new autobiography required)

This is the deliberately low-risk batch that may proceed without Marcelo writing new biographical prose:

1. **Documentation reconciliation**
   - update `docs/visual-archive-plan.md` with master-versus-delivery rules;
   - update continuity documentation so PR #28/#29, page-weight audit and the UX/SEO v1 plan are not invisible to a future session;
   - preserve older documents as historical snapshots where appropriate rather than silently rewriting their original meaning.

2. **Auditor semantics**
   - rename page-weight report language from ambiguous `estimated` wording to explicit full-scroll potential wording;
   - state clearly that lazy-loaded totals are not initial-load bytes;
   - retain 4 MiB as warning-only.

3. **Technical baseline**
   - record current `main` SHA;
   - capture Full Biography and Internet static image/HTML totals with the auditor;
   - capture current image counts;
   - if reliably obtainable, capture Lighthouse/PageSpeed baseline without changing the site.

4. **Prototype preparation, branch only**
   - only if documentation and baseline are complete;
   - no merge to `main` without UX review;
   - no robots/indexing changes;
   - no `.inc` migration yet;
   - prefer a draft PR if implementation begins so the work cannot be mistaken for production-ready architecture.

If the session stops after any item, this document is the handoff point. Do not reconstruct the plan from conversation memory.

---

## 17. Decision hierarchy

When future sources disagree, use this order for this migration:

1. explicit later decision by Marcelo;
2. current repository implementation;
3. this UX/SEO architecture v1 document for the planned migration;
4. Dossiê de Legado 2 for broader HUB constitution/history;
5. older continuity/triangulation documents as historical context.

A proposal in an older triangulation does not become adopted merely because it was written confidently.
