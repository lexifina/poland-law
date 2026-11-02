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
# Superscript numbers ("Art. 7<sup>1</sup>", "§ 2<sup>1</sup>", "art. 21<sup>1</sup>" in the text) are written as
# Unicode superscripts (7¹), as Polish typography prints them; without this "art. 21¹" would read "art. 211".
SUP = str.maketrans('0123456789abcdefghijklmnoprstuvwxyz', '⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻ')


def sup_text(e) -> str:
    """text_content() with superscripts as Unicode superscripts."""
    out = []

    def walk(x):
        if not isinstance(x.tag, str):
            out.append(x.tail or '')
            return
        if x.tag == 'sup':
            out.append(x.text_content().strip().translate(SUP))
        else:
            out.append(x.text or '')
            for c in x:
                walk(c)
        out.append(x.tail or '')
    out.append(e.text or '')
    for c in e:
        walk(c)
    return ''.join(out)


def clean(s: str) -> str:
    """Runs of white space (and no-break spaces) become one space; soft hyphens go."""
    return _WS.sub(' ', s.replace('\u00ad', ' ')).strip()


def has_class(e, c: str) -> bool:
    return c in (e.get('class') or '').split()


UNTIL = re.compile(r'obowiązuje do (dnia )?wejścia w życie')


def flat(e, body: bool = False) -> tuple[str, list[tuple[str, str]]]:
    """The text of an element without footnote markers, and the footnotes it carries as (number, text).

    In a unified text a sentence that a later act will change is printed twice: the wording in force, with a footnote
    "w tym brzmieniu obowiązuje do wejścia w życie zmiany, o której mowa w odnośniku N", then the future wording in
    bold with footnote N. With body=True (the text blocks of a unit) the bold future wording and its footnote are left
    out, so the unified text reads as it stood on its own day; the next unified text prints the change as in force."""
    glosses: list[tuple[str, str]] = []
    parts: list[str] = []
    state = {'until': False, 'skip_gloss': False}

    def walk(x):
        if not isinstance(x.tag, str):
            if x.tail:
                parts.append(x.tail)
            return
        if has_class(x, 'gloss-link'):
            tip = x.xpath('.//span[contains(@class,"pro-gloss-inner")]')
            num = x.xpath('./sup')
            g = (clean(num[0].text_content()).rstrip(')') if num else '', clean(sup_text(tip[0])) if tip else '')
            if state['skip_gloss']:
                state['skip_gloss'] = False
            else:
                glosses.append(g)
                state['until'] = bool(body and UNTIL.search(g[1]))
            if x.tail:
                parts.append(x.tail)
                if x.tail.strip():
                    state['until'] = False
            return
        if body and state['until'] and x.tag == 'b' and has_class(x, 'b'):
            state['until'], state['skip_gloss'] = False, True
            if x.tail:
                parts.append(x.tail)
            return
        if x.tag == 'br':
            parts.append(' ')
        if x.tag == 'sup':
            parts.append(x.text_content().strip().translate(SUP))
            if x.tail:
                parts.append(x.tail)
            return
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


TJ = [False]     # reading a unified text: leave out the wording it prints for the future (see flat, future_block)


DROPPED: list = []     # the elements left out as future wording by the last read_tree (check_repo reads them)
CONTAINERS = ('chpt', 'bran', 'part', 'titl', 'sect', 'dvsn', 'schp', 'book')


def _words(e, bold_only: bool) -> list[str]:
    out = []

    def walk(x, bold):
        if not isinstance(x.tag, str):
            if x.tail and (bold or not bold_only):
                out.append(x.tail)
            return
        if has_class(x, 'gloss-link'):
            if x.tail and (bold or not bold_only):
                out.append(x.tail)
            return
        b = bold or (x.tag == 'b' and has_class(x, 'b'))
        if x.text and (b or not bold_only):
            out.append(x.text)
        for c in x:
            walk(c, b)
        if x.tail and (bold or not bold_only):
            out.append(x.tail)
    if e.text and not bold_only:
        out.append(e.text)
    for c in e:
        walk(c, False)
    return re.findall(r'\w+', ' '.join(out))


def future_block(c, leaf: bool = True) -> bool:
    """A text block a unified text prints wholly in bold: a provision that is not in force yet on the unified text's
    day (an act already published adds or restates it later: "Prosta spółka akcyjna może być utworzona ..." in the
    Commercial Companies Code of 2020, in force from 2021). Inside an article (leaf=True) any wholly bold block is
    such; between articles (a chapter's own text) a bold line is a heading ("Zarząd spółki") unless it ends as a
    sentence."""
    words = _words(c, False)
    if not words or _words(c, True) != words:
        return False
    if leaf:
        return True
    last = clean(c.text_content())
    return last[-1:] in '.;:,'


class Unit:
    __slots__ = ('kind', 'id', 'label', 'glosses', 'body', 'future')

    def __init__(self, kind, id_, label, glosses):
        self.kind, self.id, self.label, self.glosses = kind, id_, label, glosses
        self.future = False
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
    dropped = [0]
    for c in (list(inner[0]) if inner else []):
        add_body(u.body, c, dropped, kind not in CONTAINERS)
    # every block of the unit was future wording: the unit itself is not in force yet
    u.future = bool(dropped[0]) and not any(isinstance(b, Unit) or b[0] in ('text', 'cite') for b in u.body)
    return u


def add_body(body: list, c, dropped: list | None = None, leaf: bool = False):
    if not isinstance(c.tag, str):
        return
    if unit_kind(c):
        u = build_unit(c)
        if u.future:
            DROPPED.append(c)
            if dropped is not None:
                dropped[0] += 1
        else:
            body.append(u)
    elif has_class(c, 'cite-box'):
        t, g = flat(c)
        inner = []
        for cb in c.xpath('./div[@class="cite-body"]'):
            for x in cb:
                if unit_kind(x):
                    inner.append(build_unit(x))
        body.append(('cite', t, g, inner))
    elif c.get('data-template') == 'xText' or has_class(c, 'pro-text'):
        if TJ[0] and future_block(c, leaf):
            DROPPED.append(c)
            if dropped is not None:
                dropped[0] += 1
            return
        t, g = flat(c, body=TJ[0])
        if t:
            body.append(('text', t, g))
    else:
        for x in c:
            add_body(body, x, dropped, leaf)


def act_part(doc):
    """The section holding the act: the annex of a unified text (Załącznik), else the first part."""
    parts = doc.xpath('//div[@class="parts"]/section')
    for p in parts:
        h = p.xpath('.//h2')
        if h and clean(h[0].text_content()).startswith('Załącznik'):
            return p
    return parts[0]


def read_tree(raw: bytes | None, doc=None) -> dict:
    DROPPED.clear()
    if doc is None:
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
            gloss[clean(ds[0].text_content()).rstrip(')')] = clean(sup_text(ds[1]))
    return {'units': top, 'title': clean(head[0].text_content()) if head else '', 'glosses': gloss,
            'parts': [clean(h.text_content()) for h in doc.xpath('//h2[@class="part"]')]}


def walk_articles(units: list):
    """(article Unit, the chapter headings that open it) in order, through chapters, branches and parts."""
    pending: list = []
    out = []

    def go(us, parent=''):
        n_text = 0
        for u in us:
            if not isinstance(u, Unit):
                # a heading printed as text between the articles of a chapter ("Zarząd spółki" in the Commercial
                # Companies Code): kept as a heading of the next article
                if parent and u[0] == 'text':
                    n_text += 1
                    pending.append((f'{parent}/x{n_text}', '## ' + u[1], list(u[2])))
                continue
            if u.kind == 'arti':
                out.append((u, list(pending)))
                pending.clear()
            else:
                if u.kind in ('chpt', 'bran', 'part', 'titl', 'sect', 'dvsn', 'schp'):
                    labels = u.label if isinstance(u.label, list) else [u.label]
                    for i, t in enumerate(labels):
                        if t:
                            pending.append((f'{u.id}/h{i}', '## ' + t, u.glosses if i == 0 else []))
                go(u.body, u.id)
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
                out.append((key, INDENT.get(u.kind, '') + ' '.join([u.label if isinstance(u.label, str) else ' '.join(u.label)] + own).strip(), gl, inherited))
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
        out.append((key, INDENT.get(u.kind, '') + ' '.join([u.label if isinstance(u.label, str) else ' '.join(u.label)] + own).strip(), gl, inherited))
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


def read_html(raw: bytes, tj: bool = False) -> dict:
    """{'files': {num: {'label', 'lines': [(key, text, glosses, inherited glosses)]}}, 'order', 'title', 'glosses'}
    With tj=True (a unified text) the wording printed for the future is left out."""
    TJ[0] = tj
    try:
        tree = read_tree(raw)
    finally:
        TJ[0] = False
    files, order = {}, []
    for a, heads in walk_articles(tree['units']):
        num = a.id.split('_', 1)[1]
        if num in files:
            # printed twice: the article in force, then (a unified text) its future form; the first is kept
            continue
        files[num] = {'label': a.label.rstrip('.'), 'lines': article_lines(a, heads)}
        order.append(num)
    return {'files': files, 'order': order, 'title': tree['title'], 'glosses': tree['glosses'], 'tree': tree}


def render(lines) -> str:
    return '\n\n'.join(l[1] for l in lines) + '\n'
