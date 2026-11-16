# Tools

The scripts behind this Poland-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/poland-law.git`, a blobless bare clone
of global-law at `sources/global-law.git`, and a `pins.json` that names only poland-law and its commit (language `pl`).
`build_vulns.py`, `flags_chart.py`, `late_ext_select.py`, `late_ext_rebut.py` and `config.json` sit two folders above the
scripts.

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, maps paths to each act's folder (`map_moved.py`), adds this repository's history rows, and runs the detectors (`bash run.sh <shards>`) |
| `map_moved.py` | Rewrites the paths in the history table to each act's folder since the move of 10 November 2026 (`data/paths.json`, `kodeks-pracy/` to `ustawa/1974/141/`), so that an act's history is not split in two at the move; here it rewrote 192,948 paths of 3,835 folders |
| `add_root.py` | Builds the history rows from this repository's own commits (global-law replays it only up to an earlier commit), so the history detectors read every change; changed for this repository (below) |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the 40 strongest lapsed time limits in law texts, and the empty periods (there were none here) |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category (there were none here) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Polish and English, light and dark |
| `config.json` | The repository, the Polish category names and chart labels, and what is not law: `data/`, `tools/`, the root files, and the folders of addresses and statements (`oredzie/`, `oswiadczenie/`, `oswiadczenie-rzadowe/`, which hold only metadata) |
| `apply_patches.py` | Applies the patches below to a copy of the scripts, each once, in a fixed order, and records them in `.kit_patches.json` (`python -X utf8 apply_patches.py <scripts dir>`); later patches edit text earlier ones inserted, so a patch is never run twice on the same copy. `patch_pl.py` is last in its order |
| `patch_detectors.py` | Fixes blind spots found in runs on several country repositories in the copy of global-law's scripts |
| `patch_detectors_vi.py`, `patch_es.py`, `patch_ca.py`, `patch_en.py`, `patch_de.py`, `patch_en_et.py`, `patch_co.py`, `patch_sv.py`, `patch_pt.py`, `patch_ru.py`, `patch_r18.py`, `patch_xk.py`, `patch_mo.py`, `patch_lu.py`, `patch_li.py`, `patch_mx.py`, `patch_mn.py`, `patch_mt.py`, `patch_np.py`, `patch_en_nr.py`, `patch_dv.py`, `patch_az.py`, `patch_ar.py`, `patch_en_nz.py`, `patch_nb.py`, `patch_mk.py`, `patch_pa.py` | The same for the dates, references and currency names of other languages and jurisdictions; they change nothing in Polish text |
| `patch_ja.py` | Japanese fixes, kept with the kit but not in `apply_patches.py`'s order; not applied here |
| `patch_pl.py` | The Polish fixes made for this repository, in the same form (`python -X utf8 patch_pl.py <scripts dir>`; a fix already in place is skipped; see below) |
| `patch_build_r7.py`, `patch_build_links.py` | Bring a country's `build_vulns.py` up to date (lapsed-limit reviews matched on 400 characters of context, links to files deleted before a folder move); already applied to the `build_vulns.py` here |
| `redo.py` | Runs `apply_patches.py`, then again only the scans and detectors the fixes change, the model review of lapsed time limits, references to deleted provisions and empty periods, and the build (`python -X utf8 redo.py <run folder> [--keep-reviews] [--full]`; `--full` runs every step again through `run.sh`, sends every category to the model and keeps every review already made; `EMBED_FONTS` names the script that embeds the chart's fonts); not needed here, as the fixes were in place before the review |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
It was run as `bash run_triage.sh '^(data|tools|vulnerabilities|oredzie|oswiadczenie|oswiadczenie-rzadowe)/|^(README|REPRODUCE|USTAWY|ROZPORZADZENIA)'`.

Changes made for this repository:

- `add_root.py` counts as law, besides commits with no `Kind:` trailer, the `Kind` values this repository gives acts and
  changes: `Ustawa`, `Rozporządzenie` and `Obwieszczenie` (an act as published, or a change it made), `tekst jednolity
  (current text)` (an act held as its newest unified text), `Orzeczenie` (a Constitutional Tribunal ruling) and
  `sprostowanie (correction of printing errors)`. 6,669 commits count as law. Editorial changes of unified texts
  (`tekst jednolity (editorial)`), corrections of the record, documentation and the metadata-only records
  (`Rozporządzenie (metadata)`, `Zarządzenie (metadata)` and the like, which add only a `metadata.json`) keep their own kind.
- `patch_pl.py`, Polish dates, references and amounts, made after testing the scans on this repository's text:
  - `ingest/textscan.py`: "nie później niż" (not later than) marks a deadline, as "najpóźniej" does, and "do końca 2035 r."
    or "do końca roku 1922" (until the end of a year) is 31 December. The Polish month names, "do dnia" and "najpóźniej"
    were already read; "listopada" is November in Polish, as the scan reads it unless the language is Croatian, Bosnian,
    Serbian or Montenegrin.
  - `ingest/refscan.py`: in an article of a code ("# Art. 154."), "§ 2" is a paragraph of that article, not § 2 of the act,
    and Polish never writes "7 §" or "7. §", so "w § 2 i 3. § 7" is not a reference to article 3; "s. 69" is a page;
    inserted articles with superscripts ("art. 4¹", "art. 1153¹⁵ᵃ", and the files `art-004-1.md`, `art-1153-15a.md`) are
    their own articles, not article 4 or 1153; "art. 47o" is article 47o (the scan dropped a final "o" as an ordinal);
    a reference followed by another act's name ("art. 7 ust. 2 ustawy z dnia ...", "art. 8 Kodeksu cywilnego",
    "art. 51 ust. 1 unijnego kodeksu celnego", "art. 3 ust. 1-3 i 5, art. 4 ust. 1, ... rozporządzenia (UE) 2017/1369",
    "art. 10 i 11 k.c.") is to that act, read up to 300 characters after the reference; and a chapter heading
    "(zawierający art. 62-70 - uchylony)" is a repeal note.
  - `detectors/placeholder_ref.py`: a placeholder is a provision that reads only "(uchylony)" as a whole, not an article
    with one repealed point; an article inside a span ("art. 759-774") is not cited on its own; "(pominięty)", an amending
    article a unified text leaves out, is not a repeal.
  - `detectors/text_detectors.py`: "najpóźniej" and "nie później niż" mark a lapsed limit as a deadline and rank it lower.
  - `detectors/dup_labels.py`: "§ 2¹", a paragraph inserted after § 2, is not a second "§ 2".
  - `detectors/currency_scan.py`: pre-1995 złoty written "złotych starych" or "starych złotych" (the scan had only the
    spelling without "ł"); no text here has either.
  With the first form of the patch, which had only the dates, the superscripts, "§" in articles and other acts named
  just after a reference, the detectors gave 139 references to deleted provisions, 195 references to repealed
  placeholders and 246 duplicate numbers; with all of it, 2, 37 and 4. The deadline ranking was added after the first
  review: 84 lapsed time limits are deadlines, and the 5 that became new among the 40 strongest were reviewed, keeping
  the 111 reviews already made.
- A first version of the list rule in `ingest/refscan.py` backtracked without end on long runs of numbers; that run was
  stopped and the rule rewritten (every numbered item ends at a word boundary, and spaces between items are read one way
  only).
