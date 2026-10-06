# -*- coding: utf-8 -*-
"""Gộp kết quả 3 lượt sinh context -> context_tmp(1..3).

Định dạng dòng của agent (index-based, tránh lỗi copy nguyên văn):
    <word>\\t<meaning_index>\\t<label1>, <label2>

meaning_index lấy theo mảng meanings trong ctx_input/chunk_*.json.
Report thiếu / thừa / lỗi format.
"""
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PARTS_ROOT = Path('ctx_parts')
INPUT_DIR = Path('ctx_input')

# map word -> [meaning, ...] từ các chunk input (word duy nhất trong danh sách)
word_meanings = {}
for cf in sorted(INPUT_DIR.glob('chunk_*.json')):
    for entry in json.loads(cf.read_text(encoding='utf-8')):
        word_meanings[entry['word']] = entry['meanings']

# thứ tự word/meaning để file output ổn định (theo words_data)
words = json.loads(Path('words_data.json').read_text(encoding='utf-8'))
order = {}
for wi, w in enumerate(words):
    for mi, m in enumerate(w['meanings']):
        order[(w['word'], m['meaning'])] = (wi, mi)

for run in (1, 2, 3):
    rows = {}
    problems = []
    part_dir = PARTS_ROOT / f'run{run}'
    files = sorted(part_dir.glob('chunk_*.txt')) if part_dir.exists() else []
    for pf in files:
        for ln, raw in enumerate(pf.read_text(encoding='utf-8').splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            bits = line.split('\t')
            if len(bits) != 3:
                problems.append(f'{pf.name}:{ln} bad format (need 3 tab cols): {line[:70]}')
                continue
            word, idx_s, labels = [b.strip() for b in bits]
            meanings = word_meanings.get(word)
            if meanings is None:
                problems.append(f'{pf.name}:{ln} unknown word: {word}')
                continue
            try:
                idx = int(idx_s)
                meaning = meanings[idx - 1]
            except (ValueError, IndexError):
                problems.append(f'{pf.name}:{ln} bad index: {word} [{idx_s}]')
                continue
            key = (word, meaning)
            if key not in order:
                problems.append(f'{pf.name}:{ln} meaning not in words_data: {word} | {meaning[:40]}')
                continue
            labs = [l.strip() for l in labels.split(',') if l.strip()]
            if key in rows:
                # cùng (word, meaning) ở nhiều index = các sense khác pos trùng text
                # -> gộp label thay vì bỏ (finalize/import đều key theo word+meaning)
                for lab in labs:
                    if lab not in rows[key]:
                        rows[key].append(lab)
                continue
            rows[key] = labs

    out = Path(f'context_tmp({run})')
    missing = []
    with out.open('w', encoding='utf-8') as f:
        for key in sorted(order, key=order.get):
            if key in rows:
                f.write(f'{key[0]}\t{key[1]}\t{", ".join(rows[key])}\n')
            else:
                missing.append(key)

    print(f'run{run}: parts={len(files)} covered={len(rows)}/{len(order)} '
          f'missing={len(missing)} problems={len(problems)} -> {out}')
    for p in problems[:20]:
        print(f'  PROBLEM: {p}')
    if len(problems) > 20:
        print(f'  ... and {len(problems) - 20} more problems')
    # tóm tắt missing theo chunk (pending chunks chưa chạy là bình thường)
    if missing:
        mwords = sorted({k[0] for k in missing})
        print(f'  missing across {len(mwords)} words, first: {mwords[:10]}')
