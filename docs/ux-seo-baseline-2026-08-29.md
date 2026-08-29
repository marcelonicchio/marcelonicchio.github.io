# UX/SEO technical baseline — before progressive disclosure

Reference date: 2026-08-29 (BRT)  
Production baseline commit: `c959fd2555fca7d39cbca8e8be8e9c9702730713`  
Purpose: preserve the pre-UX state so progressive-disclosure work can be compared against an explicit baseline rather than memory.

---

## 1. Static baseline already observed on current production state

The page-weight auditor introduced in PR #29 reported the following order of magnitude for the two main dense surfaces:

| Surface | Image count / state | `src` aggregate | max `src/srcset` aggregate | Interpretation |
|---|---:|---:|---:|---|
| Full Biography PT | 91 images, lazy-loaded | ~3.64 MiB | ~5.76 MiB | potential extended/full-scroll payload, **not initial-load bytes** |
| Internet & Performance PT | dense image surface | ~2.60 MiB | ~4.42 MiB | potential extended/full-scroll payload, **not initial-load bytes** |

Full Biography HTML was approximately 116 KiB / roughly 5.2k words at this stage. The exact byte count can vary slightly with metadata edits; the important baseline distinction is text/HTML versus media payload.

The auditor threshold is 4 MiB **warning-only**. It is a review indicator, not a pass/fail performance law.

The updated auditor terminology on the planning branch is:

- `full-scroll-src` — aggregate local files referenced as `src`;
- `full-scroll-max` — for each image, the largest local candidate present across `src` / `srcset`;
- linked archival masters are excluded from normal page-delivery totals.

Because images are lazy-loaded and browsers use loading heuristics, neither aggregate should be described as what a visitor downloads at first paint.

---

## 2. What this baseline does and does not measure

### It measures

- static HTML file size;
- number of `<img>` elements;
- local image assets referenced by `src`;
- maximum local responsive candidate represented by `src/srcset`;
- a reproducible repository-side warning threshold.

### It does not measure

- actual browser initial transfer;
- decoded bitmap memory;
- DOM layout cost;
- interaction latency;
- LCP/FCP/CLS/INP/TBT;
- browser lazy-load distance heuristics;
- cache behavior;
- field performance on a real user's device/network.

Therefore static page weight and Lighthouse/PageSpeed are complementary, not substitutes.

---

## 3. Browser baseline still required before UX merge

Before merging the progressive-disclosure prototype, capture controlled **mobile and desktop** measurements for:

1. `/pt/biografia/`;
2. `/pt/internet/`.

Record at minimum when available:

- Performance score;
- LCP;
- FCP;
- CLS;
- TBT / relevant interaction diagnostic;
- Speed Index;
- DOM size/complexity warnings;
- resource/transfer diagnostics;
- whether CrUX field data exists for the URL/origin.

Use Lab data for immediate before/after comparisons. CrUX field data has a historical window and must not be read as an instant reflection of a just-published change.

### Tooling status in this planning session

A reproducible PageSpeed/Lighthouse run was **not recorded from the assistant environment** before this file was created. The environment used for repository work did not expose a reliable browser/PageSpeed execution path. This is deliberately recorded as a pending measurement rather than replaced with an estimated score.

Do not fill this section later from memory. Record actual output from a reproducible run.

---

## 4. UX baseline — observed human problem

Before progressive disclosure, two independent readers were asked to navigate Internet & Performance and then Full Biography.

Both reported that the continuously exposed amount of text/material made it difficult to navigate/read the pages to completion.

This is the empirical UX problem the prototype is intended to address.

The test did **not** establish that chapters are individually over-written or that autobiographical content should be cut. The intervention being tested is presentation architecture.

---

## 5. Post-prototype comparison protocol

After the disclosure prototype is implemented but before broad rollout:

1. run the same static auditor;
2. run the same Lighthouse/PageSpeed protocol;
3. repeat navigation tests with Marcelo and, preferably, the same external readers;
4. test `Ctrl+F` / Find in Page;
5. test deep links to closed entries;
6. test keyboard expansion/collapse;
7. test `Open all / Collapse all`;
8. test print / Save as PDF for complete content;
9. test mobile viewport behavior.

Only then decide whether further performance engineering such as dynamic gallery materialization is warranted.

---

## 6. Baseline preservation rule

Do not overwrite this file with post-UX numbers.

Create a separate post-prototype measurement document so the before/after record remains independently inspectable.
