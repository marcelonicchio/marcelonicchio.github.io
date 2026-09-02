# Lighthouse remeasurement — post-Reader / post-media batch

Reference: 2026-09-01 BRT  
Production commit measured: `07dd061774bf0ea7990cb7ce81948b9465d91773`  
Comparison baseline: `docs/lighthouse-baseline-2026-08-29.md` (`4647e3e910d7f690950537807866438c4ad1d4f5`)  
Measurement source: Lighthouse CLI in GitHub Actions against the public GitHub Pages deployment.

The four original cases and flags were preserved. Each case was repeated three times; the table below reports the median of each metric to reduce lab-run noise. This remains lab data, not CrUX field data.

## Environment

- Lighthouse: 13.4.1 (pinned to the baseline version)
- First fetch time: 2026-09-02T01:52:39.138Z
- User agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/151.0.0.0 Safari/537.36

## Median results (3 runs per case)

| Surface | Mode | Score | FCP | LCP | CLS | TBT | Speed Index | TTI | Transfer observed | Requests | DOM elements |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Full Biography PT | mobile | 95 | 1086 ms | 2761 ms | 0.000 | 97 ms | 1086 ms | 3332 ms | 0.49 MiB | 13 | n/a |
| Full Biography PT | desktop | 100 | 296 ms | 682 ms | 0.000 | 0 ms | 296 ms | 682 ms | 0.56 MiB | 14 | n/a |
| Internet & Performance PT | mobile | 100 | 1020 ms | 1022 ms | 0.000 | 79 ms | 1020 ms | 3251 ms | 0.58 MiB | 19 | n/a |
| Internet & Performance PT | desktop | 100 | 285 ms | 745 ms | 0.011 | 0 ms | 285 ms | 752 ms | 0.52 MiB | 19 | n/a |

## LCP comparison with 29 Aug baseline

| Surface | Mode | Baseline LCP | Current median LCP | Delta |
|---|---|---:|---:|---:|
| Full Biography PT | mobile | 4130 ms | 2761 ms | -1369 ms |
| Full Biography PT | desktop | 688 ms | 682 ms | -6 ms |
| Internet & Performance PT | mobile | 905 ms | 1022 ms | +117 ms |
| Internet & Performance PT | desktop | 784 ms | 745 ms | -39 ms |

## Individual runs

### Full Biography PT — mobile

| Run | Score | FCP | LCP | TBT | Transfer | Requests |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 70 | 1127 ms | 4390 ms | 504 ms | 0.49 MiB | 13 |
| 2 | 95 | 1086 ms | 2761 ms | 97 ms | 0.49 MiB | 13 |
| 3 | 100 | 1058 ms | 1079 ms | 75 ms | 0.49 MiB | 13 |

### Full Biography PT — desktop

| Run | Score | FCP | LCP | TBT | Transfer | Requests |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 100 | 296 ms | 682 ms | 0 ms | 0.56 MiB | 14 |
| 2 | 100 | 304 ms | 700 ms | 0 ms | 0.56 MiB | 14 |
| 3 | 100 | 296 ms | 679 ms | 0 ms | 0.56 MiB | 14 |

### Internet & Performance PT — mobile

| Run | Score | FCP | LCP | TBT | Transfer | Requests |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 100 | 1020 ms | 1020 ms | 76 ms | 0.58 MiB | 19 |
| 2 | 100 | 1022 ms | 1022 ms | 87 ms | 0.58 MiB | 19 |
| 3 | 99 | 1015 ms | 1946 ms | 79 ms | 0.58 MiB | 19 |

### Internet & Performance PT — desktop

| Run | Score | FCP | LCP | TBT | Transfer | Requests |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 100 | 287 ms | 758 ms | 0 ms | 0.52 MiB | 19 |
| 2 | 100 | 285 ms | 745 ms | 0 ms | 0.52 MiB | 19 |
| 3 | 100 | 280 ms | 737 ms | 0 ms | 0.52 MiB | 19 |

## Interpretation guardrails

- Full Biography mobile LCP changed from 4130 ms to a three-run median of 2761 ms (-33.2%).
- Repository-side `full-scroll-max` image inventory is not equivalent to initial transfer.
- Lazy-loaded gallery growth should not be treated as a performance defect unless lab/field loading behavior also degrades materially.
- Do not remove autobiographical content to chase a repository-side byte total.
- If a later architecture change is proposed (for example on-demand thumbnail materialization), compare it against this measured post-Reader state rather than against intuition.

## URLs measured

- https://marcelonicchio.github.io/pt/biografia/
- https://marcelonicchio.github.io/pt/internet/
