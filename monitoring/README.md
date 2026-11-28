<!-- lawwatch: written from data/checks by the check trail; edit the records, not this page -->

# Monitorowanie: co jest czytane i co z tego wynika

[English](README.en.md)

Jak global-law monitoruje wszystkie państwa: [global-law monitoring/](https://github.com/lexifina/global-law/tree/main/monitoring). Ta strona robi to samo tylko dla jednego państwa (Polska): każde odczytanie oficjalnego źródła, kiedy nastąpiło i co z niego wynikło (akty dodane, zmienione i uchylone). Postać do odczytu maszynowego: [data/checks/](../data/checks/) (JSON Lines, schemat `lexifina-check/1`), w `git log` jako commity `Kind: check`, a miesiąc po miesiącu w [checks/](checks/).

**Ostatnie sprawdzenie:** 2026-11-28 06:08 UTC, Rejestr ELI Sejmu (Dziennik Ustaw, Monitor Polski): odczytano 2946 adresów; dodane 11, zmienione 15, uchylone 0; znaleziono zmiany; nieopublikowane 118, w tym bez podanej przyczyny 0. Oznaczenia: `verify-differ`.

## Źródła

| Źródło | Foldery | Jak często | Ostatnie udane sprawdzenie | Ostatni wynik | Stan |
| --- | --- | --- | --- | --- | --- |
| [Rejestr ELI Sejmu (Dziennik Ustaw, Monitor Polski)](https://api.sejm.gov.pl/eli) | `ustawa/`, `rozporzadzenie/`, `konstytucja/`, `monitor-polski/`, `…` | codziennie | 2026-11-28 06:08 UTC | znaleziono zmiany | śledzone |

## Ostatnie 30 dni

| Początek (UTC) | Źródło | Odczytano | Dodane | Zmienione | Uchylone | Nieopublikowane (bez przyczyny) | Wynik | Commity |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| [2026-11-28 05:16](checks/2026-11.md#pl-eli-sejm-20261128t051640z) | eli-sejm | 2946 | 11 | 15 | 0 | 118 (0) | znaleziono zmiany `verify-differ` | [24](https://github.com/lexifina/poland-law/compare/5c187419f0f5...c8dff7bd270b) |
| [2026-11-27 05:10](checks/2026-11.md#pl-eli-sejm-20261127t051007z) | eli-sejm | 3010 | 11 | 39 | 2 | 117 (0) | znaleziono zmiany `verify-differ` | [37](https://github.com/lexifina/poland-law/compare/4ab3bd00aa24...fe9f07fa1c30) |
| [2026-11-26 05:11](checks/2026-11.md#pl-eli-sejm-20261126t051129z) | eli-sejm | 2979 | 10 | 26 | 0 | 113 (0) | znaleziono zmiany `verify-differ` | [26](https://github.com/lexifina/poland-law/compare/73ee9bb1b02f...8b8a2de3e7c1) |
| [2026-11-25 05:10](checks/2026-11.md#pl-eli-sejm-20261125t051022z) | eli-sejm | 3368 | 8 | 226 | 1 | 110 (0) | znaleziono zmiany `verify-differ` | [119](https://github.com/lexifina/poland-law/compare/db9494ec6e7c...80afa9f09d45) |
| [2026-11-24 05:27](checks/2026-11.md#pl-eli-sejm-20261124t052733z) | eli-sejm | 2962 | 6 | 25 | 0 | 110 (0) | znaleziono zmiany `verify-differ` | [20](https://github.com/lexifina/poland-law/compare/e0d48a2de46e...00ffa445ac51) |
| [2026-11-23 11:48](checks/2026-11.md#pl-eli-sejm-20261123t114843z) | eli-sejm | 3184 | 16 | 29 | 2 | 111 (0) | znaleziono zmiany `verify-differ` | — |
| [2026-11-23 11:21](checks/2026-11.md#pl-eli-sejm-20261123t112107z) | eli-sejm | 0 | 58 | 85 | 0 | 0 (0) | znaleziono zmiany | [143](https://github.com/lexifina/poland-law/compare/ed3c0d0c7674...31edb0d3fcd7) |
| [2026-11-23 00:40](checks/2026-11.md#pl-eli-sejm-20261123t004018z) | eli-sejm | 218 | 0 | 0 | 0 | 155 (0) | bez zmian `publish-lag` | — |

## Sprawdź sam

```
python tools/checktrail.py                      # ostatnie sprawdzenie każdego źródła
python tools/checktrail.py --day 2026-11-23     # wszystkie sprawdzenia jednego dnia
python tools/checktrail.py --act <id>           # kiedy akt został zauważony i opublikowany
git log --grep='^Kind: check' --format='%ci %s'  # sprawdzenia w historii
```

Moc prawną ma tylko oficjalna publikacja (Dziennik Ustaw, Monitor Polski); teksty w tym repozytorium są kopiami do czytania i wyszukiwania.
