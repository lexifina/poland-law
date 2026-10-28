"""Writes data/zrodla.json, corpus.json and REPRODUCE.md into the Polish law repository, from the facts of the build
that made it. Called by build.py.

The results of the checks (check_repo.py, test_repo.py and the rebuild that compares hashes) are read from
verification.json next to this file; they describe the build before the one that writes this file, from the same data,
so a rebuild with the same data and the same verification.json gives the same hashes."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def write_manifest(repo: Path, acts: list, today: str):
    import src
    out = {'built': today, 'source': src.API, 'acts': []}
    for a in acts:
        cps = []
        for c in a.checkpoints:
            cps.append({'day': c['day'], 'eli': c['eli'], 'label': c['label'], 'kind': c['kind'], 'what': c['what'],
                        'files': len(c['files'])})
        out['acts'].append({'eli': a.conf['eli'], 'label': a.label, 'slug': a.slug, 'title': a.title,
                            'checkpoints': cps,
                            'amending': [{'eli': e['eli'], 'label': a.law(e['eli'])['displayAddress'], 'in_force': e['day'],
                                          'lines': len(e.get('changes', [])), 'kind': e['kind']}
                                         for e in a.events if e['kind'] in ('law', 'correction')]})
    files = sorted({r['file'] for r in src.REQUESTS if r['file'].exists()})
    urls = {}
    for r in src.REQUESTS:
        if r['file'].exists():
            b = r['file'].read_bytes()
            urls[r['url']] = None if b == b'\x00' else hashlib.sha256(b).hexdigest()
    out['requests'] = [{'url': u, 'sha256': h} for u, h in sorted(urls.items())]
    (repo / 'data').mkdir(exist_ok=True)
    (repo / 'data' / 'zrodla.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8',
                                               newline='\n')
    del files
    first = min(e['day'] for a in acts for e in a.events)
    last = max(e['day'] for a in acts for e in a.events if e['day'] <= today)
    corpus = {
        'corpus': 'pl/national/acts',
        'name': 'Polish law: Konstytucja Rzeczypospolitej Polskiej (Dz.U. 1997 nr 78 poz. 483) and ustawa o '
                'obywatelstwie polskim (Dz.U. 2012 poz. 161)',
        'acts': [a.label for a in acts],
        'history_from': first,
        'built': today,
        'dates': {'commit': 'in-force', 'other_trailers': ['Enacted', 'Published', 'Act-in-force'],
                  'time': '12:00 Europe/Warsaw (UTC+1, UTC+2 in summer time)'},
        'scope': {
            'trailer': 'Applies',
            'when_absent': 'this corpus records no scope notes (no commit carries Applies:); the absence is not a '
                           'statement that the change reaches every case',
            'default_reach': {
                'rule': 'lex retro non agit',
                'meaning': 'an act applies from the day it takes effect and does not reach back, unless it says so and '
                           'the rule of law allows it; acts take effect no earlier than 14 days after publication unless '
                           'a shorter period is justified; a criminal act applies only to acts that were offences when '
                           'committed',
                'authority': 'Konstytucja RP art. 2 (demokratyczne państwo prawne) and art. 42 ust. 1; ustawa z dnia '
                             '20 lipca 2000 r. o ogłaszaniu aktów normatywnych, art. 4 ust. 1 and art. 5 ("Przepisy art. 4 '
                             'nie wyłączają możliwości nadania aktowi normatywnemu wstecznej mocy obowiązującej, jeżeli '
                             'zasady demokratycznego państwa prawnego nie stoją temu na przeszkodzie.")',
                'decided_here': False}},
        'tool': 'tools/na_dzien.py',
        'in_force_trailer': 'In-force',
        'record_to': last,
        'citation': {'file': r'([a-z]+)/art-0*([0-9]+[a-z]*)\.md', 'cites': r'(art\.|Art\.) ?{n}([^0-9a-z]|$)'},
        'label': 'Poland',
        'language': 'pl',
        'checked_on': today,
        'history': 'in-force',
        'record_note': f'Checked against the official texts on {today}: every unified text (tekst jednolity) of the '
                       'citizenship act and the Sejm\'s consolidated text of the Constitution.',
    }
    (repo / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=1) + '\n', encoding='utf-8',
                                      newline='\n')


def write_reproduce(repo: Path, acts: list, log: list, tags: dict, requests: list, today: str):
    import src
    blobs = {n: subprocess.run(['git', 'hash-object', str(HERE / n)], capture_output=True, text=True).stdout.strip()
             for n in ('build.py', 'src.py', 'parse.py', 'pdfparse.py', 'gloss.py', 'reproduce.py')}
    pyv = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.strip()
    gitv = subprocess.run(['git', '--version'], capture_output=True, text=True).stdout.strip()
    import lxml.etree
    import pymupdf
    lxmlv = '.'.join(str(x) for x in lxml.etree.LXML_VERSION[:3])
    ver = json.loads((HERE / 'verification.json').read_text(encoding='utf-8')) if (HERE / 'verification.json').exists() else {}
    urls = {r['url'] for r in requests}
    files = {r['file'] for r in requests if r['file'].exists()}
    days = sorted({dt.date.fromtimestamp(f.stat().st_mtime).isoformat() for f in files})
    n_meta = sum(1 for u in urls if not u.endswith(('.html', '.pdf')))
    n_html = sum(1 for u in urls if u.endswith('.html'))
    n_pdf = sum(1 for u in urls if u.endswith('.pdf'))
    kinds = {}
    for c in log:
        kinds[c['kind']] = kinds.get(c['kind'], 0) + 1
    chk = ver.get('check', {})
    det = ver.get('rebuild', {})
    smoke = ver.get('smoke', {})
    check_lines = '\n'.join(f'   - {l}' for l in chk.get('lines', [])) or '   (not yet run)'
    rebuild_line = (f'A second build from the same cache into an empty folder gave the same history: the last law '
                    f'commit was `{det["history_tip"]}` in both, and every one of the {det["commits"]} law commits and '
                    f'{det["tags"]} tags had the same hash.' if det.get('identical') else '(not yet run)')
    smoke_lines = ('\n'.join(f'   - {"pass" if r["ok"] else "FAIL"}: {r["test"]}: {r["detail"]}' for r in smoke['results'])
                   if smoke else '   (not yet run)')
    problems = '\n'.join(f'- {p}' for a in acts for p in a.problems) or '- none'
    rows = []
    for a in acts:
        for c in a.checkpoints:
            rows.append(f'| {a.conf["short"]} | {c["label"]} | {c["day"]} | {c["kind"]} | {c["what"]} |')
    replay = '; '.join(f'{a.conf["short"]}: {a.replay["checked"]} of {a.replay["lines"]} quoted lines' for a in acts)
    text = f"""# How this history was made, and how to make it again

This file records how the repository was built: the sources, the commands, the software, the decisions made by hand,
and what an AI model did and did not do. The build writes it, so it describes the build that made this commit.

## Short version

```sh
git clone https://github.com/lexifina/poland-law && cd poland-law
pip install lxml pymupdf
python -X utf8 tools/build.py --repo ../rebuilt --today {today}
git -C ../rebuilt rev-parse main        # the same hash as this repository's main
python -X utf8 tools/check_repo.py --repo ../rebuilt --no-record
```

`tools/build.py` needs Python 3.12 or later with `lxml` and `pymupdf`, and git. It reads the Sejm's ELI API (or its own
cache, `.cache/` next to the script) and writes this repository into `--repo`. With the same data and the same
`--today` it gives the same commits with the same hashes. `data/zrodla.json` lists every address read with the sha256
of the answer, so a rebuild can show it read the same bytes.

## Sources

All legal text and all information about amending acts comes from the **ELI API of the Sejm**
(`{src.API}`, Kancelaria Sejmu): act metadata (JSON), the texts as HTML (`/acts/DU/<year>/<pos>/text.html`) and PDF
(`/acts/DU/<year>/<pos>/text/<type>/<file>`: O = the Journal as published, U = the Sejm's consolidated text). Nothing
was typed in, summarised or rewritten. The build read {n_meta} metadata records, {n_html} HTML texts and {n_pdf} PDFs,
retrieved on {', '.join(days) if days else today}, at most 4 requests at a time with gzip, with the user agent
`{src.UA}`.

Terms. The API's documentation pages (`https://api.sejm.gov.pl/`, `eli.html`, `eli_pl.html`) state no terms of use
and no rate limit. `https://api.sejm.gov.pl/robots.txt` answers with the gateway's "Request Rejected" page (no
robots.txt is served); `isap.sejm.gov.pl`, `sejm.gov.pl` and `www.sejm.gov.pl` answer every request, robots.txt
included, with an Incapsula bot challenge, so ISAP's own pages were not read at all (the challenge was not bypassed).
No rule naming ClaudeBot, Claude-Web or anthropic-ai was found anywhere. Normative acts and official documents are not
protected by copyright in Poland (ustawa o prawie autorskim i prawach pokrewnych, art. 4 pkt 1 and 2).

| Act | Checkpoint | Day | Format | What |
| --- | --- | --- | --- | --- |
{chr(10).join(rows)}

## The build, step by step

1. `python -X utf8 scripts/poland-law/build.py --today {today}` in Lexifina's own repository fetched the data into its
   cache and wrote this repository. The files in `tools/` are the same files as in `scripts/poland-law/` there
   (git blobs: {', '.join(f'`{n}` {b[:12]}' for n, b in blobs.items())}).
2. `python -X utf8 scripts/poland-law/check_repo.py` read each checkpoint back from this repository with
   `tools/na_dzien.py` and compared it with the official text. Results:
{check_lines}
3. `python -X utf8 scripts/poland-law/build.py --offline --verify-rebuild` built the repository again from the same
   cache into a temporary folder and compared the hashes. {rebuild_line}
4. `python -X utf8 scripts/poland-law/test_repo.py --record` ran the reader's commands ({smoke.get('passed', '?')} of
   {smoke.get('total', '?')} passed):
{smoke_lines}
5. The build was run again to write these results into this file, and `main` was rebuilt and compared hash for hash
   before it was pushed to the private GitHub repository `lexifina/poland-law`.

Software: {pyv}, {gitv}, lxml {lxmlv}, PyMuPDF {pymupdf.VersionBind}.

## How causes and dates were read

- **The citizenship act** (`obywatelstwo/`) starts as published (Dz.U. 2012 poz. 161, HTML), in two stages as its
  art. 70 says (chapter 5 and art. 65 from 2012-05-15, the rest from 2012-08-15). Each unified text is a checkpoint.
  Between two of them every changed unit is credited by the unified text's own footnotes ("W brzmieniu ustalonym
  przez art. ...", "Dodany przez art. ...", "Przez art. ..." for repeals), resolved to the act they name (including
  "ustawy, o której mowa w odnośniku N"). The day is the in-force day the API gives for that act's amendment of this
  act; the footnote's own day is compared with it. Where the amending act quotes the new wording, that wording is
  replayed on its day and checked against the next unified text ({replay}).
- **Editorial changes of the unified texts** (updated Journal references of the other acts cited, provisions left out
  as "(pominięty)") are separate commits, authored by the Marshal of the Sejm's unified text, on the day it was
  published. A line changed by an act keeps the Journal references it had until then.
- **The Constitution** (`konstytucja/`) has no unified text. The current text is the Sejm's consolidated text (PDF,
  type U). The 2006 and 2009 amending acts are replayed from their own words (HTML) and must equal it; the
  correction notice of 2001 (Dz.U. 2001 nr 28 poz. 319) is applied word by word and its commit is authored by the
  notice, not by a law. The text as enacted is the consolidated text with those three steps undone; art. 55 as enacted
  is read from the text layer of the 1997 Journal's scan (O), between "Art. 55." and "Art. 56.".
- Commits are dated noon in Warsaw on the in-force day (CET, CEST from the last Sunday in March to the last Sunday in
  October). Counts: {', '.join(f'{k} {v}' for k, v in sorted(kinds.items()))}; {len(tags)} tags.

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

{problems}

## What the AI did

The builder, parsers, checks and documentation were written by Claude Code with Claude Opus 5.5
(`claude-opus-5-5`), at the request of Lexifina. No AI wrote or changed any legal text, and no model runs when the
repository is built: every word of law comes from the Sejm's API.
"""
    (repo / 'REPRODUCE.md').write_text(text, encoding='utf-8', newline='\n')
