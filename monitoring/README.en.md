<!-- lawwatch: written from data/checks by the check trail; edit the records, not this page -->

# Monitoring: what is read and what came of it

[Polski](README.md)

How global-law monitors every country: [global-law monitoring/](https://github.com/lexifina/global-law/tree/main/monitoring). This page is the same for Poland only: every time an official source is read, when, and what came of it (acts added, changed and removed). The machine-readable form is [data/checks/](../data/checks/) (JSON Lines, schema `lexifina-check/1`), in `git log` as `Kind: check` commits, and month by month in [checks/](checks/).

**Last check:** 2026-11-25 06:10 UTC, Sejm ELI register (Dziennik Ustaw, Monitor Polski): 3368 addresses read; 8 added, 226 changed, 1 removed; changes found; 110 not published, 0 of them with no reason. Flags: `verify-differ`.

## Sources

| Source | Folders | How often | Last successful check | Last result | State |
| --- | --- | --- | --- | --- | --- |
| [Sejm ELI register (Dziennik Ustaw, Monitor Polski)](https://api.sejm.gov.pl/eli) | `ustawa/`, `rozporzadzenie/`, `konstytucja/`, `monitor-polski/`, `…` | daily | 2026-11-25 06:10 UTC | changes found | watched |

## The last 30 days

| Started (UTC) | Source | Read | Added | Changed | Removed | Not published (no reason) | Result | Commits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| [2026-11-25 05:10](checks/2026-11.md#pl-eli-sejm-20261125t051022z) | eli-sejm | 3368 | 8 | 226 | 1 | 110 (0) | changes found `verify-differ` | [119](https://github.com/lexifina/poland-law/compare/db9494ec6e7c...80afa9f09d45) |
| [2026-11-24 05:27](checks/2026-11.md#pl-eli-sejm-20261124t052733z) | eli-sejm | 2962 | 6 | 25 | 0 | 110 (0) | changes found `verify-differ` | [20](https://github.com/lexifina/poland-law/compare/e0d48a2de46e...00ffa445ac51) |
| [2026-11-23 11:48](checks/2026-11.md#pl-eli-sejm-20261123t114843z) | eli-sejm | 3184 | 16 | 29 | 2 | 111 (0) | changes found `verify-differ` | — |
| [2026-11-23 11:21](checks/2026-11.md#pl-eli-sejm-20261123t112107z) | eli-sejm | 0 | 58 | 85 | 0 | 0 (0) | changes found | [143](https://github.com/lexifina/poland-law/compare/ed3c0d0c7674...31edb0d3fcd7) |
| [2026-11-23 00:40](checks/2026-11.md#pl-eli-sejm-20261123t004018z) | eli-sejm | 218 | 0 | 0 | 0 | 155 (0) | no change `publish-lag` | — |

## Check it yourself

```
python tools/checktrail.py                      # the latest check of every source
python tools/checktrail.py --day 2026-11-23     # every check of a day
python tools/checktrail.py --act <id>           # when an act was seen and published
git log --grep='^Kind: check' --format='%ci %s'  # the checks in the history
```

Only the official publication has legal force; the texts here are copies for reading and searching.
