# -*- coding: utf-8 -*-
"""Tạo batch_input/batch_XX.json cho agent sinh example (50-100 từ/batch theo guide).

Input: words_data.json + contexts_final.json + cefr_map.json
Output: batch_input/batch_NN.json
"""
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BATCH_SIZE = 75
SRC = Path('words_data.json')
CTX = Path('contexts_final.json')
OUT = Path('batch_input')

words = json.loads(SRC.read_text(encoding='utf-8'))
ctx = json.loads(CTX.read_text(encoding='utf-8'))
cefr = json.loads(Path('cefr_map.json').read_text(encoding='utf-8'))

OUT.mkdir(exist_ok=True)
for f in OUT.glob('batch_*.json'):
    f.unlink()

idx = 0
n = 0
while idx < len(words):
    n += 1
    part = words[idx:idx + BATCH_SIZE]
    idx += BATCH_SIZE
    out_words = []
    for w in part:
        senses = []
        for m in w['meanings']:
            labels = ctx.get(w['word'], {}).get(m['meaning'], [])
            senses.append({
                'meaning_vi': m['meaning'],
                'pos': m['pos'],
                'source': m.get('source', 'dictionary.db'),
                'context_labels': labels,
            })
        out_words.append({
            'word': w['word'],
            'pronunciation': w['pronunciation'],
            'cefr': cefr.get(w['word']),
            'part_of_speech': [p for p in (w['pos'] or '').split(', ') if p],
            'senses': senses,
        })
    (OUT / f'batch_{n:02d}.json').write_text(
        json.dumps({'batch': n, 'words': out_words}, ensure_ascii=False, indent=1),
        encoding='utf-8')

print(f'wrote {n} batches ({BATCH_SIZE} words each) to {OUT}/')
total_senses = sum(len(w['senses']) for b in range(1, n + 1)
                   for w in json.loads((OUT / f'batch_{b:02d}.json').read_text(encoding='utf-8'))['words'])
print(f'total senses: {total_senses}')
