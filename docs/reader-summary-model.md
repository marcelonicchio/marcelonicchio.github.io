# Reader thread-summary model

**Status:** accepted baseline after the Melissa 1.0 pilot  
**Reference:** 1 Sep 2026 (BRT)

This document defines the editorial and UX model for dense entries that can exist in two reading states.

It is not a universal requirement for every thread. It is a reusable model for entries whose complete version is dense enough that the collapsed state must itself carry meaningful information.

---

## 1. Core principle

A collapsed thread is **not a teaser**.

The design assumption is intentionally conservative:

> **The expansion click rate may be very low. Therefore the collapsed state must be useful even when the reader never opens the full entry.**

The two states are separate editorial objects:

- **Version A — complete post:** full narrative, media, documents, repositories, links and context;
- **Version B — concise thread-summary:** an autonomous short version that communicates the principal arc without requiring expansion.

Version B is not the first few paragraphs of Version A and should not be generated through mechanical truncation.

---

## 2. Melissa 1.0 as the calibrated upper reference

Melissa was used because the expanded entry combines long narrative, images, research concepts, links, DOI documents and repository material.

After visual/mobile calibration, the accepted collapsed version contains four short paragraphs.

Measured visible preview copy:

- **PT:** approximately **1,638 characters**;
- **EN:** approximately **1,616 characters**.

This is intentionally treated as the current upper-density reference, not the average desired length.

### Adopted character rule

For structured rich previews (`reader_preview`):

- **hard editorial ceiling:** `1,650` visible-copy characters per language;
- **preferred design center for most entries:** approximately `1,300–1,320` characters, around 20% below the ceiling;
- entries may be materially shorter when the subject does not justify more copy;
- do not add filler merely to approach the target.

The count applies to paragraph text only.

It excludes:

- title;
- date/period metadata;
- topic labels;
- internal-content indicators;
- CTA text;
- image alt/caption.

`tools/audit_entries.py` enforces the 1,650-character maximum for a structured `reader_preview`.

---

## 3. Paragraph count is not the invariant

Melissa currently uses four paragraphs because that density reads well enough on desktop and mobile after removing the fifth paragraph.

Do not turn “four paragraphs” into a universal template.

Reasonable future shapes include:

- two moderately dense paragraphs;
- three short paragraphs;
- four short paragraphs for unusually dense entries;
- a brief intro plus a compact list only when the content genuinely benefits from list structure.

The invariant is **useful concise coverage within the character budget**, not paragraph count.

---

## 4. What a useful collapsed summary should cover

A strong compact version usually answers some subset of:

1. what this episode/project was;
2. what role Marcelo played;
3. what changed or why the episode mattered;
4. one or two concrete scale/time/result details;
5. what the episode produced or led to.

Do not force every summary into the same five-sentence order. The content determines emphasis.

For Melissa the accepted arc is:

- functional origin;
- 11 sessions / ~63 hours / 518 prompts and relational change;
- reasoning traces + EIP with epistemic caveat;
- Melissa Framework and transmission/reinstallation outcome.

The removed fifth paragraph proved useful as a calibration point: it contained valid information, but pushed the collapsed experience beyond the desired mobile density. The DOI/repository outcome remains discoverable through the internal indicators and the complete post.

---

## 5. Image rule

A rich collapsed summary may use an editorial cover image when the image materially helps recognition or narrative comprehension.

The image is **not mandatory**.

The compact-state image is a cover/summary asset, not necessarily the same presentation size used in the complete post.

Melissa's compact-state self-portrait size is approved and should be treated as the current visual reference. Do not change it as a side effect of other Reader work.

The complete Melissa post has a separate expanded-entry sizing rule (65% desktop / 100% mobile) that must not be confused with the compact preview layout.

---

## 6. Typographic rule

The first Melissa pilot revealed that a summary shown in smaller, muted-gray type looked secondary and discouraged reading.

Accepted direction:

- compact summary copy uses the same basic reading size as the full post (`1.04rem` in the current Reader implementation);
- copy uses a light neutral tone (`var(--soft)`) rather than the heavily muted gray;
- selective `<strong>` emphasis is allowed;
- bold should identify high-information phrases, not turn whole paragraphs into visual noise.

A compact post is lower-density, not lower-importance.

---

## 7. Two distinct label systems

### 7.1 Topic labels — “what this is about”

Topic labels come from the controlled taxonomy (`data/tags.json` + `topic_ids`).

They serve several functions:

- immediate human scanning;
- consistent topic vocabulary across the HUB;
- future internal linking/filtering;
- future standalone-entry/SEO planning when a post becomes its own URL.

They are **not** `meta keywords`.

Melissa example:

`AI · HAI · HCI · Prompt Engineering · Melissa 1.0`

Current visual treatment:

- neutral light/white translucent background;
- subtle light border;
- light text;
- deliberately different from the red content indicators.

### 7.2 Internal-content indicators — “what is inside if I open it”

These are interaction/UX signals, not taxonomy.

Melissa example:

- `2 imagens`;
- `1 link para download`;
- `4 documentos com DOI`;
- `1 link para repositório`.

Current visual treatment remains red.

Automatic media counting is useful where it expresses the real content. Curated indicators are also allowed for resources that DOM media counting does not describe well, such as DOI papers, downloads or repositories.

Never merge topic labels and internal-content indicators into a single ambiguous badge family.

---

## 8. Expanded-state behavior

When the user expands a rich compact entry:

- the compact preview disappears;
- the complete original body appears intact;
- no information is fetched only after the click;
- existing deep links, keyboard behavior and print behavior remain valid.

The compact copy is **not duplicated above the full text** in the expanded state.

---

## 9. Featured-card color is a separate unresolved layer

Do not confuse the accepted summary model with the still-unresolved color system.

### Open Problem 1 — collapsed featured colors

Current yellow is too beige; current red still leans too wine-like.

Future tests should explore:

- a clearer pale yellow;
- a more genuinely red, translucent red;
- possibly borderless CTA;
- possibly lighter/non-bold CTA typography.

Those are test hypotheses, not settled specs.

### Open Problem 1.1 — color must be state-dependent

Desired behavior:

- collapsed featured entry → colored frame/background as an attention cue;
- expanded entry → normal dark/black post background.

The color exists to encourage discovery of dense/high-value content, not to tint the entire reading experience after expansion.

Do not solve 1 or 1.1 accidentally while rolling out the summary model to other entries.

---

## 10. Candidate rollout logic

Do not apply rich summaries to every entry simply for consistency.

Use them where one or more of these conditions is true:

- full entry is visually/textually long;
- entry contains a substantial gallery;
- entry contains several different resource types;
- entry is important enough that a one-line excerpt underserves it;
- a likely future Chapter Page/standalone URL benefits from a stable concise description.

The first rollout after Melissa applies the model to:

- Mirantte News;
- CookieWEB;
- Meia-Noite e Uns.

These three previews are scoped to **Full Biography / Biografia Completa only**. The thematic verticals keep their own reading behavior; in particular, **Cultura & Audiovisual / Culture & Audiovisual remains fully open and has no disclosure mode**. Each entry receives its own editorial summary rather than cloning Melissa's structure mechanically.

---

## 11. Data model

The registry may use:

```json
"reader_preview": {
  "pt": {
    "image": "/assets/...",
    "alt": "...",
    "paragraphs": [
      {"text": "...", "strong": ["..."]}
    ],
    "indicators": ["..."]
  },
  "en": {
    "image": "/assets/...",
    "alt": "...",
    "paragraphs": [
      {"text": "...", "strong": ["..."]}
    ],
    "indicators": ["..."]
  }
}
```

Topic labels remain outside `reader_preview` as stable `topic_ids` because they belong to entry taxonomy, not only to this visual component.

A preview can optionally be limited to specific registered Reader targets with `reader_preview_paths`:

```json
"reader_preview_paths": {
  "pt": ["pt/biografia/index.html"],
  "en": ["en/biography/index.html"]
}
```

When this field is omitted, the preview keeps the legacy behavior and may render on any Reader target for that entry. This allows Full Biography to use a substantive compact layer without forcing the same summary UX onto a thematic vertical.

The renderer supports structured text + explicit emphasis rather than arbitrary HTML inside registry data.

---

## 12. QA requirements

A rich-preview implementation should verify:

- PT/EN preview exists when intended;
- visible copy stays within 1,650 characters per language;
- all topic IDs resolve in `data/tags.json`;
- curated indicators render in the intended language;
- image path exists;
- preview is visible while collapsed;
- preview disappears after expansion;
- full body remains unchanged;
- no mobile horizontal overflow;
- typography is readable on mobile;
- print still exposes the complete body;
- no-JS fallback remains readable.

The current Chrome smoke test already protects Melissa's core behavior and should be extended rather than weakened when new rich-summary entries are added.
