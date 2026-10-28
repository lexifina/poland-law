"""Reads an act's text from the Sejm API's HTML (text.html).

The API's HTML marks every unit of an act: `div.unit.unit_<kind>` with a `data-id` such as `arti_30`, `pass_1`,
`pint_7`, `lett_a`, a heading (`h3`, the unit's number) and a body (`div.unit-inner`) holding text blocks
(`div[data-template=xText]`), quoted text (`div.cite-box`) and the units below it. Footnotes (`a.gloss-link`) are the
unified text's notes ("W brzmieniu ustalonym przez art. 29 pkt 1 ustawy ..."): they are not part of the text; they are
kept with the unit they are attached to, as evidence of which act set its wording.

`read_tree` gives the units as a tree; `read_html` turns the act into files, one per article, of keyed lines.
"""
from __future__ import annotations

import re

from lxml import html as lhtml

INDENT = {'pass': '', 'pint': '- ', 'lett': '  - ', 'tirt': '    - '}
_WS = re.compile(r'[\s\u00a0\u00ad]+')


def clean(s: str) -> str:
    """Runs of white space (and no-break spaces) become one space; soft hyphens go."""
    return _WS.sub(' ', s.replace('\u00ad', ' ')).strip()


def has_class(e, c: str) -> bool:
    return c in (e.get('class') or '').split()


def flat(e) -> tuple[str, list[tuple[str, str]]]:
    """The text of an element without footnote markers, and the footnotes it carries as (number, text)."""
    glosses: list[tuple[str, str]] = []
    parts: list[str] = []

    def walk(x):
        if not isinstance(x.tag, str):
            if x.tail:
                parts.append(x.tail)
            return
        if has_class(x, 'gloss-link'):
            tip = x.xpath('.//span[contains(@class,"pro-gloss-inner")]')
            num = x.xpath('./sup')
            glosses.append((clean(num[0].text_content()).rstrip(')') if num else '',
                            clean(tip[0].text_content()) if tip else ''))
            if x.tail:
                parts.append(x.tail)
            return
        if x.tag == 'br':
            parts.append(' ')
        if x.text:
            parts.append(x.text)
        for c in x:
            walk(c)
        if x.tail:
            parts.append(x.tail)
    if e.text:
        parts.append(e.text)
    for c in e:
        walk(c)
    return clean(''.join(parts)), glosses


def unit_kind(e) -> str | None:
    if not isinstance(e.tag, str) or e.tag != 'div' or not has_class(e, 'unit'):
        return None
    for c in (e.get('class') or '').split():
        if c.startswith('unit_'):
            return c[5:]
    return None


class Unit:
    __slots__ = ('kind', 'id', 'label', 'glosses', 'body')

    def __init__(self, kind, id_, label, glosses):
        self.kind, self.id, self.label, self.glosses = kind, id_, label, glosses
        self.body: list = []        # ('text', str, glosses) | ('cite', str, glosses, [Unit]) | Unit

    def units(self):
        return [b for b in self.body if isinstance(b, Unit)]

    def __repr__(self):
        return f'Unit({self.kind} {self.id} {self.label!r})'


def build_unit(e) -> Unit:
    kind = unit_kind(e)
    heads = [c for c in e if isinstance(c.tag, str) and c.tag in ('h3', 'p')]
    label_parts, glosses = [], []
    for h in heads:
        t, g = flat(h)
        if t:
            label_parts.append(t)
        glosses += g
    u = Unit(kind, e.get('data-id'), label_parts if kind == 'chpt' else ' '.join(label_parts), glosses)
    inner = [c for c in e if isinstance(c.tag, str) and c.tag == 'div' and has_class(c, 'unit-inner')]
    for c in (list(inner[0]) if inner else []):
        add_body(u.body, c)
    return u


def add_body(body: list, c):
    if not isinstance(c.tag, str):
        return
    if unit_kind(c):
        body.append(build_unit(c))
    elif has_class(c, 'cite-box'):
        t, g = flat(c)
        inner = []
        for cb in c.xpath('./div[@class="cite-body"]'):
            for x in cb:
                if unit_kind(x):
                    inner.append(build_unit(x))
        body.append(('cite', t, g, inner))
    elif c.get('data-template') == 'xText' or has_class(c, 'pro-text'):
        t, g = flat(c)
        if t:
            body.append(('text', t, g))
    else:
        for x in c:
            add_body(body, x)


def act_part(doc):
    """The section holding the act: the annex of a unified text (Załącznik), else the first part."""
    parts = doc.xpath('//div[@class="parts"]/section')
    for p in parts:
        h = p.xpath('.//h2')
        if h and clean(h[0].text_content()).startswith('Załącznik'):
            return p
    return parts[0]


def read_tree(raw: bytes) -> dict:
    doc = lhtml.fromstring(raw.decode('utf-8'))
    part = act_part(doc)
    top: list = []
    U = 'contains(concat(" ", @class, " "), " unit ")'
    for c in part.xpath(f'.//div[{U} and not(ancestor::div[{U}])]'):
        if unit_kind(c) not in ('none', None):
            add_body(top, c)
    head = doc.xpath('//h1')
    gloss = {}
    for g in doc.xpath('//div[@class="gloss"]|//DIV[@class="gloss"]'):
        ds = [x for x in g if isinstance(x.tag, str)]
        if len(ds) >= 2:
            gloss[clean(ds[0].text_content()).rstrip(')')] = clean(ds[1].text_content())
    return {'units': top, 'title': clean(head[0].text_content()) if head else '', 'glosses': gloss,
            'parts': [clean(h.text_content()) for h in doc.xpath('//h2[@class="part"]')]}


def walk_articles(units: list):
    """(article Unit, the chapter headings that open it) in order, through chapters, branches and parts."""
    pending: list = []
    out = []

    def go(us):
        for u in us:
            if not isinstance(u, Unit):
                continue
            if u.kind == 'arti':
                out.append((u, list(pending)))
                pending.clear()
            else:
                if u.kind in ('chpt', 'bran', 'part', 'titl', 'sect', 'dvsn'):
                    labels = u.label if isinstance(u.label, list) else [u.label]
                    for i, t in enumerate(labels):
                        if t:
                            pending.append((f'{u.id}/h{i}', '## ' + t, u.glosses if i == 0 else []))
                go(u.units())
    go(units)
    return out


def unit_lines(u: Unit, path: str, inherited: list) -> list[tuple[str, str, list, list]]:
    """(key, text, own glosses, glosses of the units above) for a unit below an article and everything inside it."""
    key = f'{path}/{u.id}'
    out = []
    own = []
    gl = list(u.glosses)
    started = False
    n_after = 0
    for b in u.body:
        if isinstance(b, Unit):
            if not started:
                out.append((key, INDENT.get(u.kind, '') + ' '.join([u.label] + own).strip(), gl, inherited))
                started = True
            out += unit_lines(b, key, inherited + [gl])
        else:
            if started:
                n_after += 1
                out.append((f'{key}/w{n_after}', INDENT.get(u.kind, '') + b[1], list(b[2]), inherited + [gl]))
            else:
                own.append(b[1])
                gl = gl + list(b[2])
    if not started:
        out.append((key, INDENT.get(u.kind, '') + ' '.join([u.label] + own).strip(), gl, inherited))
    return out


def article_lines(a: Unit, heads: list) -> list[tuple[str, str, list, list]]:
    out = [(k, t, g, []) for k, t, g in heads]
    out.append((a.id, '# ' + a.label, list(a.glosses), []))
    n = 0
    for b in a.body:
        if isinstance(b, Unit):
            out += unit_lines(b, a.id, [a.glosses])
        else:
            n += 1
            out.append((f'{a.id}/t{n}', b[1], list(b[2]), [a.glosses]))
    return out


def read_html(raw: bytes) -> dict:
    """{'files': {num: {'label', 'lines': [(key, text, glosses, inherited glosses)]}}, 'order', 'title', 'glosses'}"""
    tree = read_tree(raw)
    files, order = {}, []
    for a, heads in walk_articles(tree['units']):
        num = a.id.split('_', 1)[1]
        files[num] = {'label': a.label.rstrip('.'), 'lines': article_lines(a, heads)}
        order.append(num)
    return {'files': files, 'order': order, 'title': tree['title'], 'glosses': tree['glosses'], 'tree': tree}


def render(lines) -> str:
    return '\n\n'.join(l[1] for l in lines) + '\n'
