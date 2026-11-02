"""Builds a git repository of Polish law from the Sejm's ELI API (https://api.sejm.gov.pl/eli), in which every
amending act is one commit, dated the day it took effect.

    python -X utf8 scripts/poland-law/build.py [--repo ../poland-law] [--today 2026-10-28] [--offline]
                                               [--verify-rebuild]

The API (Kancelaria Sejmu) gives each act of the Journal of Laws (Dziennik Ustaw) with its references: the acts that
amend it, each with the day the amendment takes effect for this act ("Akty zmieniające"), and the unified texts
(teksty jednolite) the Marshal of the Sejm has announced. Texts come as HTML (text.html) or PDF.

Method. The unified texts are the checkpoints. Between two of them we compare the text unit by unit (ustęp, punkt,
litera) and credit each change from the unified text's own footnotes, which say for each unit which act set, added or
repealed it and when that act took effect ("W brzmieniu ustalonym przez art. 29 pkt 1 ustawy z dnia ... (Dz. U.
poz. 2185), która weszła w życie z dniem 10 listopada 2022 r."). Where the amending act restates the unit ("otrzymuje
brzmienie"), its own words are replayed on its in-force day and checked against the next unified text. Changes made by
the unified text itself (updated Journal references of other acts, provisions left out as "(pominięty)") are separate
commits by the Marshal of the Sejm, labelled editorial. A change nothing explains is never credited to an act.

The Constitution has no unified text: it is the Sejm's consolidated text (tekst ujednolicony, PDF), with the two
amending acts replayed from their own words and the printing correction (sprostowanie) of 2001 applied as published.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import gloss  # noqa: E402
import parse  # noqa: E402
import pdfparse  # noqa: E402
import src  # noqa: E402

COMMITTER = ('Lexifina', 'poland-law@lexifina.com')
PUBLISHER = ('Kancelaria Sejmu (ISAP)', 'isap@sejm.invalid')
DZU = re.compile(r'\(Dz\. ?U\. [^()]*(?:\([^()]*\)[^()]*)*\)')
DASH = str.maketrans({'\u2212': '-', '\u2013': '-', '\u2011': '-', '\u2010': '-'})

ACTS = [
    {'eli': 'DU/1997/483', 'slug': 'konstytucja', 'short': 'Konstytucja', 'kind': 'constitution'},
    {'eli': 'DU/2012/161', 'slug': 'obywatelstwo', 'short': 'Obywatelstwo', 'kind': 'unified',
     # The act's own commencement (art. 70): "Ustawa wchodzi w życie po upływie 6 miesięcy od dnia ogłoszenia,
     # z wyjątkiem rozdziału 5 i art. 65, które wchodzą w życie po upływie 3 miesięcy od dnia ogłoszenia."
     # Published 2012-02-14: 3 months -> 2012-05-15, 6 months -> 2012-08-15 (the API's entryIntoForce).
     'stages': [{'from': '2012-05-15', 'chapters': ['chpt_5'], 'articles': ['65'],
                 'quote': 'art. 70: „z wyjątkiem rozdziału 5 i art. 65, które wchodzą w życie po upływie 3 miesięcy '
                          'od dnia ogłoszenia”'}]},
]

# Appended after the first publication (2026-11-02, append-only: these go on top of the published main, never into a
# rebuild of it). Each code starts as published (the API's HTML of the Journal), then every unified text with an HTML
# text is a checkpoint; changes between two of them are credited by the unified text's footnotes, as for the
# citizenship act. Unified texts the API has only as PDF (the newest ones) are not read yet: the record of each code
# ends at its last HTML unified text.
CODES = [
    {'eli': 'DU/1964/93', 'slug': 'kodeks-cywilny', 'short': 'Kodeks cywilny', 'kind': 'unified', 'html_tjs_only': True},
    {'eli': 'DU/1997/553', 'slug': 'kodeks-karny', 'short': 'Kodeks karny', 'kind': 'unified', 'html_tjs_only': True},
    {'eli': 'DU/1974/141', 'slug': 'kodeks-pracy', 'short': 'Kodeks pracy', 'kind': 'unified', 'html_tjs_only': True},
    {'eli': 'DU/1964/296', 'slug': 'kodeks-postepowania-cywilnego', 'short': 'Kodeks postępowania cywilnego',
     'kind': 'unified', 'html_tjs_only': True},
    {'eli': 'DU/1997/555', 'slug': 'kodeks-postepowania-karnego', 'short': 'Kodeks postępowania karnego',
     'kind': 'unified', 'html_tjs_only': True},
    {'eli': 'DU/2000/1037', 'slug': 'kodeks-spolek-handlowych', 'short': 'Kodeks spółek handlowych', 'kind': 'unified',
     'html_tjs_only': True},
    {'eli': 'DU/1997/926', 'slug': 'ordynacja-podatkowa', 'short': 'Ordynacja podatkowa', 'kind': 'unified',
     'html_tjs_only': True},
    # The most amended statutes (amending acts listed by the API, 2026-11-03): PIT 452, CIT 307, social insurance
    # 234, road traffic 212, building law 142, VAT 117, Code of Petty Offences 117.
    {'eli': 'DU/1991/350', 'slug': 'podatek-dochodowy-od-osob-fizycznych', 'short': 'PIT', 'kind': 'unified',
     'html_tjs_only': True},
    {'eli': 'DU/1992/86', 'slug': 'podatek-dochodowy-od-osob-prawnych', 'short': 'CIT', 'kind': 'unified',
     'html_tjs_only': True},
    {'eli': 'DU/1998/887', 'slug': 'system-ubezpieczen-spolecznych', 'short': 'System ubezpieczeń społecznych',
     'kind': 'unified', 'html_tjs_only': True},
    {'eli': 'DU/1997/602', 'slug': 'prawo-o-ruchu-drogowym', 'short': 'Prawo o ruchu drogowym', 'kind': 'unified',
     'html_tjs_only': True},
    {'eli': 'DU/1994/414', 'slug': 'prawo-budowlane', 'short': 'Prawo budowlane', 'kind': 'unified',
     'html_tjs_only': True},
    {'eli': 'DU/2004/535', 'slug': 'podatek-od-towarow-i-uslug', 'short': 'VAT', 'kind': 'unified',
     'html_tjs_only': True},
    {'eli': 'DU/1971/114', 'slug': 'kodeks-wykroczen', 'short': 'Kodeks wykroczeń', 'kind': 'unified',
     'html_tjs_only': True},
]


# ---------------------------------------------------------------- identities

def label_of(meta: dict) -> str:
    return meta['displayAddress']           # 'Dz.U. 2013 poz. 1650', 'Dz.U. 1997 nr 78 poz. 483'


def email_of(eli: str) -> str:
    _, y, p = eli.split('/')
    return f'du-{y}-{p}@sejm.invalid'


def tag_of(eli: str) -> str:
    _, y, p = eli.split('/')
    return f'du/{y}-{p}'


def eli_order(eli: str) -> tuple:
    _, y, p = eli.split('/')
    return (int(y), int(p))


# The API's article ids: '7', '7a', '7_1' (art. 7 with superscript 1), '300_71_a' (art. 300 with superscript 71a),
# '596-609' (a range of repealed articles printed as one unit).
NUM = re.compile(r'(\d+)([a-z]*)(?:_(\d+))?(?:_([a-z]+))?(?:-(\d+[a-z]*))?')
SUPD = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
UNSUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')


def file_name(num: str) -> str:
    if num == 'preambula':
        return 'preambula.md'
    m = NUM.fullmatch(num)
    if not m:
        raise SystemExit(f'article number not understood: {num}')
    out = f'art-{int(m.group(1)):03d}{m.group(2)}'
    if m.group(3):
        out += f'-{m.group(3)}{m.group(4) or ""}'
    if m.group(5):
        out += f'-do-{m.group(5)}'
    return out + '.md'


def num_order(num: str) -> tuple:
    if num == 'preambula':
        return (0, 0, '', 0, '')
    m = NUM.fullmatch(num)
    if not m:
        raise SystemExit(f'article number not understood: {num}')
    return (1, int(m.group(1)), m.group(2), int(m.group(3) or 0), m.group(4) or '')


def shown(n: str) -> str:
    """'7_1' -> '7¹', '300_71_a' -> '300⁷¹a', '596-609' as is (a unit number as printed)."""
    m = re.fullmatch(r'([0-9]+[a-z]*)_(\d+)(?:_([a-z]+))?(.*)', n)
    return f'{m.group(1)}{m.group(2).translate(SUPD)}{m.group(3) or ""}{m.group(4)}' if m else n


def api_num(n: str) -> str:
    """'7¹' -> '7_1', '300⁷¹a' -> '300_71_a' (a printed unit number as the API's id)."""
    m = re.fullmatch(r'([0-9]+[a-z]*?)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)([a-z]*)', n)
    if not m:
        return n
    return f'{m.group(1)}_{m.group(2).translate(UNSUP)}' + (f'_{m.group(3)}' if m.group(3) else '')


NAMES = {'para': '§', 'pass': 'ust.', 'pint': 'pkt', 'lett': 'lit.', 'tirt': 'tiret'}


def provision(num: str, key: str) -> str:
    """'arti_30/pass_1/pint_7' -> 'art. 30 ust. 1 pkt 7'; chapter headings and the preamble are named as such."""
    if num == 'preambula':
        return 'preambuła'
    if key.startswith('chpt_') or '/s_' in key:
        m = re.match(r'chpt_([^/]+)', key)
        return f'Rozdział {m.group(1) if m else ""} (tytuł)'.replace('  ', ' ')
    out = [f'art. {shown(num)}']
    for seg in key.split('/')[1:]:
        if '_' in seg:
            kind, n = seg.split('_', 1)
            if kind in NAMES:
                out.append(f'{NAMES[kind]} {shown(n)}')
        elif seg.startswith('w'):
            out.append('część wspólna')
    return ' '.join(out)


# ---------------------------------------------------------------- loading

def vocabulary(texts: list[dict]) -> set[str]:
    out = set()
    for r in texts:
        for a in r['order']:
            for l in r['files'][a]['lines']:
                out.update(re.findall(r'\w+(?:-\w+)+', l[1]))
    return out


def lines_of(r: dict) -> dict[str, list[tuple]]:
    return {num: [tuple(l) for l in r['files'][num]['lines']] for num in r['order']}


def pdf_name(meta: dict, kind: str) -> str | None:
    for t in meta['texts']:
        if t['type'] == kind:
            return t['fileName']
    return None


def provision_unit(tree_units: list, path: str):
    """The unit of an amending act at 'art. 29 pkt 1' (ust./pkt/lit.), from read_html's tree."""
    m = re.match(r'art\. ([0-9a-z⁰¹²³⁴⁵⁶⁷⁸⁹]+)(.*)', path or '')
    if not m:
        return None
    art = None
    for a, _ in parse.walk_articles(tree_units):
        if a.id == f'arti_{api_num(m.group(1))}':
            art = a
            break
    if art is None:
        return None
    u = art
    for kind, n in re.findall(r'(ust|pkt|lit|§)\.? ([0-9a-z⁰¹²³⁴⁵⁶⁷⁸⁹]+)', m.group(2)):
        want = {'ust': 'pass', 'pkt': 'pint', 'lit': 'lett', '§': 'para'}[kind] + '_' + api_num(n)
        nxt = [c for c in u.units() if c.id == want]
        if not nxt:
            return None
        u = nxt[0]
    return u


def cite_lines(u) -> list[tuple[str, str]]:
    """The units quoted in an amending provision ("otrzymuje brzmienie: „...”", "dodaje się ust. 6 w brzmieniu: „...”"),
    as (relative key, text) in the target act's line format."""
    out = []

    def walk(x):
        for b in x.body:
            if isinstance(b, parse.Unit):
                walk(b)
            elif b[0] == 'cite':
                for q in b[3]:
                    if q.kind == 'arti':
                        out.extend((k, t) for k, t, _, _ in parse.article_lines(q, []))
                    elif isinstance(q.label, str):      # a quoted chapter, title or part: not replayed
                        out.extend((k.lstrip('/'), t) for k, t, _, _ in parse.unit_lines(q, '', []))
    walk(u)
    return out


def amending_article_html(raw: bytes) -> bytes:
    """Some acts' HTML does not nest well enough for lxml to find their articles (the Foreigners Act 2013/1650): keep
    only the articles' markup, which parses."""
    t = raw.decode('utf-8')
    i = t.find('<div class="unit unit_arti pro-text')
    j = t.rfind('<div class="gloss-section"')
    if i < 0:
        return raw
    body = t[i:j if j > i else len(t)]
    return ('<html><body><h1></h1><div class="parts"><section id="part_1"><div class="part"><div class="block">'
            + body + '</div></div></section></div></body></html>').encode('utf-8')


class Act:
    """Everything the build knows about one act of the record."""

    def __init__(self, conf: dict):
        self.conf = conf
        self.slug = conf['slug']
        self.meta = src.act(conf['eli'])
        self.label = label_of(self.meta)
        self.title = self.meta['title']
        self.laws: dict[str, dict] = {conf['eli']: self.meta}
        self.events: list[dict] = []     # {'day', 'kind', 'eli', 'changes': [(num, key, text|None)], ...}
        self.checkpoints: list[dict] = []
        self.problems: list[str] = []
        self.replay = {'lines': 0, 'checked': 0}
        self.order: dict[str, list[str]] = {}

    def law(self, eli: str) -> dict:
        if eli not in self.laws:
            self.laws[eli] = src.act(eli)
        return self.laws[eli]


# ---------------------------------------------------------------- state

def apply(state: dict, num: str, key: str, text: str | None, ref: list[str]):
    """Sets (or removes) one line of a file, placing a new line after the nearest line that precedes it in `ref`
    (the keys of the file in the text it comes from)."""
    lines = state.setdefault(num, [])
    keys = [k for k, _ in lines]
    if key in keys:
        i = keys.index(key)
        if text is None:
            del lines[i]
        else:
            lines[i] = (key, text)
    elif text is not None:
        pos = 0
        if key in ref:
            for k in reversed(ref[:ref.index(key)]):
                if k in keys:
                    pos = keys.index(k) + 1
                    break
        lines.insert(pos, (key, text))
    if not lines:
        del state[num]


def render(lines: list[tuple[str, str]]) -> str:
    return '\n\n'.join(t for _, t in lines) + '\n'


def snapshot(lines_by_num: dict) -> dict[str, list[tuple[str, str]]]:
    return {n: [(l[0], l[1]) for l in ls] for n, ls in lines_by_num.items()}


# ---------------------------------------------------------------- the act with unified texts

def change_glosses(line: tuple, table: dict) -> tuple[list, list]:
    """(own change footnotes, the nearest ancestor's change footnotes) of a line, each resolved to acts."""
    own = [g for g in line[2] if gloss.kind(g[1]) == 'change']
    inh = []
    for lvl in reversed(line[3] if len(line) > 3 else []):
        c = [g for g in lvl if gloss.kind(g[1]) == 'change']
        if c:
            inh = c
            break

    def acts(gs):
        out = []
        for _, t in gs:
            for a in gloss.act_of(t, table):
                if a['eli']:
                    out.append({**a, 'text': t})
        return out
    return acts(own), acts(inh)


def same_but_refs(a: str, b: str) -> bool:
    def n(s):
        return re.sub(r'\s+', ' ', DZU.sub('', s).translate(DASH)).replace(' ,', ',').replace(' .', '.').strip()
    return n(a) == n(b)


def same_but_punct(a: str, b: str) -> bool:
    """The same words, differing only in punctuation and spacing: the unified texts end the points of an enumeration
    with a semicolon where the Journal printed a comma, close a quotation with its full stop, and the like."""
    def n(s):
        return re.findall(r'\w+', DZU.sub('', s).translate(DASH))
    return n(a) == n(b)


def restore_refs(new: str, old: str | None) -> str:
    """The new wording with the Journal references of the old one (the unified text updates those itself)."""
    if not old:
        return new
    a, b = DZU.findall(new), DZU.findall(old)
    if len(a) != len(b) or not a:
        return new
    parts = DZU.split(new)
    out = parts[0]
    for ref, rest in zip(b, parts[1:]):
        out += ref + rest
    return out


def build_unified(act: Act):
    parse.W_DASH[0] = not act.conf.get('html_tjs_only')
    try:
        _build_unified(act)
    finally:
        parse.W_DASH[0] = True


def _build_unified(act: Act):
    conf = act.conf
    refs = act.meta['references']
    amend = {r['id']: r.get('date') for r in refs.get('Akty zmieniające', [])}
    tjs = sorted((src.act(r['id']) for r in refs.get('Inf. o tekście jednolitym', [])),
                 key=lambda m: (m.get('promulgation') or m['announcementDate'], m['pos']))
    if conf.get('html_tjs_only'):
        act.pdf_tjs = [m for m in tjs if not m['textHTML']]
        tjs = [m for m in tjs if m['textHTML'] and m.get('promulgation')]
    for e in amend:
        act.law(e)
    htmls = [act.meta] + [m for m in tjs if m['textHTML']]
    parsed = {m['ELI']: parse.read_html(src.text_html(m['ELI']), tj=m is not act.meta) for m in htmls}
    vocab = vocabulary(list(parsed.values()))
    for m in tjs:
        if not m['textHTML']:
            raw = src.text_file(m['ELI'], 'O', pdf_name(m, 'O'))
            r = pdfparse.read_pdf(raw, vocab, start='Rozdział 1')
            # The PDF prints dashes (U+2013, U+2212) where the API's HTML of every other unified text has a
            # hyphen-minus; the HTML convention is kept, so a dash is never a change.
            for f in r['files'].values():
                f['lines'] = [(l[0], l[1].translate(DASH), *l[2:]) for l in f['lines']]
            r['pdf'] = True
            parsed[m['ELI']] = r
    # The act as enacted, in its stages.
    base = parsed[conf['eli']]
    start_day = act.meta['entryIntoForce']
    chap_of = {}
    cur_chap = None
    for num in base['order']:
        for k, *_ in base['files'][num]['lines']:
            if k.startswith('chpt_'):
                cur_chap = k.split('/')[0]
        chap_of[num] = cur_chap
    staged = set()
    for st in conf.get('stages', []):
        nums = [n for n in base['order'] if chap_of.get(n) in st['chapters'] or n in st['articles']]
        staged.update(nums)
        act.events.append({'day': st['from'], 'kind': 'start', 'eli': conf['eli'], 'stage': st,
                           'changes': [(n, l[0], l[1]) for n in nums for l in base['files'][n]['lines']]})
    base_ref = {n: [l[0] for l in base['files'][n]['lines']] for n in base['order']}
    for e in act.events:
        e['ref'] = base_ref
    act.events.append({'day': start_day, 'kind': 'start', 'eli': conf['eli'], 'stage': None, 'ref': base_ref,
                       'changes': [(n, l[0], l[1]) for n in base['order'] if n not in staged
                                   for l in base['files'][n]['lines']]})
    act.checkpoints.append({'day': start_day, 'eli': conf['eli'], 'label': act.label, 'files': snapshot(lines_of(base)),
                            'kind': 'html', 'what': 'tekst ogłoszony (the act as published)'})
    prev, prev_meta = base, act.meta
    prev_day = start_day
    used: set[str] = set()
    for m in tjs:
        cur = parsed[m['ELI']]
        day = m['promulgation']
        table = cur['glosses']
        A = {(n, l[0]): l for n in prev['order'] for l in prev['files'][n]['lines']}
        B = {(n, l[0]): l for n in cur['order'] for l in cur['files'][n]['lines']}
        ref = {n: [l[0] for l in cur['files'][n]['lines']] for n in cur['order']}
        prev_ref = {n: [l[0] for l in prev['files'][n]['lines']] for n in prev['order']}
        changed = [k for k in sorted(set(A) | set(B), key=lambda k: (num_order(k[0]), k[1]))
                   if not (k in A and k in B and A[k][1].translate(DASH) == B[k][1].translate(DASH))]
        in_interval = {e: d for e, d in amend.items() if d and prev_day < d <= day}
        by_event: dict[tuple, dict] = {}
        editorial: list = []
        unexplained: list = []

        def add(eli, d, num, key, text, why, g=None):
            ev = by_event.setdefault((d, eli), {'day': d, 'kind': 'law', 'eli': eli, 'changes': [], 'why': {},
                                                'glosses': {}, 'tj': m['ELI'], 'ref': ref})
            ev['changes'].append((num, key, text))
            ev['why'][(num, key)] = why
            if g:
                ev['glosses'][(num, key)] = g
        attributed: dict[tuple, str] = {}
        for k in changed:
            a, b = A.get(k), B.get(k)
            num, key = k
            if b is None:
                continue
            own, inh = change_glosses(b, table)
            if a is not None and same_but_refs(a[1], b[1]):
                editorial.append((num, key, b[1], 'refs'))
                continue
            if b[1].endswith('(pominięty)'):
                editorial.append((num, key, b[1], 'omitted'))
                attributed[k] = 'editorial'
                continue
            chain = own or inh
            if not chain:
                if a is not None and same_but_punct(a[1], b[1]):
                    editorial.append((num, key, b[1], 'punct'))
                    attributed[k] = 'editorial'
                    continue
                unexplained.append((num, key, b[1]))
                continue
            # The acts that wrote this line, oldest first: the ancestor's when the line has its own later note.
            steps = []
            if own and inh and {x['eli'] for x in inh} - {x['eli'] for x in own}:
                for x in inh:
                    if x['eli'] not in {y['eli'] for y in own}:
                        steps.append(('ancestor', x))
            for x in chain:
                steps.append(('own' if own else 'ancestor', x))
            steps.sort(key=lambda s: in_interval.get(s[1]['eli']) or amend.get(s[1]['eli']) or s[1]['date'] or '')
            last_text = a[1] if a else None
            for i, (whose, x) in enumerate(steps):
                eli = x['eli']
                # The footnote's own day for this unit wins when the unified text prints the unit as in force (an act
                # in force in stages: "wszedł w życie z dniem 1 marca 2020 r." while the API gives the act's main day).
                if conf.get('html_tjs_only') and x['date'] and prev_day < x['date'] <= day:
                    d = x['date']
                else:
                    d = amend.get(eli) or x['date']
                if eli not in amend:
                    act.problems.append(f'{act.slug} {provision(num, key)}: footnote names {eli}, not among the API\'s amending acts')
                if not d:
                    # no day for it anywhere (not among the API's amending acts, no day in the footnote)
                    act.problems.append(f'{act.slug} {provision(num, key)}: no in-force day for {eli}; not credited')
                    if i == len(steps) - 1:
                        unexplained.append((num, key, b[1]))
                    continue
                if d and amend.get(eli) and d != amend.get(eli):
                    act.problems.append(f'{act.slug} {provision(num, key)}: {eli} in force {d} (footnote, used) but '
                                        f'{amend.get(eli)} (API)')
                elif d and x['date'] and d != x['date']:
                    act.problems.append(f'{act.slug} {provision(num, key)}: {eli} in force {d} (API) but {x["date"]} (footnote)')
                used.add(eli)
                final = i == len(steps) - 1
                text, why = None, None
                q = quoted(act, eli, x['provision'], key)
                if q is not None:
                    act.replay['lines'] += 1
                    if final and same_but_refs(q, b[1]):
                        act.replay['checked'] += 1
                        text, why = q, 'replay'
                    elif not final:
                        text, why = q, 'replay (later changed again)'
                    else:
                        act.problems.append(f'{act.slug} {provision(num, key)}: the words of {eli} {x["provision"]} '
                                            f'differ from {m["ELI"]}; the unified text is used')
                if text is None:
                    if not final:
                        act.problems.append(f'{act.slug} {provision(num, key)}: the change by {eli} before '
                                            f'{steps[-1][1]["eli"]} is not reconstructed (no quoted wording)')
                        continue
                    text, why = restore_refs(b[1], last_text), 'footnote'
                add(eli, d, num, key, text, why, x['text'])
                last_text = text
                attributed[k] = eli
        # Lines that disappeared go with the unit above them, when that unit changed.
        for k in changed:
            if k in B:
                continue
            num, key = k
            parent = key
            owner = None
            while '/' in parent:
                parent = parent.rsplit('/', 1)[0]
                if (num, parent) in attributed:
                    owner = attributed[(num, parent)]
                    break
            if owner is None and any(v == 'editorial' and kk[0] == num for kk, v in attributed.items()):
                owner = 'editorial'      # the rest of a provision the unified text leaves out ("(pominięty)")
            if owner == 'editorial':
                editorial.append((num, key, None, 'omitted'))
            elif owner:
                ev = next(e for e in by_event.values() if e['eli'] == owner and any(c[1] == parent for c in e['changes']))
                ev['changes'].append((num, key, None))
                ev['why'][(num, key)] = 'removed with ' + provision(num, parent)
            else:
                unexplained.append((num, key, None))
        if unexplained and len(in_interval) > 1:
            # A line no footnote explains, whose words one (and only one) of the acts in force in the interval quotes
            # verbatim ("otrzymuje brzmienie: „...”", "dodaje się ... w brzmieniu: „...”"), is credited to that act:
            # e.g. a provision the previous unified text printed as not yet in force, so this one no longer footnotes.
            rest = []
            for num, key, text in unexplained:
                hits = sorted({e for e in in_interval if text and words_of(text) in quote_words(act, e)})
                if len(hits) == 1 and len(words_of(text)) >= 4:
                    add(hits[0], in_interval[hits[0]], num, key, restore_refs(text, (A.get((num, key)) or [None, None])[1]),
                        'quoted')
                    attributed[(num, key)] = hits[0]
                else:
                    rest.append((num, key, text))
            # The other lines of an article that is new in this unified text, when the lines of it that were credited
            # in this interval were all credited to one act (its heading, short points): they came with that article.
            by_num: dict[str, set] = {}
            for (n2, _k2), e2 in attributed.items():
                if e2 in in_interval:
                    by_num.setdefault(n2, set()).add(e2)
            unexplained = []
            for num, key, text in rest:
                owners = by_num.get(num, set())
                if num not in prev['files'] and len(owners) == 1 and text is not None:
                    (e2,) = owners
                    add(e2, in_interval[e2], num, key, text, 'with article')
                else:
                    unexplained.append((num, key, text))
        if unexplained:
            if len(in_interval) == 1:
                (eli, d), = in_interval.items()
                for num, key, text in unexplained:
                    add(eli, d, num, key, text, 'date only')
            else:
                act.events.append({'day': day, 'kind': 'unexplained', 'eli': None, 'tj': m['ELI'],
                                   'changes': unexplained, 'candidates': sorted(in_interval)})
                act.problems.append(f'{act.slug} {m["ELI"]}: {len(unexplained)} lines changed with no footnote')
        for ev in by_event.values():
            if ev['day'] > day:
                act.problems.append(f'{act.slug} {ev["eli"]}: in force {ev["day"]}, after the unified text {m["ELI"]} '
                                    f'of {day} that prints it')
            act.events.append(ev)
        for eli in sorted(in_interval):
            if eli not in {e['eli'] for e in by_event.values()}:
                act.problems.append(f'{act.slug} {eli} (in force {in_interval[eli]}): listed by the API, but no unit '
                                    f'of {m["ELI"]} is credited to it')
                act.events.append({'day': in_interval[eli], 'kind': 'law', 'eli': eli, 'changes': [], 'why': {},
                                   'glosses': {}, 'tj': m['ELI'], 'empty': True})
        # Everything still different on the day the unified text was published is the unified text's own doing.
        act.events.append({'day': day, 'kind': 'editorial', 'eli': m['ELI'], 'changes': editorial, 'tj': m['ELI'],
                           'ref': ref, 'final': snapshot(lines_of(cur)), 'final_order': cur['order']})
        act.checkpoints.append({'day': day, 'eli': m['ELI'], 'label': label_of(m), 'files': snapshot(lines_of(cur)),
                                'kind': 'pdf' if cur.get('pdf') else 'html', 'obwieszczenie': m['announcementDate'],
                                'what': 'tekst jednolity'})
        act.order.update(ref)
        prev, prev_meta, prev_day = cur, m, day
    for eli, d in sorted(amend.items()):
        if d and d > prev_day:
            act.problems.append(f'{act.slug} {eli} (in force {d}): after the last unified text; not in the record')
    act.tjs = tjs
    act.amend = amend


_QUOTES: dict[str, list] = {}
_QWORDS: dict[str, set] = {}


def words_of(s: str) -> tuple:
    """The words of a line, without its list marker, Journal references and punctuation."""
    return tuple(re.findall(r'\w+', DZU.sub('', s).translate(DASH)))


def quote_words(act: 'Act', eli: str) -> set:
    """words_of() of every unit an amending act quotes, anywhere in it."""
    if eli not in _QWORDS:
        quoted(act, eli, 'art. 0', '')        # parses and caches the act's units
        out = set()
        for a, _ in parse.walk_articles(_QUOTES.get(eli) or []):
            for _k, text in cite_lines(a):
                out.add(words_of(text))
        _QWORDS[eli] = out
    return _QWORDS[eli]


def quoted(act: Act, eli: str, prov: str | None, key: str) -> str | None:
    """The amending act's own words for the line `key`, when its provision quotes the unit."""
    meta = act.law(eli)
    if not meta.get('textHTML') or not prov:
        return None
    if eli not in _QUOTES:
        raw = src.text_html(eli)
        try:
            tree = parse.read_tree(raw)
            if not parse.walk_articles(tree['units']):
                tree = parse.read_tree(amending_article_html(raw))
            _QUOTES[eli] = tree['units']
        except (IndexError, ValueError):
            _QUOTES[eli] = []      # an old act whose HTML has no unit markup: no words to replay, the footnote is used
    u = provision_unit(_QUOTES[eli], prov)
    if u is None:
        return None
    for rk, t in cite_lines(u):
        if key == rk or key.endswith('/' + rk):
            return t
    return None


# ---------------------------------------------------------------- the Constitution

def build_constitution(act: Act):
    meta = act.meta
    raw = src.text_file(meta['ELI'], 'U', pdf_name(meta, 'U'))
    u = pdfparse.read_pdf(raw, set(), layout='u')
    final = lines_of(u)
    # Title and preamble: the lines before Art. 1 (letter-spaced title closed up; the preamble's two paragraphs).
    pre = [l['text'] for l in u['prelude']]
    title = [pdfparse.closed_up(l) for l in u['prelude'][:2]]
    head = ['# ' + ' '.join(title), pre[2]]
    body = pdfparse.join_lines(pre[3:], set())
    paras = re.split(r'(?<=wspólnot\.) ', body)
    final = {'preambula': [('title', head[0]), ('date', head[1])] + [(f'p{i + 1}', p) for i, p in enumerate(paras)],
             **{n: [(l[0], l[1]) for l in ls] for n, ls in final.items()}}
    act.final_u = final
    state = {n: list(ls) for n, ls in final.items()}
    # The 2009 amendment: art. 99 ust. 3 added. The 2006 amendment: art. 55 restated.
    amend = sorted(meta['references'].get('Akty zmieniające', []), key=lambda r: r['date'])
    events = []
    for r in reversed(amend):
        eli = r['id']
        m = act.law(eli)
        tree = parse.read_tree(src.text_html(eli))
        art1 = provision_unit(tree['units'], 'art. 1')
        q = cite_lines(art1)
        intro = ' '.join(b[1] for b in art1.body if not isinstance(b, parse.Unit) and b[0] == 'text')
        mnum = re.search(r'art\. (\d+)', intro)
        num = mnum.group(1)
        if 'otrzymuje brzmienie' in intro:
            new = [(k, t) for k, t in q]
            assert [l for l in state[num] if l[0].startswith('arti_')] == new, f'{eli}: quoted art. {num} differs from the U text'
            before = original_article(num)
            events.append({'day': r['date'], 'kind': 'law', 'eli': eli, 'num': num, 'before': before, 'after': new,
                           'why': 'replay'})
            state[num] = [l for l in state[num] if not l[0].startswith('arti_')] + before
        elif 'dodaje się' in intro:
            keys = [f'arti_{num}/{k}' for k, _ in q]
            got = [l for l in state[num] if l[0] in keys]
            assert got == [(f'arti_{num}/{k}', t) for k, t in q], f'{eli}: quoted text differs from the U text'
            events.append({'day': r['date'], 'kind': 'law', 'eli': eli, 'num': num, 'add': got, 'why': 'replay'})
            state[num] = [l for l in state[num] if l[0] not in keys]
        else:
            raise SystemExit(f'{eli}: amendment not understood: {intro}')
    # The printing correction of 2001: "w art. 31 w ust. 3 zamiast wyrazu „by” powinien być wyraz „być”".
    fixes = []
    for r in meta['references'].get('Sprostowanie', []):
        eli = r['id']
        m = act.law(eli)
        page = src.text_html(eli).decode('utf-8')
        page = re.sub(r'<script.*?</script>|<div id="toc">.*?</div>', ' ', page, flags=re.S)
        t = parse.clean(re.sub(r'\s*<[^>]+>\s*', ' ', page)).replace('„ ', '„').replace(' ”', '”')
        for a, p, wrong, right in re.findall(r'w art\. (\d+) w ust\. (\d+) zamiast wyrazu „([^”]+)” powinien być wyraz „([^”]+)”', t):
            key = f'arti_{a}/pass_{p}'
            line = dict(state[a])[key]
            hits = re.findall(rf'(?<!\w){re.escape(right)}(?!\w)', line)
            assert len(hits) == 1, f'{eli}: „{right}” occurs {len(hits)} times in art. {a} ust. {p}'
            old = re.sub(rf'(?<!\w){re.escape(right)}(?!\w)', wrong, line)
            fixes.append((a, key, old, line, wrong, right))
            state[a] = [(k, old if k == key else v) for k, v in state[a]]
        events.append({'day': m['promulgation'] or m['announcementDate'], 'kind': 'correction', 'eli': eli,
                       'fixes': fixes})
    act.events.append({'day': meta['entryIntoForce'], 'kind': 'start', 'eli': meta['ELI'], 'stage': None,
                       'ref': {n: [k for k, _ in ls] for n, ls in state.items()},
                       'changes': [(n, k, t) for n in sorted(state, key=num_order) for k, t in state[n]]})
    act.start_state = {n: list(ls) for n, ls in state.items()}
    for ev in sorted(events, key=lambda e: e['day']):
        if ev['kind'] == 'correction':
            act.events.append({'day': ev['day'], 'kind': 'correction', 'eli': ev['eli'], 'fixes': ev['fixes'],
                               'changes': [(a, key, new) for a, key, old, new, *_ in ev['fixes']]})
        elif 'before' in ev:
            ch = [(ev['num'], k, None) for k, _ in ev['before'] if k not in dict(ev['after'])]
            ch += [(ev['num'], k, t) for k, t in ev['after']]
            act.events.append({'day': ev['day'], 'kind': 'law', 'eli': ev['eli'], 'changes': ch,
                               'why': {(ev['num'], k): 'replay' for k, _ in ev['after']}, 'glosses': {},
                               'ref': {ev['num']: [k for k, _ in final[ev['num']]]}})
        else:
            act.events.append({'day': ev['day'], 'kind': 'law', 'eli': ev['eli'],
                               'changes': [(ev['num'], k, t) for k, t in ev['add']],
                               'why': {(ev['num'], k): 'replay' for k, _ in ev['add']}, 'glosses': {},
                               'ref': {ev['num']: [k for k, _ in final[ev['num']]]}})
    act.replay = {'lines': sum(len(e['changes']) for e in act.events if e['kind'] == 'law'),
                  'checked': sum(len(e['changes']) for e in act.events if e['kind'] == 'law')}
    act.checkpoints.append({'day': meta['entryIntoForce'], 'eli': meta['ELI'], 'label': act.label,
                            'kind': 'ocr', 'files': act.start_state,
                            'what': 'tekst ogłoszony (scan of the 1997 Journal, read word for word, OCR)'})
    act.checkpoints.append({'day': amend[-1]['date'], 'eli': meta['ELI'] + ' (U)', 'label': act.label + ' (tekst ujednolicony)',
                            'kind': 'pdf-u', 'files': final, 'what': 'tekst ujednolicony (Kancelaria Sejmu)'})
    act.order = {n: [k for k, _ in ls] for n, ls in final.items()}


def original_article(num: str) -> list[tuple[str, str]]:
    """An article as enacted in 1997, read from the Journal's scan (its text layer) between 'Art. N.' and the next
    article; the wording was checked against the page image by hand (REPRODUCE.md)."""
    import pymupdf
    meta = src.act('DU/1997/483')
    doc = pymupdf.open(stream=src.text_file('DU/1997/483', 'O', pdf_name(meta, 'O')), filetype='pdf')
    text = '\n'.join(p.get_text() for p in doc)
    m = re.search(rf'\nArt\. {num}\. *\n(.*?)\nArt\. {int(num) + 1}\. *\n', text, re.S)
    rows = [l.strip() for l in m.group(1).split('\n') if l.strip()]
    paras, cur = [], []
    for r in rows:
        if re.match(r'^\d+\. ', r) and cur:
            paras.append(cur)
            cur = []
        cur.append(r)
    paras.append(cur)
    out = [(f'arti_{num}', f'# Art. {num}.')]
    for p in paras:
        t = pdfparse.join_lines([x.replace('\u00ad', '-') for x in p], set())
        n = re.match(r'^(\d+)\. ', t).group(1)
        out.append((f'arti_{num}/pass_{n}', t))
    return out


# ---------------------------------------------------------------- git

def git(repo: Path, *args: str, env: dict | None = None, input: str | None = None) -> str:
    # Bytes, not text mode: on Windows text mode turns "\n" on stdin into "\r\n", which would put CRs into messages.
    out = subprocess.run(['git', *args], cwd=repo, capture_output=True, env=env,
                         input=input.encode('utf-8') if input is not None else None)
    if out.returncode:
        raise SystemExit(f'git {" ".join(args)} failed: {out.stderr.decode("utf-8", "replace")}')
    return out.stdout.decode('utf-8')


def last_sunday(year: int, month: int) -> dt.date:
    d = (dt.date(year, month + 1, 1) if month < 12 else dt.date(year + 1, 1, 1)) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def warsaw_offset(day: dt.date) -> int:
    """Hours ahead of UTC at noon in Warsaw (written out: this machine has no tz database). Central European Time;
    since 1996 summer time runs from the last Sunday in March to the last Sunday in October (EU rules, 2:00/3:00 UTC
    switch, so noon on the first day is summer time and noon on the last is winter time). Before 1996 Poland ended
    summer time on the last Sunday in September. Poland kept no summer time from 1965 to 1976, so those years are
    CET throughout (the codes' early amendments)."""
    y = day.year
    if y < 1977:
        return 1
    start = last_sunday(y, 3)
    end = last_sunday(y, 10 if y >= 1996 else 9)
    return 2 if start <= day < end else 1


def commit_date(day: str) -> str:
    d = dt.date.fromisoformat(day)
    off = warsaw_offset(d)
    stamp = int(dt.datetime(d.year, d.month, d.day, 12, tzinfo=dt.timezone(dt.timedelta(hours=off))).timestamp())
    return f'@{stamp} +0{off}00'


KIND_ORDER = {'start': 0, 'correction': 1, 'law': 2, 'unexplained': 3, 'editorial': 4}


def plan(acts: list[Act]) -> list[tuple[Act, dict]]:
    out = []
    for ai, a in enumerate(acts):
        for i, e in enumerate(a.events):
            out.append(((e['day'], ai, KIND_ORDER[e['kind']], eli_order(e['eli']) if e.get('eli') else (0, 0), i), a, e))
    out.sort(key=lambda x: x[0])
    return [(a, e) for _, a, e in out]


def wrap(s: str, width: int = 100) -> list[str]:
    out, cur = [], ''
    for w in s.split(' '):
        if cur and len(cur) + 1 + len(w) > width:
            out.append(cur)
            cur = w
        else:
            cur = f'{cur} {w}' if cur else w
    return out + ([cur] if cur else [])


def affected(act: Act, changes: list) -> list[str]:
    seen, out = set(), []
    for c in sorted(changes, key=lambda c: (num_order(c[0]), (act.order.get(c[0]) or []).index(c[1])
                                            if c[1] in (act.order.get(c[0]) or []) else 999, c[1])):
        num, key = c[0], c[1]
        p = provision(num, key)
        if key.endswith(('/t1',)) or key == f'arti_{num}':
            p = f'art. {shown(num)}'
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def message(act: Act, ev: dict) -> tuple[tuple[str, str], list[str], list[str]]:
    short = act.conf['short']
    day = ev['day']
    provs = affected(act, ev.get('changes', []))
    arts = []
    for p in provs:
        a = ' '.join(p.split(' ')[:2]) if p.startswith('art.') else p
        if a not in arts:
            arts.append(a)
    where = ', '.join(arts) if len(arts) <= 6 else f'{len(arts)} przepisów'
    tr = []
    if ev['kind'] == 'start':
        m = act.meta
        st = ev.get('stage')
        author = (act.label, email_of(m['ELI']))
        if st:
            msg = [f'{short}: {where} ({act.label}), pierwsza część', '', m['title'], '',
                   f'Część ustawy, która weszła w życie wcześniej niż reszta, zgodnie z jej przepisem o wejściu w życie',
                   f'({st["quote"]}).', '',
                   'The part of the act that took effect before the rest, as its own commencement provision says.', '']
            tr.append('Evidence: the act\'s own commencement provision, ' + st['quote'].split(':')[0])
        else:
            msg = [f'{short}: {act.label}' + (' (pozostałe przepisy)' if act.conf.get('stages') else ''), '', m['title'], '',
                   'Akt w brzmieniu ogłoszonym w Dzienniku Ustaw, w dniu wejścia w życie.', '',
                   'The act as published in the Journal of Laws, on the day it took effect.', '']
        tr += [f'Kind: {m["type"]}', f'Enacted: {m["announcementDate"]}']
        tr += [f'Published: {m.get("promulgation") or m["announcementDate"]} ({act.label})']
    elif ev['kind'] == 'law':
        m = act.law(ev['eli'])
        lab = label_of(m)
        author = (lab, email_of(ev['eli']))
        msg = [f'{short}: {where} ({lab})' if ev.get('changes') else f'{short}: bez zmiany tekstu ({lab})', '', m['title'], '']
        if provs:
            msg += wrap('Zmienione: ' + '; '.join(provs) + '.') + ['']
        whys = ev.get('why', {})
        n_replay = sum(1 for w in whys.values() if w.startswith('replay'))
        n_note = sum(1 for w in whys.values() if w == 'footnote')
        n_date = sum(1 for w in whys.values() if w == 'date only')
        n_quoted = sum(1 for w in whys.values() if w == 'quoted')
        n_with = sum(1 for w in whys.values() if w == 'with article')
        if n_with:
            msg += wrap(f'{n_with} wierszy (np. nagłówek artykułu) należy do artykułu dodanego tym aktem: pozostałe '
                        'wiersze tego artykułu przypisano temu aktowi, a artykułu nie było w poprzednim tekście '
                        'jednolitym.') + wrap(
                f'{n_with} lines (an article heading, for example) belong to an article this act added: the other '
                'lines of that article are credited to this act, and the article was not in the previous unified '
                'text.') + ['']
        if n_quoted:
            msg += wrap(f'{n_quoted} wierszy nie ma przypisu w tekście jednolitym; ich brzmienie znaleziono dosłownie '
                        'w tekście tego aktu i tylko tego spośród aktów, które weszły w życie między dwoma tekstami '
                        'jednolitymi.') + wrap(
                f'{n_quoted} lines carry no footnote in the unified text; their wording was found verbatim in this '
                'act\'s text, and in no other act that took effect between the two unified texts.') + ['']
            tr.append('Evidence: wording quoted verbatim by this act (no footnote) for ' + ', '.join(
                affected(act, [c for c in ev['changes'] if whys.get((c[0], c[1])) == 'quoted'])))
        if n_replay:
            msg += wrap(f'Brzmienie {n_replay} z {len(ev["changes"])} zmienionych wierszy pochodzi z tekstu tego aktu '
                        '(„otrzymuje brzmienie”, „w brzmieniu”) i zostało porównane z następnym tekstem jednolitym.') + \
                   wrap(f'The wording of {n_replay} of the {len(ev["changes"])} changed lines is the amending act\'s own '
                        'text, replayed and checked against the next unified text.') + ['']
        if n_note:
            msg += wrap(f'Brzmienie {n_note} wierszy pochodzi z tekstu jednolitego ({ev.get("tj")}), z odesłaniami do '
                        'Dziennika Ustaw w poprzednim brzmieniu.') + \
                   wrap(f'The wording of {n_note} lines is that of the unified text {ev.get("tj")}, with the Journal '
                        'references as they stood before; the unified text updated those itself (a separate commit).') + ['']
        if n_date:
            msg += wrap(f'{n_date} wierszy nie ma przypisu; przypisane tylko według daty: to jedyny akt zmieniający, który '
                        'wszedł w życie między dwoma tekstami jednolitymi.') + \
                   wrap(f'{n_date} lines carry no footnote: credited by date only, as the one amending act that took '
                        'effect between the two unified texts.') + ['']
            tr.append('Evidence: date only (the one amending act between two unified texts) for ' + ', '.join(
                affected(act, [c for c in ev['changes'] if whys.get((c[0], c[1])) == 'date only'])))
        if ev.get('empty'):
            msg += wrap('API Sejmu wymienia ten akt jako zmieniający, ale żaden przypis tekstu jednolitego nie wskazuje '
                        'zmienionego przez niego przepisu, a tekst się nie zmienił.') + \
                   wrap('The Sejm API lists this act as amending, but no footnote of the unified text names a provision '
                        'it changed, and the text did not change.') + ['']
        notes = sorted({g for g in ev.get('glosses', {}).values()})
        for g in notes:
            tr.append(f'Evidence: przypis tekstu jednolitego {ev.get("tj")}: {g}')
        if ev.get('changes') and any(w.startswith('replay') for w in whys.values()):
            tr.append('Evidence: the amending act\'s own words (cite), replayed')
        tr += [f'Kind: {m["type"]}', f'Enacted: {m["announcementDate"]}',
               f'Published: {m.get("promulgation") or m["announcementDate"]} ({lab})']
        if m.get('entryIntoForce') and m['entryIntoForce'] != day:
            tr.append(f'Act-in-force: {m["entryIntoForce"]}')
    elif ev['kind'] == 'correction':
        m = act.law(ev['eli'])
        lab = label_of(m)
        author = (f'{lab} (sprostowanie)', email_of(ev['eli']))
        msg = [f'{short}: {where} (sprostowanie błędów, {lab})', '', m['title'], '']
        for a, key, old, new, wrong, right in ev['fixes']:
            msg += [f'- {provision(a, key)}: „{wrong}” -> „{right}”']
        msg += [''] + wrap('Sprostowanie błędu w tekście ogłoszonym nie jest zmianą prawa: prostuje druk tak, by odpowiadał '
                           'tekstowi uchwalonemu. Commit ma datę ogłoszenia sprostowania.') + [''] + wrap(
            'A correction of printing errors is not an amendment: it brings the printed text into line with the text as '
            'adopted. The commit is dated the day the correction was published; it is not credited to a law.') + ['']
        tr += ['Kind: sprostowanie (correction of printing errors)', f'Published: {m["promulgation"]} ({lab})']
    elif ev['kind'] == 'editorial':
        m = act.law(ev['eli'])
        lab = label_of(m)
        author = (f'Marszałek Sejmu (tekst jednolity, {lab})', email_of(ev['eli']))
        msg = [f'{short}: tekst jednolity {lab}' + (f' ({where})' if ev.get('changes') else ''), '', m['title'], '']
        kinds = {w for *_, w in ev.get('changes', [])}
        if 'refs' in kinds:
            msg += wrap('Tekst jednolity aktualizuje odesłania do Dziennika Ustaw innych ustaw (nowe teksty '
                        'jednolite). To zmiana redakcyjna, a nie zmiana prawa.') + wrap(
                'The unified text updates the Journal references of the other acts it cites. That is an editorial '
                'change by the Marshal of the Sejm, not an amendment.') + ['']
        if 'punct' in kinds:
            msg += wrap('Tekst jednolity ujednolica znaki przestankowe (np. średnik zamiast przecinka na końcu punktu '
                        'wyliczenia); słowa się nie zmieniają. To zmiana redakcyjna, a nie zmiana prawa.') + wrap(
                'The unified text normalises punctuation (a semicolon instead of a comma at the end of a point of an '
                'enumeration, and the like); no word changes. That is an editorial change, not an amendment.') + ['']
        if 'omitted' in kinds:
            msg += wrap('Przepisy zmieniające inne ustawy tekst jednolity podaje jako „(pominięty)”.') + wrap(
                'Provisions that amended other acts are printed as "(pominięty)" (left out) in the unified text.') + ['']
        if not ev.get('changes'):
            msg += wrap('Tekst jednolity nie zmienia tu żadnego słowa: jest punktem kontrolnym.') + wrap(
                'The unified text changes no word here: it is a checkpoint.') + ['']
        msg += wrap(f'Obwieszczenie z dnia {m["announcementDate"]}, ogłoszone {m["promulgation"]}. Stan tekstu w tym '
                    f'commicie jest sprawdzony z tekstem jednolitym (tools/check_repo.py).') + ['']
        tr += ['Kind: tekst jednolity (editorial)', f'Enacted: {m["announcementDate"]}',
               f'Published: {m["promulgation"]} ({lab})']
    else:
        author = PUBLISHER
        m = act.law(ev['tj'])
        msg = [f'{short}: {where} (zmiana bez przypisu)', ''] + wrap(
            f'Tekst jednolity {label_of(m)} zmienia te wiersze, ale żaden przypis nie wskazuje aktu, który je zmienił. '
            'Commit nie jest przypisany żadnemu aktowi.') + [''] + wrap(
            f'The unified text {label_of(m)} changes these lines, but no footnote names the act that changed them, so '
            'the change is credited to no act.') + [''] + wrap(
            'Commit ma datę ogłoszenia tekstu jednolitego: zmiana weszła w życie najpóźniej tego dnia, a po dniu '
            'poprzedniego tekstu jednolitego; akty, które weszły w życie w tym okresie, są podane jako Candidate.') + wrap(
            'The commit is dated the day the unified text was published: the change took effect on or before that day '
            'and after the previous unified text; the acts that took effect in that period are listed as Candidate.') + ['']
        tr += [f'Candidate: {label_of(act.law(e))}' for e in ev.get('candidates', [])]
    tr.append(f'In-force: {day}')
    tr += [f'Affecting: {act.conf["short"]} {p}' for p in provs]
    if ev.get('eli'):
        tr.append(f'Source: {src.API}/acts/{ev["eli"]}')
    if ev['kind'] in ('law', 'editorial', 'unexplained') and ev.get('tj'):
        tr.append(f'Checkpoint: {src.API}/acts/{ev["tj"]}')
    return author, msg, tr


def write_file(repo: Path, slug: str, num: str, lines: list | None):
    path = repo / slug / file_name(num)
    if not lines:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(lines), encoding='utf-8', newline='\n')


def play(repo: Path, act: Act, ev: dict, st: dict) -> set:
    """Applies one event to the act's state and writes the files it touched."""
    touched = set()
    if ev['kind'] == 'editorial':
        # the unified text as published: every line (order included) becomes the checkpoint's
        why = {(c[0], c[1]): c[3] for c in ev['changes']}
        actual = []
        for num in sorted(set(st) | set(ev['final']), key=num_order):
            new = ev['final'].get(num)
            if st.get(num) != new:
                touched.add(num)
                old = dict(st.get(num) or [])
                nd = dict(new or [])
                for k in sorted(set(old) | set(nd)):
                    if old.get(k) != nd.get(k):
                        w = why.get((num, k)) or 'other'
                        if w == 'other' and old.get(k) and nd.get(k) and same_but_refs(old[k], nd[k]):
                            w = 'refs'
                        actual.append((num, k, nd.get(k), w))
                if not actual or actual[-1][0] != num:
                    actual.append((num, '', None, 'order'))
                if new:
                    st[num] = list(new)
                else:
                    st.pop(num, None)
        ev['changes'] = [c for c in actual if c[3] != 'order']
        other = [c for c in actual if c[3] == 'other']
        if other:
            act.problems.append(f'{act.slug} {ev["eli"]}: {len(other)} lines differ from the unified text for no '
                                f'reason found: ' + ', '.join(provision(c[0], c[1]) for c in other[:8]))
    else:
        for num, key, text in ev['changes']:
            ref = (ev.get('ref') or act.order).get(num) or act.order.get(num) or []
            apply(st, num, key, text, ref)
            touched.add(num)
    for num in sorted(touched, key=num_order):
        write_file(repo, act.slug, num, st.get(num))
    return touched


def write_repo(repo: Path, acts: list[Act], today: str) -> tuple[list[dict], dict]:
    remote = None
    if (repo / '.git').exists():
        out = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=repo, capture_output=True, text=True)
        remote = out.stdout.strip() or None

    def force(fn, path, _exc):
        os.chmod(path, 0o700)
        fn(path)
    if repo.exists():
        for p in repo.iterdir():
            shutil.rmtree(p, onexc=force) if p.is_dir() else p.unlink()
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, 'init', '-q', '-b', 'main')
    git(repo, 'config', 'core.autocrlf', 'false')
    if remote:
        git(repo, 'remote', 'add', 'origin', remote)
    states: dict[str, dict] = {a.slug: {} for a in acts}
    tags: dict[str, str] = {}
    law_days: dict[str, list] = {}
    log = []
    for act, ev in plan(acts):
        st = states[act.slug]
        touched = play(repo, act, ev, st)
        author, msg, trailers = message(act, ev)
        git(repo, 'add', '-A')
        when = commit_date(ev['day'])
        env = {**os.environ, 'GIT_AUTHOR_NAME': author[0], 'GIT_AUTHOR_EMAIL': author[1], 'GIT_AUTHOR_DATE': when,
               'GIT_COMMITTER_NAME': COMMITTER[0], 'GIT_COMMITTER_EMAIL': COMMITTER[1], 'GIT_COMMITTER_DATE': when}
        git(repo, 'commit', '-q', '--allow-empty', '--cleanup=verbatim', '-F', '-', env=env,
            input='\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n')
        head = git(repo, 'rev-parse', 'HEAD').strip()
        tags[f'{act.slug}/{ev["day"]}'] = head
        if ev['kind'] == 'editorial':
            tags[f'tj/{ev["eli"].split("/", 1)[1].replace("/", "-")}'] = head
        if ev.get('eli') and ev['kind'] in ('law', 'start', 'correction'):
            days = law_days.setdefault(ev['eli'], [])
            if days and days[-1][0] == ev['day']:
                days[-1] = (ev['day'], head)
            else:
                days.append((ev['day'], head))
        log.append({'day': ev['day'], 'slug': act.slug, 'kind': ev['kind'], 'eli': ev.get('eli'), 'author': author[0],
                    'lines': len(ev.get('changes', [])), 'files': len(touched)})
    for eli, days in law_days.items():
        if len(days) == 1:
            tags[tag_of(eli)] = days[0][1]
        else:
            for d, head in days:
                tags[f'{tag_of(eli)}/{d}'] = head
    for name, head in sorted(tags.items()):
        git(repo, 'tag', '-f', name, head)
    for p in sorted((HERE / 'repo').rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            dest = repo / p.relative_to(HERE / 'repo')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(p.read_bytes())
    for name in ('build.py', 'src.py', 'parse.py', 'pdfparse.py', 'gloss.py', 'reproduce.py', 'check_repo.py',
                 'test_repo.py'):
        (repo / 'tools' / name).write_bytes((HERE / name).read_bytes())
    write_tables(repo, acts)
    from reproduce import write_manifest, write_reproduce
    write_manifest(repo, acts, today)
    write_reproduce(repo, acts, log, tags, src.REQUESTS, today)
    git(repo, 'add', '-A')
    when = commit_date(today)
    env = {**os.environ, 'GIT_AUTHOR_NAME': COMMITTER[0], 'GIT_AUTHOR_EMAIL': COMMITTER[1], 'GIT_AUTHOR_DATE': when,
           'GIT_COMMITTER_NAME': COMMITTER[0], 'GIT_COMMITTER_EMAIL': COMMITTER[1], 'GIT_COMMITTER_DATE': when}
    git(repo, 'commit', '-q', '-F', '-', env=env, input='Dokumentacja, tabele, narzędzia i REPRODUCE.md\n\n'
        'Documentation, tables, tools and the record of how this repository was built. No law text changes.\n\n'
        f'Kind: documentation\nIn-force: {today}\n')
    return log, tags


def write_append(repo: Path, old_acts: list[Act], new_acts: list[Act], today: str) -> tuple[list[dict], dict]:
    """Grows the published history append-only: the clone's main must equal origin/main. First a labelled correction
    for any published act whose text on main differs from what this builder gives as its latest state (the published
    main carried errors from an earlier build; nothing on main is rewritten), then each new act as one block in
    in-force order, then a documentation commit. Author date: noon in Warsaw on the in-force day; committer date: the
    published head's committer time plus one second per appended commit, so committer dates never go backwards.
    Existing tags are never moved."""
    head = git(repo, 'rev-parse', 'HEAD').strip()
    if head != git(repo, 'rev-parse', 'origin/main').strip():
        raise SystemExit('main is not origin/main: fetch and check out origin/main first')
    if git(repo, 'status', '--porcelain', '--untracked-files=no').strip():
        raise SystemExit('the clone has uncommitted changes')
    base_ct = int(git(repo, 'log', '-1', '--format=%ct').strip())
    existing = set(git(repo, 'tag', '-l').split())
    seq = [0]
    log, tags = [], {}

    pre = [0]

    def commit(author, msg, trailers, day, path=None):
        if path is None or (repo / path).exists():
            git(repo, 'add', '-A', *(['--', path] if path else []))
        seq[0] += 1
        when = commit_date(day)
        if day < '1970-01-01':
            # git stores no date before 1970 (the codes of 1964): 1 January 1970, one second per commit, in order
            pre[0] += 1
            when = f'@{pre[0]} +0000'
            msg = list(msg) + wrap('Git nie zapisuje dat sprzed 1970 r., więc commit ma datę 1 stycznia 1970 r. (sekunda '
                                   'po poprzednim). Dzień wejścia w życie podaje trailer In-force.') + wrap(
                'Git cannot store a date before 1970, so this commit is dated 1 January 1970, a second after the one '
                'before it. The day the change took effect is in the In-force trailer.') + ['']
        env = {**os.environ, 'GIT_AUTHOR_NAME': author[0], 'GIT_AUTHOR_EMAIL': author[1],
               'GIT_AUTHOR_DATE': when, 'GIT_COMMITTER_NAME': COMMITTER[0],
               'GIT_COMMITTER_EMAIL': COMMITTER[1], 'GIT_COMMITTER_DATE': f'@{base_ct + seq[0]} +0100'}
        git(repo, 'commit', '-q', '--allow-empty', '--cleanup=verbatim', '-F', '-', env=env,
            input='\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n')
        return git(repo, 'rev-parse', 'HEAD').strip()

    # 1. Corrections of published acts: the files on main against this builder's latest state of the act.
    for a in old_acts:
        st: dict = {}
        for ev in sorted(a.events, key=lambda e: (e['day'], KIND_ORDER[e['kind']])):
            if ev['kind'] == 'editorial':
                st = {n: list(ls) for n, ls in ev['final'].items()}
            else:
                for num, key, text in ev['changes']:
                    apply(st, num, key, text, (ev.get('ref') or a.order).get(num) or a.order.get(num) or [])
        want = {file_name(n): render(ls) for n, ls in st.items()}
        d = repo / a.slug
        have = {f.name: f.read_text(encoding='utf-8') for f in d.glob('*.md') if f.name != 'README.md'}
        bad = sorted(n for n in set(want) | set(have) if want.get(n) != have.get(n))
        if not bad:
            continue
        for n in bad:
            if n in want:
                (d / n).write_text(want[n], encoding='utf-8', newline='\n')
            else:
                (d / n).unlink()
        last = max(e['day'] for e in a.events)
        names = ', '.join(n[:-3] for n in bad)
        msg = [f'{a.conf["short"]}: poprawka zapisu ({names})', ''] + wrap(
            'Poprawka błędu odczytu w tym repozytorium, a nie zmiana prawa. Pierwsza publikacja tej historii zawierała '
            'błędy odczytu tekstu (nagłówek rozdziału odczytany jako treść artykułu, połączone słowa tytułu). Ten commit '
            'przywraca tekst zgodny ze źródłem; wcześniejsze commity nie są przepisywane, więc stan na wcześniejszy '
            'dzień może w tych plikach zawierać błąd.') + [''] + wrap(
            'A correction of a reading error in this repository, not an amendment. The first publication of this '
            'history carried text-reading errors (a chapter heading read as the text of an article, the words of the '
            'title run together). This commit restores the text as the source has it; the history is append-only, so '
            'earlier commits are not rewritten, and the text as of an earlier day may still show the error in these '
            'files.') + ['']
        tr = ['Kind: correction (record)', f'Corrects: {a.conf["short"]} ' + names,
              f'Source: {src.API}/acts/{a.conf["eli"]}', f'In-force: {last}']
        commit(COMMITTER, msg, tr, today, a.slug)
        log.append({'day': today, 'slug': a.slug, 'kind': 'record-correction', 'eli': None, 'author': COMMITTER[0],
                    'lines': 0, 'files': len(bad)})
    # 2. New acts, one block each, in in-force order.
    law_days: dict[tuple, list] = {}
    for a in new_acts:
        if (repo / a.slug).exists():
            raise SystemExit(f'{a.slug} is already on main')
        st = {}
        for act, ev in plan([a]):
            touched = play(repo, act, ev, st)
            author, msg, trailers = message(act, ev)
            h = commit(author, msg, trailers, ev['day'], act.slug)
            tags[f'{act.slug}/{ev["day"]}'] = h
            if ev['kind'] == 'editorial':
                tags[f'tj/{ev["eli"].split("/", 1)[1].replace("/", "-")}'] = h
            if ev.get('eli') and ev['kind'] in ('law', 'start', 'correction'):
                days = law_days.setdefault((ev['eli'], act.slug), [])
                if days and days[-1][0] == ev['day']:
                    days[-1] = (ev['day'], h)
                else:
                    days.append((ev['day'], h))
            log.append({'day': ev['day'], 'slug': act.slug, 'kind': ev['kind'], 'eli': ev.get('eli'),
                        'author': author[0], 'lines': len(ev.get('changes', [])), 'files': len(touched)})
    taken = set(existing) | set(tags)
    for (eli, slug), days in law_days.items():
        name = tag_of(eli)
        if any(x == name or x.startswith(name + '/') for x in taken):
            name = f'{name}-{slug}'          # the amending act already has tags (another act it amends)
        taken.add(name)
        if len(days) == 1:
            tags[name] = days[0][1]
        else:
            for d, h in days:
                tags[f'{name}/{d}'] = h
    for name, h in sorted(tags.items()):
        if name in existing:
            print(f'tag {name} exists; not moved')
            continue
        git(repo, 'tag', name, h)
    # 3. Documentation.
    acts = old_acts + new_acts
    for d in list(repo.rglob('__pycache__')):      # bytecode from running the repository's own tools
        if '.git' not in d.parts:
            shutil.rmtree(d, ignore_errors=True)
    for p in sorted((HERE / 'repo').rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            dest = repo / p.relative_to(HERE / 'repo')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(p.read_bytes())
    for name in ('build.py', 'parse.py', 'pdfparse.py', 'gloss.py', 'reproduce.py', 'check_repo.py', 'test_repo.py'):
        (repo / 'tools' / name).write_bytes((HERE / name).read_bytes())
    write_tables(repo, acts)
    from reproduce import write_manifest, write_reproduce
    write_manifest(repo, acts, today)
    write_reproduce(repo, acts, log, tags, src.REQUESTS, today)
    commit(COMMITTER, ['Dokumentacja, tabele, narzędzia i REPRODUCE.md', '',
                       'Documentation, tables, tools and the record of how this repository was built. No law text '
                       'changes.', ''], ['Kind: documentation', f'In-force: {today}'], today)
    return log, tags


def write_tables(repo: Path, acts: list[Act]):
    import csv
    import io
    rows = []
    for a in acts:
        for e in a.events:
            if e['kind'] not in ('start', 'law', 'correction'):
                continue
            m = a.law(e['eli'])
            rows.append({'akt': a.conf['short'], 'adres': label_of(m), 'eli': e['eli'], 'tytul': m['title'],
                         'z_dnia': m['announcementDate'], 'ogloszony': m.get('promulgation') or '',
                         'w_zyciu_od': e['day'], 'wiersze': len(e.get('changes', [])),
                         'rodzaj': {'start': 'tekst ogłoszony', 'law': 'zmiana', 'correction': 'sprostowanie'}[e['kind']]})
    rows.sort(key=lambda r: (r['w_zyciu_od'], r['akt'], r['adres']))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    (repo / 'akty.csv').write_text(buf.getvalue(), encoding='utf-8', newline='\n')
    for a in acts:
        counts, last = {}, {}
        for e in a.events:
            if e['kind'] in ('law', 'correction'):
                for num in {c[0] for c in e.get('changes', [])}:
                    counts[num] = counts.get(num, 0) + 1
                    last[num] = e['day']
        final = a.checkpoints[-1]['files']
        out = [f'# {a.title}', '', f'{a.label} \u00b7 <{src.API}/acts/{a.conf["eli"]}>', '',
               '| Przepis | Plik | Zmiany | Ostatnia zmiana |', '| --- | --- | ---: | --- |']
        for num in sorted(final, key=num_order):
            name = 'Preambuła' if num == 'preambula' else f'Art. {num}'
            out.append(f'| {name} | [{file_name(num)}]({file_name(num)}) | {counts.get(num, 0)} | {last.get(num, "")} |')
        (repo / a.slug / 'README.md').write_text('\n'.join(out) + '\n', encoding='utf-8', newline='\n')


def data_day() -> str:
    files = [p for p in src.CACHE.iterdir() if p.name != '.gitignore'] if src.CACHE.exists() else []
    if not files:
        return dt.date.today().isoformat()
    return dt.date.fromtimestamp(max(p.stat().st_mtime for p in files)).isoformat()


def build_all(offline: bool) -> list[Act]:
    src.OFFLINE[0] = offline
    acts = []
    for conf in ACTS:
        a = Act(conf)
        if conf['kind'] == 'constitution':
            build_constitution(a)
        else:
            build_unified(a)
        acts.append(a)
    return acts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(ROOT.parent / 'poland-law'))
    ap.add_argument('--offline', action='store_true')
    ap.add_argument('--today', default=None)
    ap.add_argument('--verify-rebuild', action='store_true')
    ap.add_argument('--append', default=None,
                    help='comma-separated slugs of CODES to append on top of the published main (append-only)')
    args = ap.parse_args()
    if args.append:
        src.OFFLINE[0] = args.offline
        old = [Act(c) for c in ACTS]
        for a in old:
            build_constitution(a) if a.conf['kind'] == 'constitution' else build_unified(a)
        new = []
        for slug in [s for s in args.append.split(',') if s and s != 'none']:
            a = Act(next(c for c in CODES if c['slug'] == slug))
            build_unified(a)
            n = sum(len(e.get('changes', [])) for e in a.events if e['kind'] == 'law')
            print(f'{a.slug}: {len(a.events)} events, {len(a.checkpoints)} checkpoints, {n} law line changes, replay '
                  f'{a.replay["checked"]}/{a.replay["lines"]}; {len(a.problems)} notes')
            for p in a.problems:
                print('   ', p)
            new.append(a)
        log, tags = write_append(Path(args.repo), old, new, args.today or dt.date.today().isoformat())
        print(f'appended {len(log)} commits + 1 documentation commit, {len(tags)} new tags -> {args.repo}')
        return
    if args.verify_rebuild:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = subprocess.run([sys.executable, '-X', 'utf8', str(HERE / 'build.py'), '--offline', '--repo', tmp]
                                 + (['--today', args.today] if args.today else []), capture_output=True, text=True)
            if out.returncode:
                raise SystemExit(out.stderr)

            def hashes(r):
                log = git(Path(r), 'log', '--format=%H', 'main').split()
                tags = dict(l.split(' ', 1)[::-1] for l in git(Path(r), 'show-ref', '--tags').split('\n') if l)
                return log, tags
            a, b = hashes(args.repo), hashes(tmp)
            same = a[0][1:] == b[0][1:]
            rec = {'identical': same and a[1] == b[1], 'history_tip': a[0][1], 'commits': len(a[0]) - 1,
                   'tags': len(a[1]), 'main_identical': a[0][0] == b[0][0], 'main': a[0][0], 'rebuilt_main': b[0][0]}
            print(json.dumps(rec, indent=1))
            p = HERE / 'verification.json'
            ver = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
            ver['rebuild'] = {k: rec[k] for k in ('identical', 'history_tip', 'commits', 'tags')}
            p.write_text(json.dumps(ver, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
            for f in Path(tmp).rglob('*'):
                os.chmod(f, 0o700)
            raise SystemExit(0 if rec['identical'] else 1)
    acts = build_all(args.offline)
    today = args.today or data_day()
    for a in acts:
        n = sum(len(e.get('changes', [])) for e in a.events if e['kind'] == 'law')
        print(f'{a.slug}: {len(a.events)} events, {len(a.checkpoints)} checkpoints, {n} law line changes, replay '
              f'{a.replay["checked"]}/{a.replay["lines"]}; {len(a.problems)} notes')
        for p in a.problems:
            print('   ', p)
    log, tags = write_repo(Path(args.repo), acts, today)
    print(f'repo: {len(log)} commits + 1 documentation commit, {len(tags)} tags -> {args.repo}')


if __name__ == '__main__':
    main()
