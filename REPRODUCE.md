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
was typed in, summarised or rewritten. The build read 513 metadata records, 485 HTML texts and 3 PDFs,
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
| Kodeks pracy | Dz.U. 1974 nr 24 poz. 141 | 1975-01-01 | html | tekst ogłoszony (the act as published) |
| Kodeks pracy | Dz.U. 2014 poz. 1502 | 2014-11-04 | html | tekst jednolity |
| Kodeks pracy | Dz.U. 2016 poz. 1666 | 2016-10-12 | html | tekst jednolity |
| Kodeks pracy | Dz.U. 2018 poz. 108 | 2018-01-12 | html | tekst jednolity |
| Kodeks pracy | Dz.U. 2018 poz. 917 | 2018-05-16 | html | tekst jednolity |
| Kodeks pracy | Dz.U. 2019 poz. 1040 | 2019-06-05 | html | tekst jednolity |
| Kodeks pracy | Dz.U. 2020 poz. 1320 | 2020-07-30 | html | tekst jednolity |
| Kodeks pracy | Dz.U. 2022 poz. 1510 | 2022-07-19 | html | tekst jednolity |
| Kodeks pracy | Dz.U. 2023 poz. 1465 | 2023-07-31 | html | tekst jednolity |
| Kodeks postępowania cywilnego | Dz.U. 1964 nr 43 poz. 296 | 1965-01-01 | html | tekst ogłoszony (the act as published) |
| Kodeks postępowania cywilnego | Dz.U. 2014 poz. 101 | 2014-01-21 | html | tekst jednolity |
| Kodeks postępowania cywilnego | Dz.U. 2016 poz. 1822 | 2016-11-09 | html | tekst jednolity |
| Kodeks postępowania cywilnego | Dz.U. 2018 poz. 155 | 2018-01-19 | html | tekst jednolity |
| Kodeks postępowania cywilnego | Dz.U. 2018 poz. 1360 | 2018-07-16 | html | tekst jednolity |
| Kodeks postępowania cywilnego | Dz.U. 2019 poz. 1460 | 2019-08-05 | html | tekst jednolity |
| Kodeks postępowania cywilnego | Dz.U. 2020 poz. 1575 | 2020-09-14 | html | tekst jednolity |
| Kodeks postępowania cywilnego | Dz.U. 2021 poz. 1805 | 2021-10-04 | html | tekst jednolity |
| Kodeks postępowania cywilnego | Dz.U. 2023 poz. 1550 | 2023-08-08 | html | tekst jednolity |
| Kodeks postępowania cywilnego | Dz.U. 2024 poz. 1568 | 2024-10-23 | html | tekst jednolity |

## The build, step by step

1. `python -X utf8 scripts/poland-law/build.py --today 2026-11-02` in Lexifina's own repository fetched the data into its
   cache and wrote this repository. The files in `tools/` are the same files as in `scripts/poland-law/` there
   (git blobs: `build.py` 8342b2698fc8, `parse.py` 315ab387f541, `pdfparse.py` 3056ad6a05e5, `gloss.py` 404e4b159519, `reproduce.py` 9db827df15c9).
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

- **The codes and statutes added since 2026-11-02** (`kodeks-pracy/`, `kodeks-postepowania-cywilnego/`) are read the same way as the
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
  replayed on its day and checked against the next unified text (Konstytucja: 9 of 9 quoted lines; Obywatelstwo: 21 of 22 quoted lines; Kodeks pracy: 1065 of 1324 quoted lines; Kodeks postępowania cywilnego: 3190 of 3569 quoted lines).
- **Editorial changes of the unified texts** (updated Journal references of the other acts cited, provisions left out
  as "(pominięty)") are separate commits, authored by the Marshal of the Sejm's unified text, on the day it was
  published. A line changed by an act keeps the Journal references it had until then.
- **The Constitution** (`konstytucja/`) has no unified text. The current text is the Sejm's consolidated text (PDF,
  type U). The 2006 and 2009 amending acts are replayed from their own words (HTML) and must equal it; the
  correction notice of 2001 (Dz.U. 2001 nr 28 poz. 319) is applied word by word and its commit is authored by the
  notice, not by a law. The text as enacted is the consolidated text with those three steps undone; art. 55 as enacted
  is read from the text layer of the 1997 Journal's scan (O), between "Art. 55." and "Art. 56.".
- Commits are dated noon in Warsaw on the in-force day (CET, CEST from the last Sunday in March to the last Sunday in
  October). Counts: editorial 17, law 500, start 2, unexplained 17; 968 tags.

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

- kodeks-pracy art. 18³a § 5 pkt 1: the words of DU/2008/1460 art. 1 pkt 1 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 18³b § 2 pkt 1: the words of DU/2008/1460 art. 1 pkt 2 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 18³b § 2 pkt 2: the words of DU/2008/1460 art. 1 pkt 2 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 18³b § 2 pkt 3: the words of DU/2008/1460 art. 1 pkt 2 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 22¹ § 1 pkt 1: the words of DU/2003/2081 art. 1 pkt 7 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 22¹ § 1 pkt 2: the words of DU/2003/2081 art. 1 pkt 7 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 22¹ § 1 pkt 3: the words of DU/2003/2081 art. 1 pkt 7 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 22¹ § 1 pkt 4: the words of DU/2003/2081 art. 1 pkt 7 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 22¹ § 1 pkt 5: the words of DU/2003/2081 art. 1 pkt 7 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 22¹ § 2 pkt 1: the words of DU/2003/2081 art. 1 pkt 7 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 25¹ § 1: the words of DU/2003/2081 art. 1 pkt 10 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 25¹ § 3 pkt 1: the words of DU/2003/2081 art. 1 pkt 10 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 29 § 1 pkt 1: the words of DU/2003/2081 art. 1 pkt 11 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 29 § 1 pkt 2: the words of DU/2003/2081 art. 1 pkt 11 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 29 § 1 pkt 3: the words of DU/2003/2081 art. 1 pkt 11 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 29 § 1 pkt 4: the words of DU/2003/2081 art. 1 pkt 11 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 29 § 3¹: the change by DU/2003/2081 before DU/2006/935 is not reconstructed (no quoted wording)
- kodeks-pracy art. 29 § 3²: the change by DU/2003/2081 before DU/2006/935 is not reconstructed (no quoted wording)
- kodeks-pracy art. 29 § 3³: the change by DU/2003/2081 before DU/2006/935 is not reconstructed (no quoted wording)
- kodeks-pracy art. 29¹ § 1 pkt 1: the words of DU/2003/2081 art. 1 pkt 12 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 29¹ § 2 pkt 1: the words of DU/2006/935 art. 3 pkt 2 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 29¹ § 3: the change by DU/2003/2081 before DU/2006/935 is not reconstructed (no quoted wording)
- kodeks-pracy art. 29¹ § 4: the change by DU/2003/2081 before DU/2006/935 is not reconstructed (no quoted wording)
- kodeks-pracy art. 29¹ § 5: the change by DU/2003/2081 before DU/2006/935 is not reconstructed (no quoted wording)
- kodeks-pracy art. 29¹ § 6: the change by DU/2003/2081 before DU/2006/935 is not reconstructed (no quoted wording)
- kodeks-pracy art. 37 § 2 pkt 1: the words of DU/2003/2081 art. 1 pkt 15 lit. b differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 50 § 3: footnote names DU/2001/854, not among the API's amending acts
- kodeks-pracy art. 50 § 3: no in-force day for DU/2001/854; not credited
- kodeks-pracy art. 53 § 1 pkt 1 lit. b: the words of DU/2005/71 art. 2 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 67² § 1 pkt 7: the words of DU/2006/935 art. 3 pkt 3 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 67² § 2: the words of DU/2006/935 art. 3 pkt 3 lit. b differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 77³ § 3 pkt 1: the words of DU/2003/2081 art. 1 pkt 22 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 77³ § 3 pkt 2: the words of DU/2003/2081 art. 1 pkt 22 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 77⁵: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 77⁵ § 1: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 77⁵ § 2: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 77⁵ § 3: the change by DU/2000/1268 before DU/2002/1146 is not reconstructed (no quoted wording)
- kodeks-pracy art. 77⁵ § 3: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 77⁵ § 4: the change by DU/2000/1268 before DU/2002/1146 is not reconstructed (no quoted wording)
- kodeks-pracy art. 77⁵ § 4: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 77⁵ § 5: the change by DU/2000/1268 before DU/2002/1146 is not reconstructed (no quoted wording)
- kodeks-pracy art. 77⁵ § 5: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 87¹ § 1 pkt 1: the words of DU/2003/2081 art. 1 pkt 24 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 87¹ § 1 pkt 2: the words of DU/2003/2081 art. 1 pkt 24 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 88 § 1 pkt 1: the words of DU/2005/732 art. 21 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 91 § 2 pkt 1: the words of DU/2004/1001 art. 126 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 92 § 1 pkt 1: the words of DU/2009/33 art. 2 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 92 § 1 pkt 2: the words of DU/2005/71 art. 2 pkt 2 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 92 § 1¹: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 94 pkt 2a: the words of DU/2003/2081 art. 1 pkt 27 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 94 pkt 2b: the words of DU/2003/2081 art. 1 pkt 27 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 94 pkt 9b: the words of DU/2007/426 art. 2 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 103¹ § 2 pkt 1: the words of DU/2010/655 art. 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 103² § 1 pkt 1: the words of DU/2010/655 art. 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 103² § 1 pkt 2: the words of DU/2010/655 art. 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 103² § 1 pkt 3: the words of DU/2010/655 art. 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 103⁶: the words of DU/2010/655 art. 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 104¹ § 1 pkt 2: the words of DU/2003/2081 art. 1 pkt 31 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 104¹ § 1 pkt 5: the words of DU/2003/2081 art. 1 pkt 31 lit. b differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 104¹ § 1 pkt 7a: the words of DU/2001/1405 art. 1 pkt 9 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 108 § 1 pkt 1: the words of DU/2003/2081 art. 1 pkt 35 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 129 § 4 pkt 1: the words of DU/2013/896 art. 1 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 129 § 4 pkt 2: the words of DU/2013/896 art. 1 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 129 § 4 pkt 3: the words of DU/2013/896 art. 1 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 139 § 5: the words of DU/2013/896 art. 1 pkt 2 lit. b differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 154 § 1 pkt 1: the words of DU/2003/2081 art. 1 pkt 38 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 155¹ § 1: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155¹ § 1 pkt 1: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155¹ § 1 pkt 1: the words of DU/2002/1146 art. 1 pkt 33 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 155¹ § 1 pkt 2: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155¹ § 1 pkt 2 lit. a: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155¹ § 1 pkt 2 lit. b: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155¹ § 1 pkt 2 część wspólna: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155¹ § 2¹: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155¹ § 3: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155²: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155² § 1: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155² § 1 pkt 1: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155² § 1 pkt 1: the words of DU/2002/1146 art. 1 pkt 34 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 155² § 1 pkt 2: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155² § 1 pkt 2: the words of DU/2002/1146 art. 1 pkt 34 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 155² § 1 pkt 3: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155² § 1 pkt 3: the words of DU/2002/1146 art. 1 pkt 34 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 155² § 1 pkt 4: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155² § 1 pkt 4: the words of DU/2002/1146 art. 1 pkt 34 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 155² § 1 pkt 5: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155² § 1 pkt 5: the words of DU/2002/1146 art. 1 pkt 34 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 155² § 1 pkt 6: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 155² § 2: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 163 § 1¹: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 167¹: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 167¹: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 167²: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 167²: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 167³: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 167³: DU/2002/1146 in force 2003-01-01 (footnote, used) but 2002-11-29 (API)
- kodeks-pracy art. 178¹: the words of DU/2003/2081 art. 1 pkt 46 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 180 § 1 pkt 1: the words of DU/2008/1654 art. 1 pkt 1 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 180 § 1 pkt 2: the words of DU/2008/1654 art. 1 pkt 1 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 180 § 1 pkt 3: the words of DU/2008/1654 art. 1 pkt 1 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 180 § 1 pkt 4: the words of DU/2008/1654 art. 1 pkt 1 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 180 § 6¹: the change by DU/2001/1805 before DU/2008/1654 is not reconstructed (no quoted wording)
- kodeks-pracy art. 180 § 6²: the change by DU/2001/1805 before DU/2008/1654 is not reconstructed (no quoted wording)
- kodeks-pracy art. 180 § 6³: the change by DU/2001/1805 before DU/2008/1654 is not reconstructed (no quoted wording)
- kodeks-pracy art. 182¹ § 1 pkt 1: the words of DU/2013/675 art. 1 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 182¹ § 7: the change by DU/2008/1654 before DU/2013/675 is not reconstructed (no quoted wording)
- kodeks-pracy art. 182²: the change by DU/2008/1654 before DU/2013/675 is not reconstructed (no quoted wording)
- kodeks-pracy art. 182³ § 1: the words of DU/2010/1655 art. 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 183 § 1: the words of DU/2008/1654 art. 1 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 183 § 1 część wspólna: the words of DU/2008/1654 art. 1 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 183 § 3 pkt 1: the words of DU/2013/675 art. 1 pkt 7 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 183 § 3 pkt 2: the words of DU/2013/675 art. 1 pkt 7 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 183 § 5: the change by DU/2008/1654 before DU/2013/675 is not reconstructed (no quoted wording)
- kodeks-pracy art. 186³ pkt 1: the words of DU/2003/2081 art. 1 pkt 51 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 186⁷ § 1: the change by DU/2003/2081 before DU/2009/1704 is not reconstructed (no quoted wording)
- kodeks-pracy art. 186⁷ § 2: the change by DU/2003/2081 before DU/2009/1704 is not reconstructed (no quoted wording)
- kodeks-pracy art. 190 § 1: the change by DU/2001/1194 before DU/2009/458 is not reconstructed (no quoted wording)
- kodeks-pracy art. 190 § 1: DU/2009/458 in force 2009-04-22 (footnote, used) but 2018-09-01 (API)
- kodeks-pracy art. 190 § 1: the words of DU/2009/458 art. 2 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 190 § 2: the change by DU/2001/1194 before DU/2009/458 is not reconstructed (no quoted wording)
- kodeks-pracy art. 190 § 2: DU/2009/458 in force 2009-04-22 (footnote, used) but 2018-09-01 (API)
- kodeks-pracy art. 190 § 2: the words of DU/2009/458 art. 2 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 191 § 5 pkt 3: the change by DU/2001/1194 before DU/2009/458 is not reconstructed (no quoted wording)
- kodeks-pracy art. 191 § 5 pkt 3: DU/2009/458 in force 2009-04-22 (footnote, used) but 2018-09-01 (API)
- kodeks-pracy art. 191 § 5 pkt 3: the words of DU/2009/458 art. 2 pkt 2 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 191 § 5 pkt 4: the change by DU/2001/1194 before DU/2009/458 is not reconstructed (no quoted wording)
- kodeks-pracy art. 191 § 5 pkt 4: DU/2009/458 in force 2009-04-22 (footnote, used) but 2018-09-01 (API)
- kodeks-pracy art. 191 § 5 pkt 4: the words of DU/2009/458 art. 2 pkt 2 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 203 § 1¹: the words of DU/2001/1405 art. 1 pkt 17 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207 § 2 pkt 1: the words of DU/2008/1460 art. 1 pkt 5 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207 § 2 pkt 2: the words of DU/2008/1460 art. 1 pkt 5 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207 § 2 pkt 3: the words of DU/2008/1460 art. 1 pkt 5 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207 § 2 pkt 4: the words of DU/2008/1460 art. 1 pkt 5 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207 § 2 pkt 5: the words of DU/2008/1460 art. 1 pkt 5 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207 § 2 pkt 6: the words of DU/2008/1460 art. 1 pkt 5 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207¹ § 1 pkt 1: the words of DU/2008/1460 art. 1 pkt 6 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207¹ § 1 pkt 2: the words of DU/2008/1460 art. 1 pkt 6 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207¹ § 2 pkt 1: the words of DU/2008/1460 art. 1 pkt 6 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 207¹ § 2 pkt 2: the words of DU/2008/1460 art. 1 pkt 6 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 208 § 1 pkt 4: the words of DU/2008/1460 art. 1 pkt 7 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 209¹ § 4: the change by DU/2008/1460 before DU/2009/958 is not reconstructed (no quoted wording)
- kodeks-pracy art. 209² § 1 pkt 1: the words of DU/2008/1460 art. 1 pkt 8 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 209² § 2 pkt 1: the words of DU/2008/1460 art. 1 pkt 8 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 209³ § 1: the words of DU/2008/1460 art. 1 pkt 8 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 215 pkt 1: the words of DU/2008/1460 art. 1 pkt 10 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 219 pkt 4: the words of DU/2012/908 art. 4 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 222 § 3 pkt 1: the words of DU/2011/322 art. 65 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 222 § 3 pkt 2: the words of DU/2011/322 art. 65 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 222 § 3 pkt 3: the words of DU/2011/322 art. 65 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 222 § 3 pkt 4: the words of DU/2011/322 art. 65 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 222 § 3 pkt 5: the words of DU/2011/322 art. 65 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 222¹ § 3 pkt 1: the words of DU/2003/2081 art. 1 pkt 56 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 222¹ § 3 pkt 2: the words of DU/2003/2081 art. 1 pkt 56 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 222¹ § 3 pkt 3: the words of DU/2003/2081 art. 1 pkt 56 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 226 pkt 1: the words of DU/2003/2081 art. 1 pkt 57 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 227 § 2 pkt 1: the words of DU/2003/2081 art. 1 pkt 58 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 227 § 2 pkt 2: the words of DU/2003/2081 art. 1 pkt 58 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 227 § 2 pkt 3: the words of DU/2003/2081 art. 1 pkt 58 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 227 § 2 pkt 4: the words of DU/2003/2081 art. 1 pkt 58 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 229 § 1 pkt 1: the words of DU/2002/1146 art. 1 pkt 45 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 229 § 1 część wspólna: the words of DU/2002/1146 art. 1 pkt 45 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 235 § 3 pkt 1: the words of DU/2009/825 art. 1 pkt 2 lit. d differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 237 § 4 pkt 1: the words of DU/2000/1268 art. 17 pkt 4 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 237¹ § 1: the change by DU/2002/1673 before DU/2009/825 is not reconstructed (no quoted wording)
- kodeks-pracy art. 237¹¹a § 1 pkt 1: the words of DU/2011/322 art. 65 pkt 4 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 237¹¹a § 1 pkt 3: the words of DU/2009/958 art. 1 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 238 § 1 pkt 1: the words of DU/2000/1127 art. 1 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 239 § 3 pkt 1: the words of DU/2000/1127 art. 1 pkt 2 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 239 § 3 pkt 2: the words of DU/2000/1127 art. 1 pkt 2 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 239 § 3 pkt 3 lit. e: the words of DU/2000/1127 art. 1 pkt 2 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 241¹⁴ § 1: the words of DU/2000/1127 art. 1 pkt 10 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 241¹⁴ § 1 pkt 1: the words of DU/2000/1127 art. 1 pkt 10 lit. a differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 241¹⁴a § 2: the words of DU/2000/1127 art. 1 pkt 11 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 241¹⁵ pkt 1: the words of DU/2000/1127 art. 1 pkt 12 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 241¹⁸ § 1: the words of DU/2008/586 art. 1 pkt 1 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 241²³: the words of DU/2000/1127 art. 1 pkt 18 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 241²⁵a § 1 pkt 1: the words of DU/2000/1127 art. 1 pkt 20 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 281: the words of DU/2007/589 art. 95 pkt 6 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 282 § 1 część wspólna: the words of DU/2007/589 art. 95 pkt 7 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 283 § 1: the words of DU/2007/589 art. 95 pkt 8 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 283 § 2 pkt 2: the words of DU/2011/1378 art. 1 pkt 3 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 283 § 2 pkt 3: the words of DU/2007/589 art. 95 pkt 8 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 283 § 2 pkt 4: the words of DU/2007/589 art. 95 pkt 8 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 283 § 2 pkt 5 lit. c: the words of DU/2011/322 art. 65 pkt 5 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 283 § 2 pkt 6: the words of DU/2007/589 art. 95 pkt 8 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 283 § 2 pkt 7: the words of DU/2007/589 art. 95 pkt 8 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 283 § 2 pkt 8: the words of DU/2007/589 art. 95 pkt 8 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 298³: the change by DU/2001/1405 before DU/2003/1608 is not reconstructed (no quoted wording)
- kodeks-pracy art. 304 § 3 pkt 1: the words of DU/2007/589 art. 95 pkt 9 lit. b differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 304⁵ § 3 pkt 1: the words of DU/2003/2081 art. 1 pkt 72 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 304⁵ § 4 pkt 1: the words of DU/2003/2081 art. 1 pkt 72 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 304⁵ § 4 pkt 2: the words of DU/2003/2081 art. 1 pkt 72 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 304⁵ § 4 pkt 3: the words of DU/2003/2081 art. 1 pkt 72 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 304⁵ § 5 pkt 1: the words of DU/2003/2081 art. 1 pkt 72 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 304⁵ § 5 pkt 2: the words of DU/2003/2081 art. 1 pkt 72 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 304⁵ § 5 pkt 3: the words of DU/2003/2081 art. 1 pkt 72 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 304⁵ § 5 pkt 4: the words of DU/2003/2081 art. 1 pkt 72 differ from DU/2014/1502; the unified text is used
- kodeks-pracy art. 304⁵ § 5 pkt 5: the words of DU/2003/2081 art. 1 pkt 72 differ from DU/2014/1502; the unified text is used
- kodeks-pracy DU/2014/1502: 889 lines changed with no footnote
- kodeks-pracy DU/1975/91 (in force 1975-06-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1981/23 (in force 1981-03-14): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1982/214 (in force 1983-01-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1985/162 (in force 1985-08-10): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1986/201 (in force 1987-01-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1987/124 (in force 1988-01-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1988/134 (in force 1988-07-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1989/192 (in force 1989-07-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1990/19 (in force 1990-01-27): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1990/251 (in force 1990-07-03): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1990/319 (in force 1990-08-18): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1991/226 (in force 1991-07-04): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1991/236 (in force 1991-07-27): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1991/237 (in force 1991-06-26): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1996/396 (in force 1996-08-07): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1997/770 (in force 1997-10-22): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1998/668 (in force 1999-01-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1998/717 (in force 1998-09-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/1999/1152 (in force 2000-01-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2001/1075 (in force 2001-05-26): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2001/1354 (in force 2003-01-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2001/538 (in force 2001-05-26): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2002/1660 (in force 2002-11-26): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2002/676 (in force 2002-06-29): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2004/374 (in force 2004-03-12): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2004/959 (in force 2004-05-01): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2006/708 (in force 2006-07-24): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2007/1288 (in force 2007-10-16): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2007/1672 (in force 2007-12-03): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2008/740 (in force 2009-07-03): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2009/485 (in force 2010-04-11): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy DU/2010/912 (in force 2010-07-26): listed by the API, but no unit of DU/2014/1502 is credited to it
- kodeks-pracy art. 29 § 1¹: the words of DU/2015/1220 art. 1 pkt 2 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 36²: the words of DU/2015/1220 art. 1 pkt 8 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 59: the words of DU/2015/1220 art. 1 pkt 12 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 179¹ § 2: the words of DU/2015/1268 art. 1 pkt 2 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 180 § 10: the words of DU/2015/1268 art. 1 pkt 4 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 180 § 7: the words of DU/2015/1268 art. 1 pkt 4 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182: DU/2015/1268 in force 2016-03-01 (footnote, used) but 2016-01-02 (API)
- kodeks-pracy art. 182: the words of DU/2015/1268 art. 1 pkt 6 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182¹b: DU/2015/1066 in force 2015-08-14 (footnote, used) but 2016-01-01 (API)
- kodeks-pracy art. 182¹b: the change by DU/2015/1066 before DU/2015/1268 is not reconstructed (no quoted wording)
- kodeks-pracy art. 182¹c § 1: the words of DU/2015/1268 art. 1 pkt 9 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182¹c § 2: the words of DU/2015/1268 art. 1 pkt 9 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182¹c § 3: the words of DU/2015/1268 art. 1 pkt 9 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182¹d § 1: the words of DU/2015/1268 art. 1 pkt 9 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182¹d § 2: the words of DU/2015/1268 art. 1 pkt 9 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182¹e § 1: the words of DU/2015/1268 art. 1 pkt 9 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182¹e § 2: the words of DU/2015/1268 art. 1 pkt 9 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182³ § 3: the words of DU/2015/1268 art. 1 pkt 10 lit. d differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 182⁴ § 2: the words of DU/2015/1268 art. 1 pkt 11 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 183 § 2: the words of DU/2015/1268 art. 1 pkt 12 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 183 § 5: the words of DU/2015/1268 art. 1 pkt 12 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 189¹: the words of DU/2015/1268 art. 1 pkt 23 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 229 § 1²: the words of DU/2014/1662 art. 1 pkt 2 differ from DU/2016/1666; the unified text is used
- kodeks-pracy art. 281 pkt 1a: the words of DU/2015/1220 art. 1 pkt 21 differ from DU/2016/1666; the unified text is used
- kodeks-pracy DU/2016/1666: 94 lines changed with no footnote
- kodeks-pracy DU/2015/1066 (in force 2016-01-01): listed by the API, but no unit of DU/2016/1666 is credited to it
- kodeks-pracy DU/2016/868 (in force 2016-06-18): listed by the API, but no unit of DU/2016/1666 is credited to it
- kodeks-pracy art. 191 § 5 pkt 3: the change by DU/2017/60 before DU/2009/458 is not reconstructed (no quoted wording)
- kodeks-pracy art. 191 § 5 pkt 3: DU/2009/458 in force 2018-09-01 (API) but 2009-04-22 (footnote)
- kodeks-pracy art. 191 § 5 pkt 3: the words of DU/2009/458 art. 2 pkt 2 differ from DU/2018/108; the unified text is used
- kodeks-pracy art. 191 § 5 pkt 4: the change by DU/2017/60 before DU/2009/458 is not reconstructed (no quoted wording)
- kodeks-pracy art. 191 § 5 pkt 4: DU/2009/458 in force 2018-09-01 (API) but 2009-04-22 (footnote)
- kodeks-pracy art. 191 § 5 pkt 4: the words of DU/2009/458 art. 2 pkt 2 differ from DU/2018/108; the unified text is used
- kodeks-pracy DU/2018/108: 31 lines changed with no footnote
- kodeks-pracy DU/2009/458: in force 2018-09-01, after the unified text DU/2018/108 of 2018-01-12 that prints it
- kodeks-pracy DU/2018/917: 28 lines changed with no footnote
- kodeks-pracy art. 22¹a § 1: the words of DU/2019/730 art. 4 pkt 2 differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 22² § 1¹: the change by DU/2018/1000 before DU/2019/730 is not reconstructed (no quoted wording)
- kodeks-pracy art. 22³ § 3: the words of DU/2018/1000 art. 111 differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 67⁶ § 6: the words of DU/2018/1076 art. 2 pkt 1 differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 67⁶ § 7: the words of DU/2018/1076 art. 2 pkt 1 differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 142¹ § 1 pkt 1: the words of DU/2018/1076 art. 2 pkt 2 differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 142¹ § 1 pkt 2: the words of DU/2018/1076 art. 2 pkt 2 differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 142¹ § 1 pkt 3: the words of DU/2018/1076 art. 2 pkt 2 differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 142¹ § 1 pkt 3 część wspólna: the words of DU/2018/1076 art. 2 pkt 2 differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 190 § 2: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2¹: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2²: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2³: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2⁴: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2⁴: the words of DU/2018/2245 art. 4 pkt 3 lit. a differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 191 § 2⁵: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2⁶: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2⁶ pkt 1: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2⁶ pkt 2: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2⁷: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191 § 2⁷: the words of DU/2018/2245 art. 4 pkt 3 lit. a differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 191 § 5: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191¹: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 191¹: DU/2018/2245 in force 2018-12-01 (footnote, used) but 2019-09-01 (API)
- kodeks-pracy art. 229 § 1³: the words of DU/2019/730 art. 4 pkt 4 lit. b differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 229 § 7: the words of DU/2019/730 art. 4 pkt 4 lit. c differ from DU/2019/1040; the unified text is used
- kodeks-pracy art. 237³ § 2⁴: the words of DU/2018/2244 art. 2 pkt 1 differ from DU/2019/1040; the unified text is used
- kodeks-pracy DU/2019/1040: 51 lines changed with no footnote
- kodeks-pracy DU/2018/2377 (in force 2018-12-20): listed by the API, but no unit of DU/2019/1040 is credited to it
- kodeks-pracy art. 47: the words of DU/2019/1043 art. 1 pkt 3 differ from DU/2020/1320; the unified text is used
- kodeks-pracy art. 57 § 2: the words of DU/2019/1043 art. 1 pkt 5 differ from DU/2020/1320; the unified text is used
- kodeks-pracy art. 163 § 3: the words of DU/2019/1043 art. 1 pkt 9 differ from DU/2020/1320; the unified text is used
- kodeks-pracy DU/2020/1320: 38 lines changed with no footnote
- kodeks-pracy DU/2018/2245 (in force 2019-09-01): listed by the API, but no unit of DU/2020/1320 is credited to it
- kodeks-pracy art. 155² § 1 pkt 3: DU/2022/655 in force 2022-04-24 (footnote, used) but 2022-04-23 (API)
- kodeks-pracy art. 165 pkt 3: DU/2022/655 in force 2022-04-24 (footnote, used) but 2022-04-23 (API)
- kodeks-pracy art. 166 pkt 3: DU/2022/655 in force 2022-04-24 (footnote, used) but 2022-04-23 (API)
- kodeks-pracy art. 301 § 1: DU/2022/655 in force 2022-04-24 (footnote, used) but 2022-04-23 (API)
- kodeks-pracy art. 304 § 5: DU/2022/655 in force 2022-04-24 (footnote, used) but 2022-04-23 (API)
- kodeks-pracy DU/2022/1510: 32 lines changed with no footnote
- kodeks-pracy DU/2018/2432 (in force 2020-12-01): listed by the API, but no unit of DU/2022/1510 is credited to it
- kodeks-pracy art. 26¹ § 2 pkt 1: the words of DU/2023/641 art. 1 pkt 5 differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 29¹ § 5¹: the words of DU/2023/641 art. 1 pkt 7 lit. d differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 29¹ § 6: the words of DU/2023/641 art. 1 pkt 7 lit. e differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 29⁴ § 1 pkt 1: the words of DU/2023/641 art. 1 pkt 9 differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 29⁴ § 1 pkt 2: the words of DU/2023/641 art. 1 pkt 9 differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 29⁴ § 1 pkt 3: the words of DU/2023/641 art. 1 pkt 9 differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 29⁴ § 3: the words of DU/2023/641 art. 1 pkt 9 differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 94 pkt 1a: the words of DU/2023/641 art. 1 pkt 17 differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 177 § 1¹: the words of DU/2023/641 art. 1 pkt 23 lit. b differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 183 § 3: the words of DU/2022/2140 art. 4 pkt 3 lit. c differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 183 § 4¹ pkt 1: the words of DU/2023/641 art. 1 pkt 35 lit. b differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 183 § 4¹ pkt 2: the words of DU/2023/641 art. 1 pkt 35 lit. b differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 183 § 4³ pkt 1: the change by DU/2022/2140 before DU/2023/641 is not reconstructed (no quoted wording)
- kodeks-pracy art. 183 § 4³ pkt 2: the change by DU/2022/2140 before DU/2023/641 is not reconstructed (no quoted wording)
- kodeks-pracy art. 183 § 4³ pkt 3: the change by DU/2022/2140 before DU/2023/641 is not reconstructed (no quoted wording)
- kodeks-pracy art. 183 § 4⁴ pkt 1: the words of DU/2023/641 art. 1 pkt 35 lit. c differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 183 § 4⁴ pkt 2: the words of DU/2023/641 art. 1 pkt 35 lit. c differ from DU/2023/1465; the unified text is used
- kodeks-pracy art. 281 § 1 pkt 5c: the words of DU/2023/641 art. 1 pkt 43 lit. b differ from DU/2023/1465; the unified text is used
- kodeks-pracy DU/2023/1465: 231 lines changed with no footnote
- kodeks-pracy DU/2024/1222 (in force 2024-11-10): after the last unified text; not in the record
- kodeks-pracy DU/2024/1871 (in force 2025-03-19): after the last unified text; not in the record
- kodeks-pracy DU/2024/1965 (in force 2025-02-01): after the last unified text; not in the record
- kodeks-pracy DU/2024/878 (in force 2024-06-29): after the last unified text; not in the record
- kodeks-pracy DU/2025/1423 (in force 2026-01-01): after the last unified text; not in the record
- kodeks-pracy DU/2025/1661 (in force 2025-12-13): after the last unified text; not in the record
- kodeks-pracy DU/2025/807 (in force 2025-12-24): after the last unified text; not in the record
- kodeks-pracy DU/2026/1046 (in force 2026-11-05): after the last unified text; not in the record
- kodeks-pracy DU/2026/25 (in force 2026-01-27): after the last unified text; not in the record
- kodeks-pracy DU/2026/473 (in force 2026-07-08): after the last unified text; not in the record
- kodeks-pracy DU/2018/108: 2 lines differ from the unified text for no reason found: art. 191 § 5 pkt 3, art. 191 § 5 pkt 4
- kodeks-postepowania-cywilnego art. 1: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 1: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 2 § 2: DU/1989/175 in force 1989-10-01 (footnote, used) but 1989-06-02 (API)
- kodeks-postepowania-cywilnego art. 2 § 3: DU/1989/175 in force 1989-10-01 (footnote, used) but 1989-06-02 (API)
- kodeks-postepowania-cywilnego art. 9 § 2: the change by DU/2005/1398 before DU/2010/684 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 16 § 2: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 16: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 17 pkt 1: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 1: the words of DU/2008/1431 art. 3 pkt 1 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 17 pkt 2: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 2: the words of DU/2004/1804 art. 1 pkt 6 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 17 pkt 3: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 3: the words of DU/1990/306 art. 3 pkt 2 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 17 pkt 4: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 4: the words of DU/2011/1381 art. 1 pkt 5 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 17 pkt 4¹: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 4¹: the change by DU/1990/306 before DU/2005/1024 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 17 pkt 4¹: the words of DU/2005/1024 art. 2 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 17 pkt 4²: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 4²: the change by DU/1990/306 before DU/2006/1699 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 17 pkt 4²: the words of DU/2006/1699 art. 1 pkt 1 lit. b differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 17 pkt 4³: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 4³: the change by DU/1990/306 before DU/2006/1699 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 17 pkt 4³: the words of DU/2006/1699 art. 1 pkt 1 lit. b differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 17 pkt 4⁴: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 4⁴: the change by DU/1990/306 before DU/2010/1037 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 17 pkt 4⁴: the words of DU/2010/1037 art. 2 pkt 1 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 17 pkt 5: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 6: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 17 pkt 6: the change by DU/1990/306 before DU/2002/2058 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 17: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 18 § 1: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 18 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 18 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 18 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 18 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 67 § 3: DU/2005/98 in force 2005-01-21 (footnote, used) but 2005-02-06 (API)
- kodeks-postepowania-cywilnego art. 72 § 3: the words of DU/1990/318 art. 1 pkt 10 lit. b differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 87 § 2: the change by DU/1997/270 before DU/2000/554 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 87 § 2: the change by DU/1997/770 before DU/2000/554 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 87 § 4: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 87 § 4: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 87 § 5: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 87 § 5: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 87¹ § 3: the change by DU/2004/1804 before DU/2005/1417 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 109 § 2: the change by DU/2004/1804 before DU/2005/1398 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 117³ § 1: the words of DU/2010/45 art. 1 pkt 3 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 118 § 6: the words of DU/2010/45 art. 1 pkt 4 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 125 § 2: DU/2000/554 in force 2000-10-01 (footnote, used) but 2000-07-01 (API)
- kodeks-postepowania-cywilnego art. 125 § 3: DU/2000/554 in force 2000-10-01 (footnote, used) but 2000-07-01 (API)
- kodeks-postepowania-cywilnego art. 125 § 4: DU/2000/554 in force 2000-10-01 (footnote, used) but 2000-07-01 (API)
- kodeks-postepowania-cywilnego art. 126 § 6: DU/2009/156 in force 2009-02-17 (footnote, used) but 2010-01-01 (API)
- kodeks-postepowania-cywilnego art. 130 § 1¹: the words of DU/2005/1398 art. 126 pkt 11 lit. b differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 130¹: DU/2000/554 in force 2000-10-01 (footnote, used) but 2000-07-01 (API)
- kodeks-postepowania-cywilnego art. 130¹ § 1: DU/2000/554 in force 2000-10-01 (footnote, used) but 2000-07-01 (API)
- kodeks-postepowania-cywilnego art. 130¹ § 1: the words of DU/2000/554 art. 1 pkt 7 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 130¹ § 1¹: DU/2000/554 in force 2000-10-01 (footnote, used) but 2000-07-01 (API)
- kodeks-postepowania-cywilnego art. 130¹ § 1¹: the change by DU/2000/554 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 130¹ § 2: DU/2000/554 in force 2000-10-01 (footnote, used) but 2000-07-01 (API)
- kodeks-postepowania-cywilnego art. 130¹ § 3: DU/2000/554 in force 2000-10-01 (footnote, used) but 2000-07-01 (API)
- kodeks-postepowania-cywilnego art. 130¹ § 4: DU/2000/554 in force 2000-10-01 (footnote, used) but 2000-07-01 (API)
- kodeks-postepowania-cywilnego art. 130³ § 1: the words of DU/2005/1398 art. 126 pkt 12 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 130³ § 2: the words of DU/2005/1398 art. 126 pkt 12 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 144 § 4: the words of DU/2010/45 art. 1 pkt 15 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 174 § 1 pkt 4: the words of DU/2011/1381 art. 1 pkt 20 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 177 § 1 pkt 3: the words of DU/2004/1804 art. 1 pkt 25 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 182¹: the change by DU/2006/1699 before DU/2011/1381 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 183¹² § 2¹: DU/2011/1381 in force 2011-11-17 (footnote, used) but 2012-05-03 (API)
- kodeks-postepowania-cywilnego art. 187¹: the words of DU/2000/554 art. 1 pkt 10 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 193 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 204 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 205: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 206 § 2 pkt 1: the words of DU/2006/466 art. 1 pkt 1 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 206 § 2 pkt 2: the words of DU/2006/466 art. 1 pkt 1 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 232: the words of DU/1996/189 art. 1 pkt 35 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 316 § 1: the words of DU/1996/189 art. 1 pkt 36 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 331: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 331: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 331: the words of DU/1985/86 art. 1 pkt 13 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 333 § 2: DU/1990/318 in force 2001-01-04 (footnote, used) but 1990-10-01 (API)
- kodeks-postepowania-cywilnego art. 353¹: DU/2005/98 in force 2005-02-22 (footnote, used) but 2005-02-06 (API)
- kodeks-postepowania-cywilnego art. 353¹ § 1: DU/2005/98 in force 2005-02-22 (footnote, used) but 2005-02-06 (API)
- kodeks-postepowania-cywilnego art. 353¹ § 2: DU/2005/98 in force 2005-02-22 (footnote, used) but 2005-02-06 (API)
- kodeks-postepowania-cywilnego art. 357 § 1: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 357 § 1: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 367 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 368 § 1 pkt 1: the words of DU/2000/554 art. 1 pkt 17 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 368 § 1 pkt 2: the words of DU/2000/554 art. 1 pkt 17 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 368 § 1 pkt 3: the words of DU/2000/554 art. 1 pkt 17 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 368 § 1 pkt 4: the words of DU/2000/554 art. 1 pkt 17 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 394 § 1 pkt 10¹: the words of DU/2005/1438 art. 1 pkt 11 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 394 § 1 pkt 4²: the words of DU/2006/1699 art. 1 pkt 13 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 394 § 1 pkt 5: the words of DU/2006/1699 art. 1 pkt 13 lit. b differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 394¹ § 1¹: the change by DU/2005/98 before DU/2011/1381 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 397 § 1¹: the change by DU/1996/189 before DU/2000/554 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 397¹ § 2: the words of DU/2009/156 art. 1 pkt 11 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 398⁴ § 1 pkt 1: the words of DU/2009/593 art. 1 pkt 1 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 398⁴ § 1 pkt 2: the words of DU/2009/593 art. 1 pkt 1 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 401¹: the change by DU/1997/643 before DU/2005/98 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 407 § 1: the change by DU/1996/189 before DU/2005/98 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 416 § 1: the change by DU/2006/1656 before DU/2008/609 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 416 § 1: DU/2008/609 in force 2008-07-06 (footnote, used) but 2008-06-20 (API)
- kodeks-postepowania-cywilnego art. 424⁵ § 1 pkt 1: the words of DU/2010/1037 art. 2 pkt 7 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 424⁵ § 1 pkt 2: the words of DU/2010/1037 art. 2 pkt 7 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 424⁵ § 1 pkt 3: the words of DU/2010/1037 art. 2 pkt 7 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 424⁵ § 1 pkt 4: the words of DU/2010/1037 art. 2 pkt 7 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 424⁵ § 1 pkt 5: the words of DU/2010/1037 art. 2 pkt 7 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 454¹: DU/2004/1691 in force 2004-07-19 (footnote, used) but 2005-01-20 (API)
- kodeks-postepowania-cywilnego art. 454¹ § 1: DU/2004/1691 in force 2004-07-19 (footnote, used) but 2005-01-20 (API)
- kodeks-postepowania-cywilnego art. 454¹ § 2: DU/2004/1691 in force 2004-07-19 (footnote, used) but 2005-01-20 (API)
- kodeks-postepowania-cywilnego art. 454¹ § 3: DU/2004/1691 in force 2004-07-19 (footnote, used) but 2005-01-20 (API)
- kodeks-postepowania-cywilnego art. 467 § 4: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 467 § 4 pkt 1: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 467 § 4 pkt 1: the words of DU/1990/306 art. 3 pkt 5 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 467 § 4 pkt 2: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 467 § 4 pkt 2: the words of DU/1990/306 art. 3 pkt 5 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 467 § 4 pkt 3: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 473 § 2: DU/2004/1264 in force 2005-01-01 (footnote, used) but 2004-07-01 (API)
- kodeks-postepowania-cywilnego art. 476 § 1 pkt 1¹: the words of DU/1996/110 art. 29 pkt 5 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 476 § 4 pkt 1: the change by DU/1991/24 before DU/2004/1264 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 476 § 4 pkt 1: DU/2004/1264 in force 2005-01-01 (footnote, used) but 2004-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁸ § 2 pkt 1: the words of DU/2003/2255 art. 34 pkt 2 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 477⁸ § 2 pkt 2: the words of DU/2001/1070 art. 180 pkt 2 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 477⁸ § 2 pkt 3: the words of DU/2006/711 art. 6 pkt 2 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 477⁸ § 2 pkt 4: the words of DU/2003/2255 art. 34 pkt 2 lit. b differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 477⁹ § 2¹: DU/2004/1264 in force 2005-01-01 (footnote, used) but 2004-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 3¹: DU/2004/1264 in force 2005-01-01 (footnote, used) but 2004-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 3²: DU/2004/1264 in force 2005-01-01 (footnote, used) but 2004-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁴ § 4: DU/2004/1264 in force 2005-01-01 (footnote, used) but 2004-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁴a: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 477¹⁴a: DU/1990/306 in force 1991-01-01 (footnote, used) but 1990-08-10 (API)
- kodeks-postepowania-cywilnego art. 477¹⁶: DU/2004/1264 in force 2005-01-01 (footnote, used) but 2004-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁶: DU/2004/1264 in force 2005-01-01 (footnote, used) but 2004-07-01 (API)
- kodeks-postepowania-cywilnego art. 479²⁸ § 1 pkt 2: the change by DU/2002/1102 before DU/2007/331 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 479²⁸ § 1 pkt 2: the words of DU/2007/331 art. 115 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 479³¹: the change by DU/2002/1102 before DU/2002/764 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 479³¹ § 1: the change by DU/2002/1102 before DU/2002/764 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 479³¹ § 2: the change by DU/2002/1102 before DU/2002/764 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 479³¹ § 3: the change by DU/2002/1102 before DU/2002/764 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 479³¹a § 3: the words of DU/2004/1804 art. 1 pkt 73 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 479³² § 2: the words of DU/2004/1804 art. 1 pkt 74 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁵⁷ pkt 1: the words of DU/2005/2258 art. 5 pkt 1 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁶⁸ pkt 2: footnote names DU/2007/94, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 479⁶⁸ pkt 2: no in-force day for DU/2007/94; not credited
- kodeks-postepowania-cywilnego art. 485 § 1 pkt 1: the words of DU/2000/554 art. 1 pkt 50 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 485 § 1 pkt 2: the words of DU/2000/554 art. 1 pkt 50 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 485 § 1 pkt 3: the words of DU/2000/554 art. 1 pkt 50 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 485 § 1 pkt 4: the words of DU/2000/554 art. 1 pkt 50 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 485 § 2: the words of DU/2000/554 art. 1 pkt 50 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 485 § 2a: the change by DU/2000/554 before DU/2013/403 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 485 § 4: the words of DU/2009/1676 art. 2 pkt 2 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 491 § 2: the words of DU/2000/554 art. 1 pkt 54 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 492 § 3: the words of DU/2000/554 art. 1 pkt 54 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 497¹ § 3: the change by DU/2000/554 before DU/2006/1699 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 498 § 1: DU/2005/98 in force 2005-02-22 (footnote, used) but 2005-02-06 (API)
- kodeks-postepowania-cywilnego art. 502 § 1: DU/2005/98 in force 2005-02-22 (footnote, used) but 2005-02-06 (API)
- kodeks-postepowania-cywilnego art. 505 § 3: the change by DU/2000/554 before DU/2013/654 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 505¹ pkt 1: the words of DU/2004/1804 art. 1 pkt 90 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 505⁹ § 1¹ pkt 1: the words of DU/2005/98 art. 1 pkt 34 lit. b differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 505¹² § 1: the words of DU/2005/98 art. 1 pkt 35 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 507: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 519¹ § 4: the change by DU/1996/189 before DU/2005/98 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 1: the change by DU/1996/189 before DU/2005/98 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 1: the words of DU/2005/98 art. 1 pkt 36 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 2: the change by DU/1996/189 before DU/2005/98 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 2: the words of DU/2005/98 art. 1 pkt 36 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 3: the change by DU/1996/189 before DU/2005/98 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 3: the words of DU/2005/98 art. 1 pkt 36 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 4: the change by DU/1996/189 before DU/2005/98 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 4: the words of DU/2005/98 art. 1 pkt 36 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 5: the change by DU/1996/189 before DU/2006/1537 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 519¹ § 4 pkt 5: the change by DU/2005/98 before DU/2006/1537 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 561 § 1: the words of DU/1998/757 art. 2 pkt 1 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 564 pkt 5: the words of DU/1998/757 art. 2 pkt 2 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 565 § 3: the words of DU/1975/234 art. 2 pkt 4 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 570¹ § 1: the change by DU/2001/1071 before DU/2011/887 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 570¹ § 2: the change by DU/2001/1071 before DU/2011/887 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 570¹ § 3: the change by DU/2001/1071 before DU/2011/887 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 578¹ § 1: the change by DU/2004/1804 before DU/2011/854 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 578¹ § 2: the change by DU/2004/1804 before DU/2011/854 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 578¹ § 3: the change by DU/2004/1804 before DU/2011/854 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 579¹ § 1: the change by DU/2000/1322 before DU/2011/887 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 579¹ § 2: the change by DU/2000/1322 before DU/2011/887 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 579¹ § 3: the change by DU/2000/1322 before DU/2011/887 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 582¹ § 2 pkt 1: the words of DU/2008/1431 art. 3 pkt 22 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 582¹ § 2 pkt 2: the words of DU/2011/887 art. 202 pkt 5 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 582¹ § 3: the change by DU/2008/1431 before DU/2011/854 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 626² § 3: the words of DU/2009/156 art. 1 pkt 14 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 626⁸ § 2¹: the change by DU/2003/363 before DU/2009/156 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 626¹¹ § 2: the change by DU/2005/98 before DU/2005/98 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 626¹¹ § 2: the change by DU/2005/98 before DU/2005/98 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 637 § 1: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 637 § 1: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 655 § 1: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 655 § 1: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 655 § 1 pkt 1: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 655 § 1 pkt 1: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 655 § 1 pkt 2: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 655 § 1 pkt 2: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 683: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 691¹: DU/1989/175 in force 1989-10-01 (footnote, used) but 1989-06-02 (API)
- kodeks-postepowania-cywilnego art. 691¹ § 1: DU/1989/175 in force 1989-10-01 (footnote, used) but 1989-06-02 (API)
- kodeks-postepowania-cywilnego art. 691¹ § 1 pkt 1: DU/1989/175 in force 1989-10-01 (footnote, used) but 1989-06-02 (API)
- kodeks-postepowania-cywilnego art. 691¹ § 1 pkt 1: the words of DU/1989/175 art. 6 pkt 4 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 691¹ § 1 pkt 2: DU/1989/175 in force 1989-10-01 (footnote, used) but 1989-06-02 (API)
- kodeks-postepowania-cywilnego art. 691¹ § 1 pkt 2: the words of DU/1989/175 art. 6 pkt 4 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 691¹ § 1 pkt 3: DU/1989/175 in force 1989-10-01 (footnote, used) but 1989-06-02 (API)
- kodeks-postepowania-cywilnego art. 691¹ § 2: DU/1989/175 in force 1989-10-01 (footnote, used) but 1989-06-02 (API)
- kodeks-postepowania-cywilnego art. 734: the words of DU/2008/1571 art. 1 pkt 14 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 752¹ § 2: the change by DU/2005/1538 before DU/2011/1391 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 765 § 2 pkt 1: the words of DU/2000/554 art. 1 pkt 66 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 765 § 2 pkt 2: the words of DU/2006/711 art. 6 pkt 3 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 767 § 1: the words of DU/2004/1804 art. 1 pkt 108 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 767¹: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 767¹: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 767¹: the change by DU/1985/86 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 767⁴ § 3: the change by DU/2004/1804 before DU/2010/1037 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 773 § 1: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 773 § 1: the words of DU/2011/1381 art. 1 pkt 78 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 773 § 1¹: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 773 § 1¹: the change by DU/2001/1368 before DU/2011/1381 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 773 § 2: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 773 § 2¹: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 773 § 2¹: the change by DU/2001/1368 before DU/2009/156 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 773 § 2¹a: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 773 § 2¹a: the change by DU/2001/1368 before DU/2013/1289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 773 § 2²: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 773 § 2²: the change by DU/2001/1368 before DU/2011/1381 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 773 § 3: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 773 § 4: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 773¹ § 3: the change by DU/1997/882 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 773¹ § 4: the change by DU/1997/882 before DU/2007/769 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 773¹ § 4: the change by DU/2004/1804 before DU/2007/769 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 775¹: the change by DU/1996/189 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 777 § 1 pkt 1¹: the words of DU/2005/1398 art. 126 pkt 29 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 777 § 1 pkt 6: the change by DU/2004/1804 before DU/2011/1381 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 781 § 2: the change by DU/2002/1271 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 781 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 781 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 782 § 1: DU/2005/98 in force 2005-02-22 (footnote, used) but 2005-02-06 (API)
- kodeks-postepowania-cywilnego art. 782 § 2: DU/2005/98 in force 2005-02-22 (footnote, used) but 2005-02-06 (API)
- kodeks-postepowania-cywilnego art. 783 § 4: the change by DU/2004/1804 before DU/2009/156 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 783 § 5: the change by DU/2004/1804 before DU/2009/156 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 783 § 5: DU/2009/156 in force 2009-02-17 (footnote, used) but 2010-01-01 (API)
- kodeks-postepowania-cywilnego art. 786 § 2: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 786 § 2: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 795³ § 2: DU/2008/1571 in force 2008-12-12 (footnote, used) but 2009-07-01 (API)
- kodeks-postepowania-cywilnego art. 808 § 2: the change by DU/2004/1804 before DU/2011/1381 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 811 § 2 pkt 1: the words of DU/2006/711 art. 6 pkt 4 lit. b differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 811 § 2 pkt 2: the words of DU/2000/554 art. 1 pkt 67 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 814 § 3: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 814 § 3: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 814 § 3: the words of DU/1985/86 art. 1 pkt 31 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 820¹ § 3: the change by DU/2006/466 before DU/2011/735 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 829 pkt 8: the words of DU/2011/654 art. 124 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 831 § 1 pkt 5: the words of DU/1984/242 art. 72 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 831 § 1 pkt 7: the words of DU/2010/45 art. 1 pkt 40 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 833 § 1¹: the change by DU/1983/33 before DU/2007/1243 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 844 § 3: the change by DU/1997/882 before DU/2004/2356 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 865 § 1: the words of DU/1997/882 art. 95 pkt 7 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 867 § 4: the words of DU/1996/189 art. 1 pkt 95 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 881 § 3 pkt 1: the change by DU/1974/157 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 887 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 887 § 2: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 889 § 1: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 889 § 1 pkt 1: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 889 § 1 pkt 1: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 889 § 1 pkt 1: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 889 § 1 pkt 1: the change by DU/1991/92 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 889 § 1 pkt 2: the change by DU/1990/318 before DU/2009/156 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 889 § 1 pkt 2: the change by DU/1991/92 before DU/2009/156 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 890 § 1: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 890 § 1: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 890 § 1: the change by DU/1991/92 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 891: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 891: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 891: the change by DU/1991/92 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 892 § 1: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 892 § 2: the change by DU/1990/318 before DU/1991/92 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 893¹ § 5: the change by DU/1990/318 before DU/2012/1529 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 897 § 4: the change by DU/1997/769 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 910⁴ § 1: the words of DU/2004/1804 art. 1 pkt 159 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 911⁶ § 2: the words of DU/2004/1804 art. 1 pkt 160 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 911⁶ § 4: the change by DU/2004/1804 before DU/2011/1381 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 911⁷ § 4: the change by DU/2004/1804 before DU/2011/1381 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 911⁸ § 6: the change by DU/2004/1804 before DU/2011/1391 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 911⁸ § 6: the change by DU/2005/1538 before DU/2011/1391 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 913 § 1: the words of DU/2004/1804 art. 1 pkt 161 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 915 § 1: footnote names DU/2000/665, not among the API's amending acts
- kodeks-postepowania-cywilnego art. 915 § 1: no in-force day for DU/2000/665; not credited
- kodeks-postepowania-cywilnego art. 921 § 1: the words of DU/2004/1804 art. 1 pkt 166 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 926 § 1: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 926 § 1: the change by DU/2004/1804 before DU/2004/1804 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 978 § 2: DU/1996/189 in force 1996-04-30 (footnote, used) but 1996-07-01 (API)
- kodeks-postepowania-cywilnego art. 982 § 3: the words of DU/1991/496 art. 4 pkt 1 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 1008: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 10: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 2: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 2: the words of DU/2001/1368 art. 2 pkt 4 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 3: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 3: the words of DU/2001/1368 art. 2 pkt 4 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 4: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 5: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 6: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 6: the words of DU/2001/1368 art. 2 pkt 4 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 7: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 7: the words of DU/2001/1368 art. 2 pkt 4 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 8: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 9: DU/2001/1368 in force 2001-11-30 (footnote, used) but 2001-12-01 (API)
- kodeks-postepowania-cywilnego art. 1025 § 1 pkt 9: the words of DU/2001/1368 art. 2 pkt 4 lit. a differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 1036 § 1 pkt 1: the words of DU/2009/1075 art. 3 pkt 4 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 1036 § 1 pkt 2: the words of DU/2009/1075 art. 3 pkt 4 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 1036 § 1 pkt 3: the words of DU/2009/1075 art. 3 pkt 4 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego art. 1109¹ § 2: the words of DU/2008/1571 art. 1 pkt 34 differ from DU/2014/101; the unified text is used
- kodeks-postepowania-cywilnego DU/2014/101: 1117 lines changed with no footnote
- kodeks-postepowania-cywilnego DU/1974/231 (in force 1975-01-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1987/123 (in force 1988-01-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1988/324 (in force 1989-01-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1989/21 (in force 1989-02-10): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1990/464 (in force 1990-12-05): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1990/88 (in force 1990-04-11): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1993/53 (in force 1993-03-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1994/509 (in force 1994-11-12): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1997/270 (in force 1997-05-15): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1997/348 (in force 1997-12-05): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1997/770 (in force 1997-10-22): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1997/934 (in force 1999-01-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/1997/940 (in force 1998-01-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2000/1191 (in force 2001-01-04): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2000/1193 (in force 2001-01-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2000/1314 (in force 2001-01-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2000/1319 (in force 2001-04-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2000/269 (in force 2000-06-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2000/271 (in force 2000-07-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2000/552 (in force 2000-07-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2000/852 (in force 2001-01-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2001/1546 (in force 2002-06-05): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2002/1070 (in force 2002-09-09): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2002/1849 (in force 2002-12-18): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2002/253 (in force 2002-04-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2002/265 (in force 2002-03-25): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2003/1035 (in force 2003-06-27): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2003/1036 (in force 2003-06-27): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2003/1121 (in force 2004-06-30): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2003/1939 (in force 2004-01-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2003/201 (in force 2003-02-13): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2003/360 (in force 2003-03-25): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2003/535 (in force 2003-10-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2004/2091 (in force 2004-09-07): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2004/2384 (in force 2005-11-03): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2004/75 (in force 2005-07-13): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2004/891 (in force 2004-05-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2005/1413 (in force 2005-10-07): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2005/185 (in force 2005-02-09): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2006/1379 (in force 2006-10-13): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2006/1656 (in force 2006-12-11): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2007/319 (in force 2007-03-16): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2007/418 (in force 2007-04-06): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2007/58 (in force 2007-01-17): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2007/662 (in force 2007-06-20): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2007/731 (in force 2007-06-15): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2008/1056 (in force 2008-10-08): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2008/367 (in force 2008-04-09): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2008/706 (in force 2008-06-26): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2008/772 (in force 2008-07-07): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2008/796 (in force 2008-07-10): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2009/1395 (in force 2009-10-28): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2009/571 (in force 2009-05-05): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2009/592 (in force 2009-05-22): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2010/1018 (in force 2010-09-04): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2010/1418 (in force 2011-11-17): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2010/1435 (in force 2012-02-20): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2010/724 (in force 2010-06-22): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2010/842 (in force 2010-08-01): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2011/173 (in force 2011-05-17): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2011/482 (in force 2011-05-11): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2012/1254 (in force 2012-11-15): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego DU/2013/142 (in force 2013-01-30): listed by the API, but no unit of DU/2014/101 is credited to it
- kodeks-postepowania-cywilnego art. 9 § 1: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 9 § 2: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 9 § 3: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 87 § 1: the words of DU/2015/978 art. 402 pkt 1 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 131¹ § 2¹: the change by DU/2015/218 before DU/2015/1311 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 158 § 1¹: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 158 § 1¹: the change by DU/2014/1296 before DU/2015/1311 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 158 § 2: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 158 § 4: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 158 § 5 pkt 4: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 185 § 3: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 223 § 1: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 324 § 1: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 324 § 2: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 326 § 3: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 328 § 1: the words of DU/2015/1311 art. 2 pkt 34 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 328 § 1¹: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 329: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 331 § 1: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 331 § 1¹: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 331 § 1¹: the change by DU/2014/1296 before DU/2015/1311 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 331 § 2: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 369 § 2: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 377: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 387 § 1: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 387 § 2: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 387 § 2¹: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 387 § 3: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 460 § 1: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 461 § 2²: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 465 § 1¹: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 476 § 2 pkt 1: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 476 § 3: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 476 § 4 pkt 2: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 476 § 5 pkt 2 lit. a: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁸ § 2 pkt 1: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁸ § 2 pkt 3: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁸ § 2 pkt 6: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 1: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 2: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 2¹: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 3¹: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 3³: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 3³: the words of DU/2015/218 art. 1 pkt 9 lit. c differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 477⁹ § 4: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 5: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 6: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁰ § 1: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹¹ § 1: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹¹ § 2: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹¹ § 3: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹³ § 1: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹³ § 2: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁴ § 2: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁴ § 3: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁴ § 4: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁴ § 5: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁴ § 6: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 477¹⁶: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 505¹³ § 1: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 505¹³ § 3: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 505²⁹: the words of DU/2015/1311 art. 2 pkt 46 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 505³¹ § 2¹: DU/2015/1311 in force 2016-07-01 (footnote, used) but 2016-09-08 (API)
- kodeks-postepowania-cywilnego art. 505³⁷ § 1: the words of DU/2015/1311 art. 2 pkt 52 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 505³⁸: the words of DU/2015/1311 art. 2 pkt 53 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 509¹ § 1: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 509¹ § 2: DU/2015/218 in force 2015-03-20 (footnote, used) but 2016-07-01 (API)
- kodeks-postepowania-cywilnego art. 525 pkt 2: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego art. 610³: DU/2015/1311 in force 2015-09-22 (footnote, used) but 2016-09-08 (API)
- kodeks-postepowania-cywilnego art. 626¹² § 1: DU/2015/1311 in force 2015-09-22 (footnote, used) but 2016-09-08 (API)
- kodeks-postepowania-cywilnego art. 638¹ § 1: the words of DU/2015/539 art. 2 pkt 11 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 638¹ § 3: the words of DU/2015/539 art. 2 pkt 11 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 638⁸ § 5: the words of DU/2015/539 art. 2 pkt 11 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 679¹: the words of DU/2015/1311 art. 2 pkt 60 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 756² § 2: the words of DU/2015/1062 art. 2 pkt 4 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 783 § 2: the words of DU/2014/293 art. 1 pkt 2 lit. c differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 783 § 3²: the words of DU/2015/1311 art. 2 pkt 74 lit. a differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 794¹ § 2: the words of DU/2015/1311 art. 2 pkt 75 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 794² § 2: the words of DU/2015/1311 art. 2 pkt 76 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 795 § 2: the words of DU/2014/293 art. 1 pkt 4 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 795 § 3: the words of DU/2015/1311 art. 2 pkt 77 lit. b differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 831 § 1 pkt 8: the words of DU/2015/539 art. 2 pkt 15 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 896 § 1 pkt 2: the words of DU/2014/1626 art. 2 pkt 14 differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 911⁸ § 6: the words of DU/2015/1311 art. 2 pkt 117 lit. b differ from DU/2016/1822; the unified text is used
- kodeks-postepowania-cywilnego art. 1196 § 1: DU/2014/1296 in force 2015-03-27 (footnote, used) but 2014-10-27 (API)
- kodeks-postepowania-cywilnego DU/2016/1822: 220 lines changed with no footnote
- kodeks-postepowania-cywilnego DU/2014/567 (in force 2014-05-15): listed by the API, but no unit of DU/2016/1822 is credited to it
- kodeks-postepowania-cywilnego DU/2015/1634 (in force 2016-04-17): listed by the API, but no unit of DU/2016/1822 is credited to it
- kodeks-postepowania-cywilnego art. 775: the words of DU/2017/768 art. 2 differ from DU/2018/155; the unified text is used
- kodeks-postepowania-cywilnego DU/2018/155: 197 lines changed with no footnote
- kodeks-postepowania-cywilnego DU/2015/1527 (in force 2017-04-03): listed by the API, but no unit of DU/2018/155 is credited to it
- kodeks-postepowania-cywilnego DU/2016/2199 (in force 2016-12-29): listed by the API, but no unit of DU/2018/155 is credited to it
- kodeks-postepowania-cywilnego DU/2017/1727 (in force 2017-09-11): listed by the API, but no unit of DU/2018/155 is credited to it
- kodeks-postepowania-cywilnego DU/2017/1883 (in force 2017-10-10): listed by the API, but no unit of DU/2018/155 is credited to it
- kodeks-postepowania-cywilnego DU/2017/2180 (in force 2017-12-12): listed by the API, but no unit of DU/2018/155 is credited to it
- kodeks-postepowania-cywilnego DU/2017/2245 (in force 2018-01-05): listed by the API, but no unit of DU/2018/155 is credited to it
- kodeks-postepowania-cywilnego art. 163 § 4: DU/2018/138 in force 2018-05-20 (footnote, used) but 2018-02-01 (API)
- kodeks-postepowania-cywilnego art. 477⁸ § 2 pkt 3: the words of DU/2018/730 art. 2 pkt 3 differ from DU/2018/1360; the unified text is used
- kodeks-postepowania-cywilnego art. 761 § 1¹: the words of DU/2018/771 art. 261 pkt 4 lit. b differ from DU/2018/1360; the unified text is used
- kodeks-postepowania-cywilnego art. 814 § 4: the change by DU/2018/138 before DU/2018/730 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 890 § 1³: the words of DU/2017/2491 art. 1 pkt 1 lit. a differ from DU/2018/1360; the unified text is used
- kodeks-postepowania-cywilnego art. 890² § 1: the words of DU/2017/2491 art. 1 pkt 2 differ from DU/2018/1360; the unified text is used
- kodeks-postepowania-cywilnego DU/2018/1360: 125 lines changed with no footnote
- kodeks-postepowania-cywilnego DU/2018/771: in force 2019-01-01, after the unified text DU/2018/1360 of 2018-07-16 that prints it
- kodeks-postepowania-cywilnego DU/2018/1104 (in force 2018-07-09): listed by the API, but no unit of DU/2018/1360 is credited to it
- kodeks-postepowania-cywilnego DU/2019/1460: 137 lines changed with no footnote
- kodeks-postepowania-cywilnego DU/2018/1467 (in force 2019-01-01): listed by the API, but no unit of DU/2019/1460 is credited to it
- kodeks-postepowania-cywilnego DU/2018/1544 (in force 2018-09-11): listed by the API, but no unit of DU/2019/1460 is credited to it
- kodeks-postepowania-cywilnego DU/2018/2385 (in force 2019-01-05): listed by the API, but no unit of DU/2019/1460 is credited to it
- kodeks-postepowania-cywilnego DU/2018/756 (in force 2019-04-21): listed by the API, but no unit of DU/2019/1460 is credited to it
- kodeks-postepowania-cywilnego art. 18 § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 25 § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 44² pkt 2: the words of DU/2019/1469 art. 1 pkt 14 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 52 § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 63³: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 98 § 1²: the words of DU/2019/1469 art. 1 pkt 26 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 110: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 125 § 2¹a: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 133 § 3: the words of DU/2019/1469 art. 1 pkt 43 lit. d differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 139 § 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 139 § 5: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 148 § 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 148¹ § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 169 § 5: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 172: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 178¹: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 178¹: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 182 § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 182 § 1 pkt 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 182 § 1 pkt 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 182 § 1 pkt 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 182 § 1 pkt 4: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 182 § 1 pkt 5: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 182 § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 183: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 183⁵ § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 183⁸ § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 183¹⁴ § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 199 § 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 200 § 1³: the words of DU/2019/1469 art. 1 pkt 67 lit. b differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 210 § 2¹: the words of DU/2019/1469 art. 1 pkt 76 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 240 § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 275: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 344 § 2: the words of DU/2019/1469 art. 1 pkt 116 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 346 § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 350 § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 351 § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 352: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 355: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 364 § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 391¹ § 1: the words of DU/2019/1469 art. 1 pkt 138 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 391¹ § 6: the words of DU/2019/1469 art. 1 pkt 138 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 394¹ § 3: the words of DU/2019/1469 art. 1 pkt 140 lit. b differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 394¹a § 1 pkt 13: the words of DU/2019/1469 art. 1 pkt 141 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 394¹a § 1 pkt 14: the change by DU/2019/1469 before DU/2019/1495 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 394¹a § 1 pkt 15: the change by DU/2019/1469 before DU/2019/1495 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 398² § 5 pkt 2: the words of DU/2019/1469 art. 1 pkt 146 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 410 § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 414: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 424⁶ § 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 424⁶ § 3: the words of DU/2019/1469 art. 1 pkt 153 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 450 § 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 461 § 2²: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 464 § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 477⁹ § 3²: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 477¹¹ § 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 477¹²: DU/2019/1495 in force 2019-09-08 (footnote, used) but 2020-01-01 (API)
- kodeks-postepowania-cywilnego art. 477¹³ § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 479³⁰ § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 479³⁰ § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 479³⁰ § 2: the change by DU/2019/1469 before DU/2019/1495 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 479³⁰a § 1: the words of DU/2019/1495 art. 2 pkt 4 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 479³⁰f: the words of DU/2019/1495 art. 2 pkt 4 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁵²: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 479⁵²a § 1: the words of DU/2019/1495 art. 2 pkt 5 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁵²a § 2: the words of DU/2019/1495 art. 2 pkt 5 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁶³: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 479⁶³a § 2: the words of DU/2019/1495 art. 2 pkt 6 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁷⁴: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 479⁷⁴a § 1: the words of DU/2019/1495 art. 2 pkt 7 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁷⁴a § 2: the words of DU/2019/1495 art. 2 pkt 7 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁷⁷a: the words of DU/2020/462 art. 2 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁸⁵a § 1: the words of DU/2019/1495 art. 2 pkt 8 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 479⁸⁵a § 2: the words of DU/2019/1495 art. 2 pkt 8 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 493 § 2: the words of DU/2019/1469 art. 1 pkt 181 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 505 § 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505¹ § 2 pkt 4: the words of DU/2019/1469 art. 1 pkt 188 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 505⁸ § 4: the words of DU/2019/1469 art. 1 pkt 192 lit. b differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 505¹² § 1¹: the words of DU/2019/1469 art. 1 pkt 195 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 505¹⁴ § 1: the words of DU/2019/1469 art. 1 pkt 196 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 505²⁸ § 2: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505²⁸ § 2 pkt 1: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505²⁸ § 2 pkt 2: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505²⁹ § 1: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505²⁹ § 1: the words of DU/2019/1469 art. 1 pkt 199 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 505²⁹ § 2: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505²⁹ § 3: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505²⁹ § 4: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505²⁹ § 4: the words of DU/2019/1469 art. 1 pkt 199 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 505³² § 4: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505³³: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505³⁴ § 1: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505³⁴ § 2: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505³⁶: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505³⁷ § 1: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505³⁷ § 2: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505³⁸: DU/2019/1469 in force 2020-02-07 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 505³⁸: the words of DU/2019/1469 art. 1 pkt 202 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 508 § 4: the words of DU/2019/1469 art. 1 pkt 203 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 735 § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 782¹: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 782¹ § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 782¹ § 1 pkt 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 782¹ § 1 pkt 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 782¹ § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 788 § 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 797 § 1¹: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 804 § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 804²: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 804² § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 804² § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 804² § 3: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 805 § 1¹: the words of DU/2019/1469 art. 1 pkt 229 differ from DU/2020/1575; the unified text is used
- kodeks-postepowania-cywilnego art. 820³ § 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 825 pkt 1¹: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 840 § 1 pkt 2: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 952¹: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-postepowania-cywilnego art. 952¹ § 1: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-postepowania-cywilnego art. 952¹ § 2: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-postepowania-cywilnego art. 952¹ § 3: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-postepowania-cywilnego art. 952¹ § 4: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-postepowania-cywilnego art. 952¹ § 5: DU/2020/875 in force 2020-05-30 (footnote, used) but 2020-05-16 (API)
- kodeks-postepowania-cywilnego art. 1064³ § 1: DU/2019/1469 in force 2019-08-21 (footnote, used) but 2019-11-07 (API)
- kodeks-postepowania-cywilnego art. 1157 pkt 1: DU/2019/1495 in force 2019-09-08 (footnote, used) but 2020-01-01 (API)
- kodeks-postepowania-cywilnego art. 1157 pkt 2: DU/2019/1495 in force 2019-09-08 (footnote, used) but 2020-01-01 (API)
- kodeks-postepowania-cywilnego art. 1157: DU/2019/1495 in force 2019-09-08 (footnote, used) but 2020-01-01 (API)
- kodeks-postepowania-cywilnego art. 1161 § 3: DU/2019/1495 in force 2019-09-08 (footnote, used) but 2020-01-01 (API)
- kodeks-postepowania-cywilnego art. 1163 § 1: DU/2019/1495 in force 2019-09-08 (footnote, used) but 2020-01-01 (API)
- kodeks-postepowania-cywilnego art. 1163 § 2: DU/2019/1495 in force 2019-09-08 (footnote, used) but 2020-01-01 (API)
- kodeks-postepowania-cywilnego art. 1163 § 3: DU/2019/1495 in force 2019-09-08 (footnote, used) but 2020-01-01 (API)
- kodeks-postepowania-cywilnego art. 1169 § 2¹: DU/2019/1495 in force 2019-09-08 (footnote, used) but 2020-01-01 (API)
- kodeks-postepowania-cywilnego DU/2020/1575: 340 lines changed with no footnote
- kodeks-postepowania-cywilnego DU/2020/1017 (in force 2020-06-09): listed by the API, but no unit of DU/2020/1575 is credited to it
- kodeks-postepowania-cywilnego DU/2020/1086 (in force 2020-06-24): listed by the API, but no unit of DU/2020/1575 is credited to it
- kodeks-postepowania-cywilnego DU/2021/1805: 71 lines changed with no footnote
- kodeks-postepowania-cywilnego DU/2019/1655 (in force 2021-07-01): listed by the API, but no unit of DU/2021/1805 is credited to it
- kodeks-postepowania-cywilnego DU/2019/1798 (in force 2021-02-28): listed by the API, but no unit of DU/2021/1805 is credited to it
- kodeks-postepowania-cywilnego DU/2020/1747 (in force 2020-10-09): listed by the API, but no unit of DU/2021/1805 is credited to it
- kodeks-postepowania-cywilnego DU/2021/1655 (in force 2021-09-24): listed by the API, but no unit of DU/2021/1805 is credited to it
- kodeks-postepowania-cywilnego art. 117 § 5²: the words of DU/2021/2328 art. 2 pkt 1 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 117 § 5⁴: the words of DU/2021/2328 art. 2 pkt 1 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 458² § 1 pkt 3: the words of DU/2023/614 art. 1 pkt 62 lit. a differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 479²⁸ § 1 pkt 6: the words of DU/2021/2262 art. 52 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 560²: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 560³ § 1: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 560³a § 8: the words of DU/2023/289 art. 1 pkt 4 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 560⁶ § 4: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 560⁷ § 1: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 560⁷ § 2: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 560⁸: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 560⁹ § 1: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 733 § 2: the words of DU/2021/2328 art. 2 pkt 2 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 754: the words of DU/2021/2328 art. 2 pkt 4 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 755² § 1: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 755² § 5: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 755³: the change by DU/2023/535 before DU/2023/289 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 805 § 1²: the words of DU/2023/614 art. 1 pkt 106 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 829² § 1: the words of DU/2021/2289 art. 1 pkt 1 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 829² § 2: the words of DU/2021/2289 art. 1 pkt 1 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 829² § 6: the words of DU/2021/2289 art. 1 pkt 1 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 829⁴: the words of DU/2021/2289 art. 1 pkt 1 differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 879⁴ § 2: the words of DU/2023/614 art. 1 pkt 116 lit. a differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 902² § 2¹: the words of DU/2022/1301 art. 2 pkt 6 lit. c differ from DU/2023/1550; the unified text is used
- kodeks-postepowania-cywilnego art. 952¹ § 5: DU/2022/830 in force 2022-04-15 (footnote, used) but 2022-02-24 (API)
- kodeks-postepowania-cywilnego art. 1049 § 1: DU/2023/614 in force 2023-04-15 (footnote, used) but 2023-07-01 (API)
- kodeks-postepowania-cywilnego art. 1049 § 1¹: DU/2023/614 in force 2023-04-15 (footnote, used) but 2023-07-01 (API)
- kodeks-postepowania-cywilnego art. 1049 § 1²: DU/2023/614 in force 2023-04-15 (footnote, used) but 2023-07-01 (API)
- kodeks-postepowania-cywilnego art. 1049 § 1³: DU/2023/614 in force 2023-04-15 (footnote, used) but 2023-07-01 (API)
- kodeks-postepowania-cywilnego art. 1049 § 1⁴: DU/2023/614 in force 2023-04-15 (footnote, used) but 2023-07-01 (API)
- kodeks-postepowania-cywilnego art. 1049 § 1⁵: DU/2023/614 in force 2023-04-15 (footnote, used) but 2023-07-01 (API)
- kodeks-postepowania-cywilnego art. 1049 § 1⁶: DU/2023/614 in force 2023-04-15 (footnote, used) but 2023-07-01 (API)
- kodeks-postepowania-cywilnego art. 1049 § 1⁷: DU/2023/614 in force 2023-04-15 (footnote, used) but 2023-07-01 (API)
- kodeks-postepowania-cywilnego art. 1050 § 4: DU/2023/614 in force 2023-04-15 (footnote, used) but 2023-07-01 (API)
- kodeks-postepowania-cywilnego DU/2023/1550: 200 lines changed with no footnote
- kodeks-postepowania-cywilnego DU/2023/289: in force 2023-08-15, after the unified text DU/2023/1550 of 2023-08-08 that prints it
- kodeks-postepowania-cywilnego DU/2019/55 (in force 2021-12-01): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2020/2320 (in force 2022-10-01): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2021/2270 (in force 2022-01-01): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2021/2459 (in force 2022-06-30): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2022/1 (in force 2022-01-04): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2022/1371 (in force 2022-06-30): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2022/1692 (in force 2022-08-12): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2022/1967 (in force 2022-09-20): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2022/2180 (in force 2023-01-01): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2022/480 (in force 2022-02-28): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2022/807 (in force 2022-10-13): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego DU/2023/739 (in force 2023-04-19): listed by the API, but no unit of DU/2023/1550 is credited to it
- kodeks-postepowania-cywilnego art. 9 § 1¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 131¹a: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 131¹a § 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 131¹a § 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 131¹a § 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 131¹a § 4: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 142 § 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 142 § 1 pkt 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 142 § 1 pkt 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 142 § 1 pkt 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 142 § 1 pkt 4: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 150 pkt 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 151 § 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 151 § 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 151 § 4: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 151 § 5: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 151 § 6: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 151 § 7: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 151 § 8: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 151 § 9: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 235 § 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 235 § 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 263¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 263¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 284 § 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 284 § 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 289: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 367 § 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 367¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 367¹ § 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 367¹ § 1 pkt 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 367¹ § 1 pkt 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 367¹ § 1 pkt 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 367¹ § 1 część wspólna: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 367¹ § 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 367¹ § 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 387 § 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 387 § 1¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 387 § 1¹ pkt 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 387 § 1¹ pkt 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 387 § 1¹ pkt 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 387 § 1¹ część wspólna: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 394¹a § 1²: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 394² § 1¹ pkt 4¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 394² § 1¹ pkt 5¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 394² § 1³: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 397 § 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 397 § 1¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 446¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 446¹: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 451 § 2: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 451 § 2: the words of DU/2023/1860 art. 1 pkt 23 lit. b differ from DU/2024/1568; the unified text is used
- kodeks-postepowania-cywilnego art. 477⁸ § 2 pkt 4a: the words of DU/2023/1429 art. 33 pkt 3 differ from DU/2024/1568; the unified text is used
- kodeks-postepowania-cywilnego art. 479³⁴a: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479³⁴a: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479⁵⁵a: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479⁵⁵a: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479⁶⁶b: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479⁶⁶b: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479⁷⁷b: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479⁷⁷b: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479⁸⁷a: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479⁸⁷a: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 479⁹⁰ § 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 505¹⁰: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 505²⁷ § 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 544 § 1: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 547 § 4: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 560 § 3: DU/2023/1860 in force 2024-03-14 (footnote, used) but 2023-09-28 (API)
- kodeks-postepowania-cywilnego art. 755⁵ § 2: the words of DU/2023/1667 art. 2 pkt 2 differ from DU/2024/1568; the unified text is used
- kodeks-postepowania-cywilnego art. 833 § 6: the change by DU/2024/859 before DU/2024/858 is not reconstructed (no quoted wording)
- kodeks-postepowania-cywilnego art. 1049 § 2: DU/2023/1615 in force 2023-09-15 (footnote, used) but 2023-11-15 (API)
- kodeks-postepowania-cywilnego DU/2024/1568: 127 lines changed with no footnote
- kodeks-postepowania-cywilnego DU/2022/2600 (in force 2023-10-01): listed by the API, but no unit of DU/2024/1568 is credited to it
- kodeks-postepowania-cywilnego DU/2024/1237 (in force 2024-08-29): listed by the API, but no unit of DU/2024/1568 is credited to it
- kodeks-postepowania-cywilnego DU/2024/859 (in force 2024-06-13): listed by the API, but no unit of DU/2024/1568 is credited to it
- kodeks-postepowania-cywilnego DU/2024/1222 (in force 2024-11-10): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2024/1841 (in force 2025-01-01): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2024/863 (in force 2024-11-01): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2025/1172 (in force 2026-03-01): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2025/1302 (in force 2025-09-30): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2025/1518 (in force 2025-12-05): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2025/1661 (in force 2025-12-13): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2025/620 (in force 2025-06-01): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2026/1003 (in force 2026-10-28): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2026/1046 (in force 2026-11-05): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2026/1296 (in force 2026-11-06): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2026/26 (in force 2026-04-13): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2026/473 (in force 2026-07-08): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2026/830 (in force 2026-07-08): after the last unified text; not in the record
- kodeks-postepowania-cywilnego DU/2014/101: 1 lines differ from the unified text for no reason found: art. 398⁶ § 2
- kodeks-postepowania-cywilnego DU/2016/1822: 1 lines differ from the unified text for no reason found: art. 398⁶ § 2
- kodeks-postepowania-cywilnego DU/2018/1360: 2 lines differ from the unified text for no reason found: art. 761 § 1¹, art. 761 § 1¹ pkt 8
- kodeks-postepowania-cywilnego DU/2023/1550: 12 lines differ from the unified text for no reason found: art. 560², art. 560³ § 1, art. 560³a, art. 560³a § 8, art. 560⁶ § 4, art. 560⁷ § 1, art. 560⁷ § 2, art. 560⁸

## What the AI did

The builder, parsers, checks and documentation were written by Claude Code with Claude Opus 5.5
(`claude-opus-5-5`), at the request of Lexifina. No AI wrote or changed any legal text, and no model runs when the
repository is built: every word of law comes from the Sejm's API.
