# Reader thread-summary model

**Status:** accepted selective model  
**Updated:** 2 Sep 2026 (BRT)

This document defines the editorial and UX model for dense entries that benefit from two reading states. It is deliberately **not universal**.

## 1. Core principle

A collapsed thread is not a teaser.

> **The expansion click rate may be low. Therefore the collapsed state must be useful even when the reader never opens the full entry.**

The two states are separate editorial objects:

- **Version A — complete post:** full narrative, media, documents, links and context;
- **Version B — concise thread-summary:** autonomous short version communicating the principal arc.

Version B is not mechanical truncation of Version A.

## 2. Density rule

Melissa 1.0 established the upper-density calibration.

For structured `reader_preview` copy:

- hard ceiling: **1,650 visible-copy characters per language**;
- preferred design center for most dense entries: around **1,300 characters**;
- shorter is correct when the subject does not justify more;
- paragraph count is not an invariant.

The count covers preview paragraph text only. Title, meta/date, topic chips, content indicators, CTA and alt text do not count.

`tools/audit_entries.py` enforces the 1,650-character maximum.

## 3. What a compact summary should usually cover

Depending on the entry:

1. what the episode/project was;
2. Marcelo's role;
3. why it mattered or what changed;
4. one or two concrete scale/time/result details;
5. what it produced or led to.

Do not force every entry into the same five-sentence pattern.

## 4. Image rule

A rich summary may use an editorial cover image when it materially helps recognition or comprehension. It is optional.

Do not confuse compact-cover sizing with the image treatment inside the complete post.

Current Mirantte/CookieWEB/Meia-Noite preview image choices are not operator-approved final selections. Do not replace them autonomously before the planned visual review.

## 5. Typography

Compact summary copy is reading content, not secondary metadata.

Current direction:

- normal body-like reading size;
- light neutral text rather than heavily muted gray;
- selective `<strong>` emphasis only on high-information phrases.

## 6. Two distinct label systems

### Topic labels — what the entry is about

From `data/tags.json` + `topic_ids`.

They support scanning, controlled vocabulary, future linking/filtering and later standalone-entry planning. They are not meta keywords.

Visual treatment: neutral/light translucent chips.

### Internal-content indicators — what exists inside

Examples: photos, videos, DOI documents, download links, repository links.

They are UX promises, not taxonomy. Curated indicators are allowed when automatic DOM media counting cannot express the useful resource type.

Visual treatment: red.

Never merge the two badge families.

## 7. Expanded-state behavior

When a rich entry opens:

- compact preview disappears;
- complete original body appears intact;
- nothing essential is fetched only after click;
- deep links, keyboard behavior and print remain valid;
- compact copy is not duplicated above the full body.

## 8. Surface-specific behavior is allowed

The same entry may legitimately use different Reader presentation by surface.

Melissa is the canonical example after C2.1:

- **AI/HAI vertical PT/EN:** Melissa stays completely open; no compact preview/card/disclosure;
- **Full Biography PT/EN:** Melissa uses its compact summary because the integral chronology is much denser.

This is implemented through path-scoped presentation/preview metadata. Do not infer a universal “oldest entry should be open” rule from this case.

## 9. Featured color is a separate unresolved layer

Rich-summary acceptance does not mean the featured-card palette is accepted.

Technical rule is settled:

- collapsed featured entry may carry an attention treatment;
- expanded entry returns to the normal dark reading surface.

Aesthetic color selection remains deferred to a joint visual session with Marcelo.

## 10. Current rollout

Current Full Biography rich-summary entries:

- Melissa 1.0;
- Mirantte News;
- CookieWEB;
- Meia-Noite e Uns.

Current deliberate always-open examples include Minduim/BBS, Clickland and Folhateen where registered.

The rollout is selective. A long entry, a substantial gallery, mixed resource types, strong biographical importance or likely standalone value may justify a rich summary; visual consistency alone does not.

The next candidate should be chosen by those criteria, not by chronology or a quota.

## 11. Data model

Typical registry shape:

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

Topic labels remain outside `reader_preview` as stable `topic_ids`.

A preview can be limited to registered Reader targets:

```json
"reader_preview_paths": {
  "pt": ["pt/biografia/index.html"],
  "en": ["en/biography/index.html"]
}
```

An entry can also remain open only on selected targets through path-scoped presentation metadata.

## 12. QA requirements

A rich-preview implementation should verify:

- PT/EN preview exists where intended;
- copy stays within 1,650 characters;
- topic IDs resolve;
- curated indicators render in the intended language;
- image path exists when used;
- preview is visible while collapsed and absent after expansion;
- full body remains unchanged;
- no mobile horizontal overflow;
- typography remains readable;
- print and no-JS expose complete content;
- path-scoped behavior does not leak to other Reader surfaces.

Extend Chrome smoke coverage when adding a new rich-summary entry; do not weaken existing assertions.
