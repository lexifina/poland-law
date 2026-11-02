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
was typed in, summarised or rewritten. The build read 291 metadata records, 262 HTML texts and 3 PDFs,
retrieved on 2026-10-28, 2026-11-02, 2026-11-03.

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
| Kodeks karny | Dz.U. 1997 nr 88 poz. 553 | 1998-09-01 | html | tekst ogłoszony (the act as published) |
| Kodeks karny | Dz.U. 2016 poz. 1137 | 2016-07-29 | html | tekst jednolity |
| Kodeks karny | Dz.U. 2017 poz. 2204 | 2017-11-29 | html | tekst jednolity |
| Kodeks karny | Dz.U. 2018 poz. 1600 | 2018-08-21 | html | tekst jednolity |
| Kodeks karny | Dz.U. 2019 poz. 1950 | 2019-10-14 | html | tekst jednolity |
| Kodeks karny | Dz.U. 2020 poz. 1444 | 2020-08-25 | html | tekst jednolity |
| Kodeks karny | Dz.U. 2021 poz. 2345 | 2021-12-17 | html | tekst jednolity |
| Kodeks karny | Dz.U. 2022 poz. 1138 | 2022-05-30 | html | tekst jednolity |
| Kodeks karny | Dz.U. 2024 poz. 17 | 2024-01-04 | html | tekst jednolity |
| Kodeks postępowania karnego | Dz.U. 1997 nr 89 poz. 555 | 1998-09-01 | html | tekst ogłoszony (the act as published) |
| Kodeks postępowania karnego | Dz.U. 2016 poz. 1749 | 2016-10-24 | html | tekst jednolity |
| Kodeks postępowania karnego | Dz.U. 2017 poz. 1904 | 2017-10-12 | html | tekst jednolity |
| Kodeks postępowania karnego | Dz.U. 2018 poz. 1987 | 2018-10-17 | html | tekst jednolity |
| Kodeks postępowania karnego | Dz.U. 2020 poz. 30 | 2020-01-09 | html | tekst jednolity |
| Kodeks postępowania karnego | Dz.U. 2021 poz. 534 | 2021-03-24 | html | tekst jednolity |
| Kodeks postępowania karnego | Dz.U. 2022 poz. 1375 | 2022-06-30 | html | tekst jednolity |
| Kodeks postępowania karnego | Dz.U. 2024 poz. 37 | 2024-01-11 | html | tekst jednolity |

## The build, step by step

1. `python -X utf8 scripts/poland-law/build.py --today 2026-11-02` in Lexifina's own repository fetched the data into its
   cache and wrote this repository. The files in `tools/` are the same files as in `scripts/poland-law/` there
   (git blobs: `build.py` 785d3646a1da, `parse.py` 315ab387f541, `pdfparse.py` 3056ad6a05e5, `gloss.py` 404e4b159519, `reproduce.py` 035c8d9409f3).
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

- **The codes** (`kodeks-cywilny/`, `kodeks-karny/`, `kodeks-pracy/`, `kodeks-postepowania-cywilnego/`,
  `kodeks-postepowania-karnego/`, `kodeks-spolek-handlowych/`, `ordynacja-podatkowa/`) are read the same way as the
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
  replayed on its day and checked against the next unified text (Konstytucja: 9 of 9 quoted lines; Obywatelstwo: 21 of 22 quoted lines; Kodeks karny: 825 of 948 quoted lines; Kodeks postępowania karnego: 1228 of 1599 quoted lines).
- **Editorial changes of the unified texts** (updated Journal references of the other acts cited, provisions left out
  as "(pominięty)") are separate commits, authored by the Marshal of the Sejm's unified text, on the day it was
  published. A line changed by an act keeps the Journal references it had until then.
- **The Constitution** (`konstytucja/`) has no unified text. The current text is the Sejm's consolidated text (PDF,
  type U). The 2006 and 2009 amending acts are replayed from their own words (HTML) and must equal it; the
  correction notice of 2001 (Dz.U. 2001 nr 28 poz. 319) is applied word by word and its commit is authored by the
  notice, not by a law. The text as enacted is the consolidated text with those three steps undone; art. 55 as enacted
  is read from the text layer of the 1997 Journal's scan (O), between "Art. 55." and "Art. 56.".
- Commits are dated noon in Warsaw on the in-force day (CET, CEST from the last Sunday in March to the last Sunday in
  October). Counts: editorial 15, law 287, start 2, unexplained 14; 582 tags.

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

- kodeks-karny art. 7 § 3: the words of DU/2015/396 art. 1 pkt 2 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 34 § 1a pkt 1: the words of DU/2015/396 art. 1 pkt 5 lit. b differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 34 § 2 pkt 1: the words of DU/2009/1589 art. 1 pkt 4 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 39 pkt 2a: the words of DU/2005/1363 art. 1 pkt 1 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 39 pkt 2b: the words of DU/2015/396 art. 1 pkt 10 lit. a differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 39 pkt 2c: the words of DU/2009/504 art. 72 pkt 1 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 39 pkt 2d: the words of DU/2009/1540 art. 99 pkt 1 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 39 pkt 2e: the words of DU/2015/396 art. 1 pkt 10 lit. b differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 41 § 1a: the words of DU/2016/862 art. 26 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 41a § 3a: the change by DU/2005/1363 before DU/2015/396 is not reconstructed (no quoted wording)
- kodeks-karny art. 41a § 5: the change by DU/2005/1363 before DU/2015/396 is not reconstructed (no quoted wording)
- kodeks-karny art. 41b: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 41b § 1: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 41b § 2: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 41b § 3: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 41b § 4: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 41b § 5: the change by DU/2009/504 before DU/2011/1280 is not reconstructed (no quoted wording)
- kodeks-karny art. 41b § 5: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 41b § 6: the change by DU/2009/504 before DU/2011/1280 is not reconstructed (no quoted wording)
- kodeks-karny art. 41b § 6: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 41b § 7: the change by DU/2009/504 before DU/2011/1280 is not reconstructed (no quoted wording)
- kodeks-karny art. 41b § 7: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 41b § 8: the change by DU/2009/504 before DU/2011/1280 is not reconstructed (no quoted wording)
- kodeks-karny art. 41b § 8: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 41b § 9: the change by DU/2009/504 before DU/2011/1280 is not reconstructed (no quoted wording)
- kodeks-karny art. 41b § 9: DU/2011/1280 in force 2012-01-01 (footnote, used) but 2011-11-12 (API)
- kodeks-karny art. 43a § 2: the words of DU/2015/396 art. 1 pkt 15 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 45 § 1: the words of DU/2003/1061 art. 1 pkt 2 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 47 § 3: the change by DU/2010/227 before DU/2015/541 is not reconstructed (no quoted wording)
- kodeks-karny art. 47 § 4: the change by DU/2010/227 before DU/2015/541 is not reconstructed (no quoted wording)
- kodeks-karny art. 47 § 5: the change by DU/2010/227 before DU/2015/541 is not reconstructed (no quoted wording)
- kodeks-karny art. 59a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-karny art. 72 § 1 pkt 7a: the words of DU/2005/1363 art. 1 pkt 7 lit. b differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 75 § 1: DU/2015/396 in force 2015-04-04 (footnote, used) but 2015-07-01 (API)
- kodeks-karny art. 84a: the change by DU/2005/1363 before DU/2015/396 is not reconstructed (no quoted wording)
- kodeks-karny art. 85 § 3a: the change by DU/2015/396 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-karny art. 86 § 2b: the words of DU/2015/396 art. 1 pkt 48 lit. b differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 93a § 1 pkt 1: the words of DU/2015/396 art. 1 pkt 55 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 93a § 1 pkt 2: the words of DU/2015/396 art. 1 pkt 55 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 93a § 1 pkt 3: the words of DU/2015/396 art. 1 pkt 55 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 93c pkt 1: the words of DU/2015/396 art. 1 pkt 55 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 93c pkt 2: the words of DU/2015/396 art. 1 pkt 55 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 93c pkt 3: the words of DU/2015/396 art. 1 pkt 55 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 93c pkt 4: the words of DU/2015/396 art. 1 pkt 55 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 95a: the change by DU/2005/1363 before DU/2015/396 is not reconstructed (no quoted wording)
- kodeks-karny art. 101 § 1 pkt 2a: the words of DU/2005/1109 art. 1 pkt 1 lit. a differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 101 § 4 pkt 1: the change by DU/2008/1344 before DU/2015/396 is not reconstructed (no quoted wording)
- kodeks-karny art. 101 § 4 pkt 2: the change by DU/2008/1344 before DU/2015/396 is not reconstructed (no quoted wording)
- kodeks-karny art. 101 § 4 część wspólna: the change by DU/2008/1344 before DU/2015/396 is not reconstructed (no quoted wording)
- kodeks-karny art. 107 § 4: DU/2015/396 in force 2015-03-21 (footnote, used) but 2015-07-01 (API)
- kodeks-karny art. 107 § 4a: DU/2015/396 in force 2015-03-21 (footnote, used) but 2015-07-01 (API)
- kodeks-karny art. 107 § 6: DU/2015/396 in force 2015-03-21 (footnote, used) but 2015-07-01 (API)
- kodeks-karny art. 112 pkt 1: the words of DU/2004/626 art. 1 pkt 1 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 112 pkt 1a: the change by DU/2004/626 before DU/2008/1080 is not reconstructed (no quoted wording)
- kodeks-karny art. 112 pkt 1a: DU/2006/1592 in force 2007-03-15 (footnote, used) but 2007-03-01 (API)
- kodeks-karny art. 112 pkt 3: the words of DU/2004/626 art. 1 pkt 1 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 114 § 3 pkt 1: the words of DU/2004/626 art. 1 pkt 2 lit. b differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 114 § 3 pkt 2: the words of DU/2004/626 art. 1 pkt 2 lit. b differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 114 § 3 pkt 3: the words of DU/2004/626 art. 1 pkt 2 lit. b differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 114a § 2 pkt 2: the words of DU/2015/396 art. 1 pkt 65 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 115 § 13 pkt 2a: the words of DU/2004/219 art. 179 pkt 1 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 115 § 13 pkt 3: the words of DU/2007/850 art. 22 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 115 § 20 pkt 3: the words of DU/2004/889 art. 1 pkt 3 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 115 § 22 część wspólna: the words of DU/2010/626 art. 1 pkt 2 lit. b differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 118a § 1 pkt 3: the words of DU/2010/626 art. 1 pkt 4 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 118a § 2 pkt 6: the words of DU/2010/626 art. 1 pkt 4 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 118a § 3 pkt 2: the words of DU/2010/626 art. 1 pkt 4 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 126a: the words of DU/2010/626 art. 1 pkt 8 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 132a: DU/2006/1592 in force 2007-03-15 (footnote, used) but 2007-03-01 (API)
- kodeks-karny art. 165a: the change by DU/2009/1317 before DU/2015/1855 is not reconstructed (no quoted wording)
- kodeks-karny art. 178a § 2: DU/2013/1247 in force 2013-11-09 (footnote, used) but 2015-07-01 (API)
- kodeks-karny art. 178a § 2: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-karny art. 178a § 2: DU/2016/437 in force 2013-11-09 (footnote, used) but 2016-04-15 (API)
- kodeks-karny art. 178a § 4: DU/2010/227 in force 2010-07-01 (footnote, used) but 2012-01-01 (API)
- kodeks-karny art. 179: the words of DU/2010/1018 art. 6 pkt 2 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 189 § 2: footnote names DU/2009/46, not among the API's amending acts
- kodeks-karny art. 189 § 3: footnote names DU/2009/46, not among the API's amending acts
- kodeks-karny art. 189a § 2: the words of DU/2010/626 art. 1 pkt 9 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 200 § 2: the words of DU/2005/1363 art. 1 pkt 20 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 202 § 1: the words of DU/2004/626 art. 1 pkt 7 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 202 § 2: the words of DU/2004/626 art. 1 pkt 7 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 202 § 3: the words of DU/2004/626 art. 1 pkt 7 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 202 § 4: the words of DU/2004/626 art. 1 pkt 7 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 202 § 4a: the change by DU/2004/626 before DU/2005/1363 is not reconstructed (no quoted wording)
- kodeks-karny art. 202 § 4a: the words of DU/2005/1363 art. 1 pkt 21 lit. b differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 202 § 5: the words of DU/2004/626 art. 1 pkt 7 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 211a: the words of DU/2010/626 art. 1 pkt 11 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 217a: the words of DU/2010/1602 art. 1 pkt 4 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 231b § 1: the words of DU/2015/396 art. 1 pkt 68 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 234: the words of DU/1999/931 art. 4 § 6 pkt 1 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 244a: DU/2010/1021 in force 2012-01-01 (footnote, used) but 2010-09-04 (API)
- kodeks-karny art. 244a § 1: DU/2010/1021 in force 2012-01-01 (footnote, used) but 2010-09-04 (API)
- kodeks-karny art. 244a § 2: DU/2010/1021 in force 2012-01-01 (footnote, used) but 2010-09-04 (API)
- kodeks-karny art. 244a § 2: the change by DU/2010/1021 before DU/2015/396 is not reconstructed (no quoted wording)
- kodeks-karny art. 244b § 1: the words of DU/2015/396 art. 1 pkt 72 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 248 pkt 6: the words of DU/2004/219 art. 179 pkt 2 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 252 § 1: footnote names DU/2009/46, not among the API's amending acts
- kodeks-karny art. 252 § 2: footnote names DU/2009/46, not among the API's amending acts
- kodeks-karny art. 252 § 5: footnote names DU/2009/46, not among the API's amending acts
- kodeks-karny art. 255a § 2: the change by DU/2011/1135 before DU/2016/904 is not reconstructed (no quoted wording)
- kodeks-karny art. 269a: the words of DU/2004/626 art. 1 pkt 10 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 269b § 1: the words of DU/2004/626 art. 1 pkt 10 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 296a § 1: the words of DU/2003/1061 art. 1 pkt 7 differ from DU/2016/1137; the unified text is used
- kodeks-karny art. 296b: the change by DU/2003/1061 before DU/2010/857 is not reconstructed (no quoted wording)
- kodeks-karny art. 309: the words of DU/2009/1589 art. 1 pkt 30 differ from DU/2016/1137; the unified text is used
- kodeks-karny DU/2016/1137: 81 lines changed with no footnote
- kodeks-karny DU/2016/862: in force 2017-01-01, after the unified text DU/2016/1137 of 2016-07-29 that prints it
- kodeks-karny DU/2000/1027 (in force 2001-02-04): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2001/1071 (in force 2002-01-01): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2003/1142 (in force 2003-07-11): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2003/2255 (in force 2004-05-01): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2005/1479 (in force 2005-12-17): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2005/732 (in force 2005-06-01): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2006/1409 (in force 2006-10-19): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2008/560 (in force 2008-05-26): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2009/533 (in force 2009-04-23): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2010/1474 (in force 2012-05-31): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2010/46 (in force 2010-04-19): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2011/202 (in force 2011-03-08): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2011/678 (in force 2012-01-02): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2011/78 (in force 2011-02-25): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2013/905 (in force 2015-02-09): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny DU/2015/1528 (in force 2015-10-02): listed by the API, but no unit of DU/2016/1137 is credited to it
- kodeks-karny art. 47 § 2a: the words of DU/2017/768 art. 1 pkt 4 differ from DU/2017/2204; the unified text is used
- kodeks-karny art. 277b: the words of DU/2017/244 art. 1 pkt 4 differ from DU/2017/2204; the unified text is used
- kodeks-karny DU/2017/2204: 11 lines changed with no footnote
- kodeks-karny DU/2017/1214 (in force 2017-06-24): listed by the API, but no unit of DU/2017/2204 is credited to it
- kodeks-karny DU/2018/1600: 7 lines changed with no footnote
- kodeks-karny DU/2019/1950: 7 lines changed with no footnote
- kodeks-karny DU/2019/1135 (in force 2019-06-18): listed by the API, but no unit of DU/2019/1950 is credited to it
- kodeks-karny DU/2019/858 (in force 2019-05-09): listed by the API, but no unit of DU/2019/1950 is credited to it
- kodeks-karny art. 304 § 2: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-karny art. 304 § 3: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-karny DU/2020/1444: 10 lines changed with no footnote
- kodeks-karny DU/2022/1138: 3 lines changed with no footnote
- kodeks-karny art. 40 § 3: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 78 § 2: the words of DU/2022/2600 art. 1 pkt 26 differ from DU/2024/17; the unified text is used
- kodeks-karny art. 79 § 1: the words of DU/2022/2600 art. 1 pkt 27 differ from DU/2024/17; the unified text is used
- kodeks-karny art. 101 § 4 pkt 2: the words of DU/2022/2600 art. 1 pkt 36 lit. d differ from DU/2024/17; the unified text is used
- kodeks-karny art. 112a: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 112a: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 130 § 1: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 130 § 2: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 130 § 3: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 130 § 4: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 130 § 5: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 130 § 6: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 130 § 7: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 130 § 8: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 130 § 9: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 131 § 1: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 131 § 2: DU/2023/1834 in force 2023-10-01 (footnote, used) but 2023-09-23 (API)
- kodeks-karny art. 178 § 1a: the words of DU/2022/2600 art. 1 pkt 67 lit. b differ from DU/2024/17; the unified text is used
- kodeks-karny art. 178 § 1a pkt 1: the words of DU/2022/2600 art. 1 pkt 67 lit. b differ from DU/2024/17; the unified text is used
- kodeks-karny art. 178 § 1a pkt 2: the words of DU/2022/2600 art. 1 pkt 67 lit. b differ from DU/2024/17; the unified text is used
- kodeks-karny DU/2024/17: 29 lines changed with no footnote
- kodeks-karny DU/2023/1860 (in force 2023-09-28): listed by the API, but no unit of DU/2024/17 is credited to it
- kodeks-karny DU/2023/852 (in force 2023-05-20): listed by the API, but no unit of DU/2024/17 is credited to it
- kodeks-karny DU/2023/1963 (in force 2024-07-01): after the last unified text; not in the record
- kodeks-karny DU/2024/1228 (in force 2025-02-13): after the last unified text; not in the record
- kodeks-karny DU/2024/1907 (in force 2025-01-01): after the last unified text; not in the record
- kodeks-karny DU/2024/1965 (in force 2025-02-01): after the last unified text; not in the record
- kodeks-karny DU/2025/1818 (in force 2026-01-02): after the last unified text; not in the record
- kodeks-karny DU/2025/1872 (in force 2026-01-29): after the last unified text; not in the record
- kodeks-karny DU/2026/902 (in force 2026-07-21): after the last unified text; not in the record
- kodeks-karny DU/2026/988 (in force 2026-08-23): after the last unified text; not in the record
- kodeks-postepowania-karnego art. 2 § 1 pkt 1: the words of DU/2016/437 art. 1 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 2 § 1 pkt 3: the words of DU/2015/21 art. 20 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 20 § 2a: the words of DU/2007/664 art. 1 pkt 3 lit. d differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 23a § 6: the change by DU/2003/155 before DU/2013/1247 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 23a § 7: the change by DU/2003/155 before DU/2013/1247 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 23a § 8: the change by DU/2003/155 before DU/2013/1247 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 23b: the change by DU/2015/396 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 25 § 1 pkt 1: the words of DU/2003/155 art. 1 pkt 7 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 25 § 1 pkt 2: the words of DU/2010/626 art. 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 49 § 2 pkt 1: the words of DU/2013/1247 art. 1 pkt 9 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 49a: the words of DU/2013/1247 art. 1 pkt 10 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 61 § 1: the words of DU/2013/1247 art. 1 pkt 16 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 72 § 2: DU/2016/437 in force 2013-11-09 (footnote, used) but 2016-04-15 (API)
- kodeks-postepowania-karnego art. 74 § 2 pkt 1: the words of DU/2005/70 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 74 § 2 pkt 2: the words of DU/2005/70 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 74 § 3a: DU/2013/1247 in force 2013-11-09 (footnote, used) but 2015-07-01 (API)
- kodeks-postepowania-karnego art. 79 § 1 pkt 1: the words of DU/2013/1247 art. 1 pkt 22 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 79 § 1 pkt 2: the words of DU/2013/1247 art. 1 pkt 22 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 79 § 1 pkt 3: the words of DU/2013/1247 art. 1 pkt 22 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 80a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 81 § 1: the words of DU/2016/437 art. 1 pkt 16 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 81 § 1a: the change by DU/2013/1247 before DU/2015/1186 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 81 § 1b: the change by DU/2013/1247 before DU/2015/1186 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 81a § 2: the words of DU/2013/1247 art. 1 pkt 25 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 87a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 95a § 1: the words of DU/2013/1247 art. 1 pkt 32 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 95a § 2: the words of DU/2013/1247 art. 1 pkt 32 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 100 § 1: the words of DU/2013/1247 art. 1 pkt 34 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 100 § 9: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 124: DU/2013/1247 in force 2013-11-09 (footnote, used) but 2015-07-01 (API)
- kodeks-postepowania-karnego art. 143 § 1 pkt 1: the words of DU/2004/626 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 143 § 1 pkt 10: the words of DU/2004/626 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 143 § 1 pkt 2: the words of DU/2004/626 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 143 § 1 pkt 3: the words of DU/2004/626 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 143 § 1 pkt 4: the words of DU/2004/626 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 143 § 1 pkt 5: the words of DU/2004/626 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 143 § 1 pkt 6: the words of DU/2004/626 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 143 § 1 pkt 7: the words of DU/2004/626 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 143 § 1 pkt 8: the words of DU/2016/437 art. 1 pkt 26 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 143 § 1 pkt 9: the words of DU/2004/626 art. 2 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 147 § 2 pkt 1: the words of DU/2013/849 art. 2 pkt 2 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 148a § 4 pkt 1: the words of DU/2016/437 art. 1 pkt 29 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 156 § 1a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 171 § 5 pkt 1: the words of DU/2003/155 art. 1 pkt 53 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 178 pkt 1: the words of DU/2013/1247 art. 1 pkt 54 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 181 § 1a: the words of DU/2016/1070 art. 1 pkt 3 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 184 § 3: the words of DU/2003/155 art. 1 pkt 61 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 184 § 5: the words of DU/2010/1228 art. 108 pkt 5 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 185a § 4: the change by DU/2003/155 before DU/2013/849 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 185b § 2: the words of DU/2013/849 art. 2 pkt 3 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 185b § 3: the change by DU/2005/1181 before DU/2013/849 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 185c § 3: the words of DU/2013/849 art. 2 pkt 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 192a § 3: the change by DU/2003/155 before DU/2005/70 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 202 § 5: the words of DU/2013/1247 art. 1 pkt 57 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 214 § 2 pkt 1: the words of DU/2003/155 art. 1 pkt 70 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 214 § 4 pkt 1: the words of DU/2003/155 art. 1 pkt 70 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 214 § 4 pkt 2: the words of DU/2003/155 art. 1 pkt 70 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 214 § 4 pkt 3: the words of DU/2003/155 art. 1 pkt 70 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 214 § 4 pkt 4: the words of DU/2003/155 art. 1 pkt 70 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 217 § 1: the words of DU/2003/155 art. 1 pkt 71 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 218 § 2: the words of DU/2004/626 art. 2 pkt 2 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 218b: the words of DU/2015/2281 art. 11 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 220 § 3: the words of DU/2003/155 art. 1 pkt 73 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 232a § 1: DU/2013/1247 in force 2013-11-09 (footnote, used) but 2015-07-01 (API)
- kodeks-postepowania-karnego art. 232a § 5: the change by DU/2003/155 before DU/2011/678 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 237a: the words of DU/2011/273 art. 1 pkt 2 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 244 § 1b: the words of DU/2010/842 art. 6 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 244 § 2: the words of DU/2013/1247 art. 1 pkt 65 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 244 § 5: the words of DU/2013/1247 art. 1 pkt 65 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 245 § 2: the words of DU/2013/1247 art. 1 pkt 66 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 247 § 1 pkt 1: the words of DU/2013/1247 art. 1 pkt 67 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 249a § 1: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 249a § 1 pkt 1: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 249a § 1 pkt 1: the words of DU/2016/437 art. 1 pkt 45 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 249a § 1 pkt 2: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 249a § 2: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 250 § 2a: the words of DU/2013/1247 art. 1 pkt 70 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 251 § 3: the words of DU/2013/1247 art. 1 pkt 71 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 254 § 1: the words of DU/2000/717 art. 1 pkt 7 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 254 § 3: the change by DU/2000/717 before DU/2003/155 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 258 § 1 pkt 1: the words of DU/2013/1247 art. 1 pkt 75 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 258 § 1 pkt 2: the words of DU/2013/1247 art. 1 pkt 75 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 259 § 3: the words of DU/2016/437 art. 1 pkt 49 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 260 § 1: the words of DU/2013/1247 art. 1 pkt 77 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 260 § 2: the words of DU/2013/1247 art. 1 pkt 77 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 261 § 3: DU/2008/1485 in force 2009-01-22 (footnote, used) but 2009-01-15 (API)
- kodeks-postepowania-karnego art. 263 § 2: the words of DU/2000/717 art. 1 pkt 8 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 263 § 3a: the change by DU/2000/717 before DU/2009/171 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 263 § 4: DU/2008/1485 in force 2009-01-22 (footnote, used) but 2009-01-15 (API)
- kodeks-postepowania-karnego art. 263 § 4a: the change by DU/2000/717 before DU/2008/1485 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 263 § 4a: DU/2008/1485 in force 2009-01-22 (footnote, used) but 2009-01-15 (API)
- kodeks-postepowania-karnego art. 263 § 4b: the change by DU/2000/717 before DU/2013/1247 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 263 § 5: DU/2008/1485 in force 2009-01-22 (footnote, used) but 2009-01-15 (API)
- kodeks-postepowania-karnego art. 263 § 8: the change by DU/2000/717 before DU/2013/1247 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 263 § 8: DU/2013/1247 in force 2014-06-02 (footnote, used) but 2015-07-01 (API)
- kodeks-postepowania-karnego art. 263 § 8: the words of DU/2013/1247 art. 1 pkt 79 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 275a § 1: the words of DU/2010/842 art. 6 pkt 2 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 275a § 3: the words of DU/2010/842 art. 6 pkt 2 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 275a § 5: the words of DU/2010/842 art. 6 pkt 2 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 289 § 1: the words of DU/2007/664 art. 1 pkt 7 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 291 § 1: the words of DU/2013/1247 art. 1 pkt 84 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 291 § 2: the words of DU/2013/1247 art. 1 pkt 84 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 291 § 4: the words of DU/2013/1247 art. 1 pkt 84 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 293 § 2: the words of DU/2013/1247 art. 1 pkt 86 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 297 § 1 pkt 1: the words of DU/2009/1589 art. 2 pkt 7 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 297 § 1 pkt 2: the words of DU/2009/1589 art. 2 pkt 7 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 297 § 1 pkt 3: the words of DU/2009/1589 art. 2 pkt 7 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 297 § 1 pkt 4: the words of DU/2009/1589 art. 2 pkt 7 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 306 § 1 pkt 1: the words of DU/2013/480 art. 1 pkt 1 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 306 § 1 pkt 2: the words of DU/2013/480 art. 1 pkt 1 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 306 § 1b: the words of DU/2016/437 art. 1 pkt 58 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 309 pkt 1: the words of DU/2007/432 art. 2 pkt 14 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 309 pkt 2: the words of DU/2009/1323 art. 201 pkt 2 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 309 pkt 3: the words of DU/2005/1479 art. 6 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 309 pkt 4: the words of DU/2003/155 art. 1 pkt 117 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 312 pkt 1: the words of DU/2013/1247 art. 1 pkt 91 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 325e § 4: the change by DU/2007/432 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 331 § 1: the words of DU/2003/155 art. 1 pkt 136 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 332 § 1 pkt 1: the words of DU/2013/1247 art. 1 pkt 102 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 332 § 1 pkt 2: the words of DU/2013/1247 art. 1 pkt 102 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 332 § 1 pkt 3: the words of DU/2013/1247 art. 1 pkt 102 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 332 § 1 pkt 4: the words of DU/2013/1247 art. 1 pkt 102 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 332 § 3: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 333 § 1 pkt 1: the words of DU/2016/437 art. 1 pkt 67 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 333 § 4: the words of DU/2013/1247 art. 1 pkt 103 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 334 § 2 pkt 1: the words of DU/2016/437 art. 1 pkt 68 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 335 § 1a: the words of DU/2016/437 art. 1 pkt 69 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 335 § 2a: the words of DU/2016/437 art. 1 pkt 69 lit. c differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 338 § 1b: the words of DU/2013/1247 art. 1 pkt 107 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 338a: the words of DU/2016/437 art. 1 pkt 74 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 339 § 3 pkt 3a: the words of DU/2016/437 art. 1 pkt 75 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 339 § 3a: the words of DU/2016/437 art. 1 pkt 75 lit. c differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 340 § 2: the words of DU/2013/1247 art. 1 pkt 110 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 343 § 1: the words of DU/2013/1247 art. 1 pkt 112 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 343 § 5: the words of DU/2013/1247 art. 1 pkt 112 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 343 § 5a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 343 § 7: the words of DU/2013/1247 art. 1 pkt 112 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 350 § 2 pkt 1: the words of DU/2013/1247 art. 1 pkt 115 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 350 § 2 pkt 2: the words of DU/2013/1247 art. 1 pkt 115 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 350 § 3: the words of DU/2013/1247 art. 1 pkt 115 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 354 pkt 2: the words of DU/2003/155 art. 1 pkt 150 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 354a § 1 pkt 1: the words of DU/2016/437 art. 1 pkt 84 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 354a § 1 pkt 2: the words of DU/2016/437 art. 1 pkt 84 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 360 § 1 pkt 1 lit. d: the words of DU/2016/1070 art. 1 pkt 5 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 360 § 1 pkt 2: the words of DU/2016/1070 art. 1 pkt 5 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 370 § 2a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 377 § 4: the words of DU/2013/1247 art. 1 pkt 121 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 385 § 1a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 387 § 1: the words of DU/2016/437 art. 1 pkt 91 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 387 § 1a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 392 § 1: the words of DU/2003/155 art. 1 pkt 161 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 393a: the words of DU/2016/437 art. 1 pkt 95 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 396a § 2: the words of DU/2016/437 art. 1 pkt 97 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 396a § 4: the words of DU/2016/437 art. 1 pkt 97 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 400 § 2: the change by DU/2001/1149 before DU/2008/1651 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 422 § 2: the words of DU/2013/1247 art. 1 pkt 142 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 422 § 2a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 422 § 3: the words of DU/2013/1247 art. 1 pkt 142 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 423 § 1a: the words of DU/2003/155 art. 1 pkt 173 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 424 § 1 pkt 1: the words of DU/2013/1247 art. 1 pkt 144 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 427 § 5: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 437 § 2: the words of DU/2013/1247 art. 1 pkt 149 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 438 pkt 4: the words of DU/2013/1247 art. 1 pkt 150 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 1: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 10: the words of DU/2009/1589 art. 2 pkt 10 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 2: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 3: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 4: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 5: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 6: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 7: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 8: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 1 pkt 9: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 439 § 2: the words of DU/2003/155 art. 1 pkt 177 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 443: the words of DU/2013/1247 art. 1 pkt 151 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 447 § 5: the words of DU/2013/1247 art. 1 pkt 154 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 449a § 1: the change by DU/2003/155 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 449a § 1: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 449a § 2: the change by DU/2003/155 before DU/2013/1247 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 457 § 2: the words of DU/2013/1247 art. 1 pkt 161 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 501 pkt 1: the change by DU/2003/155 before DU/2013/1247 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 504 § 1 pkt 1: the words of DU/2003/155 art. 1 pkt 199 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 504 § 1 pkt 2: the words of DU/2003/155 art. 1 pkt 199 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 504 § 1 pkt 3: the words of DU/2003/155 art. 1 pkt 199 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 504 § 1 pkt 4: the words of DU/2003/155 art. 1 pkt 199 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 523 § 1a: the change by DU/2000/717 before DU/2016/1070 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 523 § 1a: the words of DU/2016/1070 art. 1 pkt 12 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 523 § 4 pkt 1: the words of DU/2000/717 art. 1 pkt 16 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 530 § 3: the words of DU/2000/717 art. 1 pkt 20 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 540a pkt 1: the words of DU/2005/1479 art. 6 pkt 5 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 540b § 2: the words of DU/2013/1247 art. 1 pkt 188 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 545 § 1: the words of DU/2013/1247 art. 1 pkt 189 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 552a: the change by DU/2013/1247 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 553 § 3: the words of DU/2016/437 art. 1 pkt 133 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 561 § 2: the words of DU/2011/1430 art. 1 pkt 1 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 592c § 1: the words of DU/2012/1091 art. 1 pkt 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 604 § 1 pkt 6: the words of DU/2003/155 art. 1 pkt 230 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 604 § 2 pkt 6: the words of DU/2006/1647 art. 1 pkt 3 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607b pkt 1: the words of DU/2013/1247 art. 1 pkt 202 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607l § 1a: DU/2013/1247 in force 2013-11-09 (footnote, used) but 2015-07-01 (API)
- kodeks-postepowania-karnego art. 607l § 1a: the words of DU/2013/1247 art. 1 pkt 204 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607l § 4: DU/2013/1247 in force 2014-06-02 (footnote, used) but 2015-07-01 (API)
- kodeks-postepowania-karnego art. 607l § 4: the words of DU/2013/1247 art. 1 pkt 204 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607m § 1: the words of DU/2009/1589 art. 2 pkt 20 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607m § 1a: the words of DU/2009/1589 art. 2 pkt 20 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607p § 1 pkt 1: the words of DU/2006/1647 art. 1 pkt 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607p § 1 pkt 2: the words of DU/2006/1647 art. 1 pkt 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607p § 1 pkt 3: the words of DU/2006/1647 art. 1 pkt 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607p § 1 pkt 4: the words of DU/2006/1647 art. 1 pkt 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607p § 1 pkt 5: the words of DU/2006/1647 art. 1 pkt 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607s § 4: DU/2011/245 in force 2011-03-22 (footnote, used) but 2011-05-08 (API)
- kodeks-postepowania-karnego art. 607w pkt 1: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 10: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 11: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 12: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 13: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 14: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 15: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 16: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 17: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 18: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 19: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 2: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 20: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 21: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 22: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 23: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 24: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 25: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 26: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 27: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 28: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 29: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 3: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 30: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 31: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 32: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 4: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 5: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 6: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 7: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 8: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 607w pkt 9: the words of DU/2006/1647 art. 1 pkt 6 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 611fg pkt 10 lit. b: the words of DU/2011/1135 art. 2 pkt 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 611fw § 3 pkt 8: the words of DU/2011/1135 art. 2 pkt 5 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 611fw § 3 pkt 8 lit. b: the words of DU/2011/1135 art. 2 pkt 5 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 611h § 2: the words of DU/2006/1647 art. 1 pkt 7 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 611t § 5 pkt 2: the words of DU/2013/1650 art. 477 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 611wd § 2: the words of DU/2016/437 art. 1 pkt 140 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 612 § 1: the words of DU/2009/1589 art. 2 pkt 23 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 613 § 1: DU/2015/21 in force 2015-01-11 (footnote, used) but 2015-04-08 (API)
- kodeks-postepowania-karnego art. 615 § 1: the words of DU/2004/2405 art. 1 pkt 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 615 § 4: the words of DU/2004/2405 art. 1 pkt 4 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618 § 1 pkt 11: the words of DU/2013/1247 art. 1 pkt 208 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618 § 1 pkt 12: the words of DU/2001/1071 art. 96 pkt 2 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618 § 1 pkt 9a: the change by DU/2003/155 before DU/2011/654 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 618 § 1 pkt 9a: the words of DU/2011/654 art. 152 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618f § 1: the words of DU/2012/1101 art. 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618f § 2: the words of DU/2012/1101 art. 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618f § 4: the words of DU/2012/1101 art. 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618f § 4a: the change by DU/2012/1101 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 618f § 4b: the change by DU/2012/1101 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 618g: the words of DU/2012/1101 art. 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618h § 1: the words of DU/2012/1101 art. 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618h § 2: the words of DU/2012/1101 art. 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618i: the words of DU/2012/1101 art. 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618k § 2: the words of DU/2012/1101 art. 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 618k § 4: the words of DU/2012/1101 art. 1 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 632a § 2: the change by DU/2006/659 before DU/2016/437 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 632a § 2 pkt 1: the words of DU/2016/437 art. 1 pkt 143 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 632a § 2 pkt 2: the words of DU/2016/437 art. 1 pkt 143 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 647 § 1 pkt 1 lit. d: the words of DU/2008/1651 art. 1 pkt 2 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 647 § 1 pkt 2 lit. b: the words of DU/2008/1651 art. 1 pkt 2 lit. a differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 647 § 4: DU/2008/1651 in force 2016-04-04 (footnote, used) but 2009-01-01 (API)
- kodeks-postepowania-karnego art. 647 § 4: the words of DU/2008/1651 art. 1 pkt 2 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 647 § 5: DU/2008/1651 in force 2016-04-04 (footnote, used) but 2009-01-01 (API)
- kodeks-postepowania-karnego art. 647 § 5: the words of DU/2008/1651 art. 1 pkt 2 lit. b differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego art. 671a: the change by DU/2003/155 before DU/2007/766 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 672a: DU/2003/155 in force 2016-04-04 (footnote, used) but 2003-07-01 (API)
- kodeks-postepowania-karnego art. 672a: DU/2003/155 in force 2016-04-04 (footnote, used) but 2003-07-01 (API)
- kodeks-postepowania-karnego art. 672a: the words of DU/2003/155 art. 1 pkt 246 differ from DU/2016/1749; the unified text is used
- kodeks-postepowania-karnego DU/2016/1749: 1021 lines changed with no footnote
- kodeks-postepowania-karnego DU/1999/931 (in force 1999-10-17): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2000/1027 (in force 2001-02-04): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2000/852 (in force 2001-01-01): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2002/676 (in force 2002-06-29): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2003/1188 (in force 2003-08-24): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2004/2641 (in force 2004-12-15): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2004/514 (in force 2004-03-30): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2005/1203 (in force 2005-08-02): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2005/1363 (in force 2005-09-26): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2005/461 (in force 2005-03-25): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2005/680 (in force 2006-11-05): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2005/821 (in force 2005-06-02): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2006/1009 (in force 2007-02-08): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2006/1013 (in force 2006-08-08): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2006/118 (in force 2007-01-31): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2006/1192 (in force 2006-09-19): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2006/708 (in force 2006-07-24): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2006/711 (in force 2006-10-01): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2007/539 (in force 2007-05-24): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2007/903 (in force 2008-10-19): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2008/1133 (in force 2008-10-14): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2008/1308 (in force 2008-12-31): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2008/1344 (in force 2008-12-18): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2008/1571 (in force 2009-07-01): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2008/162 (in force 2009-02-20): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2008/648 (in force 2008-06-11): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2008/686 (in force 2008-06-23): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2008/802 (in force 2009-01-12): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2009/39 (in force 2009-02-05): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2009/585 (in force 2009-05-06): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2010/46 (in force 2010-04-19): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2010/826 (in force 2010-08-07): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2011/1438 (in force 2011-11-10): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2011/1645 (in force 2012-12-28): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2012/1327 (in force 2012-11-28): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2012/1426 (in force 2013-12-18): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2012/1447 (in force 2013-12-21): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2013/1262 (in force 2013-10-29): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2013/1436 (in force 2013-12-04): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2014/1375 (in force 2014-10-10): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2014/694 (in force 2014-05-28): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2015/1185 (in force 2015-09-01): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2015/1788 (in force 2015-11-04): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego DU/2015/290 (in force 2015-12-04): listed by the API, but no unit of DU/2016/1749 is credited to it
- kodeks-postepowania-karnego art. 415a § 1: the words of DU/2017/768 art. 6 pkt 13 differ from DU/2017/1904; the unified text is used
- kodeks-postepowania-karnego art. 605a § 1: the words of DU/2017/768 art. 6 pkt 16 differ from DU/2017/1904; the unified text is used
- kodeks-postepowania-karnego DU/2017/1904: 172 lines changed with no footnote
- kodeks-postepowania-karnego DU/2016/2103 (in force 2017-01-01): listed by the API, but no unit of DU/2017/1904 is credited to it
- kodeks-postepowania-karnego DU/2018/1987: 186 lines changed with no footnote
- kodeks-postepowania-karnego DU/2018/138 (in force 2018-02-01): listed by the API, but no unit of DU/2018/1987 is credited to it
- kodeks-postepowania-karnego DU/2018/1387 (in force 2018-07-19): listed by the API, but no unit of DU/2018/1987 is credited to it
- kodeks-postepowania-karnego DU/2018/1937 (in force 2018-10-09): listed by the API, but no unit of DU/2018/1987 is credited to it
- kodeks-postepowania-karnego DU/2018/942 (in force 2018-05-18): listed by the API, but no unit of DU/2018/1987 is credited to it
- kodeks-postepowania-karnego art. 340 § 2: the words of DU/2019/1694 art. 1 pkt 47 differ from DU/2020/30; the unified text is used
- kodeks-postepowania-karnego art. 418 § 1b: DU/2019/1694 in force 2019-09-05 (footnote, used) but 2019-10-05 (API)
- kodeks-postepowania-karnego art. 418 § 3: DU/2019/1694 in force 2019-09-05 (footnote, used) but 2019-10-05 (API)
- kodeks-postepowania-karnego DU/2020/30: 41 lines changed with no footnote
- kodeks-postepowania-karnego DU/2017/2405 (in force 2019-06-23): listed by the API, but no unit of DU/2020/30 is credited to it
- kodeks-postepowania-karnego DU/2018/1467 (in force 2019-01-01): listed by the API, but no unit of DU/2020/30 is credited to it
- kodeks-postepowania-karnego DU/2018/771 (in force 2019-01-01): listed by the API, but no unit of DU/2020/30 is credited to it
- kodeks-postepowania-karnego DU/2019/1255 (in force 2019-07-08): listed by the API, but no unit of DU/2020/30 is credited to it
- kodeks-postepowania-karnego art. 276a § 1a: the change by DU/2020/568 before DU/2020/1086 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego DU/2021/534: 23 lines changed with no footnote
- kodeks-postepowania-karnego DU/2020/1458 (in force 2020-08-26): listed by the API, but no unit of DU/2021/534 is credited to it
- kodeks-postepowania-karnego DU/2020/413 (in force 2020-03-12): listed by the API, but no unit of DU/2021/534 is credited to it
- kodeks-postepowania-karnego art. 218b: the words of DU/2021/1023 art. 3 pkt 3 differ from DU/2022/1375; the unified text is used
- kodeks-postepowania-karnego DU/2022/1375: 40 lines changed with no footnote
- kodeks-postepowania-karnego DU/2020/2320 (in force 2021-10-05): listed by the API, but no unit of DU/2022/1375 is credited to it
- kodeks-postepowania-karnego DU/2022/958 (in force 2022-05-06): listed by the API, but no unit of DU/2022/1375 is credited to it
- kodeks-postepowania-karnego art. 52a: the change by DU/2023/289 before DU/2023/1860 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego art. 213 § 2: the change by DU/2020/2320 before DU/2022/2600 is not reconstructed (no quoted wording)
- kodeks-postepowania-karnego DU/2024/37: 32 lines changed with no footnote
- kodeks-postepowania-karnego DU/2023/1606 (in force 2024-02-15): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2023/818 (in force 2024-02-15): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2024/1222 (in force 2024-11-10): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2024/1248 (in force 2024-08-31): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2025/1178 (in force 2026-03-01): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2025/1420 (in force 2025-11-04): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2025/1872 (in force 2026-01-29): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2025/304 (in force 2025-03-27): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2026/187 (in force 2028-05-19): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2026/421 (in force 2026-04-14): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2026/638 (in force 2026-05-28): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2026/760 (in force 2026-06-12): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2026/882 (in force 2026-07-16): after the last unified text; not in the record
- kodeks-postepowania-karnego DU/2026/901 (in force 2026-07-21): after the last unified text; not in the record

## What the AI did

The builder, parsers, checks and documentation were written by Claude Code with Claude Opus 5.5
(`claude-opus-5-5`), at the request of Lexifina. No AI wrote or changed any legal text, and no model runs when the
repository is built: every word of law comes from the Sejm's API.
