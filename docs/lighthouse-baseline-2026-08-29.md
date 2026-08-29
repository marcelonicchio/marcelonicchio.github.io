# Lighthouse baseline — before progressive disclosure

Reference: 2026-08-29 BRT  
Production commit measured: `4647e3e910d7f690950537807866438c4ad1d4f5`  
Measurement source: Lighthouse CLI in GitHub Actions against the public GitHub Pages deployment.

This is **lab data**, not CrUX field data. Values can vary between runs; use the same protocol for post-UX comparison and interpret direction/magnitude rather than treating one run as an immutable truth.

## Environment

- Lighthouse: 13.4.1
- Fetch time: 2026-08-29T04:23:04.305Z
- User agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/151.0.0.0 Safari/537.36

## Results

| Surface | Mode | Score | FCP | LCP | CLS | TBT | Speed Index | TTI | Transfer observed | Requests | DOM elements |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Full Biography PT | mobile | 68 | 1092 ms | 4130 ms | 0.000 | 619 ms | 4327 ms | 4130 ms | 0.20 MiB | 7 | n/a |
| Full Biography PT | desktop | 100 | 283 ms | 688 ms | 0.000 | 0 ms | 283 ms | 688 ms | 0.27 MiB | 8 | n/a |
| Internet & Performance PT | mobile | 98 | 905 ms | 905 ms | 0.000 | 150 ms | 905 ms | 2718 ms | 0.27 MiB | 8 | n/a |
| Internet & Performance PT | desktop | 100 | 319 ms | 784 ms | 0.000 | 1 ms | 319 ms | 790 ms | 1.20 MiB | 25 | n/a |

## Interpretation guardrails

- These numbers measure the current public pages **before** progressive disclosure.
- They are browser/lab measurements and are distinct from the repository-side `full-scroll-max` inventory.
- Lazy-loaded image inventory is not equivalent to initial transfer.
- Do not turn any single score or millisecond value into an editorial law.
- Repeat the same four-case protocol after the disclosure prototype/production UX is implemented.
- If repeated runs vary materially, record multiple runs/median before drawing a performance conclusion.

## URLs measured

- https://marcelonicchio.github.io/pt/biografia/
- https://marcelonicchio.github.io/pt/internet/
