# HUB continuity addendum — 2026-08-29

Status: **current addendum to `docs/hub-continuity-guide.md`**  
Planning baseline `main`: `c959fd2555fca7d39cbca8e8be8e9c9702730713`

The original continuity guide remains historically useful, but several sections describe the repository as it existed on 27 August 2026. This addendum records later constitutional and technical decisions without pretending that the older document was written in the current state.

If this addendum conflicts with an older status statement, use the newer explicit decision here or the current repository implementation.

---

## 1. Permanent autobiographical publicability rule

The HUB is an autobiography, not a proof site.

Permanent rule:

> **Information with a useful source → publish the information and the source.**  
> **Autobiographical information without an external source → publish the information normally without inventing a disclaimer.**

Absence of external corroboration is not, by itself, a reason to exclude routine autobiographical memory or add phrases such as “according to Nicchio”, “could not be independently confirmed” or “no documentation is known”.

Separate issues remain separate:

- privacy;
- copyright;
- uncertainty in the author's own memory;
- reputational/legal exposure involving identifiable third parties.

Those can justify different editorial treatment. They must not be confused with a generic lack-of-source gate.

---

## 2. Full Biography status

The Full Biography is already published in PT/EN and synchronized from registered editorial units.

Constitution remains:

> **Full Biography = totality. Verticals = thematic cuts.**

A new complementary UX rule was adopted during the 28–29 August triangulation:

> **Editorial totality does not require simultaneous visual exposure.**

The complete autobiographical text remains part of the Full Biography, but dense chapters may be progressively disclosed in the interface.

The implementation plan is now documented in:

`docs/ux-seo-architecture-v1.md`

Do not revive earlier proposals in which the Full Biography automatically becomes only summaries + links merely because Chapter Pages are introduced.

---

## 3. Planned progressive-disclosure architecture

This is **planned, not yet live** at the date of this addendum.

First pilot targets:

- Full Biography PT/EN;
- Internet & Performance PT/EN.

Adopted design direction:

- native `<details>/<summary>`;
- complete text remains in delivered HTML;
- multiple chapters may remain open;
- `Open all / Collapse all` enhancement;
- existing deep links continue to resolve and should open their closed disclosure;
- Ctrl+F behavior is explicitly browser-tested;
- print/PDF must expose complete content;
- no robots/indexation change during the UX prototype.

Rejected design:

- fetching the primary autobiographical text only after the reader clicks to expand a chapter.

Dynamic materialization may later be evaluated for gallery media only if real performance data justifies it.

---

## 4. Chapter Pages — future selective layer

A Chapter Page is not created for every chronological unit.

Eligibility is qualitative: the subject should be autonomous enough for reading, search, citation and sharing.

First structural pilot candidates:

- Coitado do Próximo;
- Mirantte News;
- CookieWEB;
- Meia-Noite e Uns.

Preferred URL pattern is currently vertical-nested and human-readable, e.g. `/pt/internet/cookieweb/`.

A published URL should be treated as stable. If thematic classification changes, preserve the old URL as a compatibility path rather than silently deleting it.

Current proposed Search experiment: three pilot Chapter Pages `noindex,follow`, one controlled `index,follow` pilot after explicit review. This is not permission for mass indexation.

---

## 5. Source-of-truth migration rule

Current entries may continue using the existing model:

```text
vertical HTML → Full Biography sync
```

When an entry is actually promoted to a Chapter Page, migrate **that entry only** to a neutral shared source, provisionally:

```text
content/entries/pt/<entry>.inc
content/entries/en/<entry>.inc
```

which then feeds vertical + Full Biography + Chapter Page.

Permanent migration principle:

> **The unique editorial source migrates by batch, together with the pages that require it, and never through a mass rewrite merely for architectural purity.**

---

## 6. Verticals and indexation

Do not revert to the earlier proposal that all thematic verticals must remain permanently `noindex` because Full Biography contains their text.

Current policy remains gradual:

- Full Biography: indexable;
- AI/HAI: already an indexable mature thematic surface;
- other verticals: indexation evaluated progressively as content/architecture matures;
- Search Console and actual query behavior guide later decisions.

At the same time, do not transform Internet & Performance into a thematic index before the new UX/Chapter Page pilot produces evidence that such a change is useful.

“Vertical becomes index” is a **post-pilot hypothesis**, not an adopted migration step.

---

## 7. Goobec correction — completed

The restored 2009 Goobec class photograph was initially placed too low in the CookieWEB/GAP certification passage.

It has been corrected and belongs to the earlier **2008–2009 Search professionalization** section, alongside the Goobec course narrative, João Dalla and the meeting with Herik Mourão.

Do not move it back beside the GAP certificate records.

---

## 8. Folhateen correction — completed

The three archival scans that incorrectly carried `23-04-2000` in their filenames were renamed to the correct date:

**23-04-2001**.

Published chronology, official Folha references and the optimized derivative already used 2001.

The filename trap should therefore no longer be treated as an unresolved issue.

---

## 9. Page-weight auditor

`tools/audit_page_weight.py` now exists and is included in CI.

Important semantics:

- it measures static **full-scroll image potential**, not initial-load browser transfer;
- `loading="lazy"` means the page does not necessarily fetch all of those bytes at first paint;
- `full-scroll-src` represents the aggregate of local files named in `src`;
- `full-scroll-max` represents the larger local candidate per image across `src`/`srcset`;
- archival masters linked only through `<a href>` are excluded from normal page-delivery weight;
- 4 MiB remains a **review warning**, not a constitutional hard failure threshold.

Do not reinterpret the warning as evidence that a reader downloads the full aggregate immediately.

---

## 10. Archive master versus delivery derivative

The distinction is now documented in `docs/visual-archive-plan.md`.

Summary:

- preservation format and web-delivery format serve different jobs;
- archival masters may remain where historically justified;
- ordinary rendering should use optimized derivatives where appropriate;
- new ordinary photography should avoid unnecessary lossless PNG bloat;
- do not rewrite repository history merely to recover already-committed small amounts of storage.

---

## 11. Current authorial roadmap

The next unpublished authorial block remains:

**Block 4 — 2012–2015: Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto.**

Writing and integration are distinct:

- Marcelo may write Block 4 at any time;
- do not force new autobiographical material into a container actively being restructured;
- once the UX container is settled, integrate the block using the current single-source/parity/sync discipline.

No new source requirement is introduced for Block 4.

Third-party conduct, especially potentially defamatory/reputational material, requires careful editorial framing even when Marcelo remembers the events clearly. This is a privacy/reputational constraint, not a contradiction of the autobiographical source rule.

---

## 12. Recent repository milestones after the old guide

- PR #24 — chronological Full Biography PT/EN + parity/sync/coverage infrastructure;
- PR #25 — Block 3A expansion, Mirantte/CookieWEB media;
- PR #26 — Folhateen cover integrated;
- PR #27 — Folhateen responsive sizing;
- PR #28 — Goobec class photograph introduced;
- PR #29 — Goobec moved to correct 2008–2009 section, Folhateen archival filenames corrected, Full Biography social preview added, page-weight auditor added.

Planning baseline after PR #29:

`c959fd2555fca7d39cbca8e8be8e9c9702730713`

---

## 13. Documents to read before the next structural implementation

1. `docs/ux-seo-architecture-v1.md` — current UX/SEO migration plan;
2. this addendum — current constitutional/status corrections;
3. `docs/full-biography-workflow.md` — current Full Bio mechanics until source migration begins;
4. `docs/visual-archive-plan.md` — media/archival policy;
5. `docs/hub-continuity-guide.md` — broader historical constitution, interpreted with this addendum;
6. Dossiê de Legado 2 — broader snapshot, noting it predates PR #28/#29 and the UX/SEO triangulation.

Before writing to the repository, always refetch `main` because Marcelo may upload assets directly between sessions.
