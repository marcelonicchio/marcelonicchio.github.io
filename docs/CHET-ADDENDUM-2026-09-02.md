# Chet addendum — 2 Sep 2026

**Historical bridge document.** This file captured the handoff immediately after PR #64 and before Chet C1–C3. It is preserved for rationale only.

For current operational state, read **`docs/CURRENT-HUB-STATE.md`** first.

## What this addendum originally captured

At the start of Chet's cycle:

- Communication + Audiovisual had already been fused into Mídia & Cultura / Media & Culture;
- Mirantte, CookieWEB and Meia-Noite had rich Full Biography summaries but no standalone Chapter Pages;
- Melissa still used the earlier compact treatment on AI/HAI;
- BEST/Kenshoo existed as a `noindex,follow` Chapter Page candidate;
- stale global sitemap `lastmod` values still required sanitation;
- Home/entity prose and later vertical indexation remained future work.

## What happened afterward

### C0 — sanitation

- corrected active Folhateen filenames to the verified 23 Apr 2001 publication date;
- regenerated managed gallery surfaces;
- removed fabricated global sitemap `lastmod` values;
- added regression guards and EN rich-summary browser smoke.

### C1 — dense Chapter Pages

- promoted Mirantte News, CookieWEB and Meia-Noite e Uns to neutral fragments;
- generated PT/EN Chapter Pages;
- added generic title permalinks;
- fixed the Full Biography generator so title normalization preserves nested permalinks.

### C2 + C2.1 — Melissa

- added HAI support to Chapter Page generation;
- promoted Melissa to fragment-backed PT/EN Chapter Pages;
- changed AI/HAI so Melissa remains completely open there while the Full Biography can still use the compact summary.

### C3 — BEST/Kenshoo

- strengthened copy using already documented facts only;
- promoted BEST/Kenshoo PT/EN Chapter Pages to `index,follow`;
- added both URLs to sitemap and the indexable audit set.

## Operator decisions that remain current

- `/` is intended to become the strongest human-readable entity page for **Marcelo Nicchio**; Marcelo will provide the substantive prose separately.
- Mature thematic verticals are intended to become `index,follow` after the root entity page is strengthened.
- Full Biography remains `index,follow` unless Marcelo later explicitly changes that decision.
- Featured-card colors are technically functional but aesthetically unresolved and require collaborative review.
- Current Mirantte/CookieWEB/Meia-Noite rich-summary cover images are not final operator-approved selections.
- Neutral topic chips and red internal-content indicators remain semantically distinct.
- Coitado do Próximo remains a later archive workstream with raw-frame/timestamp provenance separated from treated derivatives and AI reconstructions labeled as illustration.

This addendum no longer carries a live roadmap. `CURRENT-HUB-STATE.md` and current `main` are authoritative for implementation status.
