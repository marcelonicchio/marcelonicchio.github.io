# Progressive-disclosure UX prototype harness

Status: **experimental branch-only implementation**  
Base: `5cd97c1565367e18572169aa8b71ca6aea677b50` (PR #30)

This document describes the cheap test harness used before changing canonical authoring/generation markup.

The accepted production architecture remains defined by `docs/ux-seo-architecture-v1.md`.

---

## 1. Why this harness exists

The immediate question is human UX:

> Does progressive disclosure make Full Biography and Internet & Performance materially easier to navigate without shortening the autobiography?

Answering that question does not require prematurely rewriting the source-of-truth pipeline.

The current Full Biography managed region must not be hand-edited, and Internet remains an editorial source surface. Therefore this prototype operates as **progressive enhancement on the already-delivered HTML**.

---

## 2. Activation

Normal URLs remain unchanged.

Prototype activation is explicit via query parameter:

```text
/pt/biografia/?ux=disclosure
/en/biography/?ux=disclosure
/pt/internet/?ux=disclosure
/en/internet/?ux=disclosure
```

Without `?ux=disclosure`, the experimental module does nothing and the existing interface remains byte-for-byte/content-equivalent in behavior except for the dormant loader check.

---

## 3. Prototype mechanism

The existing gallery/lightbox JavaScript is already included on the four target pages.

On the four target paths only, and only when `ux=disclosure` is present, it may load a separate experimental module:

`assets/js/progressive-disclosure-prototype.js`

The module:

1. leaves all autobiographical text in the original delivered HTML;
2. restructures eligible chapter sections in the browser into native `<details>/<summary>` elements;
3. does not fetch chapter text;
4. does not change robots/canonical/hreflang;
5. does not create Chapter Pages or tags;
6. does not change the normal non-prototype view.

This is deliberately a **test harness**, not the final source-markup implementation.

If the UX is approved, the accepted production implementation must be evaluated against the architecture v1 requirements rather than blindly promoting this runtime transformer.

---

## 4. Prototype behavior

### Full Biography

Target only:

`section.chapter.bio-entry`

Era dividers and chronology/context introductions remain visible outside disclosures.

### Internet & Performance

Target direct thematic chapters inside the main article body:

`article.article-body > section.chapter`

### Closed card

Prototype summary contains:

- existing period/domain metadata where available;
- existing chapter heading;
- a provisional excerpt generated from the first paragraph;
- media/content indicators derived from the chapter DOM when meaningful;
- explicit Expand/Collapse affordance.

The generated excerpt is **prototype-only** and must not silently become permanent editorial copy. Final summaries can be curated after the human test demonstrates that the interaction model is useful.

---

## 5. Required controls

- Open all / Abrir todos;
- Collapse all / Recolher todos;
- multiple chapters can remain open;
- existing hash/deep links open their containing disclosure;
- print preparation opens all disclosures, then restores prior state after print where browser events permit;
- no animation requirement; reduced-motion users are not forced through animated transitions.

---

## 6. Test protocol

Before considering production implementation, manually test:

1. desktop Chrome;
2. desktop Firefox;
3. Safari where available;
4. mobile browser;
5. keyboard-only open/close;
6. direct hash URL;
7. aside/navigation hash click;
8. Ctrl+F / Find in Page for text inside a closed chapter;
9. Print / Save as PDF;
10. gallery/lightbox behavior after a chapter is expanded;
11. several chapters left open simultaneously;
12. normal URL **without** query parameter to confirm zero visible regression.

Human validation should preferably include the same readers who reported the original wall-of-text problem.

---

## 7. Explicit limitations

This harness is not evidence that runtime DOM transformation is the final preferred production implementation.

It intentionally postpones:

- curated per-entry summaries;
- controlled taxonomy vocabulary;
- Chapter Page links;
- source `.inc` migration;
- entry registry/auditor;
- indexation experiments;
- dynamic gallery materialization.

Those belong to later phases only after the basic disclosure UX is validated.

---

## 8. Merge policy

Prototype code should first live in a **draft PR**.

Do not merge it into `main` merely because CI passes. A merge is useful only when Marcelo explicitly wants the query-parameter prototype available on the deployed site for browser/human testing.

If merged for testing, default canonical URLs must remain visually unchanged without the activation parameter.
