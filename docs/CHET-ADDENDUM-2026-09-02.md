# Chet addendum — 2 Sep 2026

This is a short continuity addendum after PR #64. It does not replace `CURRENT-HUB-STATE.md` or the Duke legacy dossier; a consolidated documentation rewrite should wait until several more implementation cycles have landed.

## Baseline inherited

Chet begins from `main` after PR #64 (`6896f90805765c0040147fbc060417c5ec5bacff`). The Communication + Audiovisual fusion is complete. The combined vertical uses **Mídia & Cultura / Media & Culture** in navigation and **Cultura & Audiovisual / Culture & Audiovisual** as its editorial H1. Rich collapsed summaries for Mirantte News, CookieWEB and Meia-Noite e Uns are scoped to Full Biography; Melissa retains its existing rich-summary behavior.

## Duke roadmap status clarified

Completed before handoff:

- metadata/Lighthouse foundation batch;
- permanent URL/stub policy;
- Communication + Audiovisual structural fusion;
- permanent Search/Performance compatibility stubs;
- rich-summary rollout for selected dense Full Biography entries.

Still pending after the handoff:

- standalone Chapter Pages for Mirantte News, CookieWEB and Meia-Noite e Uns;
- the BEST/Kenshoo indexation experiment (the page already exists but remains `noindex,follow`);
- substantive entity prose for `/`;
- promotion of historical thematic verticals to `index,follow`;
- any decision to change Full Biography robots.

## Operator decisions received 2 Sep 2026

The following later decisions override older staging language where necessary:

1. `/` is intended to be the strongest human-readable entity page for the query **Marcelo Nicchio** and will remain indexable. Marcelo will provide substantive autobiographical/entity prose separately; the final page is not constrained to only three or four paragraphs.
2. Mature thematic verticals are also intended to become `index,follow` after the root entity page is strengthened. Promotion must update robots, sitemap and the audit whitelist atomically in PT/EN.
3. Full Biography remains `index,follow` until Marcelo gives an explicit later decision after triangulation. Do not infer or automate a `noindex` change.
4. Reader featured-card colors are not approved aesthetically even though collapsed/open state behavior is correct. Color work is deferred to a joint visual session.
5. Current rich-summary cover choices are not final. Marcelo will select replacement images; do not substitute them autonomously.
6. Two label families remain intentionally distinct: neutral topic/taxonomy chips describe what an entry is about; red content indicators describe what resources exist inside it.
7. Coitado do Próximo will become a larger visual-archive workstream. When video frames are used, retain raw frame provenance/timestamp separately from treated versions; AI reconstruction remains clearly identified as illustration rather than historical evidence.

## C0 sanitation completed on branch

- corrected the three active Folhateen gallery master filenames from `23-04-2000` to the verified publication date `23-04-2001` and regenerated every managed surface that references them;
- reaccepted the affected PT/EN parity checkpoint and regenerated Full Biography and the Folhateen Chapter Pages;
- removed stale global `<lastmod>2026-08-24</lastmod>` values from `sitemap.xml` instead of replacing them with fabricated freshness dates;
- added a gallery-audit guard against reintroducing the Folhateen 2000 filename regression;
- added dedicated browser smoke coverage for English rich summaries, because registry parity alone did not verify that Mirantte, CookieWEB, Meia-Noite e Uns and Melissa actually render their EN compact cards correctly.

## Next implementation sequence

1. C1 — promote Mirantte News, CookieWEB and Meia-Noite e Uns to neutral shared fragments and generated PT/EN Chapter Pages, without indexing them yet.
2. C2 — extend Chapter Page architecture to the HAI domain and prepare Melissa for a standalone URL.
3. C3 — strengthen BEST/Kenshoo editorially and prepare its controlled indexation pilot.
4. C4/C5 — after Marcelo supplies the root entity prose, expand `/` and then promote mature thematic verticals to `index,follow` with sitemap/auditor changes.
5. Reader colors, preview-image replacement, Coitado archive and missing entry prose remain separate workstreams with operator input where noted.
