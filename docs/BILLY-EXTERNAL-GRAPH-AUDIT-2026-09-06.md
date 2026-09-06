# Billy external entity graph audit — 6 Sep 2026

Purpose: identify external profile edits that strengthen bidirectional entity resolution between Marcelo Nicchio's canonical HUB and public professional/research profiles.

Canonical person URL: `https://marcelonicchio.github.io/`
Canonical entity id: `https://marcelonicchio.github.io/#marcelo-nicchio`

## Principle

The HUB already links outward through `sameAs` / site-wide presence links. The remaining B2 task is to create a stronger **return path** from authoritative external profiles back to the canonical HUB wherever each platform allows a website/homepage field.

Do not create artificial backlinks, duplicate profiles or keyword-heavy bios. Prefer one clean canonical website link plus identity/profile fields that agree with the HUB.

## Confirmed observations

### GitHub — high priority

Public profile inspected on 6 Sep 2026.

Current profile exposes external links for:

- Medium;
- ORCID;
- LinkedIn;
- X.

The canonical HUB root was not exposed as the website link in the inspected public profile.

**Manual action:** set the primary Website field to `https://marcelonicchio.github.io/` if GitHub's current profile editor allows it. Keep ORCID and relevant social links in the remaining social-link slots.

**Bio alignment:** current short bio strongly emphasizes the present AI-research phase. That is valid as a current-role bio, but the HUB's canonical identity is intentionally broader. A later manual review can decide whether GitHub should remain research-forward or mention the multidisciplinary trajectory more explicitly.

### HAL — high priority

Public HAL CV inspected on 6 Sep 2026.

The website area currently exposes Medium, LinkedIn, Twitter/X and Academia.edu. The canonical HUB root was not present in the inspected website list.

**Manual action:** add `https://marcelonicchio.github.io/` as the primary personal website if HAL permits it; retain ORCID as the persistent researcher identifier.

**Bio alignment:** the current HAL presentation is coherent as a research CV but contains chronology/positioning language written before the current HUB entity model was finalized. Review after the site's core copy is frozen; do not rewrite HAL independently before the canonical wording is settled.

### Academia.edu — medium priority

Public profile inspected on 6 Sep 2026. The profile and uploaded works are visible, but the canonical HUB URL was not found in the public page text returned by the inspection.

**Manual action:** check whether the profile editor provides a website/homepage field or an About/Bio field suitable for one canonical HUB link. If available, add the root URL once.

**Bio alignment:** the current profile is strongly Melissa/AI-Soul-Composing centered and includes claims/terminology that should be reviewed against the final 2026 research framing. This is an editorial consistency task, not a reason to remove historical uploads.

### SSRN — identity/work record confirmed; backlink field not yet verified

The public PRO v1 paper and Marcelo Nicchio author identity are discoverable. The inspected paper surface does not establish whether the author-profile editor offers a personal website field.

**Manual action:** verify the author profile settings. If a personal/homepage URL is supported, use the canonical HUB root. Do not create a second publication record merely to obtain a backlink.

### ORCID — manual verification required

The public ORCID identifier resolves, but the current public page requires client-side execution in the inspection environment, so website-link state was not reliably readable.

**Manual action:** inspect `Websites & social links` in ORCID while logged in. Add `https://marcelonicchio.github.io/` as the personal/canonical website if absent. Keep the ORCID record focused on identity and works rather than copying the whole HUB biography.

### OSF — manual verification required

The HUB already points to the OSF user/profile record. Public profile backlink state was not reliably readable in the inspection environment.

**Manual action:** inspect profile settings for Website / Personal URL. Add the HUB root if supported.

### PubPub — manual verification required

The HUB already points to Marcelo Nicchio's PubPub user profile. Public backlink state was not reliably readable in the inspection environment.

**Manual action:** inspect profile settings for Website / Personal URL or short biography and add one canonical HUB link if supported.

## Recommended manual order

1. GitHub — primary Website → HUB root.
2. HAL — personal website → HUB root.
3. ORCID — Websites & social links → HUB root.
4. OSF — website/personal URL if available.
5. SSRN — author homepage if available.
6. PubPub — website/bio link if available.
7. Academia.edu — website or one canonical bio link.
8. LinkedIn / Medium / Substack / social profiles — align only after the site's final entity wording is frozen.

## Canonical wording rule

External profiles do **not** need identical bios. They should agree on identity facts and point back to the same canonical person URL. Platform-specific emphasis is useful:

- GitHub: research/repositories;
- HAL, ORCID, OSF, SSRN, PubPub, Academia.edu: research identity and works;
- LinkedIn: professional trajectory;
- Medium/Substack: writing/publication identity;
- Instagram/YouTube/Facebook/X: public/social presence.

The HUB remains the only surface expected to integrate the complete trajectory.

## B2 completion criterion

B2 is operationally complete when:

- the HUB's outbound `sameAs` graph remains valid;
- the highest-authority editable profiles that support a website field point back to the HUB root;
- ORCID and publication identities remain consistent;
- no external profile creates a contradictory primary identity or falsely inflates repository copies into separate publications.

External-platform edits require Marcelo's authenticated sessions and therefore remain a manual task; they do not block today's autonomous site engineering.
