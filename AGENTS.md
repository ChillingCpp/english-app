# AGENTS.md — english-app vocabulary pipeline

## What this is
Data-generation pipeline building `dataset/vocabulary.sqlite` from `words.txt` + `dictionary/words2.txt`, using `dataset/dictionary.db` (gitignored source of Vietnamese meanings). Not an app; `main.py` is a one-off PDF→markdown converter.
Spec authority: `Content Generation Task Specification.md` is the guide, but user chat instructions (`prompt_history.md`, Prompt 1) override it on conflict.

## Running scripts
- Windows + PowerShell. Invoke Python as `py` (e.g. `py import_to_db.py`).
- Any script printing Vietnamese must first set `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`, or it crashes on cp1252 (`UnicodeEncodeError`).
- No build/lint/test framework. `test_dictionary_query.py` is stale — it imports `dictionary_query`, `verify_batch`, and `batches/`, none of which exist. Do not rely on it.

## Pipeline order
1. `query_meanings.py` → `tmp` (strip trailing sense numbers like `do1` before lookup; dedupe lookups via set).
2. Manual review of `tmp` with the Read tool — no Python for judgment calls → `sus.json`, `add_meaning.json`.
3. `build_words_data.py` → `words_data.json`.
4. `make_ctx_chunks.py` → `ctx_input/` → 3 independent context runs → `ctx_parts/runN/` → `merge_ctx_runs.py` → `context_tmp(1..3)`.
5. `finalize_contexts.py` → `contexts_final.json` + `ctx_conflicts.json` (conflicts need manual judgment).
6. `make_batch_inputs.py` → `batch_input/` → example-generation agents → `batch_output/` → `import_to_db.py` → `dataset/vocabulary.sqlite` (+ `import_report.json`).

## Data contracts
- `sus.json`: `[{word, meaning, "từ loại"}]` — `meaning` must match the `tmp` text exactly.
- `add_meaning.json`: `[{word, meaning, "từ loại", "ngữ cảnh"}]`.
- Agent context output is index-based TSV: `word<TAB>meaning_index<TAB>label1, label2` (1-based into that chunk's `meanings` array). Never key on meaning text: 70 same-text senses differ only by pos, and merge unions their labels.
- Batch JSON schema: see the `import_to_db.py` docstring. The importer is idempotent (matches on word / `meaning_vi` / sentence); env overrides are `VOCAB_DB`, `VOCAB_BATCH_DIR`, `VOCAB_REPORT`.
- `tmp` has CRLF line endings — `$`-anchored grep patterns silently fail on it.

## Hard constraints (from user)
- `words.txt` must stay ≥ 3000 lines, `dictionary/words2.txt` ≥ 2000 lines. Never drop lines.
- Keep sense suffixes (`do1`/`do2`, `can1`) and same-spelling words with different meanings.
- Never invent CEFR levels, sources, or synonyms. Absence in `cefr_map.json` means unknown, not a guess.

## Known gotchas
- `ctx_missing.json` logic was fixed (it tested tuple `(word, meaning)` against a `{word: {meaning: …}}` dict, producing 26,036 false positives). If it ever reports mass `not in any run` again, re-check that membership test before trusting the file.
- All 3 context runs now cover 25,966/25,966 meanings. Merge unions labels across runs.
- Delete test artifacts before final import: `test_batch/`, `test_report.json`, `dataset/test_vocab.sqlite`.
