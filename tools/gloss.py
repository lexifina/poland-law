"""Reads the footnotes of a Polish unified text (tekst jednolity): which act set, added or repealed a unit."""
from __future__ import annotations

import re

MONTHS = {'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4, 'maja': 5, 'czerwca': 6, 'lipca': 7, 'sierpnia': 8,
          'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12}
CHANGE = re.compile(r'^(W brzmieniu ustalonym przez|Ze zmian[aą] wprowadzon[aą] przez|Ze zmianami wprowadzonymi przez|'
                    r'Dodany przez|Dodana przez|Dodane przez|Uchylony przez|Uchylona przez|Uchylone przez|Przez|'
                    r'Utracił moc|Utraciła moc|Utraciły moc|Skreślony przez|Pominięty)')
INFO = re.compile(r'^(Zmiany tekstu jednolitego|Zmiany wymienionej|Ustawa utraciła moc|Ustawa została ogłoszona|'
                  r'Zamieszczony w obwieszczeniu|Niniejsz|Wymieniona ustawa|Utraciła moc na podstawie)')
_DATE = re.compile(r'(\d{1,2}) (' + '|'.join(MONTHS) + r') (\d{4}) r\.')


def pl_date(s: str) -> str | None:
    m = _DATE.search(s)
    return f'{m.group(3)}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}' if m else None


def kind(text: str) -> str:
    if INFO.match(text):
        return 'info'
    if CHANGE.match(text):
        return 'change'
    return 'other'


def act_of(text: str, table: dict[str, str], seen: set | None = None) -> list[dict]:
    """The acts a change footnote names: [{'eli', 'provision', 'date'}]. 'ustawy, o której mowa w odnośniku N' is
    resolved through footnote N of the same text."""
    seen = seen or set()
    out = []
    prev_start = 0
    for part in re.split(r';| oraz (?=art\.)', text):
        start = len(out)
        m = re.search(r'(art\. [0-9a-z⁰¹²³⁴⁵⁶⁷⁸⁹]+(?: (?:ust|pkt|lit|\u00a7)\.? [0-9a-z⁰¹²³⁴⁵⁶⁷⁸⁹]+)*)', part)
        prov = m.group(1) if m else None
        ref = re.search(r'o której mowa w odnośniku (\d+)', part)
        if ref and ref.group(1) not in seen:
            seen.add(ref.group(1))
            own = re.search(r'(?:wesz[łl]a|wesz[łl]y|wszed[łl]|weszło) w życie z dniem (\d{1,2} \w+ \d{4} r\.)', part)
            for a in act_of(table.get(ref.group(1), ''), table, seen):
                # "ustawy, o której mowa w odnośniku 2; wszedł w życie z dniem 15 września 2023 r.": this unit's own day
                out.append({**a, 'provision': prov or a['provision'], 'date': pl_date(own.group(1)) if own else a['date']})
            prev_start = start
            continue
        dz = re.search(r'\(Dz\. ?U\. (?:z (\d{4}) r\. )?(?:Nr \d+, )?poz\. (\d+)', part)
        if not dz:
            # "...ustawy, o której mowa w odnośniku 3; wszedł w życie z dniem 1 marca 2020 r.": the day of the part
            # before (this unit's own day, when the act took effect in stages)
            own = re.search(r'^\s*(?:wesz[łl]a|wesz[łl]y|wszed[łl]|weszło) w życie z dniem (\d{1,2} \w+ \d{4} r\.)', part)
            if own:
                for x in out[prev_start:]:
                    x['date'] = pl_date(own.group(1))
            continue
        year = dz.group(1)
        if not year:
            y = re.search(r'z dnia \d{1,2} \w+ (\d{4}) r\.', part)
            year = y.group(1) if y else None
        eli = f'DU/{year}/{dz.group(2)}' if year else None
        d = re.search(r'(?:wesz[łl]a|wesz[łl]y|wszed[łl]|weszło) w życie z dniem (\d{1,2} \w+ \d{4} r\.)', part)
        out.append({'eli': eli, 'provision': prov, 'date': pl_date(d.group(1)) if d else None})
        prev_start = start
    return out
