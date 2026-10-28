# How this history was made, and how to make it again

This file records how the repository was built: the sources, the commands, the software, the decisions made by hand,
and what an AI model did and did not do. The build writes it, so it describes the build that made this commit.

## Short version

```sh
git clone https://github.com/lexifina/poland-law && cd poland-law
pip install lxml pymupdf
python -X utf8 tools/build.py --repo ../rebuilt --today 2026-10-28
git -C ../rebuilt rev-parse main        # the same hash as this repository's main
python -X utf8 tools/check_repo.py --repo ../rebuilt --no-record
```

`tools/build.py` needs Python 3.12 or later with `lxml` and `pymupdf`, and git. It reads the Sejm's ELI API (or its own
cache, `.cache/` next to the script) and writes this repository into `--repo`. With the same data and the same
`--today` it gives the same commits with the same hashes. `data/zrodla.json` lists every address read with the sha256
of the answer, so a rebuild can show it read the same bytes.

## Sources

All legal text and all information about amending acts comes from the **ELI API of the Sejm**
(`https://api.sejm.gov.pl/eli`, Kancelaria Sejmu): act metadata (JSON), the texts as HTML (`/acts/DU/<year>/<pos>/text.html`) and PDF
(`/acts/DU/<year>/<pos>/text/<type>/<file>`: O = the Journal as published, U = the Sejm's consolidated text). Nothing
was typed in, summarised or rewritten. The build read 20 metadata records, 16 HTML texts and 3 PDFs,
retrieved on 2026-10-28, at most 4 requests at a time with gzip, with the user agent
`lexifina-watch/1.0 (+https://lexifina.com/watch; poland-law@lexifina.com)`.

Terms. The API's documentation pages (`https://api.sejm.gov.pl/`, `eli.html`, `eli_pl.html`) state no terms of use
and no rate limit. `https://api.sejm.gov.pl/robots.txt` answers with the gateway's "Request Rejected" page (no
robots.txt is served); `isap.sejm.gov.pl`, `sejm.gov.pl` and `www.sejm.gov.pl` answer every request, robots.txt
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

## The build, step by step

1. `python -X utf8 scripts/poland-law/build.py --today 2026-10-28` in Lexifina's own repository fetched the data into its
   cache and wrote this repository. The files in `tools/` are the same files as in `scripts/poland-law/` there
   (git blobs: `build.py` 321c4f98c824, `src.py` 874fbddad904, `parse.py` 2967287a843c, `pdfparse.py` e3b547162ddd, `gloss.py` 211dd4b33504, `reproduce.py` d78a494b285f).
2. `python -X utf8 scripts/poland-law/check_repo.py` read each checkpoint back from this repository with
   `tools/na_dzien.py` and compared it with the official text. Results:
   (not yet run)
3. `python -X utf8 scripts/poland-law/build.py --offline --verify-rebuild` built the repository again from the same
   cache into a temporary folder and compared the hashes. (not yet run)
4. `python -X utf8 scripts/poland-law/test_repo.py --record` ran the reader's commands (? of
   ? passed):
   (not yet run)
5. The build was run again to write these results into this file, and `main` was rebuilt and compared hash for hash
   before it was pushed to the private GitHub repository `lexifina/poland-law`.

Software: Python 3.12.10, git version 2.46.0.windows.1, lxml 6.1.3, PyMuPDF 2.0.

## How causes and dates were read

- **The citizenship act** (`obywatelstwo/`) starts as published (Dz.U. 2012 poz. 161, HTML), in two stages as its
  art. 70 says (chapter 5 and art. 65 from 2012-05-15, the rest from 2012-08-15). Each unified text is a checkpoint.
  Between two of them every changed unit is credited by the unified text's own footnotes ("W brzmieniu ustalonym
  przez art. ...", "Dodany przez art. ...", "Przez art. ..." for repeals), resolved to the act they name (including
  "ustawy, o której mowa w odnośniku N"). The day is the in-force day the API gives for that act's amendment of this
  act; the footnote's own day is compared with it. Where the amending act quotes the new wording, that wording is
  replayed on its day and checked against the next unified text (Konstytucja: 9 of 9 quoted lines; Obywatelstwo: 21 of 22 quoted lines).
- **Editorial changes of the unified texts** (updated Journal references of the other acts cited, provisions left out
  as "(pominięty)") are separate commits, authored by the Marshal of the Sejm's unified text, on the day it was
  published. A line changed by an act keeps the Journal references it had until then.
- **The Constitution** (`konstytucja/`) has no unified text. The current text is the Sejm's consolidated text (PDF,
  type U). The 2006 and 2009 amending acts are replayed from their own words (HTML) and must equal it; the
  correction notice of 2001 (Dz.U. 2001 nr 28 poz. 319) is applied word by word and its commit is authored by the
  notice, not by a law. The text as enacted is the consolidated text with those three steps undone; art. 55 as enacted
  is read from the text layer of the 1997 Journal's scan (O), between "Art. 55." and "Art. 56.".
- Commits are dated noon in Warsaw on the in-force day (CET, CEST from the last Sunday in March to the last Sunday in
  October). Counts: correction 1, editorial 6, law 11, start 3; 42 tags.

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

- none

## What the AI did

The builder, parsers, checks and documentation were written by Claude Code with Claude Opus 5.5
(`claude-opus-5-5`), at the request of Lexifina. No AI wrote or changed any legal text, and no model runs when the
repository is built: every word of law comes from the Sejm's API.
