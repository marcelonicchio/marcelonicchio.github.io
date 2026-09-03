# External profile alignment — authority hub

Internal working document for post-launch entity reconciliation.

**Latest public recheck:** 3 Sep 2026 (BRT)

The goal is not to make every external profile identical. The goal is to make name, chronology, URLs, research-version metadata, current positioning and public-contact exposure compatible with the canonical hub.

## HAL

Public profile rechecked on 3 Sep 2026:
- profile: https://cv.hal.science/marcelonicchio
- ORCID remains correctly linked as `0009-0002-5626-8973`;
- the website/contact section still needs operator review so the official HUB becomes the canonical personal-site destination;
- the current presentation still describes full-time AI/HCI research as beginning in 2024;
- the hub distinguishes the later public/current HAI research cycle rather than collapsing research interest, career transition and public research chronology into one date;
- the HAL text also contains interpretive bridges between the music/Search career and later AI methodology that are stronger than the intentionally more conservative wording adopted by this site.

Operator-side action:
1. make `https://marcelonicchio.github.io/` the primary personal website where HAL permits it;
2. keep Medium, if retained, as a publication/profile node rather than the canonical personal website;
3. reconcile 2024/2025 wording so that `career transition`, `research interest` and `public research cycle` are not conflated;
4. shorten the profile if useful so the current AI phase does not erase the earlier lifetime;
5. keep exact publication titles and identifiers synchronized with `data/publications.json`.

## ORCID

Canonical identifier:
- https://orcid.org/0009-0002-5626-8973

Operator-side action:
- add or confirm the official hub as a personal website;
- ensure the preferred public name is `Marcelo Nicchio`;
- keep work titles and DOI/version relationships aligned with the canonical publication index.

A reliable live content audit of the full ORCID record remains an operator-side task if automated retrieval is unavailable.

## GitHub

Canonical account:
- https://github.com/marcelonicchio

The personal-site repository documents the hub architecture. Research repositories should link back to the official hub in README/repository metadata where appropriate.

Priority repositories:
- `marcelonicchio.github.io`
- `melissa-framework`
- `punk-rock-orchestra`

## SSRN / PRO v1

The public SSRN record for `The Punk Rock Orchestra` was rechecked on 3 Sep 2026 and remains discoverable as a preprint/authority node for Marcelo Nicchio.

Authority rule:
- treat SSRN as one public instance of PRO v1, not a separate work from the other canonical deposits/instances.

Privacy review:
- the public SSRN author/contact area currently exposes direct personal contact information;
- do not duplicate those contact details into the hub, schema or repository documentation;
- review SSRN profile/record privacy settings and reduce public contact exposure where the platform permits it while preserving the research record itself.

## Folha de S.Paulo

The official Folha archive was previously rechecked during QA and confirms:
- date: 23 April 2001;
- internal title: `Onde estão os ídolos?`;
- Marcelo Nicchio is named and quoted in the article.

This remains one of the strongest independent historical anchors in the hub.

## Alignment principle

External profiles should point inward to the hub whenever the platform allows it. The hub should point outward only to profiles and records that materially help entity resolution, verification, preservation or access.

No platform biography should be rewritten merely to repeat SEO phrases. Consistency of facts is the target; verbatim duplication is not.

Privacy is part of authority maintenance: external records may remain useful as corroborating sources without the hub reproducing unnecessary personal contact details.

This is an operator-side maintenance queue, not a blocker for site engineering or deployment.
