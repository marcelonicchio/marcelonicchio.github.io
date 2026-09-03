# Reader presentation policy

**Current policy — 3 Sep 2026**

The Reader has two independent concerns: **behavior** and **visual emphasis**. They must not be conflated.

## 1. Behavior is path-specific

`data/entries.json` controls whether an entry is `normal`, explicitly `featured`, or `always-open`. `always_open_paths` can override the base state on selected surfaces.

This is how the same source entry can remain compact in Full Biography while staying fully open on a thematic vertical. Melissa 1.0 is the current reference case: compact in Full Biography, always open on AI/HAI.

## 2. Full Biography visual rule

On Full Biography / Biografia Completa, an entry that renders an active rich `reader_preview` automatically receives the highlighted editorial outline.

That outline currently means:

- no yellow fill;
- 1.5px translucent baby-yellow border (`rgba(255,239,153,.78)`);
- neutral dark interior surface;
- near-white expand/collapse controls with bold dark text;
- existing red content indicators remain semantically separate.

Therefore a future rich compact summary does **not** need a second per-entry visual decision merely to obtain the outline. If the rich preview is active on Full Biography, the outline follows automatically.

## 3. Vertical rule

The Full Biography rule does not decide thematic-vertical layout. Verticals keep their own Reader behavior and may be:

- fully open;
- normal disclosure;
- explicitly featured disclosure;
- or later redesigned through an explicit editorial decision.

A Full Biography rich preview must not force a vertical to become collapsed or visually featured.

## 4. Biography-only chapters

A Full Biography entry may become a registered `biography-only` chapter when it is editorially substantial enough to deserve controlled tags and/or a standalone Chapter Page but does not belong to a thematic vertical.

For these entries:

- Full Biography remains the canonical Reader surface;
- no synthetic thematic vertical is created merely to host the chapter;
- `reader_scope: biography-only` explicitly relaxes the normal vertical + Full Biography target requirement;
- an `always-open` biography-only chapter remains plain open HTML, with no expand/collapse controls;
- controlled topic chips remain visible even when the chapter is always open;
- standalone-page indexation remains an independent decision. Creating a URL does not automatically promote it to `index,follow`.

**Espiritualidade — “O Buscador”** is the reference implementation of this pattern.

## 5. Scroll principle

Full Biography is the dense chronology. Rich previews are selective compression devices, not a default for every entry. Use them when they materially reduce scroll cost while preserving enough context to decide whether to expand.

The default remains: ordinary entries use ordinary compact Reader treatment; only editorially substantial records receive a rich preview.

## 6. Regression gate

`tools/audit_reader_visual_policy.py` verifies that:

- PT/EN rich-preview sets remain aligned;
- Melissa remains a rich Full Biography preview;
- Melissa remains `always-open` on PT/EN AI/HAI verticals;
- the shared Full Biography rich-preview outline rule remains present;
- the approved palette tokens remain intact.

This prevents future entries from requiring manual CSS exceptions and keeps behavior decisions separate from visual emphasis.
