"""Prints an act, or one article of it, as it stood on a given day, from this repository's history.

    python tools/na_dzien.py 2010-01-01 konstytucja 55        # art. 55 of the Constitution on 1 January 2010
    python tools/na_dzien.py 2020-01-01 obywatelstwo          # the whole citizenship act on 1 January 2020
    python tools/na_dzien.py 2020-01-01 konstytucja preambula
    python tools/na_dzien.py 2024-01-01 kodeks-spolek-handlowych 7^1   # art. 7¹ (also 7_1 or 7¹)

Each commit carries the day its change took effect in an `In-force:` trailer; the text in force on a day is the last
commit on or before it that touches the act. Standard library only.
"""
import datetime as dt
import re
import subprocess
import sys


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True, encoding='utf-8', check=True).stdout


def order(path: str) -> tuple:
    name = path.rsplit('/', 1)[1][:-3]
    if name == 'preambula':
        return (0, 0, '', 0, '')
    m = re.fullmatch(r'art-(\d+)([a-z]*)(?:-(\d+)([a-z]*))?(?:-do-.*)?', name)
    return (1, int(m.group(1)), m.group(2), int(m.group(3) or 0), m.group(4) or '') if m else (2, 0, name, 0, '')


def file_for(key: str) -> str:
    """'55' -> art-055.md; art. 7 with superscript 1 (7¹, 7^1 or 7_1) -> art-007-1.md."""
    m = re.fullmatch(r'(\d+)([a-z]*)(?:[_^](\d+))?', key)
    sup = re.fullmatch(r'(\d+[a-z]*)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', key)
    if sup:
        m = re.fullmatch(r'(\d+)([a-z]*)()', sup.group(1))
        return f'art-{int(m.group(1)):03d}{m.group(2)}-{sup.group(2).translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"))}.md'
    if m:
        return f'art-{int(m.group(1)):03d}{m.group(2)}' + (f'-{m.group(3)}' if m.group(3) else '') + '.md'
    return key if key.endswith('.md') else f'{key}.md'


def commit_on(day: str, act: str) -> str:
    out = git('log', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)', 'main', '--', act)
    for line in out.splitlines():
        h, _, d = line.partition('\t')
        if d.strip() and d.strip() <= day:
            return h
    return ''


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    day, act = sys.argv[1], sys.argv[2].strip('/')
    dt.date.fromisoformat(day)
    commit = commit_on(day, act)
    if not commit:
        sys.exit(f'{act} is not in the record on {day}.')
    if len(sys.argv) > 3:
        name = file_for(sys.argv[3])
        try:
            sys.stdout.write(git('show', f'{commit}:{act}/{name}'))
        except subprocess.CalledProcessError:
            sys.exit(f'{act}/{name} was not in the text on {day}.')
        return
    files = [f for f in git('ls-tree', '-r', '--name-only', commit, f'{act}/').split('\n')
             if f.endswith('.md') and not f.endswith('/README.md')]
    # one `git cat-file --batch` for every file (one `git show` per file is slow for a code of a thousand articles)
    files = sorted(files, key=order)
    data = subprocess.run(['git', 'cat-file', '--batch'], input=''.join(f'{commit}:{f}\n' for f in files).encode(),
                          capture_output=True, check=True).stdout
    pos = 0
    for _ in files:
        nl = data.index(b'\n', pos)
        size = int(data[pos:nl].split()[2])
        sys.stdout.write(data[nl + 1:nl + 1 + size].decode('utf-8') + '\n')
        pos = nl + 1 + size + 1


if __name__ == '__main__':
    main()
