"""Reads an act's text from a PDF of the Journal of Laws (Dziennik Ustaw) or of the Sejm's own consolidated text
(tekst ujednolicony, ISAP), into the same keyed lines as parse.read_html.

Each unit of Polish legislation starts on a new printed line with its label: "Art. 12." (bold), "3." (ustęp,
indented), "4)" (punkt), "b)" (litera); a line that starts with none of these continues the unit before it. Running
heads and page numbers are removed by their content; footnote markers are superscript spans and footnote texts are
the small-type lines at the foot of a page: both are kept apart from the text, as with the HTML. A word broken at the
end of a line is joined again; the hyphen is kept only when the word is printed with a hyphen elsewhere in the act's
HTML texts, or when the hyphen is repeated at the start of the next line (the Polish rule for compounds).
"""
from __future__ import annotations

import re

import pymupdf

from parse import INDENT, clean

_H = r'(Dziennik Ustaw|[\u2013-] ?\d+ ?[\u2013-]|Poz\. \d+|\u00a9 ?Kancelaria Sejmu|s\. \d+/\d+|\d{4}-\d{2}-\d{2})'
HEAD = re.compile(rf'^{_H}( {_H})*$')
ART = re.compile(r'^Art\. (\d+[a-z]*)\. ?')
PASS = re.compile(r'^(\d+[a-z]*)\. ')
PINT = re.compile(r'^(\d+[a-z]*)\) ?')
LETT = re.compile(r'^([a-z]{1,2})\) ')
CHPT = re.compile(r'^Rozdział ([0-9IVXLC]+[a-z]*)$')
DASHES = str.maketrans({'\u2212': '-', '\u2013': '-', '\u2011': '-', '\u2010': '-'})


def visual_lines(doc, max_x: float = 10000) -> list[dict]:
    """Every printed line: text (footnote markers removed), x0, bold start, size, the markers, page."""
    out = []
    for pno, page in enumerate(doc):
        rows = []
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                for s in l['spans']:
                    if s['bbox'][0] > max_x:
                        continue
                    rows.append((round(l['bbox'][1]), s['bbox'][0], s))
        rows.sort(key=lambda r: (r[0], r[1]))
        merged: list[list] = []
        for y, x, s in rows:
            if merged and abs(merged[-1][0] - y) <= 2:
                merged[-1][1].append(s)
            else:
                merged.append([y, [s]])
        for y, spans in merged:
            spans.sort(key=lambda s: s['bbox'][0])
            text, marks = '', []
            body = [s for s in spans if s['text'].strip()]
            if not body:
                continue
            size = max(s['size'] for s in body)
            for s in spans:
                if s['flags'] & 1 and s['text'].strip() and s['size'] < size - 0.5:   # superscript: a footnote marker
                    marks.append(s['text'].strip().rstrip(')'))
                    continue
                text += s['text']
            out.append({'page': pno, 'y': y, 'x0': body[0]['bbox'][0], 'x1': body[-1]['bbox'][2], 'size': size,
                        'bold': bool(body[0]['flags'] & 16), 'text': clean(text), 'marks': marks,
                        'small': size < 9.5 and not any(s['size'] >= 9.5 for s in body)})
    return out


def join_lines(parts: list[str], vocab: set[str]) -> str:
    s = ''
    for p in parts:
        if not s:
            s = p
            continue
        m = re.search(r'(\w+)[-\u00ad]$', s)
        if m and p[:1].isalpha():
            nxt = re.match(r'[\w]+', p).group(0)
            if f'{m.group(1)}-{nxt}' in vocab:
                s = s + p
            else:
                s = s[:-1] + p
        elif m and p.startswith('-'):
            s = s + p[1:]
        else:
            s = s + ' ' + p
    return clean(s)


def read_pdf(raw: bytes, vocab: set[str], start: str | None = None, layout: str = 'du') -> dict:
    """{'files', 'order', 'glosses'} like parse.read_html. `start` is text that opens the act (the annex of a unified
    text); everything before it is skipped."""
    doc = pymupdf.open(stream=raw, filetype='pdf')
    lines = visual_lines(doc, 470 if layout == 'u' else 10000)
    glosses: dict[str, str] = {}
    body = []
    cur_note = None
    left = min(l['x0'] for l in lines if not l['small'])
    for l in lines:
        t = l['text']
        if not t or HEAD.match(t):
            continue
        if layout == 'u' and l['x0'] > 470:          # the margin note of the Sejm's consolidated text
            continue
        if l['small']:
            m = re.match(r'^(\d+)\) ?(.*)$', t)
            if m and l['x0'] < left + 30:
                cur_note = m.group(1)
                glosses[cur_note] = m.group(2)
            elif cur_note:
                glosses[cur_note] = join_lines([glosses[cur_note], t], vocab)
            continue
        cur_note = None
        body.append(l)
    if start:
        for i, l in enumerate(body):
            if l['text'].startswith(start):
                body = body[i:]
                break
    files: dict[str, dict] = {}
    order: list[str] = []
    units: list[dict] = []          # {'key', 'kind', 'parts', 'marks', 'file'}
    heads: list[dict] = []
    stack: dict[str, str] = {}      # kind -> key of the open unit
    art = [None]
    chapter = [None]
    prelude: list[dict] = []

    def new(key, kind, text, marks, file):
        u = {'key': key, 'kind': kind, 'parts': [text] if text else [], 'marks': list(marks), 'file': file}
        units.append(u)
        return u

    cur = [None]
    for i, l in enumerate(body):
        t = l['text']
        indented = l['x0'] > left + 8
        m = ART.match(t)
        if m and (l['bold'] or layout == 'u'):
            num = m.group(1)
            art[0] = num
            order.append(num)
            files[num] = {'label': f'Art. {num}', 'lines': []}
            for h in heads:
                h['file'] = num
            heads.clear()
            key = f'arti_{num}'
            stack.clear()
            stack['arti'] = key
            new(key, 'arti-head', f'# Art. {num}.', l['marks'], num)
            rest = t[m.end():]
            mp = PASS.match(rest)
            if mp:
                stack['pass'] = f'{key}/pass_{mp.group(1)}'
                cur[0] = new(stack['pass'], 'pass', rest, [], num)
            else:
                cur[0] = new(f'{key}/t1', 'text', rest, [], num) if rest else None
                stack['text'] = f'{key}/t1'
            continue
        m = CHPT.match(t)
        if m and art[0] is not None or (m and l['x0'] > left + 100):
            chapter[0] = m.group(1)
            ck = f'chpt_{m.group(1)}'
            h = new(f'{ck}/h0', 'head', '## ' + t, l['marks'], None)
            heads.append(h)
            # the chapter title follows on the next line (bold, centred)
            cur[0] = None
            stack.clear()
            stack['chpt'] = ck
            continue
        if stack.get('chpt') and not stack.get('arti') and l['bold'] and l['x0'] > left + 40:
            h = new(f'{stack["chpt"]}/h{sum(1 for x in heads)}', 'head', '## ' + t, l['marks'], None)
            heads.append(h)
            continue
        if art[0] is None:
            prelude.append(l)
            continue
        if l['bold'] and l['x0'] > left + 40 and not ART.match(t):
            # an unnumbered heading inside a chapter (the Constitution's "Wybory i kadencja")
            key = f'{stack.get("chpt", "chpt_x")}/s_{len(units)}'
            h = new(key, 'head', '## ' + t, l['marks'], None)
            heads.append(h)
            cur[0] = None
            stack.pop('arti', None)
            continue
        a = f'arti_{art[0]}'
        mp, mi, ml = PASS.match(t), PINT.match(t), LETT.match(t)
        if mp and indented and 'arti' in stack:
            stack['pass'] = f'{a}/pass_{mp.group(1)}'
            for k in ('pint', 'lett'):
                stack.pop(k, None)
            cur[0] = new(stack['pass'], 'pass', t, l['marks'], art[0])
        elif mi and 'arti' in stack:
            parent = stack.get('pass') or a
            stack['pint'] = f'{parent}/pint_{mi.group(1)}'
            stack.pop('lett', None)
            cur[0] = new(stack['pint'], 'pint', f'{mi.group(1)}) {t[mi.end():]}'.rstrip(), l['marks'], art[0])
        elif ml and 'arti' in stack and (stack.get('pint') or stack.get('pass')):
            parent = stack.get('pint') or stack.get('pass')
            stack['lett'] = f'{parent}/lett_{ml.group(1)}'
            cur[0] = new(stack['lett'], 'lett', t, l['marks'], art[0])
        elif t[:1] in '-\u2013\u2212' and t[1:2] == ' ' and 'arti' in stack and (stack.get('pint') or stack.get('lett')):
            # the words after a list (część wspólna) belong to the unit that opened the list
            owner = stack.get('pass') or a
            if stack.get('lett') and stack.get('pint') and l['x0'] > left + 15:
                owner = stack['pint']
            n = sum(1 for u in units if u['key'].startswith(owner + '/w')) + 1
            kind = 'pass' if owner.rsplit('/', 1)[-1].startswith('pass') else 'pint' if '/pint_' in owner.rsplit('/', 1)[-1] else 'text'
            cur[0] = new(f'{owner}/w{n}', 'wsp-' + kind, t, l['marks'], art[0])
            stack.pop('pint', None) if owner == (stack.get('pass') or a) else None
            stack.pop('lett', None)
        else:
            if cur[0] is None:
                cur[0] = new(f'{a}/t1', 'text', t, l['marks'], art[0])
            else:
                cur[0]['parts'].append(t)
                cur[0]['marks'] += l['marks']
    for u in units:
        text = join_lines(u['parts'], vocab)
        if u['kind'] in ('pint', 'lett', 'pass'):
            text = INDENT[u['kind']] + text
        elif u['kind'].startswith('wsp-'):
            text = INDENT.get(u['kind'][4:], '') + text
        u['text'] = text
        if u['file']:
            files[u['file']]['lines'].append((u['key'], text, [(m, glosses.get(m, '')) for m in u['marks']], []))
    return {'files': files, 'order': order, 'glosses': glosses, 'prelude': prelude, 'units': units}


def words(s: str) -> list[str]:
    """Words for a comparison across sources: dashes unified, markdown marks and spacing dropped."""
    s = s.translate(DASHES)
    s = re.sub(r'(?m)^(#+ |\s*- )', '', s)
    return re.findall(r'[^\s]+', s)
