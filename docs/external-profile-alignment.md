# External profile alignment — authority hub

Internal working document for post-launch entity reconciliation.

The goal is not to make every external profile identical. The goal is to make name, chronology, URLs, research-version metadata, current positioning and public-contact exposure compatible with the canonical hub.

## HAL

Public profile checked on 2026-08-24:
- profile: https://cv.hal.science/marcelonicchio
- ORCID is correctly linked as `0009-0002-5626-8973`;
- the website section currently points to Medium rather than the official hub;
- the current presentation heavily foregrounds AI/HCI and describes the transition to full-time AI research as beginning in 2024;
- the hub currently uses 2025 as the beginning of the present HAI research cycle;
- the HAL text also contains interpretive bridges between the music/Search career and later AI methodology that are stronger than the intentionally more conservative wording adopted by this site.

Post-launch action:
1. add `https://marcelonicchio.github.io/` as the primary personal website;
2. keep Medium, if retained, as a publication/profile node rather than the canonical personal website;
3. reconcile 2024/2025 wording so that `career transition`, `research interest` and `public research cycle` are not conflated;
4. shorten the profile so the current AI phase does not erase the earlier lifetime;
5. keep exact publication titles and identifiers synchronized with `data/publications.json`.

## ORCID

Canonical identifier:
- https://orcid.org/0009-0002-5626-8973

Post-launch action:
- add the official hub as a personal website if it is not already present;
- ensure the preferred public name is `Marcelo Nicchio`;
- keep work titles and DOI/version relationships aligned with the canonical publication index.

A live content audit of the ORCID record is still pending because automated retrieval was not reliable in the current QA session.

## GitHub

Canonical account:
- https://github.com/marcelonicchio

The personal-site repository already documents the hub architecture. Research repositories should eventually link back to the official hub in their README/repository metadata where appropriate.

Priority repositories:
- `marcelonicchio.github.io`
- `melissa-framework`
- `punk-rock-orchestra`

## SSRN / PRO v1

The public SSRN record for `The Punk Rock Orchestra` is discoverable and identifies Marcelo Nicchio as author, with the manuscript date in May 2026.

Authority rule:
- treat SSRN as one public instance of PRO v1, not a separate work from the OSF, Zenodo, PubPub and GitHub instances.

Privacy review:
- the public SSRN record currently exposes direct personal contact information in its author/contact area;
- do not duplicate those contact details into the hub or machine-readable records;
- review the SSRN profile/record settings after launch and reduce public contact exposure where the platform permits it, while preserving the research record itself.

## Folha de S.Paulo

The official Folha archive was rechecked during QA and confirms:
- date: 23 April 2001;
- internal title: `Onde estão os ídolos?`;
- Marcelo Nicchio is named and quoted in the article.

This remains one of the strongest independent historical anchors in the hub.

## Alignment principle

External profiles should point inward to the hub whenever the platform allows it. The hub should point outward only to profiles and records that materially help entity resolution, verification, preservation or access.

No platform biography should be rewritten merely to repeat SEO phrases. Consistency of facts is the target; verbatim duplication is not.

Privacy is part of authority maintenance: external records may remain useful as corroborating sources without the hub reproducing unnecessary personal contact details.

This is a post-launch alignment queue, not a reason to delay the first public release once the site itself has passed launch QA.
