# Polish law, change by change

Two acts of the Republic of Poland as a git repository: the Constitution (Konstytucja Rzeczypospolitej Polskiej,
Dz.U. 1997 nr 78 poz. 483) and the Polish Citizenship Act (ustawa z dnia 2 kwietnia 2009 r. o obywatelstwie polskim,
Dz.U. 2012 poz. 161). Each amending act is one commit, credited to that act and dated the day it took effect, at noon
in Warsaw. The text comes from the Sejm's ELI API (api.sejm.gov.pl), run by the Chancellery of the Sejm.

*Po polsku: [niżej](#po-polsku).*

## The questions, as git commands

| Question | Command |
| --- | --- |
| What did art. 55 of the Constitution say on 1 January 2006? | `python tools/na_dzien.py 2006-01-01 konstytucja 55` |
| The whole Constitution as it stood in 2000 | `python tools/na_dzien.py 2000-01-01 konstytucja` |
| Art. 30 of the citizenship act on 1 January 2015 | `python tools/na_dzien.py 2015-01-01 obywatelstwo 30` |
| Which act wrote each paragraph of art. 30? | `git blame obywatelstwo/art-030.md` |
| Every change to art. 30, with the act and the day | `git log --follow obywatelstwo/art-030.md` |
| Everything one act changed | `git show --stat du/2013-1650` |
| What changed in the citizenship act on one day | `git show --stat obywatelstwo/2022-11-10` |
| What changed between two unified texts | `git diff tj/2022-465 tj/2023-1989 -- obywatelstwo` |
| The unified texts' own editorial changes | `git log --author="Marszałek Sejmu" --format="%ad %s" --date=short` |
| Acts amending the citizenship act in 2025 | `git log --format="%an %s" --author="Dz.U. 2025" -- obywatelstwo` |
| The Constitution's amendments and correction | `git log --format="%ad %an %s" --date=short -- konstytucja` |
| The amending acts with all their dates | [`akty.csv`](akty.csv) |

`--before` takes a bare date at the current time of day; to ask about a day, give its end:
`git rev-list -1 --before="2015-01-01T23:59:59+01:00" main -- obywatelstwo`. In PowerShell, quote the revision:
`$r = git rev-list -1 --before="2015-01-01T23:59:59+01:00" main; git show "$($r):obywatelstwo/art-030.md"`.
After a rebuild, refresh tags with `git fetch --force --tags`.

## The dates, and which one we use

A Polish act has the day it was passed (`Enacted:`, the "z dnia" date in its title), the day it was published in the
Journal of Laws (`Published:`), and the day it took effect (`In-force:`). **Commits are dated the day the change took
effect**, at noon in Warsaw (CET, or CEST in summer time). That day comes from the Sejm API, which gives for every
amending act the day its amendment of this act takes effect (an act can amend different acts on different days), and is
compared with the day the unified text's footnote gives. Where the amending act as a whole took effect on another day,
that day is in `Act-in-force:`.

## What "author" means

The author of a commit is the act that made the change: `Dz.U. 2013 poz. 1650` (with an address ending
`@sejm.invalid`, which cannot exist), so `git blame` names the act.

- **The citizenship act.** The Marshal of the Sejm periodically announces a unified text (tekst jednolity). Each unified
  text marks every unit changed since the last one with a footnote naming the act and its in-force day ("W brzmieniu
  ustalonym przez art. 29 pkt 1 ustawy z dnia 7 października 2022 r. ... (Dz. U. poz. 2185), która weszła w życie z
  dniem 10 listopada 2022 r."). Those footnotes credit each change. Where the amending act quotes the new wording
  ("otrzymuje brzmienie"), that wording is replayed on its day and checked against the next unified text, so a unit
  changed twice between two unified texts shows both steps (art. 30 ust. 1 pkt 7: 2014, then 2016).
- **Editorial changes** made by the unified text itself (updated Journal references of other acts, and provisions that
  amended other acts printed as "(pominięty)") are commits by `Marszałek Sejmu (tekst jednolity, ...)` on the day the
  unified text was published, labelled as editorial. They are never credited to a law.
- **The Constitution** has no unified text. Its two amendments (2006, art. 55; 2009, art. 99 ust. 3) are replayed from
  their own words and must equal the Sejm's consolidated text; the 2001 correction of two printing errors is a commit by
  the correction notice (`Dz.U. 2001 nr 28 poz. 319 (sprostowanie)`), not by a law.
- A change no footnote explains goes to the one act that took effect between the two unified texts ("date only"), or,
  if there were several, to `Kancelaria Sejmu (ISAP)` naming them in `Candidate:` trailers.

The committer is always `Lexifina`.

## How it is checked

`tools/check_repo.py` reads each checkpoint back from git with `tools/na_dzien.py` and compares it with the official
text: the citizenship act as published and every unified text (five as HTML, file by file and byte for byte; the 2025
one as PDF), and the Constitution's consolidated text; then word for word against all the words of the official text,
read independently of the parser. It also checks that, the day before each unified text was published, the history
differs from it only by that unified text's editorial changes. `tools/test_repo.py` checks that the commands above
work. The results are in [`REPRODUCE.md`](REPRODUCE.md).

## Files

Each act is a folder (`konstytucja/`, `obywatelstwo/`). Each article is one file (`art-055.md` is art. 55).
`## ` lines at the top of a file are the headings of the chapter (rozdział) or section that begins there, `# Art. 55.`
is the article's number, and each ustęp is one line; each punkt and litera is a list item. `konstytucja/preambula.md`
is the title and preamble. A repealed unit stays as "(uchylony)", as the unified texts print it.

## What it does not show

- A unified text of the Constitution: none exists; its consolidated text is the Sejm's, for information.
- Which words of a line each act wrote, when two acts changed the same line: blame credits whole lines (use
  `git log -p --word-diff`).
- Any act beyond these two. The same build works for any act with unified texts in the API: add it to `ACTS` in
  `tools/build.py`.
- The unified texts and the Sejm's consolidated texts are for information; the legally binding text is the act as
  published in the Journal of Laws.

## How it is built

`tools/build.py` reads the Sejm's API and writes this repository from scratch; the same data gives the same hashes.
Every step, the software, the decisions made by hand and what an AI model did are in [`REPRODUCE.md`](REPRODUCE.md).
Each act's folder has a `README.md` listing its articles with how often each changed. [`corpus.json`](corpus.json)
describes the corpus for tools that read several of Lexifina's law repositories.

## Licence

Normative acts and official documents are not protected by copyright in Poland (ustawa z dnia 4 lutego 1994 r. o prawie
autorskim i prawach pokrewnych, art. 4 pkt 1 and 2). Source: Sejm Rzeczypospolitej Polskiej, ELI API
(api.sejm.gov.pl), Kancelaria Sejmu. The Sejm's consolidated text of the Constitution is marked "©Kancelaria Sejmu"; it
is used here as a checkpoint for the text of the act. The history, commit messages, tables and tools are released under
[CC0 1.0](LICENSE).

---

## Po polsku

Dwa akty Rzeczypospolitej Polskiej jako repozytorium git: Konstytucja RP (Dz.U. 1997 nr 78 poz. 483) i ustawa z dnia
2 kwietnia 2009 r. o obywatelstwie polskim (Dz.U. 2012 poz. 161), z API ELI Sejmu.

- **Każdy commit to jeden akt zmieniający**, wpisany jako autor (`Dz.U. 2013 poz. 1650`), więc `git blame` pokazuje,
  który akt napisał który ustęp. Akt wskazują przypisy tekstów jednolitych.
- **Każdy commit ma dzień wejścia w życie**, w południe czasu warszawskiego; dzień uchwalenia i ogłoszenia są w treści.
- **Każdy artykuł to plik**, każdy ustęp to wiersz.
- **Zmiany redakcyjne tekstu jednolitego** (odesłania do Dziennika Ustaw, przepisy pominięte) mają osobne commity
  Marszałka Sejmu i nie są przypisane żadnej ustawie.

Teksty jednolite i tekst ujednolicony Konstytucji mają charakter informacyjny; tekstem wiążącym jest tekst ogłoszony
w Dzienniku Ustaw.
