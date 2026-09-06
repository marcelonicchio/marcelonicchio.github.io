# External profile alignment — authority hub

Internal working document for entity reconciliation.

**Latest strategy update:** 5 Sep 2026 (BRT)  
**Latest public recheck baseline:** 3–5 Sep 2026.

The goal is not to make every external profile identical. The goal is to make name, chronology, URLs, research-version metadata, current positioning and public-contact exposure compatible with the canonical HUB, while creating legitimate inward links to `https://marcelonicchio.github.io/` where platforms permit them.

## Core rule

External links must not be treated as decorative social icons only. Material external profiles/records should participate in a coherent entity graph:

- preferred public name = Marcelo Nicchio;
- official personal-site destination = `https://marcelonicchio.github.io/` where possible;
- chronology/current positioning compatible with the HUB;
- exact publication titles and version relationships;
- persistent identifiers connected accurately;
- platform-native descriptions that remain factually compatible with the HUB.

**Do not force one identical SEO sentence word-for-word into every platform.** Consistency of facts and entity identity is the goal; verbatim duplication is not.

## Priority external nodes

Current material nodes include:

- ORCID;
- HAL;
- SSRN;
- Zenodo;
- OSF;
- PubPub;
- GitHub;
- LinkedIn;
- Medium;
- Substack;
- YouTube;
- X;
- Academia.edu;
- Archive.org;
- other material profile/repository nodes discovered during audit.

Google Scholar may be evaluated as an additional academic identity node if useful/eligible. Do not describe it as a guaranteed LLM-ranking mechanism.

Wikidata is **not** an operator-created SEO shortcut. It is community-governed infrastructure with notability/self-promotion policy. Do not create person/work items merely to manufacture graph signals; only pursue a policy-compliant path if independent notability/creation supports it.

## HAL

Profile:
- https://cv.hal.science/marcelonicchio

Known alignment points:

- ORCID is linked as `0009-0002-5626-8973`;
- the official HUB should become the primary personal-site destination where HAL permits it;
- reconcile wording that can conflate research interest, career transition and the public/current HAI research cycle;
- avoid an AI-only profile that erases the earlier lifetime;
- keep exact publication titles/identifiers synchronized with `data/publications.json`.

## ORCID

Canonical identifier:
- https://orcid.org/0009-0002-5626-8973

Operator-side goals:

- add/confirm the official HUB as a personal website;
- preferred public name `Marcelo Nicchio`;
- keep works and DOI/version relationships aligned with the canonical publication inventory;
- use keywords/biographical positioning that are accurate, not copied merely for search-engine repetition.

## GitHub

Canonical account:
- https://github.com/marcelonicchio

Priority repositories include:

- `marcelonicchio.github.io`;
- `melissa-framework`;
- `punk-rock-orchestra`.

Research repositories should link back to the official HUB in README/repository metadata where appropriate. `CITATION.cff` is worth evaluating per repository when it reflects a real citable work/version.

## Research repositories / publication instances

Zenodo, OSF, SSRN, PubPub and other deposits should be treated as authority/preservation instances, not separate publications when they represent the same intellectual work/version.

For PRO v1, preserve the rule:

> repository instances are records of one work/version and are not counted as separate publications.

Related identifiers/cross-links can be strengthened where platforms support them, but do not overstate identity relationships among DOI records. The HUB structured-data model should be designed around one work + repository instances rather than mechanically treating every DOI as an independent work.

## SSRN / privacy

The public SSRN record remains discoverable and useful as a preprint/authority node.

Public third-party pages may expose more direct contact detail than the HUB needs. Privacy cleanup on those services is an operator-side decision. Do not duplicate unnecessary personal phone/address information into HUB HTML, JSON-LD or documentation.

The same rule applies to other external profiles that expose direct personal contact data.

## Search-discovery observation — 5 Sep 2026

Current external search checks show that the exact `Punk Rock Orchestra` phrase remains strongly ambiguous because it collides with a long-established San Francisco music entity and other musical uses.

However, queries that add **methodology** and **Marcelo Nicchio** already surface Marcelo's research record. The problem is therefore primarily one of lexical/entity disambiguation, not total invisibility.

Operational response:

- use `Punk Rock Orchestra (PRO) methodology` or equivalent disambiguating context on first relevant occurrences;
- preserve the full research title in publication metadata;
- do not force the expanded phrase into unrelated musical contexts;
- build authority through coherent pages and records rather than keyword repetition alone.

## Independent historical anchors

External historical sources that materially corroborate the trajectory should remain connected where useful. Example already documented:

- Folha de S.Paulo, 23 Apr 2001, `Onde estão os ídolos?`, naming/quoting Marcelo Nicchio.

The HUB should point outward to records that materially help entity resolution, preservation, verification or reader access — not to maximize link count.

## Maintenance workflow

For each priority external node, record:

1. current display name;
2. current profile/record description;
3. current website/HUB link state;
4. ORCID/DOI/other identifiers;
5. chronology conflicts;
6. publication/version conflicts;
7. privacy issues Marcelo chooses to fix;
8. operator-side edit required;
9. date last checked.

This work can proceed in parallel with site engineering because many external edits require Marcelo's authenticated operator access.
