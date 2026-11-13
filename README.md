# Prawo polskie, zmiana po zmianie

**Polski** · [English](README.en.md)

<picture>
<source media="(prefers-color-scheme: dark)" srcset="data/pl/effort-dark.svg">
<img alt="Przepisy Polski w tym repozytorium: zawartość, zmiany według roku wejścia w życie, kompletność względem oficjalnych źródeł i poprawność zawartości" src="data/pl/effort-light.svg" width="880">
</picture>

Część projektu [lexifina/global-law](https://github.com/lexifina/global-law), jednej historii git prawa wszystkich państw: to jest prawo krajowe Polski, które global-law odczytuje ze ścieżki `poland/national/acts/`.

Dwa akty Rzeczypospolitej Polskiej jako repozytorium git: Konstytucja Rzeczypospolitej Polskiej (Dz.U. 1997 nr 78
poz. 483) i ustawa z dnia 2 kwietnia 2009 r. o obywatelstwie polskim (Dz.U. 2012 poz. 161). Każdy akt zmieniający to
jeden commit, przypisany temu aktowi i opatrzony datą dnia, w którym wszedł w życie, w południe czasu warszawskiego.
Tekst pochodzi z API ELI Sejmu (api.sejm.gov.pl), prowadzonego przez Kancelarię Sejmu.

## Pytania jako polecenia git

| Pytanie | Polecenie |
| --- | --- |
| Co stanowił art. 55 Konstytucji w dniu 1 stycznia 2006 r.? | `python tools/na_dzien.py 2006-01-01 konstytucja 55` |
| Cała Konstytucja w brzmieniu z 2000 r. | `python tools/na_dzien.py 2000-01-01 konstytucja` |
| Art. 30 ustawy o obywatelstwie w dniu 1 stycznia 2015 r. | `python tools/na_dzien.py 2015-01-01 obywatelstwo 30` |
| Który akt napisał każdy ustęp art. 30? | `git blame obywatelstwo/art-030.md` |
| Każda zmiana art. 30, z aktem i dniem | `git log --follow obywatelstwo/art-030.md` |
| Wszystko, co zmienił jeden akt | `git show --stat du/2013-1650` |
| Co zmieniło się w ustawie o obywatelstwie jednego dnia | `git show --stat obywatelstwo/2022-11-10` |
| Co zmieniło się między dwoma tekstami jednolitymi | `git diff tj/2022-465 tj/2023-1989 -- obywatelstwo` |
| Własne zmiany redakcyjne tekstów jednolitych | `git log --author="Marszałek Sejmu" --format="%ad %s" --date=short` |
| Akty zmieniające ustawę o obywatelstwie w 2025 r. | `git log --format="%an %s" --author="Dz.U. 2025" -- obywatelstwo` |
| Zmiany i sprostowanie Konstytucji | `git log --format="%ad %an %s" --date=short -- konstytucja` |
| Akty zmieniające ze wszystkimi ich datami | [`akty.csv`](akty.csv) |

`--before` przyjmuje samą datę z bieżącą godziną; aby zapytać o dany dzień, podaj jego koniec:
`git rev-list -1 --before="2015-01-01T23:59:59+01:00" main -- obywatelstwo`. W PowerShell ujmij rewizję w cudzysłów:
`$r = git rev-list -1 --before="2015-01-01T23:59:59+01:00" main; git show "$($r):obywatelstwo/art-030.md"`.
Po przebudowie odśwież tagi poleceniem `git fetch --force --tags`.

## Daty i która z nich jest używana

Polski akt ma dzień uchwalenia (`Enacted:`, data „z dnia” w jego tytule), dzień ogłoszenia w Dzienniku Ustaw
(`Published:`) i dzień wejścia w życie (`In-force:`). **Commity mają datę dnia, w którym zmiana weszła w życie**,
w południe czasu warszawskiego (CET, a w czasie letnim CEST). Ten dzień pochodzi z API Sejmu, które dla każdego aktu
zmieniającego podaje dzień wejścia w życie dokonanej przez niego zmiany tej ustawy (akt może zmieniać różne akty
w różnych dniach), i jest porównywany z dniem podanym w przypisie tekstu jednolitego. Jeżeli akt zmieniający jako
całość wszedł w życie innego dnia, ten dzień jest podany w `Act-in-force:`.

## Co oznacza „autor”

Autorem commita jest akt, który wprowadził zmianę: `Dz.U. 2013 poz. 1650` (z adresem zakończonym na
`@sejm.invalid`, który nie może istnieć), dzięki czemu `git blame` wskazuje akt.

- **Ustawa o obywatelstwie.** Marszałek Sejmu okresowo ogłasza tekst jednolity. Każdy tekst jednolity oznacza każdą
  jednostkę zmienioną od poprzedniego tekstu przypisem wskazującym akt i dzień jego wejścia w życie („W brzmieniu
  ustalonym przez art. 29 pkt 1 ustawy z dnia 7 października 2022 r. ... (Dz. U. poz. 2185), która weszła w życie
  z dniem 10 listopada 2022 r.”). Według tych przypisów każda zmiana jest przypisywana aktowi. Jeżeli akt zmieniający
  przytacza nowe brzmienie („otrzymuje brzmienie”), to brzmienie jest odtwarzane w jego dniu i sprawdzane
  z następnym tekstem jednolitym, więc jednostka zmieniona dwukrotnie między dwoma tekstami jednolitymi pokazuje oba
  kroki (art. 30 ust. 1 pkt 7: 2014, potem 2016).
- **Zmiany redakcyjne** dokonane przez sam tekst jednolity (zaktualizowane odesłania do Dziennika Ustaw dotyczące
  innych aktów oraz przepisy zmieniające inne akty, wydrukowane jako „(pominięty)”) są commitami
  `Marszałek Sejmu (tekst jednolity, ...)` z dnia ogłoszenia tekstu jednolitego, oznaczonymi jako redakcyjne. Nigdy
  nie są przypisywane ustawie.
- **Konstytucja** nie ma tekstu jednolitego. Jej dwie zmiany (2006, art. 55; 2009, art. 99 ust. 3) są odtwarzane
  z ich własnego brzmienia i muszą być zgodne z tekstem ujednoliconym Sejmu; sprostowanie dwóch błędów drukarskich
  z 2001 r. jest commitem obwieszczenia o sprostowaniu (`Dz.U. 2001 nr 28 poz. 319 (sprostowanie)`), a nie ustawy.
- Zmiana, której nie wyjaśnia żaden przypis, jest przypisywana jedynemu aktowi, który wszedł w życie między dwoma
  tekstami jednolitymi („date only”), a jeżeli było ich kilka, `Kancelaria Sejmu (ISAP)` z ich wskazaniem
  w trailerach `Candidate:`.

Committerem jest zawsze `Lexifina`.

## Jak jest sprawdzane

`tools/check_repo.py` odczytuje każdy punkt kontrolny z gita za pomocą `tools/na_dzien.py` i porównuje go z tekstem
urzędowym: z ustawą o obywatelstwie w brzmieniu ogłoszonym i z każdym tekstem jednolitym (pięcioma w HTML, plik po
pliku i bajt po bajcie; tym z 2025 r. w PDF) oraz z tekstem ujednoliconym Konstytucji; następnie słowo po słowie ze
wszystkimi słowami tekstu urzędowego, odczytanymi niezależnie od parsera. Sprawdza też, czy w dniu poprzedzającym
ogłoszenie każdego tekstu jednolitego historia różni się od niego wyłącznie zmianami redakcyjnymi tego tekstu
jednolitego. `tools/test_repo.py` sprawdza, czy powyższe polecenia działają. Wyniki są w [`REPRODUCE.md`](REPRODUCE.md).

## Pliki

Każdy akt to folder (`konstytucja/`, `obywatelstwo/`). Każdy artykuł to jeden plik (`art-055.md` to art. 55).
Wiersze `## ` na początku pliku to nagłówki rozdziału albo oddziału, który się tam zaczyna, `# Art. 55.` to numer
artykułu, a każdy ustęp to jeden wiersz; każdy punkt i każda litera to element listy. `konstytucja/preambula.md` to
tytuł i preambuła. Uchylona jednostka pozostaje jako „(uchylony)”, tak jak drukują ją teksty jednolite.

## Czego nie pokazuje

- Tekstu jednolitego Konstytucji: taki nie istnieje; jej tekst ujednolicony pochodzi od Sejmu i ma charakter
  informacyjny.
- Tego, które słowa wiersza napisał każdy akt, gdy dwa akty zmieniły ten sam wiersz: blame przypisuje całe wiersze
  (użyj `git log -p --word-diff`).
- Żadnego aktu poza tymi dwoma. Ten sam proces budowy działa dla każdego aktu, który ma teksty jednolite w API: dodaj
  go do `ACTS` w `tools/build.py`.
- Teksty jednolite i teksty ujednolicone Sejmu mają charakter informacyjny; tekstem prawnie wiążącym jest akt
  w brzmieniu ogłoszonym w Dzienniku Ustaw.

## Jak jest budowane

`tools/build.py` odczytuje API Sejmu i tworzy to repozytorium od zera; te same dane dają te same hashe.
Każdy krok, oprogramowanie, decyzje podjęte ręcznie i to, co zrobił model AI, są opisane w [`REPRODUCE.md`](REPRODUCE.md).
Folder każdego aktu zawiera `README.md` z listą jego artykułów i informacją, jak często każdy z nich się zmieniał.
[`corpus.json`](corpus.json) opisuje korpus dla narzędzi, które odczytują kilka repozytoriów prawa Lexifina.

## Licencja

Akty normatywne i dokumenty urzędowe nie są w Polsce przedmiotem prawa autorskiego (ustawa z dnia 4 lutego 1994 r.
o prawie autorskim i prawach pokrewnych, art. 4 pkt 1 i 2). Źródło: Sejm Rzeczypospolitej Polskiej, API ELI
(api.sejm.gov.pl), Kancelaria Sejmu. Tekst ujednolicony Konstytucji przygotowany przez Sejm jest oznaczony
„©Kancelaria Sejmu”; służy tu jako punkt kontrolny dla tekstu aktu. Historia, opisy commitów, tabele i narzędzia są
udostępnione na licencji [CC0 1.0](LICENSE).

To jest tłumaczenie wersji angielskiej ([README.en.md](README.en.md)); w razie rozbieżności rozstrzyga wersja angielska.

## Więcej

Z repozytorium [lexifina/global-law](https://github.com/lexifina/global-law) (po angielsku):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): wszystkie funkcje i to, co musi obsługiwać każdy korpus (`git blame`, `law.py`, narzędzia MCP)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): pytania i odpowiedzi · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proponowanie zmian · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): serwer MCP · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): jak powstał · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): jak aktualny jest każdy korpus · [Monitorowanie](https://github.com/lexifina/global-law/tree/main/monitoring): czy aktualizacje działają · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): jak każde oficjalne źródło jest obserwowane pod kątem zmian
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): jak szybkie są narzędzia, zmierzone
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): wykresy i powiązania w prawie całego świata
- [Podatności](https://github.com/lexifina/global-law/tree/main/vulnerabilities): błędy w przepisach w opublikowanej postaci
