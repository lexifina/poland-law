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
was typed in, summarised or rewritten. The build read 95 metadata records, 87 HTML texts and 3 PDFs,
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
| Kodeks spółek handlowych | Dz.U. 2000 nr 94 poz. 1037 | 2001-01-01 | html | tekst ogłoszony (the act as published) |
| Kodeks spółek handlowych | Dz.U. 2013 poz. 1030 | 2013-09-06 | html | tekst jednolity |
| Kodeks spółek handlowych | Dz.U. 2016 poz. 1578 | 2016-09-29 | html | tekst jednolity |
| Kodeks spółek handlowych | Dz.U. 2017 poz. 1577 | 2017-08-24 | html | tekst jednolity |
| Kodeks spółek handlowych | Dz.U. 2019 poz. 505 | 2019-03-15 | html | tekst jednolity |
| Kodeks spółek handlowych | Dz.U. 2020 poz. 1526 | 2020-09-04 | html | tekst jednolity |
| Kodeks spółek handlowych | Dz.U. 2022 poz. 1467 | 2022-07-12 | html | tekst jednolity |
| Kodeks spółek handlowych | Dz.U. 2024 poz. 18 | 2024-01-05 | html | tekst jednolity |

## The build, step by step

1. `python -X utf8 scripts/poland-law/build.py --today 2026-11-02` in Lexifina's own repository fetched the data into its
   cache and wrote this repository. The files in `tools/` are the same files as in `scripts/poland-law/` there
   (git blobs: `build.py` 23a531f09456, `parse.py` 899e414d2153, `pdfparse.py` 3056ad6a05e5, `gloss.py` 404e4b159519, `reproduce.py` 035c8d9409f3).
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
  replayed on its day and checked against the next unified text (Konstytucja: 9 of 9 quoted lines; Obywatelstwo: 21 of 22 quoted lines; Kodeks spółek handlowych: 751 of 859 quoted lines).
- **Editorial changes of the unified texts** (updated Journal references of the other acts cited, provisions left out
  as "(pominięty)") are separate commits, authored by the Marshal of the Sejm's unified text, on the day it was
  published. A line changed by an act keeps the Journal references it had until then.
- **The Constitution** (`konstytucja/`) has no unified text. The current text is the Sejm's consolidated text (PDF,
  type U). The 2006 and 2009 amending acts are replayed from their own words (HTML) and must equal it; the
  correction notice of 2001 (Dz.U. 2001 nr 28 poz. 319) is applied word by word and its commit is authored by the
  notice, not by a law. The text as enacted is the consolidated text with those three steps undone; art. 55 as enacted
  is read from the text layer of the 1997 Journal's scan (O), between "Art. 55." and "Art. 56.".
- Commits are dated noon in Warsaw on the in-force day (CET, CEST from the last Sunday in March to the last Sunday in
  October). Counts: editorial 7, law 70, record-correction 1, start 1, unexplained 7; 148 tags.

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

- kodeks-spolek-handlowych art. 4 § 1 pkt 6: the words of DU/2005/1539 art. 114 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 4 § 1 pkt 7: the words of DU/2012/596 art. 9 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 4 § 3: the words of DU/2005/1108 art. 14 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 4 § 4: the words of DU/2005/1108 art. 14 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 4 § 5: the words of DU/2005/1108 art. 14 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 126 § 1 pkt 1: the words of DU/2003/2276 art. 1 pkt 14 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 127 § 5 pkt 1: the words of DU/2006/1540 art. 5 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 127 § 5 pkt 2: the words of DU/2006/1540 art. 5 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 127 § 5 pkt 3: the words of DU/2006/1540 art. 5 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 154 § 1: the words of DU/2008/1381 art. 1 pkt 5 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 157¹ § 5: the words of DU/2011/531 art. 1 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 163 pkt 2: the words of DU/2011/531 art. 1 pkt 3 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 167 § 4 pkt 1: the words of DU/2011/531 art. 1 pkt 4 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 167 § 4 pkt 2: the words of DU/2011/531 art. 1 pkt 4 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 167 § 5 pkt 1: the words of DU/2011/531 art. 1 pkt 4 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 206 § 1 pkt 1: the words of DU/2006/1540 art. 5 pkt 2 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 206 § 1 pkt 2: the words of DU/2006/1540 art. 5 pkt 2 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 206 § 1 pkt 3: the words of DU/2006/1540 art. 5 pkt 2 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 228 pkt 4: the words of DU/2003/2276 art. 1 pkt 30 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 312¹ § 1: the words of DU/2008/747 art. 1 pkt 3 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 312¹ § 1 pkt 1: the words of DU/2008/747 art. 1 pkt 3 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 312¹ § 1 pkt 2: the words of DU/2008/747 art. 1 pkt 3 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 312¹ § 2: the words of DU/2008/747 art. 1 pkt 3 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 312¹ § 2 pkt 1: the words of DU/2008/747 art. 1 pkt 3 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 312¹ § 5 pkt 1: the words of DU/2008/747 art. 1 pkt 3 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 312¹ § 5 pkt 2: the words of DU/2008/747 art. 1 pkt 3 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 345 § 6 pkt 1: the words of DU/2008/747 art. 1 pkt 4 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 345 § 6 pkt 2: the words of DU/2008/747 art. 1 pkt 4 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 345 § 6 pkt 3: the words of DU/2008/747 art. 1 pkt 4 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 345 § 6 pkt 4: the words of DU/2008/747 art. 1 pkt 4 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 1 pkt 1: the words of DU/2003/2276 art. 1 pkt 52 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 1 pkt 2: the words of DU/2003/2276 art. 1 pkt 52 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 1 pkt 2a: the change by DU/2003/2276 before DU/2005/1538 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 362 § 1 pkt 3: the words of DU/2003/2276 art. 1 pkt 52 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 1 pkt 4: the words of DU/2003/2276 art. 1 pkt 52 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 1 pkt 5: the words of DU/2003/2276 art. 1 pkt 52 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 1 pkt 6: the words of DU/2003/2276 art. 1 pkt 52 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 1 pkt 7: the words of DU/2003/2276 art. 1 pkt 52 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 1 pkt 8: the words of DU/2008/747 art. 1 pkt 5 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 2 pkt 1: the words of DU/2003/2276 art. 1 pkt 52 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 362 § 2 pkt 2: the words of DU/2008/747 art. 1 pkt 5 lit. b differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 374 § 1 pkt 1: the words of DU/2006/1540 art. 5 pkt 3 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 374 § 1 pkt 2: the words of DU/2006/1540 art. 5 pkt 3 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 374 § 1 pkt 3: the words of DU/2006/1540 art. 5 pkt 3 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 393 pkt 4: the words of DU/2003/2276 art. 1 pkt 61 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 393 pkt 5: the words of DU/2003/2276 art. 1 pkt 61 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 393 pkt 6: the words of DU/2003/2276 art. 1 pkt 61 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402² pkt 1: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402² pkt 2 lit. g: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402² pkt 3: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402² pkt 4: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402² pkt 5: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402³ § 1 pkt 1: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402³ § 1 pkt 2: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402³ § 1 pkt 3: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402³ § 1 pkt 4: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402³ § 3 pkt 1: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402³ § 3 pkt 2: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 402³ § 3 pkt 3: the words of DU/2009/69 art. 1 pkt 7 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406³ § 3 pkt 1: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406³ § 3 pkt 2: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406³ § 3 pkt 3: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406³ § 3 pkt 4: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406³ § 3 pkt 5: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406³ § 3 pkt 6: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406³ § 3 pkt 7: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406³ § 3 pkt 8: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406³ § 3 pkt 9: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406⁵ § 1 pkt 1: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 406⁵ § 1 pkt 2: the words of DU/2009/69 art. 1 pkt 9 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 411 § 3: DU/2009/860 in force 2009-08-01 (footnote, used) but 2009-08-02 (API)
- kodeks-spolek-handlowych art. 412 § 5¹: the change by DU/2009/69 before DU/2011/1391 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 441 § 2 pkt 6: the words of DU/2005/1539 art. 114 pkt 5 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 450 § 1 pkt 1: the words of DU/2003/2276 art. 1 pkt 74 lit. a differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 453 § 2: the words of DU/2003/2276 art. 1 pkt 76 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 453 § 3 pkt 1: the words of DU/2003/2276 art. 1 pkt 76 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 453 § 3 pkt 2: the words of DU/2003/2276 art. 1 pkt 76 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 453 § 3 pkt 3: the words of DU/2003/2276 art. 1 pkt 76 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 455 § 5: the words of DU/2008/1547 art. 4 pkt 4 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 491 § 1¹: the words of DU/2008/524 art. 1 pkt 1 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 503¹: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 503¹ § 1: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 503¹ § 1: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 503¹ § 1 pkt 1: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 503¹ § 1 pkt 1: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 503¹ § 1 pkt 2: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 503¹ § 1 pkt 2: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 503¹ § 1 pkt 3: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 503¹ § 1 pkt 3: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 503¹ § 2: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 503¹ § 2: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 538¹: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 538¹ § 1: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 538¹ § 1: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 538¹ § 1 pkt 1: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 538¹ § 1 pkt 1: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 538¹ § 1 pkt 2: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 538¹ § 1 pkt 2: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 538¹ § 1 pkt 3: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 538¹ § 1 pkt 3: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 538¹ § 2: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 538¹ § 2: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 538¹ § 3: DU/2009/69 in force 2009-02-28 (footnote, used) but 2009-08-03 (API)
- kodeks-spolek-handlowych art. 538¹ § 3: the change by DU/2009/69 before DU/2011/1182 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 587 § 1: the words of DU/2003/2276 art. 1 pkt 99 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 590 pkt 2: the words of DU/2003/2276 art. 1 pkt 100 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 590 pkt 3: the change by DU/2003/2276 before DU/2009/69 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 590 pkt 4: the change by DU/2003/2276 before DU/2009/69 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 591 pkt 3: the words of DU/2003/2276 art. 1 pkt 100 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych art. 591 pkt 4: the change by DU/2003/2276 before DU/2009/69 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 591 pkt 5: the change by DU/2003/2276 before DU/2009/69 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 595 § 1: the words of DU/2008/1381 art. 1 pkt 13 differ from DU/2013/1030; the unified text is used
- kodeks-spolek-handlowych DU/2013/1030: 230 lines changed with no footnote
- kodeks-spolek-handlowych DU/2003/535 (in force 2003-10-01): listed by the API, but no unit of DU/2013/1030 is credited to it
- kodeks-spolek-handlowych DU/2004/1808 (in force 2004-08-21): listed by the API, but no unit of DU/2013/1030 is credited to it
- kodeks-spolek-handlowych DU/2006/935 (in force 2006-08-05): listed by the API, but no unit of DU/2013/1030 is credited to it
- kodeks-spolek-handlowych art. 10 § 4: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 10 § 5: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 40¹: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 40¹ § 1: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 40¹ § 2: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 58 § 2: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 158 § 1²: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 180 § 2: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 188 § 4: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 208 § 11: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 240¹: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 240¹ § 1: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 240¹ § 2: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 240¹ § 3: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 240¹ § 4: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 248 § 3: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 255 § 4: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 259¹: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 259¹: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 259¹: the words of DU/2015/4 art. 1 pkt 23 differ from DU/2016/1578; the unified text is used
- kodeks-spolek-handlowych art. 259¹: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych art. 270 pkt 2¹: DU/2015/4 in force 2016-04-01 (footnote, used) but 2015-01-15 (API)
- kodeks-spolek-handlowych DU/2016/1578: 48 lines changed with no footnote
- kodeks-spolek-handlowych DU/2017/1577: 19 lines changed with no footnote
- kodeks-spolek-handlowych DU/2016/996 (in force 2016-10-09): listed by the API, but no unit of DU/2017/1577 is credited to it
- kodeks-spolek-handlowych DU/2017/791 (in force 2017-04-29): listed by the API, but no unit of DU/2017/1577 is credited to it
- kodeks-spolek-handlowych art. 18 § 2: DU/2018/398 in force 2018-10-01 (footnote, used) but 2018-03-15 (API)
- kodeks-spolek-handlowych art. 18 § 3: DU/2018/398 in force 2018-10-01 (footnote, used) but 2018-03-15 (API)
- kodeks-spolek-handlowych art. 18 § 5: DU/2018/398 in force 2018-10-01 (footnote, used) but 2018-03-15 (API)
- kodeks-spolek-handlowych art. 23¹ § 2: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 106¹ § 2: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 157¹ § 2: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 167 § 4 pkt 1: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 167 § 4 pkt 2: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 167 § 4 pkt 3: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 188 § 4: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 270 pkt 2¹: the change by DU/2018/1544 before DU/2019/60 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych DU/2019/505: 14 lines changed with no footnote
- kodeks-spolek-handlowych DU/2018/2244 (in force 2019-03-01): listed by the API, but no unit of DU/2019/505 is credited to it
- kodeks-spolek-handlowych art. 5 § 5: DU/2019/1798 in force 2020-01-01 (footnote, used) but 2021-03-01 (API)
- kodeks-spolek-handlowych art. 234¹ § 2 pkt 1: the change by DU/2019/1543 before DU/2020/568 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 234¹ § 2 pkt 2: the change by DU/2019/1543 before DU/2020/568 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 234¹ § 3: the change by DU/2019/1543 before DU/2020/568 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 276 § 1¹: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 328⁴: DU/2019/1798 in force 2020-01-01 (footnote, used) but 2021-03-01 (API)
- kodeks-spolek-handlowych art. 328⁴ § 2: DU/2019/1798 in force 2020-01-01 (footnote, used) but 2021-03-01 (API)
- kodeks-spolek-handlowych art. 328⁴ § 2: the words of DU/2019/1798 art. 1 pkt 8 differ from DU/2020/1526; the unified text is used
- kodeks-spolek-handlowych art. 463 § 3¹: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 515 § 1: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 515 § 1: the words of DU/2019/1655 art. 1 pkt 13 differ from DU/2020/1526; the unified text is used
- kodeks-spolek-handlowych art. 515 § 2: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 553 § 3: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 556 pkt 4: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 558 § 1 pkt 2: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 558 § 2 pkt 3: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 559 § 1: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 560 § 1: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 560 § 2: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 561 § 2: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 563 § 1: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 563 § 1 pkt 1: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 563 § 1 pkt 2: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 563 § 1 pkt 2: the words of DU/2019/1655 art. 1 pkt 23 differ from DU/2020/1526; the unified text is used
- kodeks-spolek-handlowych art. 563 § 1 pkt 3: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 563 § 1 pkt 4: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 563 § 1 pkt 5: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 563 § 2: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 564: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 565: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 566: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 567 § 2: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 569 § 2: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 576¹: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 576¹ § 1: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 576¹ § 2: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 576¹ § 3: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 576¹ § 3: the words of DU/2019/1655 art. 1 pkt 27 differ from DU/2020/1526; the unified text is used
- kodeks-spolek-handlowych art. 576¹ § 4: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 576¹ § 5: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 576¹ § 6: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 576¹ § 6: the words of DU/2019/1655 art. 1 pkt 27 differ from DU/2020/1526; the unified text is used
- kodeks-spolek-handlowych art. 576¹ § 7: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych art. 576¹ § 8: DU/2019/1655 in force 2020-03-01 (footnote, used) but 2021-07-01 (API)
- kodeks-spolek-handlowych DU/2020/1526: 76 lines changed with no footnote
- kodeks-spolek-handlowych art. 18 § 2: the change by DU/2021/2052 before DU/2022/807 is not reconstructed (no quoted wording)
- kodeks-spolek-handlowych art. 18 § 2: the words of DU/2022/807 art. 1 pkt 3 differ from DU/2022/1467; the unified text is used
- kodeks-spolek-handlowych DU/2022/1467: 195 lines changed with no footnote
- kodeks-spolek-handlowych DU/2022/807: in force 2022-10-13, after the unified text DU/2022/1467 of 2022-07-12 that prints it
- kodeks-spolek-handlowych DU/2021/2052 (in force 2021-11-30): listed by the API, but no unit of DU/2022/1467 is credited to it
- kodeks-spolek-handlowych art. 454³ § 1: the words of DU/2023/825 art. 7 pkt 2 differ from DU/2024/18; the unified text is used
- kodeks-spolek-handlowych art. 454⁶ § 1: the words of DU/2023/825 art. 7 pkt 2 differ from DU/2024/18; the unified text is used
- kodeks-spolek-handlowych art. 459 pkt 2: the words of DU/2023/1705 art. 1 pkt 5 differ from DU/2024/18; the unified text is used
- kodeks-spolek-handlowych art. 595¹ § 1: the words of DU/2022/1488 art. 48 pkt 3 differ from DU/2024/18; the unified text is used
- kodeks-spolek-handlowych art. 595² § 1: the words of DU/2022/1488 art. 48 pkt 3 differ from DU/2024/18; the unified text is used
- kodeks-spolek-handlowych DU/2024/18: 324 lines changed with no footnote
- kodeks-spolek-handlowych DU/2023/739 (in force 2023-04-19): listed by the API, but no unit of DU/2024/18 is credited to it
- kodeks-spolek-handlowych DU/2024/96 (in force 2024-01-26): after the last unified text; not in the record
- kodeks-spolek-handlowych DU/2026/176 (in force 2027-02-18): after the last unified text; not in the record
- kodeks-spolek-handlowych DU/2026/187 (in force 2028-05-19): after the last unified text; not in the record
- kodeks-spolek-handlowych DU/2026/644 (in force 2030-01-10): after the last unified text; not in the record
- kodeks-spolek-handlowych DU/2022/1467: 1 lines differ from the unified text for no reason found: art. 18 § 2
- kodeks-spolek-handlowych DU/2024/18: 1 lines differ from the unified text for no reason found: art. 483 § 2

## What the AI did

The builder, parsers, checks and documentation were written by Claude Code with Claude Opus 5.5
(`claude-opus-5-5`), at the request of Lexifina. No AI wrote or changed any legal text, and no model runs when the
repository is built: every word of law comes from the Sejm's API.
