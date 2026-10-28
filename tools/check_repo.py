"""Checks the git repository against the official texts: every checkpoint (the act as published, each unified text,
the Constitution's consolidated text), read back from git with tools/na_dzien.py on its day.

    python -X utf8 scripts/poland-law/check_repo.py [--repo ../poland-law] [--no-record]

Per checkpoint, from the cached API answers (no network):
1. File by file: the act's files in git on that day are exactly the files the build's parser makes from the official
   text (same files, same bytes; for a PDF, dash characters are compared as one character).
2. Word for word: the whole act printed by na_dzien.py, markdown marks removed, has the same words in the same order as
   the official text read independently of the parser's structure (HTML: every text node of the act without its
   footnotes; PDF: every printed line of body type size, running heads removed).
3. Editorial only: on each unified text's day, the commit before the unified text's own commit differs from it only
   in Journal references and provisions left out ("(pominięty)").
The 1997 Constitution is compared word for word with the text layer of the scanned Journal (OCR): reported, not
required to match, because the scan's text layer has recognition errors.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from lxml import html as lhtml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
import parse  # noqa: E402
import pdfparse  # noqa: E402
import src  # noqa: E402

TOKEN = re.compile(r'\w+|[^\w\s]')


def norm(s: str) -> str:
    return s.translate(build.DASH)


def html_words(raw: bytes) -> list[str]:
    doc = lhtml.fromstring(raw.decode('utf-8'))
    part = parse.act_part(doc)
    for g in part.xpath('.//a[contains(@class,"gloss-link")]'):
        g.drop_tree()
    for g in part.xpath('.//div[contains(@class,"gloss")]|.//h2'):
        g.drop_tree()

    def text(e) -> str:
        if not isinstance(e.tag, str):
            return e.tail or ''
        gap = ' ' if e.tag in ('div', 'br', 'p', 'h3', 'h2', 'td', 'tr') else ''
        return gap + (e.text or '') + ''.join(text(c) for c in e) + gap + (e.tail or '')
    return TOKEN.findall(norm(text(part).replace('\u00a0', ' ').replace('\u00ad', ' ')))


def pdf_words(raw: bytes, start: str | None, layout: str) -> list[str]:
    import pymupdf
    lines = pdfparse.visual_lines(pymupdf.open(stream=raw, filetype='pdf'), 470 if layout == 'u' else 10000)
    body = [l['text'] for l in lines if l['text'] and not l['small'] and not pdfparse.HEAD.match(l['text'])]
    if start:
        body = body[next(i for i, t in enumerate(body) if t.startswith(start)):]
    text = pdfparse.join_lines(body, set())
    return TOKEN.findall(norm(text))


def repo_words(text: str, dehyphen: bool = False) -> list[str]:
    lines = [re.sub(r'^\s*(#+ |- )', '', l) for l in text.split('\n')]
    t = norm(' '.join(lines))
    return TOKEN.findall(t)


def nohyphen(ws: list[str]) -> list[str]:
    """Words with hyphens dropped and joined again: a PDF line break can split or join a hyphenated word either way."""
    return TOKEN.findall(re.sub(r'\s*-\s*', '', ' '.join(ws)))


def na_dzien(repo: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, 'tools/na_dzien.py', *args], cwd=repo, capture_output=True, text=True,
                          encoding='utf-8')


def commit_on(repo: str, day: str, slug: str) -> str:
    return subprocess.run([sys.executable, '-c', 'import sys; sys.path.insert(0, "tools"); import na_dzien; '
                           f'print(na_dzien.commit_on("{day}", "{slug}"))'], cwd=repo, capture_output=True,
                          text=True).stdout.strip()


def files_at(repo: str, commit: str, slug: str) -> dict[str, str]:
    out = subprocess.run(['git', 'ls-tree', '-r', commit, f'{slug}/'], cwd=repo, capture_output=True,
                         text=True, encoding='utf-8').stdout.split('\n')
    blobs = []
    for line in out:
        if not line:
            continue
        info, f = line.split('\t', 1)
        if f.endswith('.md') and not f.endswith('/README.md'):
            blobs.append((f[len(slug) + 1:], info.split()[2]))
    if not blobs:
        return {}
    data = subprocess.run(['git', 'cat-file', '--batch'], cwd=repo, input=''.join(f'{sha}\n' for _, sha in blobs).encode(),
                          capture_output=True).stdout
    res, pos = {}, 0
    for name, _ in blobs:
        nl = data.index(b'\n', pos)
        size = int(data[pos:nl].split()[2])
        res[name] = data[nl + 1:nl + 1 + size].decode('utf-8')
        pos = nl + 1 + size + 1
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(build.ROOT.parent / 'poland-law'))
    ap.add_argument('--no-record', action='store_true')
    args = ap.parse_args()
    repo = args.repo
    acts = build.build_all(offline=True)
    n_cp = n_files = bad = 0
    n_words = wbad = 0
    edit_checked = edit_bad = 0
    ocr = None
    lines = []
    for a in acts:
        for cp in a.checkpoints:
            commit = commit_on(repo, cp['day'], a.slug)
            got = files_at(repo, commit, a.slug) if commit else {}
            expected = {build.file_name(n): build.render(ls) for n, ls in cp['files'].items()}
            if cp['kind'] == 'ocr':
                # the 1997 scan: word for word against its text layer, reported only
                meta = a.meta
                raw = src.text_file(meta['ELI'], 'O', build.pdf_name(meta, 'O'))
                ow = nohyphen(pdf_words(raw, 'W trosce', 'du'))
                rw = nohyphen(repo_words(na_dzien(repo, cp['day'], a.slug).stdout))
                import difflib
                sm = difflib.SequenceMatcher(None, ow, rw, autojunk=False)
                diffs = [(' '.join(ow[i1:i2]), ' '.join(rw[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes()
                         if op != 'equal']
                same_files = got == expected
                ocr = {'words': len(ow), 'differences': len(diffs), 'examples': diffs[:12], 'files_equal': same_files}
                print(f'OCR {a.slug} {cp["day"]}: {len(ow)} words in the scan\'s text layer, {len(diffs)} differing '
                      f'passages (e.g. {diffs[:4]}); files equal the build\'s text as enacted: {same_files}')
                n_cp += 1
                n_files += len(expected)
                if not same_files:
                    bad += 1
                continue
            n_cp += 1
            n_files += len(expected)
            pdf = cp['kind'].startswith('pdf')
            ok = ({k: norm(v) for k, v in got.items()} == {k: norm(v) for k, v in expected.items()}) if pdf \
                else got == expected
            if not ok:
                bad += 1
                diff = sorted(set(got) ^ set(expected)) or [k for k in expected if got.get(k) != expected[k]]
                print(f'MISMATCH {a.slug} {cp["day"]} {cp["eli"]}: {diff[:5]}')
            # words, independently of the parser's structure
            whole = na_dzien(repo, cp['day'], a.slug).stdout
            if cp['kind'] == 'html':
                ow = html_words(src.text_html(cp['eli']))
                rw = repo_words(whole)
            else:
                meta = a.law(cp['eli'].split(' ')[0])
                kind = 'U' if cp['kind'] == 'pdf-u' else 'O'
                raw = src.text_file(meta['ELI'], kind, build.pdf_name(meta, kind))
                ow = nohyphen(pdf_words(raw, 'Rozdział 1' if kind == 'O' else 'K O N S T', 'u' if kind == 'U' else 'du'))
                rw = nohyphen(repo_words(whole))
                if kind == 'U':
                    rw = nohyphen(TOKEN.findall(norm(re.sub(r'^# ', '', whole.replace('KONSTYTUCJA RZECZYPOSPOLITEJ POLSKIEJ',
                                                                                        'K O N S T Y T U C J A R Z E C Z Y P O S P O L I T E J P O L S K I E J')))))
                    rw = nohyphen([w for l in whole.split('\n') for w in repo_words(l.replace(
                        'KONSTYTUCJA RZECZYPOSPOLITEJ POLSKIEJ', 'K O N S T Y T U C J A R Z E C Z Y P O S P O L I T E J P O L S K I E J'))])
            n_words += len(ow)
            if ow != rw:
                wbad += 1
                i = next((i for i, (x, y) in enumerate(zip(ow, rw)) if x != y), min(len(ow), len(rw)))
                print(f'WORDS {a.slug} {cp["day"]} {cp["eli"]}: official {len(ow)} vs repo {len(rw)}; first difference '
                      f'at {i}: {" ".join(ow[max(0, i - 6):i + 6])!r} / {" ".join(rw[max(0, i - 6):i + 6])!r}')
            lines.append(f'{a.conf["short"]} {cp["label"]} ({cp["day"]}, {cp["kind"]}): {len(expected)} files '
                         f'{"equal" if ok else "DIFFER"}; {len(ow)} words {"equal" if ow == rw else "DIFFER"}')
        # 3: before each unified text's own commit, only editorial differences remain
        for e in a.events:
            if e['kind'] != 'editorial':
                continue
            tag = f'tj/{e["eli"].split("/", 1)[1].replace("/", "-")}'
            before = files_at(repo, f'{tag}~1', a.slug)
            final = {build.file_name(n): ls for n, ls in e['final'].items()}
            for name in sorted(set(before) | set(final)):
                old = {}
                if name in before:
                    blocks = before[name].rstrip('\n').split('\n\n')
                    old = blocks
                new = [t for _, t in final.get(name, [])]
                if old == new:
                    continue
                import difflib
                sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
                for op, i1, i2, j1, j2 in sm.get_opcodes():
                    if op == 'equal':
                        continue
                    edit_checked += 1
                    o, n = old[i1:i2], new[j1:j2]
                    fine = (len(o) == len(n) and all(build.same_but_refs(x, y) for x, y in zip(o, n))) or \
                        any('(pominięty)' in y for y in n)
                    if not fine:
                        edit_bad += 1
                        print(f'EDITORIAL {a.slug} {tag} {name}: {o[:2]} -> {n[:2]}')
    head = (f'{n_cp} checkpoints ({n_files} files), {bad} mismatches; {n_cp - (1 if ocr else 0)} word for word '
            f'({n_words} words), {wbad} mismatches; {edit_checked} differences before the unified texts\' own commits, '
            f'{edit_bad} not editorial')
    print(head)
    lines.insert(0, head)
    if ocr:
        lines.append(f'Konstytucja as enacted (1997-10-17) against the scan\'s text layer: {ocr["words"]} words, '
                     f'{ocr["differences"]} differing passages (OCR), e.g. '
                     + '; '.join(f'"{x}" / "{y}"' for x, y in ocr['examples'][:5]))
    if not args.no_record:
        p = HERE / 'verification.json'
        rec = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        rec['check'] = {'checkpoints': n_cp, 'files': n_files, 'mismatches': bad, 'words': n_words,
                        'word_mismatches': wbad, 'editorial_checked': edit_checked, 'editorial_bad': edit_bad,
                        'ocr': ocr, 'lines': lines}
        p.write_text(json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8',
                     newline='\n')
    raise SystemExit(1 if bad or wbad or edit_bad else 0)


if __name__ == '__main__':
    main()
