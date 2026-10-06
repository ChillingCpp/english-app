# -*- coding: utf-8 -*-
"""Import batch JSON (sinh bởi agent) vào dataset/vocabulary.sqlite.

Định dạng batch_output/batch_XX.json:
{
 "batch": 1,
 "words": [
  {"word": "abandon", "pronunciation": "/.../", "part_of_speech": ["V","N"],
   "senses": [
    {"meaning_vi": "...", "pos": "V", "source": "dictionary.db",
     "context_labels": ["general", "feelings"],
     "examples": [
      {"sentence": "...", "blank_sentence": "...", "answer": "abandon",
       "accepted_answers": []}]}]}]
}

Nguyên tắc:
- idempotent: chạy lại không tạo trùng (khớp theo word / meaning_vi / sentence)
- không bỏ dữ liệu im lặng: bản ghi lỗi -> import_report.json + status=needs_review
- provenance: senses.source_id, examples.source_id, words.word_source, words.cefr
"""
import json
import os
import re
import sqlite3
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB = Path(os.environ.get('VOCAB_DB', 'dataset/vocabulary.sqlite'))
BATCH_DIR = Path(os.environ.get('VOCAB_BATCH_DIR', 'batch_output'))
REPORT = Path(os.environ.get('VOCAB_REPORT', 'import_report.json'))

words1 = set(Path('words.txt').read_text(encoding='utf-8').splitlines())
words2 = set(Path('dictionary/words2.txt').read_text(encoding='utf-8').splitlines())
cefr_map = json.loads(Path('cefr_map.json').read_text(encoding='utf-8'))

BLANK_RE = re.compile(r'_{2,}|\(\s*\.\s*\.\s*\.\s*\)')


def word_source(w):
    if w in words1:
        return 'Oxford 3000'
    if w in words2:
        return 'dictionary/2000.md'
    return None


con = sqlite3.connect(DB)
con.execute('PRAGMA foreign_keys = ON')
cur = con.cursor()

src_id = {}
for sid, name in cur.execute('SELECT id, source_name FROM sources').fetchall():
    src_id[name] = sid


def get_source_id(name):
    if name in src_id:
        return src_id[name]
    cur.execute('INSERT INTO sources (source_name, verified) VALUES (?, 0)', (name,))
    src_id[name] = cur.lastrowid
    return src_id[name]


def ctx_id(name):
    cur.execute('SELECT id FROM contexts WHERE name = ?', (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute('INSERT INTO contexts (name) VALUES (?)', (name,))
    return cur.lastrowid


def validate_example(ex, word):
    errs = []
    sent = (ex.get('sentence') or '').strip()
    blank = (ex.get('blank_sentence') or '').strip()
    ans = (ex.get('answer') or '').strip()
    if not sent:
        errs.append('empty sentence')
    if not blank:
        errs.append('empty blank_sentence')
    if not ans:
        errs.append('empty answer')
    if sent and ans and ans.lower() not in sent.lower():
        errs.append('answer not in sentence')
    if blank and not BLANK_RE.search(blank):
        errs.append('blank_sentence has no blank marker')
    if blank and ans and ans.lower() in blank.lower():
        errs.append('answer leaked into blank_sentence')
    for alt in ex.get('accepted_answers') or []:
        if not str(alt).strip():
            errs.append('empty accepted_answer')
        elif str(alt).strip().lower() == ans.lower():
            errs.append('accepted_answer duplicates primary answer')
    return errs


files = sorted(BATCH_DIR.glob('batch_*.json'))
if not files:
    print('no batch files found in batch_output/')
    sys.exit(0)

report = {'files': [], 'stats': {}}
stats = {'words_inserted': 0, 'words_existing': 0, 'senses_inserted': 0,
         'senses_existing': 0, 'links_inserted': 0, 'examples_inserted': 0,
         'answers_inserted': 0, 'invalid': []}

for bf in files:
    try:
        data = json.loads(bf.read_text(encoding='utf-8'))
    except Exception as e:
        report['files'].append({'file': bf.name, 'error': f'JSON parse error: {e}'})
        continue

    fentry = {'file': bf.name, 'words': 0, 'errors': []}
    for w in data.get('words', []):
        wname = (w.get('word') or '').strip()
        if not wname:
            fentry['errors'].append('word entry missing "word"')
            continue
        senses = w.get('senses') or []
        if not senses:
            fentry['errors'].append(f'{wname}: no senses')
            stats['invalid'].append({'word': wname, 'error': 'no senses'})
            continue

        # --- word ---
        cur.execute('SELECT id, pronunciation, cefr, part_of_speech FROM words WHERE word = ?',
                    (wname,))
        row = cur.fetchone()
        ws = word_source(wname)
        cefr = cefr_map.get(wname)
        pos_list = w.get('part_of_speech') or sorted(
            {s.get('pos') for s in senses if s.get('pos')})
        pos_str = ','.join(p for p in pos_list if p) or None
        if row:
            wid = row[0]
            stats['words_existing'] += 1
            cur.execute('''UPDATE words SET pronunciation = COALESCE(?, pronunciation),
                           cefr = COALESCE(?, cefr),
                           part_of_speech = COALESCE(?, part_of_speech),
                           word_source = COALESCE(?, word_source) WHERE id = ?''',
                        (w.get('pronunciation'), cefr, pos_str, ws, wid))
        else:
            cur.execute('''INSERT INTO words (word, pronunciation, cefr, part_of_speech, word_source)
                           VALUES (?, ?, ?, ?, ?)''',
                        (wname, w.get('pronunciation'), cefr, pos_str, ws))
            wid = cur.lastrowid
            stats['words_inserted'] += 1

        # --- senses ---
        for order, s in enumerate(senses, 1):
            mv = (s.get('meaning_vi') or '').strip()
            if not mv:
                fentry['errors'].append(f'{wname}: sense #{order} missing meaning_vi')
                stats['invalid'].append({'word': wname, 'error': 'missing meaning_vi'})
                continue
            ssource = s.get('source') or 'dictionary.db'
            cur.execute('SELECT id FROM senses WHERE word_id = ? AND meaning_vi = ?',
                        (wid, mv))
            srow = cur.fetchone()
            if srow:
                sid = srow[0]
                stats['senses_existing'] += 1
            else:
                cur.execute('''INSERT INTO senses (word_id, meaning_vi, pos, sense_order, source_id)
                               VALUES (?, ?, ?, ?, ?)''',
                            (wid, mv, s.get('pos'), order, get_source_id(ssource)))
                sid = cur.lastrowid
                stats['senses_inserted'] += 1

            # --- contexts ---
            labels = s.get('context_labels') or []
            if not labels:
                fentry['errors'].append(f'{wname}: sense "{mv[:30]}" has no context_labels')
            for lab in labels:
                lab = str(lab).strip()
                if not lab:
                    continue
                cid = ctx_id(lab)
                cur.execute('''INSERT OR IGNORE INTO sense_contexts (sense_id, context_id)
                               VALUES (?, ?)''', (sid, cid))
                stats['links_inserted'] += cur.rowcount

            # --- examples ---
            examples = s.get('examples') or []
            if not examples:
                fentry['errors'].append(f'{wname}: sense "{mv[:30]}" has no examples')
                stats['invalid'].append({'word': wname, 'sense': mv[:40],
                                         'error': 'no examples'})
            for ex in examples:
                errs = validate_example(ex, wname)
                if errs:
                    fentry['errors'].append(
                        f'{wname}: example "{str(ex.get("sentence"))[:40]}": {"; ".join(errs)}')
                    stats['invalid'].append({'word': wname, 'sentence': ex.get('sentence'),
                                             'error': '; '.join(errs)})
                    continue
                sent = ex['sentence'].strip()
                cur.execute('SELECT id FROM examples WHERE sense_id = ? AND sentence = ?',
                            (sid, sent))
                erow = cur.fetchone()
                if erow:
                    eid = erow[0]
                else:
                    cur.execute('''INSERT INTO examples (sense_id, sentence, blank_sentence,
                                   answer, source_id) VALUES (?, ?, ?, ?, ?)''',
                                (sid, sent, ex['blank_sentence'].strip(),
                                 ex['answer'].strip(), get_source_id('AI-generated')))
                    eid = cur.lastrowid
                    stats['examples_inserted'] += 1
                for alt in ex.get('accepted_answers') or []:
                    alt = str(alt).strip()
                    if not alt or alt.lower() == ex['answer'].strip().lower():
                        continue
                    cur.execute('''INSERT OR IGNORE INTO accepted_answers
                                   (example_id, answer) VALUES (?, ?)''', (eid, alt))
                    stats['answers_inserted'] += cur.rowcount

        # mark word needs_review if any structural error for this word
        word_errs = [e for e in fentry['errors'] if e.startswith(wname + ':')]
        if word_errs:
            cur.execute("UPDATE words SET status = 'needs_review' WHERE id = ?", (wid,))

        fentry['words'] += 1

    report['files'].append(fentry)

con.commit()

# --- final stats ---
report['stats'] = stats
for t in ('words', 'senses', 'contexts', 'sense_contexts', 'examples', 'accepted_answers'):
    cur.execute(f'SELECT COUNT(*) FROM {t}')
    report.setdefault('db_counts', {})[t] = cur.fetchone()[0]
con.close()

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps({'db_counts': report['db_counts'],
                  'stats': {k: v for k, v in stats.items() if k != 'invalid'},
                  'invalid_count': len(stats['invalid']),
                  'file_errors': sum(len(f.get('errors', [])) for f in report['files'])},
                 ensure_ascii=False, indent=1))
print(f'report -> {REPORT}')
