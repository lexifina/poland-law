# How this history was made, and how to make it again

This file records how the repository was built: the sources, the commands, the software, the decisions made by hand,
and what an AI model did and did not do. The build writes it, so it describes the build that made this commit.

## Short version

```sh
git clone https://github.com/lexifina/poland-law && cd poland-law
pip install lxml pymupdf
python -X utf8 tools/build.py --repo ../rebuilt --today 2026-11-02
git -C ../rebuilt rev-parse main        # the same hash as this repository's main
python -X utf8 tools/check_repo.py --repo ../rebuilt --no-record
```

Since 2026-11-02 this history grows append-only: new acts and corrections go on top of the published
`main`, and nothing published is rewritten. The first 22 commits (the Constitution and the citizenship act) come from
the first build of 2026-10-28; a rebuild gives the same law text, but not their hashes. The codes appended later are
built by `tools/build.py --append <slugs>` on top of the published `main`.

`tools/build.py` needs Python 3.12 or later with `lxml` and `pymupdf`, and git. It reads the Sejm's ELI API (or its own
cache, `.cache/` next to the script) and writes this repository into `--repo`. With the same data and the same
`--today` it gives the same commits with the same hashes. `data/zrodla.json` lists every address read with the sha256
of the answer, so a rebuild can show it read the same bytes.

## Sources

All legal text and all information about amending acts comes from the **ELI API of the Sejm**
(`https://api.sejm.gov.pl/eli`, Kancelaria Sejmu): act metadata (JSON), the texts as HTML (`/acts/DU/<year>/<pos>/text.html`) and PDF
(`/acts/DU/<year>/<pos>/text/<type>/<file>`: O = the Journal as published, U = the Sejm's consolidated text). Nothing
was typed in, summarised or rewritten. The build read 375 metadata records, 322 HTML texts and 3 PDFs,
retrieved on 2026-10-28, 2026-11-02.

Terms. The API's documentation pages (`https://api.sejm.gov.pl/`, `eli.html`, `eli_pl.html`) state no terms of use
and no rate limit. `https://api.sejm.gov.pl/robots.txt` answers with the gateway's "Request Rejected" page (no
robots.txt is served). ISAP's own pages (`isap.sejm.gov.pl`) were not read; only the API was used.
No rule naming ClaudeBot, Claude-Web or anthropic-ai was found anywhere. Normative acts and official documents are not
protected by copyright in Poland (ustawa o prawie autorskim i prawach pokrewnych, art. 4 pkt 1 and 2).

| Act | Checkpoint | Day | Format | What |
| --- | --- | --- | --- | --- |
| Konstytucja | Dz.U. 1997 nr 78 poz. 483 | 1997-10-17 | ocr | tekst ogłoszony (scan of the 1997 Journal, read word for word, OCR) |
| Konstytucja | Dz.U. 1997 nr 78 poz. 483 (tekst ujednolicony) | 2009-10-21 | pdf-u | tekst ujednolicony (Kancelaria Sejmu) |
| Obywatelstwo | Dz.U. 2012 poz. 161 | 2012-08-15 | html | tekst ogłoszony (the act as published) |
| Obywatelstwo | Dz.U. 2017 poz. 1462 | 2017-07-31 | html | tekst jednolity |
| Obywatelstwo | Dz.U. 2018 poz. 1829 | 2018-09-26 | html | tekst jednolity |
| Obywatelstwo | Dz.U. 2020 poz. 347 | 2020-03-04 | html | tekst jednolity |
| Obywatelstwo | Dz.U. 2022 poz. 465 | 2022-02-25 | html | tekst jednolity |
| Obywatelstwo | Dz.U. 2023 poz. 1989 | 2023-09-25 | html | tekst jednolity |
| Obywatelstwo | Dz.U. 2025 poz. 1611 | 2025-11-24 | pdf | tekst jednolity |
| Kodeks cywilny | Dz.U. 1964 nr 16 poz. 93 | 1965-01-01 | html | tekst ogłoszony (the act as published) |
| Kodeks cywilny | Dz.U. 2014 poz. 121 | 2014-01-23 | html | tekst jednolity |
| Kodeks cywilny | Dz.U. 2016 poz. 380 | 2016-03-22 | html | tekst jednolity |
| Kodeks cywilny | Dz.U. 2017 poz. 459 | 2017-03-02 | html | tekst jednolity |
| Kodeks cywilny | Dz.U. 2018 poz. 1025 | 2018-05-29 | html | tekst jednolity |
| Kodeks cywilny | Dz.U. 2019 poz. 1145 | 2019-06-19 | html | tekst jednolity |
| Kodeks cywilny | Dz.U. 2020 poz. 1740 | 2020-10-08 | html | tekst jednolity |
| Kodeks cywilny | Dz.U. 2022 poz. 1360 | 2022-06-29 | html | tekst jednolity |
| Kodeks cywilny | Dz.U. 2023 poz. 1610 | 2023-08-14 | html | tekst jednolity |
| Kodeks cywilny | Dz.U. 2024 poz. 1061 | 2024-07-17 | html | tekst jednolity |
| Ordynacja podatkowa | Dz.U. 1997 nr 137 poz. 926 | 1998-01-01 | html | tekst ogłoszony (the act as published) |
| Ordynacja podatkowa | Dz.U. 2005 nr 8 poz. 60 | 2005-01-14 | html | tekst jednolity |
| Ordynacja podatkowa | Dz.U. 2012 poz. 749 | 2012-07-03 | html | tekst jednolity |
| Ordynacja podatkowa | Dz.U. 2015 poz. 613 | 2015-05-06 | html | tekst jednolity |
| Ordynacja podatkowa | Dz.U. 2017 poz. 201 | 2017-02-01 | html | tekst jednolity |
| Ordynacja podatkowa | Dz.U. 2018 poz. 800 | 2018-04-27 | html | tekst jednolity |
| Ordynacja podatkowa | Dz.U. 2019 poz. 900 | 2019-05-14 | html | tekst jednolity |
| Ordynacja podatkowa | Dz.U. 2020 poz. 1325 | 2020-07-31 | html | tekst jednolity |
| Ordynacja podatkowa | Dz.U. 2021 poz. 1540 | 2021-08-23 | html | tekst jednolity |
| Ordynacja podatkowa | Dz.U. 2022 poz. 2651 | 2022-12-16 | html | tekst jednolity |

## The build, step by step

1. `python -X utf8 scripts/poland-law/build.py --today 2026-11-02` in Lexifina's own repository fetched the data into its
   cache and wrote this repository. The files in `tools/` are the same files as in `scripts/poland-law/` there
   (git blobs: `build.py` 6bec877eae70, `parse.py` 864eda49695b, `pdfparse.py` 3056ad6a05e5, `gloss.py` 404e4b159519, `reproduce.py` 9db827df15c9).
2. `python -X utf8 scripts/poland-law/check_repo.py` read each checkpoint back from this repository with
   `tools/na_dzien.py` and compared it with the official text. Results:
   (not yet run)
3. `python -X utf8 scripts/poland-law/build.py --offline --verify-rebuild` built the repository again from the same
   cache into a temporary folder and compared the hashes. A second build from the same cache into an empty folder gave the same history: the last law commit was `ca2d3817cf159f42b24db9ca16dfe001a6a918fe` in both, and every one of the 21 law commits and 42 tags had the same hash.
4. `python -X utf8 scripts/poland-law/test_repo.py --record` ran the reader's commands (? of
   ? passed):
   (not yet run)
5. The build was run again to write these results into this file, and `main` was rebuilt and compared hash for hash
   before it was pushed to the private GitHub repository `lexifina/poland-law`.

Software: Python 3.12.10, git version 2.46.0.windows.1, lxml 6.1.3, PyMuPDF 2.0.

## How causes and dates were read

- **The codes and statutes added since 2026-11-02** (`kodeks-cywilny/`, `ordynacja-podatkowa/`) are read the same way as the
  citizenship act: each starts as published in the Journal (the API's HTML of the original act, on its in-force day),
  each unified text with an HTML text is a checkpoint, and every change between two of them is credited by the unified
  text's footnotes to the act they name, on the in-force day the API gives (a footnote that gives a unit its own later
  day, "wszedł w życie z dniem ...", is dated by that day). The first unified text of an old code footnotes the changes
  of decades; a change no footnote explains is committed on the unified text's day and credited to no act. Each code's
  record ends at its last unified text published as HTML; the newer unified texts (PDF only) and the amendments in
  force after that day are not in the record yet.
- A unit numbered with a paragraph sign (§) is named `§ N` in the commit messages.

- **The citizenship act** (`obywatelstwo/`) starts as published (Dz.U. 2012 poz. 161, HTML), in two stages as its
  art. 70 says (chapter 5 and art. 65 from 2012-05-15, the rest from 2012-08-15). Each unified text is a checkpoint.
  Between two of them every changed unit is credited by the unified text's own footnotes ("W brzmieniu ustalonym
  przez art. ...", "Dodany przez art. ...", "Przez art. ..." for repeals), resolved to the act they name (including
  "ustawy, o której mowa w odnośniku N"). The day is the in-force day the API gives for that act's amendment of this
  act; the footnote's own day is compared with it. Where the amending act quotes the new wording, that wording is
  replayed on its day and checked against the next unified text (Konstytucja: 9 of 9 quoted lines; Obywatelstwo: 21 of 22 quoted lines; Kodeks cywilny: 722 of 838 quoted lines; Ordynacja podatkowa: 2121 of 2529 quoted lines).
- **Editorial changes of the unified texts** (updated Journal references of the other acts cited, provisions left out
  as "(pominięty)") are separate commits, authored by the Marshal of the Sejm's unified text, on the day it was
  published. A line changed by an act keeps the Journal references it had until then.
- **The Constitution** (`konstytucja/`) has no unified text. The current text is the Sejm's consolidated text (PDF,
  type U). The 2006 and 2009 amending acts are replayed from their own words (HTML) and must equal it; the
  correction notice of 2001 (Dz.U. 2001 nr 28 poz. 319) is applied word by word and its commit is authored by the
  notice, not by a law. The text as enacted is the consolidated text with those three steps undone; art. 55 as enacted
  is read from the text layer of the 1997 Journal's scan (O), between "Art. 55." and "Art. 56.".
- Commits are dated noon in Warsaw on the in-force day (CET, CEST from the last Sunday in March to the last Sunday in
  October). Counts: editorial 18, law 332, start 2, unexplained 18; 635 tags.

## Decisions made by hand

- The acts: the Constitution, and the citizenship act (ustawa o obywatelstwie polskim) as the frequently amended
  mid-size act: 9 amending acts, 6 unified texts, all footnoted. The Electoral Code (Kodeks wyborczy) was considered;
  15 of its 40 amending acts fall before its first unified text, so most of its changes could not be told apart.
- Art. 55 of the Constitution as enacted was compared with the page image of the 1997 Journal (page 12 of the PDF) by
  eye; the text layer reads it correctly. The 1997 scan's text layer has OCR errors elsewhere, so the word check against
  it is reported, not required to be zero.
- The PDF unified text (Dz.U. 2025 poz. 1611, no HTML) is read with `tools/pdfparse.py`; the same parser, run on the
  PDF of Dz.U. 2023 poz. 1989, gives exactly the lines of that text's HTML except dash characters (the PDF prints
  U+2212 where the HTML has a hyphen), so dashes are compared as one character.
- The title and preamble of the Constitution are `konstytucja/preambula.md`; the preamble is two paragraphs, split
  where its first sentence ends.

## Notes from the build

- kodeks-cywilny art. 8 § 2: DU/1993/78 in force 1993-03-16 (footnote, used) but 1993-03-14 (API)
- kodeks-cywilny art. 34: the words of DU/1990/321 art. 1 pkt 4 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 40 § 3: the change by DU/1990/321 before DU/2003/408 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 55¹ pkt 7: the change by DU/1990/321 before DU/2003/408 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 55¹ pkt 8: the change by DU/1990/321 before DU/2003/408 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 55¹ pkt 9: the change by DU/1990/321 before DU/2003/408 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 55¹: the change by DU/1990/321 before DU/2003/408 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 70¹ § 3: the change by DU/1996/542 before DU/2003/408 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 70¹ § 4: the change by DU/1996/542 before DU/2003/408 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 70² § 3: the change by DU/1996/542 before DU/2003/408 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 72 § 2: the words of DU/2003/408 art. 1 pkt 17 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 79: the change by DU/1996/542 before DU/2002/984 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 79: the change by DU/1998/668 before DU/2002/984 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 156: the words of DU/2011/458 art. 1 pkt 1 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 215: the change by DU/1982/81 before DU/1990/321 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 216 § 2 pkt 1: the words of DU/1990/321 art. 1 pkt 37 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 232 § 1: the change by DU/1985/99 before DU/1996/542 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 232 § 1: the change by DU/1990/198 before DU/1996/542 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 232 § 1: the change by DU/1990/321 before DU/1996/542 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 232 § 2: the change by DU/1990/321 before DU/1997/741 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 243: the change by DU/1990/321 before DU/1996/542 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 246 § 2: the words of DU/1982/147 art. 113 pkt 2 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 267 § 2: DU/1994/96 in force 1994-09-02 (footnote, used) but 1994-09-01 (API)
- kodeks-cywilny art. 270¹: the change by DU/2000/855 before DU/2011/1370 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 357¹: the change by DU/1990/321 before DU/1996/542 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 384 § 4: the change by DU/2000/271 before DU/2003/408 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 384 § 5: the change by DU/2000/271 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 385¹ § 1: the change by DU/1990/321 before DU/2000/271 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 385¹ § 1: the words of DU/2000/271 art. 18 pkt 4 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385¹ § 2: the change by DU/1990/321 before DU/2000/271 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 385¹ § 3: the change by DU/1990/321 before DU/2000/271 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 385¹ § 3: the words of DU/2000/271 art. 18 pkt 4 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385¹ § 4: the change by DU/1990/321 before DU/2000/271 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 385²: the change by DU/1990/321 before DU/2000/271 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 385³ pkt 1: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 10: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 11: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 12: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 13: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 14: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 15: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 16: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 17: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 18: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 19: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 2: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 20: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 21: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 22: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 3: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 4: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 5: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 6: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 7: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 8: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 385³ pkt 9: the words of DU/2000/271 art. 18 pkt 5 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 420¹: the change by DU/1996/542 before DU/2004/1692 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 421: the words of DU/2004/1692 art. 1 pkt 4 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 446¹: DU/1993/78 in force 1993-03-16 (footnote, used) but 1993-03-14 (API)
- kodeks-cywilny art. 446¹: DU/1993/78 in force 1993-03-16 (footnote, used) but 1993-03-14 (API)
- kodeks-cywilny art. 575¹: the words of DU/1996/542 art. 1 pkt 25 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 579: the words of DU/1996/542 art. 1 pkt 29 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 647¹: DU/2003/408 in force 2003-04-24 (footnote, used) but 2003-09-25 (API)
- kodeks-cywilny art. 647¹ § 1: DU/2003/408 in force 2003-04-24 (footnote, used) but 2003-09-25 (API)
- kodeks-cywilny art. 647¹ § 2: DU/2003/408 in force 2003-04-24 (footnote, used) but 2003-09-25 (API)
- kodeks-cywilny art. 647¹ § 3: DU/2003/408 in force 2003-04-24 (footnote, used) but 2003-09-25 (API)
- kodeks-cywilny art. 647¹ § 4: DU/2003/408 in force 2003-04-24 (footnote, used) but 2003-09-25 (API)
- kodeks-cywilny art. 647¹ § 5: DU/2003/408 in force 2003-04-24 (footnote, used) but 2003-09-25 (API)
- kodeks-cywilny art. 647¹ § 6: DU/2003/408 in force 2003-04-24 (footnote, used) but 2003-09-25 (API)
- kodeks-cywilny art. 691 § 1: the change by DU/1994/509 before DU/2001/733 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 691 § 2: the change by DU/1994/509 before DU/2001/733 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 691 § 3: the change by DU/1994/509 before DU/2001/733 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 691 § 4: the change by DU/1994/509 before DU/2001/733 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 691 § 5: the change by DU/1994/509 before DU/2001/733 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 720 § 2: the words of DU/1990/321 art. 1 pkt 96 lit. b differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 812 § 9: the change by DU/2003/1151 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 817 § 2: the change by DU/2007/557 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 819 § 4: the change by DU/2007/557 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 819 § 4: the change by DU/2007/557 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 822 § 5: the change by DU/2003/1151 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 824¹ § 3: the change by DU/2003/1151 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 828 § 1: the change by DU/2007/557 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 828 § 1: the change by DU/2007/557 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 828 § 3: the change by DU/1984/242 before DU/2007/557 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 846 § 5: the words of DU/1998/758 art. 1 pkt 1 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 932 § 6: the change by DU/2009/662 before DU/2011/458 is not reconstructed (no quoted wording)
- kodeks-cywilny art. 995 § 1: the words of DU/2011/458 art. 1 pkt 16 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 1026: the words of DU/2007/1287 art. 2 pkt 2 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 1034¹ § 2: the words of DU/2011/458 art. 1 pkt 24 differ from DU/2014/121; the unified text is used
- kodeks-cywilny art. 1039 § 2: the words of DU/2011/458 art. 1 pkt 25 differ from DU/2014/121; the unified text is used
- kodeks-cywilny DU/2014/121: 448 lines changed with no footnote
- kodeks-cywilny DU/1985/99 (in force 1985-08-01): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/1990/198 (in force 1990-05-27): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/1991/496 (in force 1992-03-15): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/1997/1040 (in force 1997-12-23): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/1997/272 (in force 1997-05-15): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/1997/439 (in force 1994-11-12): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/1998/668 (in force 1999-01-01): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/2000/855 (in force 2000-12-09): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/2001/1638 (in force 2001-12-18): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/2005/462 (in force 2006-07-15): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/2006/1166 (in force 2007-12-31): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/2006/935 (in force 2006-08-05): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/2007/554 (in force 2008-05-11): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/2009/1675 (in force 2009-12-18): listed by the API, but no unit of DU/2014/121 is credited to it
- kodeks-cywilny DU/2016/380: 53 lines changed with no footnote
- kodeks-cywilny DU/2015/1311: in force 2016-09-08, after the unified text DU/2016/380 of 2016-03-22 that prints it
- kodeks-cywilny DU/2015/1357 (in force 2016-03-11): listed by the API, but no unit of DU/2016/380 is credited to it
- kodeks-cywilny art. 109⁸ § 2: the words of DU/2016/2255 art. 1 pkt 2 differ from DU/2017/459; the unified text is used
- kodeks-cywilny DU/2017/459: 20 lines changed with no footnote
- kodeks-cywilny DU/2015/1433 (in force 2016-05-01): listed by the API, but no unit of DU/2017/459 is credited to it
- kodeks-cywilny DU/2018/1025: 2 lines changed with no footnote
- kodeks-cywilny DU/2019/1145: 8 lines changed with no footnote
- kodeks-cywilny art. 387¹: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-cywilny art. 387¹ pkt 1: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-cywilny art. 387¹ pkt 1: the words of DU/2020/875 art. 1 differ from DU/2020/1740; the unified text is used
- kodeks-cywilny art. 387¹ pkt 2: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-cywilny art. 387¹ pkt 3: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-cywilny art. 387¹: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-cywilny DU/2020/1740: 19 lines changed with no footnote
- kodeks-cywilny DU/2022/1360: 20 lines changed with no footnote
- kodeks-cywilny DU/2023/1610: 46 lines changed with no footnote
- kodeks-cywilny art. 448 § 1: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 448 § 2: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 448 § 3: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 480 § 4: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 928 § 1 pkt 4: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 928 § 1 pkt 5: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 934 § 2: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 934 § 2¹: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 934 § 3: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 1015 § 1¹: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 1015 § 1²: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny art. 1019 § 1 pkt 3: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-cywilny DU/2024/1061: 6 lines changed with no footnote
- kodeks-cywilny DU/2023/1285 (in force 2024-01-07): listed by the API, but no unit of DU/2024/1061 is credited to it
- kodeks-cywilny DU/2024/1237 (in force 2024-08-29): after the last unified text; not in the record
- kodeks-cywilny DU/2025/1172 (in force 2025-11-27): after the last unified text; not in the record
- kodeks-cywilny DU/2025/1508 (in force 2025-12-04): after the last unified text; not in the record
- kodeks-cywilny DU/2025/769 (in force 2025-07-13): after the last unified text; not in the record
- kodeks-cywilny DU/2026/184 (in force 2026-05-19): after the last unified text; not in the record
- kodeks-cywilny DU/2026/507 (in force 2028-11-01): after the last unified text; not in the record
- kodeks-cywilny DU/2016/380: 10 lines differ from the unified text for no reason found: art. 65¹, art. 65¹, art. 77², art. 77², art. 77³, art. 77³, art. 78¹, art. 78¹ § 1
- ordynacja-podatkowa art. 3 pkt 1: the words of DU/2002/1387 art. 1 pkt 2 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 3 pkt 2: the words of DU/2002/1387 art. 1 pkt 2 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 3 pkt 7: the words of DU/2002/1387 art. 1 pkt 2 lit. d differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 3 pkt 8: the words of DU/2002/1387 art. 1 pkt 2 lit. d differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 12 § 6 pkt 1: the words of DU/2002/1387 art. 1 pkt 5 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 12 § 6 pkt 2: the words of DU/2003/1188 art. 83 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 12 § 6 pkt 3: the words of DU/2002/1387 art. 1 pkt 5 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 12 § 6 pkt 4: the words of DU/2002/1387 art. 1 pkt 5 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 13 § 1 pkt 1: the words of DU/2003/1302 art. 20 pkt 1 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 13 § 1 pkt 2 lit. c: the words of DU/2003/1302 art. 20 pkt 1 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 13 § 2 pkt 1: the words of DU/2003/1302 art. 20 pkt 1 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 14a § 1: the words of DU/2002/1387 art. 1 pkt 6 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 14a § 2: the words of DU/2002/1387 art. 1 pkt 6 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 14a § 3: the words of DU/2002/1387 art. 1 pkt 6 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 14a § 4: the words of DU/2002/1387 art. 1 pkt 6 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 14a § 5: the words of DU/2002/1387 art. 1 pkt 6 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 14b § 1: the words of DU/2002/1387 art. 1 pkt 6 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 14b § 2: the words of DU/2002/1387 art. 1 pkt 6 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 14b § 3: the words of DU/2002/1387 art. 1 pkt 6 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 18 § 2: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 22 § 1: DU/2000/1315 in force 2001-01-01 (footnote, used) but 2001-01-15 (API)
- ordynacja-podatkowa art. 22 § 1 pkt 1: DU/2000/1315 in force 2001-01-01 (footnote, used) but 2001-01-15 (API)
- ordynacja-podatkowa art. 22 § 1 pkt 1: the words of DU/2000/1315 art. 5 pkt 1 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 22 § 1 pkt 2: DU/2000/1315 in force 2001-01-01 (footnote, used) but 2001-01-15 (API)
- ordynacja-podatkowa art. 22 § 1a: DU/2000/1315 in force 2001-01-01 (footnote, used) but 2001-01-15 (API)
- ordynacja-podatkowa art. 22 § 5: DU/2000/1315 in force 2001-01-01 (footnote, used) but 2001-01-15 (API)
- ordynacja-podatkowa art. 22 § 6: the change by DU/2001/459 before DU/2002/1387 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 23 § 3 pkt 1: the words of DU/2002/1387 art. 1 pkt 15 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 23 § 3 pkt 2: the words of DU/2002/1387 art. 1 pkt 15 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 23 § 3 pkt 3: the words of DU/2002/1387 art. 1 pkt 15 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 23 § 3 pkt 4: the words of DU/2002/1387 art. 1 pkt 15 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 23 § 3 pkt 5: the words of DU/2002/1387 art. 1 pkt 15 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 25: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 28 § 3: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 28 § 3 pkt 1: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 28 § 3 pkt 1: the words of DU/2001/459 art. 1 pkt 6 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 29 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 21 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 29 § 2 pkt 2: the words of DU/2002/1387 art. 1 pkt 21 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 29 § 2 pkt 3: the words of DU/2002/1387 art. 1 pkt 21 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 33 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 24 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 33 § 2 pkt 2: the words of DU/2002/1387 art. 1 pkt 24 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 33 § 4 pkt 1: the words of DU/2002/1387 art. 1 pkt 24 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 33a § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 25 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 33a § 1 pkt 2: the words of DU/2002/1387 art. 1 pkt 25 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 33b pkt 1: the words of DU/2002/1387 art. 1 pkt 25 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 34 § 3 pkt 1: the words of DU/2002/1387 art. 1 pkt 26 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 34 § 3 pkt 2: the words of DU/2002/1387 art. 1 pkt 26 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 34 § 4 pkt 1: the words of DU/2002/1387 art. 1 pkt 26 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 34 § 4 pkt 2: the words of DU/2002/1387 art. 1 pkt 26 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 34 § 4 pkt 3: the words of DU/2002/1387 art. 1 pkt 26 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 34 § 4 pkt 4: the words of DU/2002/1387 art. 1 pkt 26 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 35 § 2 pkt 1 lit. g: the words of DU/2002/1387 art. 1 pkt 27 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 39 § 3: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 39 § 3a: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 46 § 3: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 46 § 3 pkt 1: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 46 § 3 pkt 1: the words of DU/2001/459 art. 1 pkt 18 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 46 § 3 pkt 2: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 47 § 5: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 48 § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 37 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 48 § 1 pkt 2: the words of DU/2002/1387 art. 1 pkt 37 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 48 § 3: the words of DU/2002/1387 art. 1 pkt 37 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 50: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 53 § 5 pkt 1: the words of DU/2002/1387 art. 1 pkt 42 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 54 § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 44 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 54 § 1 pkt 2: the words of DU/2002/1387 art. 1 pkt 44 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 54 § 1 pkt 3: the words of DU/2002/1387 art. 1 pkt 44 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 54 § 1 pkt 4: the words of DU/2002/1387 art. 1 pkt 44 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 54 § 1 pkt 5: the words of DU/2002/1387 art. 1 pkt 44 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 54 § 1 pkt 6: the words of DU/2002/1387 art. 1 pkt 44 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 54 § 1 pkt 7: the words of DU/2002/1387 art. 1 pkt 44 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 1 pkt 2: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 1 pkt 3: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 1 pkt 4: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 1 pkt 5: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 1 pkt 6: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 1 pkt 7: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 1 pkt 8: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 2 pkt 2: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 2 pkt 3: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 59 § 2 pkt 4: the words of DU/2002/1387 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 60 § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 48 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 60 § 3: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 61 § 4: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 63 § 2 pkt 1: the change by DU/2001/459 before DU/2002/1387 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 63 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 51 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 64 § 1 pkt 4: the words of DU/1997/1083 art. 5 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 64 § 5 pkt 1: the words of DU/2002/1387 art. 1 pkt 52 lit. c differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 64 § 7: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- ordynacja-podatkowa art. 65 § 2: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- ordynacja-podatkowa art. 67 § 1a: DU/2000/1315 in force 2001-01-01 (footnote, used) but 2001-01-15 (API)
- ordynacja-podatkowa art. 67 § 1a: the words of DU/2000/1315 art. 5 pkt 3 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 67 § 3: the change by DU/2001/459 before DU/2002/1387 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 67 § 4: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 67 § 4 pkt 1: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 67 § 4 pkt 1: the words of DU/2001/459 art. 1 pkt 26 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 67 § 4 pkt 2: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 67 § 4 pkt 2: the words of DU/2001/459 art. 1 pkt 26 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 67 § 4 pkt 3: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 67 § 4 pkt 3: the words of DU/2001/459 art. 1 pkt 26 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 67 § 4 pkt 4: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 70 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 58 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 70 § 6 pkt 1: the words of DU/2002/1387 art. 1 pkt 58 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 70 § 7 pkt 1: the words of DU/2002/1387 art. 1 pkt 58 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 82 § 1 pkt 2: the change by DU/2001/459 before DU/2002/1387 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 82 § 6 pkt 1: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 82 § 6 pkt 1: the words of DU/2001/459 art. 1 pkt 34 lit. d differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 82a § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 63 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 83: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 84 § 2: the change by DU/2001/459 before DU/2002/1387 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 85: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 87 § 5: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 89 pkt 1: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 89 pkt 2: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 89 pkt 2 lit. b: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 89: DU/2001/459 in force 2001-05-04 (footnote, used) but 2001-06-05 (API)
- ordynacja-podatkowa art. 93 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 71 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 93a § 2 pkt 1 lit. b: the words of DU/2002/1387 art. 1 pkt 72 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 93c § 1 pkt 1 lit. b: the words of DU/2002/1387 art. 1 pkt 72 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 94: DU/2002/1387 in force 2001-01-01 (footnote, used) but 2003-01-01 (API)
- ordynacja-podatkowa art. 98 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 77 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 98 § 2 pkt 2: the words of DU/2002/1387 art. 1 pkt 77 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 98 § 2 pkt 3: the words of DU/2002/1387 art. 1 pkt 77 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 98 § 2 pkt 4: the words of DU/2002/1387 art. 1 pkt 77 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 98 § 2 pkt 5: the words of DU/2002/1387 art. 1 pkt 77 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 98 § 2 pkt 6: the words of DU/2002/1387 art. 1 pkt 77 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 102 § 3: the words of DU/2002/1387 art. 1 pkt 81 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 103 § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 82 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 103 § 1 pkt 2: the words of DU/2002/1387 art. 1 pkt 82 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 103 § 1 pkt 3: the words of DU/2002/1387 art. 1 pkt 82 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 103 § 1 pkt 4: the words of DU/2002/1387 art. 1 pkt 82 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 103 § 1 pkt 5: the words of DU/2002/1387 art. 1 pkt 82 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 105 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 84 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 108 § 1: the words of DU/2002/1387 art. 1 pkt 86 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 108 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 86 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 108 § 2 pkt 2 lit. d: the words of DU/2002/1387 art. 1 pkt 86 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 109 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 87 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 109 § 2 pkt 2: the words of DU/2002/1387 art. 1 pkt 87 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 112 § 4 pkt 1: the words of DU/2002/1387 art. 1 pkt 90 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 112 § 7 pkt 1: the words of DU/2002/1387 art. 1 pkt 90 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 116 § 1 pkt 1 lit. b: the words of DU/2002/1387 art. 1 pkt 94 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 130 § 1: the words of DU/2002/1387 art. 1 pkt 102 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 130 § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 102 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 130 § 1 pkt 2: the words of DU/2002/1387 art. 1 pkt 102 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 130 § 1 pkt 3: the words of DU/2002/1387 art. 1 pkt 102 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 130 § 1 pkt 4: the words of DU/2002/1387 art. 1 pkt 102 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 130 § 1 pkt 5: the words of DU/2002/1387 art. 1 pkt 102 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 130 § 1 pkt 6: the words of DU/2002/1387 art. 1 pkt 102 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 130 § 1 pkt 7: the words of DU/2002/1387 art. 1 pkt 102 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 131 § 1 pkt 1: the words of DU/2003/1302 art. 20 pkt 10 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 131 § 1 pkt 2: the words of DU/2003/1302 art. 20 pkt 10 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 131 § 1 pkt 3: the words of DU/2003/1302 art. 20 pkt 10 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 131 § 2 pkt 1: the words of DU/2003/1302 art. 20 pkt 10 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 132 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 104 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 132 § 2 pkt 2: the words of DU/2002/1387 art. 1 pkt 104 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 141 § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 111 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 143 § 2 pkt 3: the words of DU/2003/1302 art. 20 pkt 13 lit. b differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 150 § 1 pkt 1: the change by DU/2002/1387 before DU/2003/1302 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 150 § 1 pkt 2: the change by DU/2002/1387 before DU/2003/1302 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 150 § 1a: the change by DU/2001/459 before DU/2003/1302 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 165 § 5 pkt 1: the words of DU/2001/459 art. 1 pkt 47 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 169 § 3 pkt 1: the words of DU/2002/1387 art. 1 pkt 124 lit. b differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 181: the words of DU/2002/1387 art. 1 pkt 128 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 183 pkt 1: the words of DU/2003/1302 art. 20 pkt 17 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 183 pkt 2: the words of DU/2003/1302 art. 20 pkt 17 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 184 § 3 pkt 1: the words of DU/2003/1302 art. 20 pkt 17 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 200 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 137 lit. b differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 205a § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 141 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 205a § 1 pkt 2: the words of DU/2002/1387 art. 1 pkt 141 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 205a § 1 pkt 3: the words of DU/2002/1387 art. 1 pkt 141 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 221: the change by DU/2001/459 before DU/2002/1387 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 224 § 3 pkt 1: the words of DU/2002/1387 art. 1 pkt 151 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 241 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 162 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 245 § 1 pkt 1: the words of DU/2002/1387 art. 1 pkt 166 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 245 § 1 pkt 2: the words of DU/2002/1387 art. 1 pkt 166 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 248 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 169 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 253b pkt 1: the words of DU/2002/1387 art. 1 pkt 173 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 253b pkt 2: the words of DU/2002/1387 art. 1 pkt 173 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 253b pkt 3: the words of DU/2002/1387 art. 1 pkt 173 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 253b pkt 4: the words of DU/2002/1387 art. 1 pkt 173 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 253b pkt 5: the words of DU/2002/1387 art. 1 pkt 173 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 259 § 1: the words of DU/2001/459 art. 1 pkt 55 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 262 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 180 lit. b differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 278 § 1 pkt 1: the words of DU/2003/1302 art. 20 pkt 24 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 278 § 1 pkt 2: the words of DU/2003/1302 art. 20 pkt 24 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 278 § 1 pkt 3: the words of DU/2003/1302 art. 20 pkt 24 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 278 § 6 pkt 1: the words of DU/2003/1302 art. 20 pkt 24 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 283 § 1 pkt 1a: the words of DU/2003/1302 art. 20 pkt 27 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 283 § 2 pkt 3: the words of DU/2004/1808 art. 27 pkt 7 lit. b differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 283 § 2 pkt 6: the words of DU/2004/1808 art. 27 pkt 7 lit. c differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 283 § 2 pkt 7: the words of DU/2004/1808 art. 27 pkt 7 lit. c differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 286 § 1 pkt 4: the words of DU/2004/1808 art. 27 pkt 11 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 293 § 2 pkt 1: the words of DU/2002/1387 art. 1 pkt 194 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 293 § 2 pkt 2: the words of DU/2002/1387 art. 1 pkt 194 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 293 § 2 pkt 3: the words of DU/2002/1387 art. 1 pkt 194 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 293 § 2 pkt 4: the words of DU/2002/1387 art. 1 pkt 194 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 294 § 1 pkt 1a: the words of DU/2003/1302 art. 20 pkt 30 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 294 § 1 pkt 2: the words of DU/2002/1387 art. 1 pkt 195 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 295 pkt 1: the words of DU/2004/868 art. 1 pkt 2 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 297 § 1 pkt 2a: the words of DU/2000/1216 art. 46 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 297 § 1 pkt 4: the words of DU/2002/1271 art. 53 pkt 3 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 297 § 1 pkt 5 lit. b: the words of DU/2002/1271 art. 53 pkt 3 lit. b differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 298 pkt 3a: the words of DU/2001/459 art. 1 pkt 61 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 298 pkt 5: the words of DU/2002/1387 art. 1 pkt 197 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 298 pkt 6a: the words of DU/2001/475 art. 5 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 1: the words of DU/2001/459 art. 1 pkt 62 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 10: the change by DU/2001/459 before DU/2004/593 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 299 § 3 pkt 3: the words of DU/2001/459 art. 1 pkt 62 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 4: the words of DU/2001/459 art. 1 pkt 62 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 5: the words of DU/2001/459 art. 1 pkt 62 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 6: the words of DU/2002/1387 art. 1 pkt 198 lit. b differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 7: the change by DU/2001/459 before DU/2001/1189 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 299 § 3 pkt 7: the words of DU/2001/1189 art. 70 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 8: the change by DU/2001/459 before DU/2001/1452 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 299 § 3 pkt 8: the words of DU/2001/1452 art. 3 lit. a differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 9: the change by DU/2001/459 before DU/2003/2255 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 299 § 3 pkt 9: the words of DU/2003/2255 art. 43 pkt 1 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 4 pkt 1: the words of DU/2003/2255 art. 43 pkt 2 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 4 pkt 2: the words of DU/2003/2255 art. 43 pkt 2 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 4 pkt 3: the words of DU/2003/2255 art. 43 pkt 2 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 299 § 4 pkt 4: the change by DU/2003/2255 before DU/2004/593 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 304 § 1: the change by DU/2001/459 before DU/2003/1302 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 306m § 2 pkt 1: the words of DU/2004/894 art. 6 pkt 4 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa art. 306n: the words of DU/2004/894 art. 6 pkt 4 differ from DU/2005/60; the unified text is used
- ordynacja-podatkowa DU/2005/60: 430 lines changed with no footnote
- ordynacja-podatkowa DU/1998/1014 (in force 1999-01-01): listed by the API, but no unit of DU/2005/60 is credited to it
- ordynacja-podatkowa DU/1999/1062 (in force 2001-05-08): listed by the API, but no unit of DU/2005/60 is credited to it
- ordynacja-podatkowa DU/1999/931 (in force 1999-10-17): listed by the API, but no unit of DU/2005/60 is credited to it
- ordynacja-podatkowa DU/2000/1037 (in force 2001-01-01): listed by the API, but no unit of DU/2005/60 is credited to it
- ordynacja-podatkowa DU/2000/1268 (in force 2001-03-30): listed by the API, but no unit of DU/2005/60 is credited to it
- ordynacja-podatkowa DU/2000/960 (in force 2001-01-01): listed by the API, but no unit of DU/2005/60 is credited to it
- ordynacja-podatkowa DU/2001/166 (in force 2001-03-24): listed by the API, but no unit of DU/2005/60 is credited to it
- ordynacja-podatkowa DU/2002/984 (in force 2002-10-27): listed by the API, but no unit of DU/2005/60 is credited to it
- ordynacja-podatkowa DU/2004/535 (in force 2004-05-01): listed by the API, but no unit of DU/2005/60 is credited to it
- ordynacja-podatkowa art. 3 pkt 10: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3 pkt 11: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3 pkt 12: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3 pkt 12: the words of DU/2006/1590 art. 1 pkt 1 lit. b differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 3a § 1: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3a § 2: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3a § 3: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3a § 3: the words of DU/2005/1199 art. 1 pkt 2 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 3b: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 1: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 1 pkt 1: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 1 pkt 2: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 1 pkt 2: the words of DU/2005/1199 art. 1 pkt 3 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 3b § 2: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 2 pkt 1: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 2 pkt 1: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 3b § 2 pkt 2: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 2 pkt 3: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 2 pkt 3: the words of DU/2005/1199 art. 1 pkt 3 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 3b § 3: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 3 pkt 1: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3b § 3 pkt 2: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3c: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3d: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 3d: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 13 § 2 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 13 § 2 pkt 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 13 § 2 pkt 4: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 13 § 2 pkt 4: the words of DU/2006/1590 art. 1 pkt 2 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 13 § 2 pkt 5: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 14 § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14 § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14 § 2: the change by DU/2006/1590 before DU/2010/1306 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 14 § 2: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 14 § 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14 § 3: the change by DU/2006/1590 before DU/2010/1306 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 14 § 3: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 14a § 3: the words of DU/2011/1378 art. 9 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 14b § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14b § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14b § 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14b § 4: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14b § 5: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14b § 6: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14b § 7: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14c § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14c § 1: the words of DU/2006/1590 art. 1 pkt 6 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 14c § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14c § 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14c § 3: the words of DU/2006/1590 art. 1 pkt 6 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 14d: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14d: the words of DU/2006/1590 art. 1 pkt 6 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 14e: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 14e: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14e § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 14e § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14e § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 14e § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14f: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14f § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14f § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14f § 2a: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14f § 2a: the change by DU/2006/1590 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 14f § 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14g: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14g § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14g § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14g § 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14h: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14h: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14i: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14i § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14i § 1: the words of DU/2006/1590 art. 1 pkt 7 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 14i § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14i § 2: the words of DU/2006/1590 art. 1 pkt 7 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 14i § 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14i § 3: the words of DU/2006/1590 art. 1 pkt 7 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 14j: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14j § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14j § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14j § 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14k: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14k § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14k § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14k § 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14l: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14l: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m § 1 pkt 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m § 1 pkt 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m § 2 pkt 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m § 2 pkt 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m § 2 pkt 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m § 3: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14m § 4: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14n: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14n § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14n § 1 pkt 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14n § 1 pkt 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14n § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14o: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14o § 1: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14o § 2: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14p: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 14p: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 21 § 3a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 21b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 21b pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 21b pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 21b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 21b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 22 § 1a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 24: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 24a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 24b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33b pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33c § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 1: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 2: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 2 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 2 pkt 1: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 2 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 2 pkt 2: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 2 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 2 pkt 3: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 2 pkt 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 2 pkt 4: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 2 pkt 5: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 2 pkt 5: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 2 pkt 6: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 2 pkt 6: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 2 pkt 7: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 2 pkt 7: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 3: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33d § 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33d § 4: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33e: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33e: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33e: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33f: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33f § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33f § 1: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33f § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33f § 2: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 33g: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 33g: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 34 § 3 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 45a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 48 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 48 § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 48 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 49 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 51 § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 53 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 53a § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 53a § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 53a § 2: the change by DU/2005/1199 before DU/2008/1320 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 53a § 2: DU/2008/1320 in force 2009-01-01 (footnote, used) but 2008-12-01 (API)
- ordynacja-podatkowa art. 54 § 1 pkt 5: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 54 § 1 pkt 5: the change by DU/2005/1199 before DU/2008/1109 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 54 § 1 pkt 5: DU/2008/1109 in force 2009-09-01 (footnote, used) but 2008-11-10 (API)
- ordynacja-podatkowa art. 54 § 1 pkt 7a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 54 § 5: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 56 § 1: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 57 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 59 § 1 pkt 10: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 59 § 2 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 59 § 2 pkt 6: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 63 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 63 § 1a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 63 § 1a: the change by DU/2005/1199 before DU/2011/1707 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 63 § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 65 § 1 pkt 2: the words of DU/2008/1318 art. 1 pkt 17 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 66 § 2 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 67: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 67b § 3: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 67b § 4: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 67b § 5: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 70 § 2 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 5: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 6: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 6: the words of DU/2005/1199 art. 1 pkt 34 lit. d differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 70 § 6 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 6 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 6 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 6 pkt 3: the words of DU/2005/1199 art. 1 pkt 34 lit. d differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 70 § 6 pkt 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 6 pkt 4: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 70 § 7: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 7: the words of DU/2005/1199 art. 1 pkt 34 lit. d differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 70 § 7 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 7 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 7 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 7 pkt 3: the words of DU/2005/1199 art. 1 pkt 34 lit. d differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 70 § 7 pkt 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 7 pkt 4: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 70 § 7 pkt 4: the words of DU/2008/1318 art. 1 pkt 18 lit. b differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 70 § 7 pkt 5: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 70 § 7 pkt 5: the change by DU/2005/1199 before DU/2008/1318 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 70b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 71: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 72 § 1 pkt 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 73 § 1 pkt 5: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 73 § 2 pkt 4: DU/2008/1320 in force 2009-01-01 (footnote, used) but 2008-12-01 (API)
- ordynacja-podatkowa art. 75 § 2 pkt 1 lit. b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 75 § 2 pkt 1a: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 75 § 3a: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 75 § 5a: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 76 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 76 § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 76 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 76 § 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 76 § 4: the change by DU/2005/1199 before DU/2010/1306 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 76 § 4: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 76a § 2 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 77 § 1 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 77 § 1 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 77 § 1 pkt 5: DU/2008/1320 in force 2009-01-01 (footnote, used) but 2008-12-01 (API)
- ordynacja-podatkowa art. 77 § 1 pkt 6: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 77 § 1 pkt 6 lit. a: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 77 § 1 pkt 6 lit. b: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 77 § 1 pkt 6 część wspólna: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 77 § 1 pkt 7: DU/2008/1320 in force 2009-01-01 (footnote, used) but 2008-12-01 (API)
- ordynacja-podatkowa art. 77 § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 77 § 2 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 77 § 2 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 77 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 77b § 5: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 78 § 3 pkt 4: DU/2008/1320 in force 2009-01-01 (footnote, used) but 2008-12-01 (API)
- ordynacja-podatkowa art. 78 § 3 pkt 5: DU/2008/1320 in force 2009-01-01 (footnote, used) but 2008-12-01 (API)
- ordynacja-podatkowa art. 81 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 81 § 1a: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 81a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 81b § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 81b § 1 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 81b § 1 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 81b § 1 pkt 2 lit. a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 81b § 1 pkt 2 lit. b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 81b § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 81c: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 82 § 2: DU/2010/1306 in force 2011-08-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 82 § 2b: DU/2005/1199 in force 2007-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 82 § 2c: the words of DU/2008/1318 art. 1 pkt 21 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 82 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 82 § 7: DU/2005/1199 in force 2007-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 82 § 7 pkt 1: DU/2005/1199 in force 2007-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 82 § 7 pkt 2: DU/2005/1199 in force 2007-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 82 § 8: DU/2005/1199 in force 2007-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 89: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 90: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 93 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 93c § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 93c § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 97a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 100 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 100 § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 100 § 2a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 103 § 1 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 109 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 117 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 117 § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 117 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 117a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 117a § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 117a § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 117a § 2: the change by DU/2005/1199 before DU/2008/1320 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 133 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 133 § 2b: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 133a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 133a § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 133a § 1 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 133a § 1 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 133a § 1 część wspólna: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 133a § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 133a § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 143 § 1a: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 143 § 1a: the words of DU/2010/1131 art. 84 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 144a: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 144a § 1: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 144a § 2: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 148 § 2 pkt 3: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 152 § 3: DU/2005/1199 in force 2006-08-16 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 152a § 2: the words of DU/2010/230 art. 6 pkt 11 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 153 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 154a: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 154a § 1: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 154a § 1a: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 154a § 1a: the change by DU/2005/1199 before DU/2010/1306 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 154a § 1a: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 154a § 2: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 154b: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 154b: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 154c: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 154c: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 165 § 5 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 165 § 5 pkt 2: the words of DU/2005/1199 art. 1 pkt 72 lit. b differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 165 § 5 pkt 3: the words of DU/2008/1318 art. 1 pkt 31 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 165 § 5 pkt 4: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 165 § 7: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 199a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 199a § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 199a § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 199a § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 201 § 1 pkt 6: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 208 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 212: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 223a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 224c: DU/2006/1590 in force 2007-07-01 (footnote, used) but 2007-01-01 (API)
- ordynacja-podatkowa art. 233 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 234a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 234a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 240 § 1 pkt 10: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 240 § 1 pkt 11: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 240 § 1 pkt 9: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 240 § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 240 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 241 § 2 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 243 § 1a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 272a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 272a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 274 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 274 § 1 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 274 § 1 pkt 1: the words of DU/2005/1199 art. 1 pkt 92 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 274 § 1 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 274 § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 274 § 2 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 274 § 2 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 274 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 274 § 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 274 § 5: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 281 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 281 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 282c § 1 pkt 1 lit. g: the words of DU/2008/1318 art. 1 pkt 42 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 282c § 1 pkt 1 lit. h: the change by DU/2008/1318 before DU/2012/362 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 283 § 1 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 284 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 284 § 1: the words of DU/2005/1199 art. 1 pkt 97 lit. a differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 284 § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 284 § 3: the words of DU/2005/1199 art. 1 pkt 97 lit. b differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 284a § 1: the words of DU/2009/97 art. 21 pkt 3 lit. a differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 284a § 5: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 284a § 5a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 284a § 5b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 284a § 6: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 285a § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 285a § 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 285a § 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 286a § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 288 § 4: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 290 § 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 290a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 291a: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 291a § 1: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 291a § 2: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 293 § 2 pkt 6: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 294 § 1 pkt 5: the words of DU/2006/1590 art. 1 pkt 35 lit. a differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 294 § 1 pkt 6: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 295a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 295a: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 295a: the words of DU/2005/1199 art. 1 pkt 108 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 296 § 1 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 296 § 1 pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 296 § 1 pkt 3: the words of DU/2005/1199 art. 1 pkt 109 lit. b differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 297 § 1 pkt 2a: the words of DU/2009/1317 art. 10 pkt 2 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 297b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 297b: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 297b: the words of DU/2005/1199 art. 1 pkt 110 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 298 pkt 5b: the words of DU/2006/708 art. 176 pkt 2 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 1: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 299 § 3 pkt 12: the words of DU/2006/1590 art. 1 pkt 36 lit. a differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 299 § 4: the words of DU/2007/1378 art. 37 pkt 2 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 305a: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 305b pkt 2: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 305c § 1: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 305c § 2: DU/2005/1199 in force 2005-08-02 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 305c § 2: the words of DU/2005/1199 art. 1 pkt 114 differ from DU/2012/749; the unified text is used
- ordynacja-podatkowa art. 305n § 4: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 305n § 5: DU/2010/1306 in force 2011-01-01 (footnote, used) but 2010-11-09 (API)
- ordynacja-podatkowa art. 306h § 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 306i § 2 pkt 2: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 306j pkt 3: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa art. 306j pkt 6: DU/2005/1199 in force 2006-01-01 (footnote, used) but 2005-09-01 (API)
- ordynacja-podatkowa DU/2012/749: 209 lines changed with no footnote
- ordynacja-podatkowa DU/2005/732 (in force 2005-06-01): listed by the API, but no unit of DU/2012/749 is credited to it
- ordynacja-podatkowa DU/2006/1031 (in force 2006-08-10): listed by the API, but no unit of DU/2012/749 is credited to it
- ordynacja-podatkowa DU/2007/1414 (in force 2007-10-23): listed by the API, but no unit of DU/2012/749 is credited to it
- ordynacja-podatkowa DU/2007/1671 (in force 2007-12-03): listed by the API, but no unit of DU/2012/749 is credited to it
- ordynacja-podatkowa DU/2007/721 (in force 2007-06-14): listed by the API, but no unit of DU/2012/749 is credited to it
- ordynacja-podatkowa DU/2009/362 (in force 2009-03-19): listed by the API, but no unit of DU/2012/749 is credited to it
- ordynacja-podatkowa DU/2010/961 (in force 2010-08-09): listed by the API, but no unit of DU/2012/749 is credited to it
- ordynacja-podatkowa DU/2011/173 (in force 2011-05-17): listed by the API, but no unit of DU/2012/749 is credited to it
- ordynacja-podatkowa art. 3a § 1: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 3a § 3: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 22 § 2a: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 22 § 2a: the words of DU/2014/1215 art. 21 pkt 3 differ from DU/2015/613; the unified text is used
- ordynacja-podatkowa art. 73 § 2 pkt 1a: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 76b § 2: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 76b § 3: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 76b § 4: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 76b § 4 pkt 1: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 76b § 4 pkt 2: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 87 § 1: DU/2013/35 in force 2014-01-01 (footnote, used) but 2013-04-01 (API)
- ordynacja-podatkowa art. 93a § 4: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 93b: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 144: the words of DU/2012/1529 art. 147 pkt 5 differ from DU/2015/613; the unified text is used
- ordynacja-podatkowa art. 230: the change by DU/2012/1342 before DU/2014/1215 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 230: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 306ha: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 306ha § 1: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 306ha § 2: DU/2014/1215 in force 2014-09-27 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa DU/2015/613: 49 lines changed with no footnote
- ordynacja-podatkowa DU/2015/251: in force 2016-01-01, after the unified text DU/2015/613 of 2015-05-06 that prints it
- ordynacja-podatkowa DU/2012/848 (in force 2012-07-24): listed by the API, but no unit of DU/2015/613 is credited to it
- ordynacja-podatkowa DU/2013/1313 (in force 2013-11-13): listed by the API, but no unit of DU/2015/613 is credited to it
- ordynacja-podatkowa DU/2013/985 (in force 2015-02-27): listed by the API, but no unit of DU/2015/613 is credited to it
- ordynacja-podatkowa art. 3 pkt 15: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 3 pkt 15: the words of DU/2016/1948 art. 38 pkt 1 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 13 § 2 pkt 4a: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 13 § 2 pkt 4a: the change by DU/2015/1269 before DU/2016/1948 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 13 § 2 pkt 4a: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 14a § 1: the words of DU/2016/1948 art. 38 pkt 5 lit. a differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 14b § 2a: the words of DU/2016/1948 art. 38 pkt 6 lit. b differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 14b § 5c: the words of DU/2016/1948 art. 38 pkt 6 lit. d differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 14i § 2: the words of DU/2016/1948 art. 38 pkt 9 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 14n § 4 część wspólna: the words of DU/2016/2255 art. 8 pkt 4 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 14n § 6: the words of DU/2016/2255 art. 8 pkt 4 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 15 § 2: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 15 § 2: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 20i § 2a: the words of DU/2016/1948 art. 38 pkt 17 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 54 § 3: the words of DU/2015/1649 art. 1 pkt 46 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 56b pkt 2 lit. b: the words of DU/2015/1649 art. 1 pkt 48 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 75 § 4b: the words of DU/2016/1948 art. 38 pkt 24 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 80a § 2c: the words of DU/2016/1948 art. 38 pkt 26 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 82 § 1a: DU/2015/1932 in force 2017-01-01 (footnote, used) but 2015-12-31 (API)
- ordynacja-podatkowa art. 82 § 1b: DU/2016/846 in force 2016-07-01 (footnote, used) but 2016-07-15 (API)
- ordynacja-podatkowa art. 82 § 1b: the words of DU/2016/1948 art. 38 pkt 27 lit. a differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 82 § 3: the words of DU/2016/1948 art. 38 pkt 27 lit. d differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 93a § 2 pkt 3: DU/2015/1923 in force 2017-01-01 (footnote, used) but 2016-05-20 (API)
- ordynacja-podatkowa art. 108 § 2 pkt 4: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 108 § 2 pkt 4: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 108 § 3a: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 108 § 3a: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 108 § 4: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 108 § 4: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 116a § 1: DU/2015/1923 in force 2017-01-01 (footnote, used) but 2016-05-20 (API)
- ordynacja-podatkowa art. 116a § 2: DU/2015/1923 in force 2017-01-01 (footnote, used) but 2016-05-20 (API)
- ordynacja-podatkowa art. 116a § 3: DU/2015/1923 in force 2017-01-01 (footnote, used) but 2016-05-20 (API)
- ordynacja-podatkowa art. 116a § 4: DU/2015/1923 in force 2017-01-01 (footnote, used) but 2016-05-20 (API)
- ordynacja-podatkowa art. 116a § 5: DU/2015/1923 in force 2017-01-01 (footnote, used) but 2016-05-20 (API)
- ordynacja-podatkowa art. 144b: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 144b: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 144b § 1: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 144b § 1: the words of DU/2016/1948 art. 38 pkt 49 lit. a differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 144b § 2: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 144b § 2 pkt 1: the words of DU/2016/1948 art. 38 pkt 49 lit. a differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 144b § 2 pkt 2: the words of DU/2016/1948 art. 38 pkt 49 lit. a differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 144b § 3: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 144b § 3: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 144b § 4: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 144b § 4: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 146a: DU/2015/1649 in force 2016-07-01 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 146a § 1: DU/2015/1649 in force 2016-07-01 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 146a § 2: DU/2015/1649 in force 2016-07-01 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 181a: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 181a: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 181a § 1: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 181a § 1: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 181a § 2: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 181a § 2: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 181a § 3: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 181a § 3: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 193a: DU/2015/1649 in force 2016-07-01 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 193a § 1: DU/2015/1649 in force 2016-07-01 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 193a § 2: DU/2015/1649 in force 2016-07-01 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 193a § 3: DU/2015/1649 in force 2016-07-01 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 200 § 3: the words of DU/2016/1948 art. 38 pkt 54 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 262 § 1a: the words of DU/2015/1649 art. 1 pkt 143 lit. b differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 266 § 1: the words of DU/2016/1948 art. 38 pkt 60 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 269 § 2: the words of DU/2016/1948 art. 38 pkt 61 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 274c § 1b: DU/2015/1649 in force 2016-07-01 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 283 § 1 pkt 1: DU/2016/1948 in force 2016-12-02 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 287 § 1 pkt 3: DU/2015/1649 in force 2016-07-01 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 294 § 1 pkt 1: DU/2016/1948 in force 2016-12-02 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 295 pkt 1: the words of DU/2016/1948 art. 38 pkt 69 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 295a: the words of DU/2016/1948 art. 38 pkt 70 differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 298 pkt 6d: the words of DU/2016/1948 art. 38 pkt 72 lit. d differ from DU/2017/201; the unified text is used
- ordynacja-podatkowa art. 299 § 3 pkt 8a: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 299 § 3 pkt 8a: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 299 § 3 pkt 8b: DU/2015/1269 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 299 § 3 pkt 8b: DU/2016/1948 in force 2016-01-01 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 305c § 3: DU/2016/1948 in force 2016-12-02 (footnote, used) but 2017-03-01 (API)
- ordynacja-podatkowa art. 305ja: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 1: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 1 pkt 1: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 1 pkt 2: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 1 pkt 3: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 1 pkt 4: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 1 pkt 5: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 1 pkt 6: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 1 pkt 7: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 1 część wspólna: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa art. 305ja § 2: DU/2015/1649 in force 2015-10-21 (footnote, used) but 2016-01-01 (API)
- ordynacja-podatkowa DU/2017/201: 153 lines changed with no footnote
- ordynacja-podatkowa DU/2016/1948: in force 2017-03-01, after the unified text DU/2017/201 of 2017-02-01 that prints it
- ordynacja-podatkowa DU/2015/2184 (in force 2015-12-25): listed by the API, but no unit of DU/2017/201 is credited to it
- ordynacja-podatkowa art. 293 § 2 pkt 7: DU/2017/648 in force 2017-05-01 (footnote, used) but 2017-04-04 (API)
- ordynacja-podatkowa art. 293 § 2 pkt 7: the words of DU/2017/648 art. 94 pkt 5 differ from DU/2018/800; the unified text is used
- ordynacja-podatkowa art. 295b: DU/2017/648 in force 2017-05-01 (footnote, used) but 2017-04-04 (API)
- ordynacja-podatkowa art. 295b: DU/2017/648 in force 2017-05-01 (footnote, used) but 2017-04-04 (API)
- ordynacja-podatkowa art. 295b: the words of DU/2017/648 art. 94 pkt 7 differ from DU/2018/800; the unified text is used
- ordynacja-podatkowa art. 297 § 1 pkt 8 część wspólna: the words of DU/2017/2491 art. 4 pkt 6 differ from DU/2018/800; the unified text is used
- ordynacja-podatkowa DU/2018/800: 258 lines changed with no footnote
- ordynacja-podatkowa DU/2015/1269 (in force 2017-03-01): listed by the API, but no unit of DU/2018/800 is credited to it
- ordynacja-podatkowa DU/2017/768 (in force 2017-04-27): listed by the API, but no unit of DU/2018/800 is credited to it
- ordynacja-podatkowa art. 3 pkt 17: the words of DU/2018/1629 art. 78 pkt 1 differ from DU/2019/900; the unified text is used
- ordynacja-podatkowa art. 14c § 4: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 119l: the change by DU/2018/2193 before DU/2018/2354 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 119zp § 3: DU/2018/1499 in force 2018-10-01 (footnote, used) but 2018-08-22 (API)
- ordynacja-podatkowa art. 119zr § 3 pkt 9: DU/2018/1499 in force 2018-08-08 (footnote, used) but 2018-08-22 (API)
- ordynacja-podatkowa art. 119zu § 1: DU/2018/1499 in force 2018-08-08 (footnote, used) but 2018-08-22 (API)
- ordynacja-podatkowa art. 119zu § 1 pkt 1: DU/2018/1499 in force 2018-08-08 (footnote, used) but 2018-08-22 (API)
- ordynacja-podatkowa art. 119zu § 1 pkt 2: DU/2018/1499 in force 2018-08-08 (footnote, used) but 2018-08-22 (API)
- ordynacja-podatkowa art. 119zu § 1 pkt 3: DU/2018/1499 in force 2018-08-08 (footnote, used) but 2018-08-22 (API)
- ordynacja-podatkowa art. 138a § 3: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 138a § 5: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 144b § 1: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 144b § 2 pkt 1: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 159 § 2: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 168 § 3a pkt 1: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 194a § 2a: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 210 § 1 pkt 8: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 217 § 1 pkt 7: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 282b § 4 pkt 6: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 306d § 3: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- ordynacja-podatkowa DU/2019/900: 381 lines changed with no footnote
- ordynacja-podatkowa DU/2018/1544 (in force 2018-09-11): listed by the API, but no unit of DU/2019/900 is credited to it
- ordynacja-podatkowa DU/2019/694 (in force 2019-04-30): listed by the API, but no unit of DU/2019/900 is credited to it
- ordynacja-podatkowa art. 3 pkt 16: DU/2019/1495 in force 2020-01-01 (footnote, used) but 2019-09-08 (API)
- ordynacja-podatkowa art. 3 pkt 17: DU/2019/1495 in force 2020-01-01 (footnote, used) but 2019-09-08 (API)
- ordynacja-podatkowa art. 7a § 2: DU/2019/1495 in force 2020-01-01 (footnote, used) but 2019-09-08 (API)
- ordynacja-podatkowa art. 13 § 2 pkt 10: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 14b § 5: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 14b § 5f: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 58a § 5: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 61b: DU/2019/1520 in force 2020-01-01 (footnote, used) but 2019-09-01 (API)
- ordynacja-podatkowa art. 61b § 1: DU/2019/1520 in force 2020-01-01 (footnote, used) but 2019-09-01 (API)
- ordynacja-podatkowa art. 61b § 2: DU/2019/1520 in force 2020-01-01 (footnote, used) but 2019-09-01 (API)
- ordynacja-podatkowa art. 61b § 2 pkt 1: DU/2019/1520 in force 2020-01-01 (footnote, used) but 2019-09-01 (API)
- ordynacja-podatkowa art. 61b § 2 pkt 2: DU/2019/1520 in force 2020-01-01 (footnote, used) but 2019-09-01 (API)
- ordynacja-podatkowa art. 61b § 2 pkt 3: DU/2019/1520 in force 2020-01-01 (footnote, used) but 2019-09-01 (API)
- ordynacja-podatkowa art. 61b § 3: DU/2019/1520 in force 2020-01-01 (footnote, used) but 2019-09-01 (API)
- ordynacja-podatkowa art. 61b § 4: DU/2019/1520 in force 2020-01-01 (footnote, used) but 2019-09-01 (API)
- ordynacja-podatkowa art. 61b § 4: the change by DU/2019/1520 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 86a § 5: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 86a § 5 pkt 1: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 86a § 5 pkt 2: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 117ba § 3 pkt 1: the change by DU/2019/1018 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 117ba § 3 pkt 2: the change by DU/2019/1018 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 117ba § 3 pkt 3: the change by DU/2019/1018 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 117ba § 3 pkt 3 lit. a: the change by DU/2019/1018 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 117ba § 3 pkt 3 lit. b: the change by DU/2019/1018 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 117ba § 3 pkt 3 lit. c: the change by DU/2019/1018 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 117ba § 3 pkt 3 część wspólna: the change by DU/2019/1018 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 117ba § 3 pkt 4: the change by DU/2019/1018 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 117ba § 3 pkt 5: the change by DU/2019/1018 before DU/2020/1065 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 119b § 1 pkt 6: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 293 § 2 pkt 12: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 295d: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 295d § 1: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 295d § 2: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 296 § 1 pkt 4: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 297 § 1 pkt 10: DU/2019/1495 in force 2019-08-09 (footnote, used) but 2019-09-08 (API)
- ordynacja-podatkowa art. 297 § 1 pkt 10: the words of DU/2019/1495 art. 19 pkt 2 differ from DU/2020/1325; the unified text is used
- ordynacja-podatkowa art. 297f: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 297f: DU/2019/2200 in force 2020-07-01 (footnote, used) but 2019-11-29 (API)
- ordynacja-podatkowa art. 298 pkt 6f: the words of DU/2019/1667 art. 2 differ from DU/2020/1325; the unified text is used
- ordynacja-podatkowa art. 299e § 2: DU/2019/1495 in force 2019-08-09 (footnote, used) but 2019-09-08 (API)
- ordynacja-podatkowa art. 299f § 1: the words of DU/2019/1649 art. 5 pkt 3 differ from DU/2020/1325; the unified text is used
- ordynacja-podatkowa art. 299f § 4: the change by DU/2019/1649 before DU/2020/1086 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 299f § 5: the change by DU/2019/1649 before DU/2020/1086 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 299f § 9: the change by DU/2019/1649 before DU/2020/1086 is not reconstructed (no quoted wording)
- ordynacja-podatkowa DU/2020/1325: 221 lines changed with no footnote
- ordynacja-podatkowa art. 272 pkt 6: the words of DU/2021/72 art. 2 differ from DU/2021/1540; the unified text is used
- ordynacja-podatkowa DU/2021/1540: 19 lines changed with no footnote
- ordynacja-podatkowa DU/2020/2320: in force 2021-10-05, after the unified text DU/2021/1540 of 2021-08-23 that prints it
- ordynacja-podatkowa DU/2019/2020 (in force 2021-01-02): listed by the API, but no unit of DU/2021/1540 is credited to it
- ordynacja-podatkowa art. 28 § 3 pkt 1: the words of DU/2022/1265 art. 3 pkt 1 differ from DU/2022/2651; the unified text is used
- ordynacja-podatkowa art. 77b § 1 pkt 2: DU/2022/1301 in force 2022-07-23 (footnote, used) but 2022-07-07 (API)
- ordynacja-podatkowa art. 77b § 1 pkt 3: DU/2022/1301 in force 2022-07-23 (footnote, used) but 2022-07-07 (API)
- ordynacja-podatkowa art. 82 § 1c: the words of DU/2022/2180 art. 6 pkt 1 differ from DU/2022/2651; the unified text is used
- ordynacja-podatkowa art. 133 § 2c: DU/2021/2105 in force 2022-07-01 (footnote, used) but 2022-01-01 (API)
- ordynacja-podatkowa art. 133 § 2c pkt 1: DU/2021/2105 in force 2022-07-01 (footnote, used) but 2022-01-01 (API)
- ordynacja-podatkowa art. 133 § 2c pkt 2: DU/2021/2105 in force 2022-07-01 (footnote, used) but 2022-01-01 (API)
- ordynacja-podatkowa art. 297e § 1 pkt 6: the words of DU/2022/835 art. 17 pkt 2 differ from DU/2022/2651; the unified text is used
- ordynacja-podatkowa art. 297e § 1 pkt 7: the change by DU/2022/835 before DU/2022/1301 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 297e § 1 pkt 8: the change by DU/2022/835 before DU/2022/1301 is not reconstructed (no quoted wording)
- ordynacja-podatkowa art. 299 § 5a: DU/2022/1301 in force 2022-09-01 (footnote, used) but 2022-07-07 (API)
- ordynacja-podatkowa art. 299 § 5b: DU/2022/1301 in force 2022-09-01 (footnote, used) but 2022-07-07 (API)
- ordynacja-podatkowa art. 299 § 6a: DU/2022/1301 in force 2022-09-01 (footnote, used) but 2022-07-07 (API)
- ordynacja-podatkowa art. 299 § 7 pkt 1: DU/2022/1301 in force 2022-09-01 (footnote, used) but 2022-07-07 (API)
- ordynacja-podatkowa art. 299 § 7 pkt 2: DU/2022/1301 in force 2022-09-01 (footnote, used) but 2022-07-07 (API)
- ordynacja-podatkowa art. 299 § 7 pkt 3: DU/2022/1301 in force 2022-09-01 (footnote, used) but 2022-07-07 (API)
- ordynacja-podatkowa DU/2022/2651: 137 lines changed with no footnote
- ordynacja-podatkowa DU/2022/2180: in force 2023-01-01, after the unified text DU/2022/2651 of 2022-12-16 that prints it
- ordynacja-podatkowa DU/2022/2180 (in force 2023-01-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2022/2707 (in force 2022-12-31): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/1059 (in force 2023-07-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/1193 (in force 2023-07-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/1234 (in force 2023-07-14): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/1450 (in force 2024-01-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/1598 (in force 2026-02-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/1705 (in force 2023-09-15): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/1723 (in force 2024-01-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/1785 (in force 2023-09-19): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/180 (in force 2023-02-10): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/2760 (in force 2023-12-31): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/326 (in force 2023-05-22): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/511 (in force 2023-04-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/556 (in force 2024-03-25): after the last unified text; not in the record
- ordynacja-podatkowa DU/2023/614 (in force 2023-07-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2024/1685 (in force 2025-01-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2024/1831 (in force 2024-12-12): after the last unified text; not in the record
- ordynacja-podatkowa DU/2024/879 (in force 2024-07-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/1203 (in force 2025-09-02): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/1235 (in force 2026-07-12): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/1414 (in force 2025-11-04): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/1417 (in force 2025-11-04): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/1669 (in force 2027-04-02): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/1804 (in force 2026-01-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/1863 (in force 2026-01-13): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/497 (in force 2025-05-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/621 (in force 2025-06-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/622 (in force 2025-06-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/769 (in force 2025-07-13): after the last unified text; not in the record
- ordynacja-podatkowa DU/2025/820 (in force 2025-07-25): after the last unified text; not in the record
- ordynacja-podatkowa DU/2026/1098 (in force 2027-01-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2026/1154 (in force 2026-09-16): after the last unified text; not in the record
- ordynacja-podatkowa DU/2026/1206 (in force 2027-01-11): after the last unified text; not in the record
- ordynacja-podatkowa DU/2026/252 (in force 2026-04-03): after the last unified text; not in the record
- ordynacja-podatkowa DU/2026/347 (in force 2026-03-18): after the last unified text; not in the record
- ordynacja-podatkowa DU/2026/473 (in force 2026-07-08): after the last unified text; not in the record
- ordynacja-podatkowa DU/2026/825 (in force 2026-09-24): after the last unified text; not in the record
- ordynacja-podatkowa DU/2026/846 (in force 2026-10-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2026/875 (in force 2027-01-01): after the last unified text; not in the record
- ordynacja-podatkowa DU/2005/60: 1 lines differ from the unified text for no reason found: art. 64 § 1 pkt 4
- ordynacja-podatkowa DU/2015/613: 2 lines differ from the unified text for no reason found: art. 68 § 4a, art. 272 pkt 4
- ordynacja-podatkowa DU/2017/201: 4 lines differ from the unified text for no reason found: art. 14b § 6a, art. 14b § 6a pkt 4, art. 14b § 6a część wspólna, art. 298 pkt 6d
- ordynacja-podatkowa DU/2021/1540: 1 lines differ from the unified text for no reason found: art. 119zt pkt 3

## What the AI did

The builder, parsers, checks and documentation were written by Claude Code with Claude Opus 5.5
(`claude-opus-5-5`), at the request of Lexifina. No AI wrote or changed any legal text, and no model runs when the
repository is built: every word of law comes from the Sejm's API.
