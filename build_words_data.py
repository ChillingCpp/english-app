# -*- coding: utf-8 -*-
"""Gộp tmp + sus.json + add_meaning.json -> words_data.json.

- Loại meaning bị đánh dấu sai (sus.json)
- Bổ sung nghĩa thủ công cho từ không có nghĩa dùng được (add_meaning.json)
Python chỉ xử lý dữ liệu; việc đọc/đánh nghĩa đã do assistant review thủ công.
"""
import json
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TMP = Path('tmp')
SUS = Path('sus.json')
ADD = Path('add_meaning.json')
OUT = Path('words_data.json')

# --- parse tmp ---
words = []
current = None
meaning_re = re.compile(r'^\s+(\d+)\.\s+\[([^\]]*)\]\s+(.*)$')

for raw in TMP.read_text(encoding='utf-8').splitlines():
    line = raw.rstrip('\r')
    if line.startswith('=== ') and line.endswith(' ==='):
        current = {
            'word': line[4:-4].strip(),
            'root_form': None,
            'lang': None,
            'pos': '',
            'pronunciation': None,
            'found': True,
            'meanings': [],
        }
        words.append(current)
        continue
    if current is None:
        continue
    if line.startswith('(root: '):
        current['root_form'] = line[7:-1]
    elif line.startswith('(lang: '):
        current['lang'] = line[7:-1]
    elif line.startswith('POS: '):
        current['pos'] = line[5:].strip()
    elif line.startswith('Pronunciation: '):
        current['pronunciation'] = line[14:].strip()
    elif line.startswith('NOT FOUND'):
        current['found'] = False
    elif line.startswith('Meanings ('):
        pass
    else:
        m = meaning_re.match(line)
        if m:
            body = m.group(3)
            ex = None
            if ' | Ex: ' in body:
                body, ex = body.split(' | Ex: ', 1)
            current['meanings'].append({
                'pos': m.group(2).strip(),
                'meaning': body.strip(),
                'example': ex,
                'source': 'dictionary',
            })

print(f'parsed words: {len(words)}')

# --- apply sus exclusions ---
sus = json.loads(SUS.read_text(encoding='utf-8'))
sus_index = {}
for s in sus:
    sus_index.setdefault((s['word'], s['meaning']), 0)
    sus_index[(s['word'], s['meaning'])] += 1

removed = 0
for w in words:
    kept = []
    for m in w['meanings']:
        key = (w['word'], m['meaning'])
        if sus_index.get(key, 0) > 0:
            sus_index[key] -= 1
            removed += 1
            continue
        kept.append(m)
    w['meanings'] = kept

unmatched = [k for k, v in sus_index.items() if v > 0]
print(f'sus entries removed: {removed}, unmatched: {len(unmatched)}')
for k in unmatched:
    print(f'  UNMATCHED sus: {k[0]} | {k[1][:60]}')

# --- apply manual meanings ---
adds = json.loads(ADD.read_text(encoding='utf-8'))
by_word = {w['word']: w for w in words}
added = 0
missing_words = []
for a in adds:
    w = by_word.get(a['word'])
    if w is None:
        missing_words.append(a['word'])
        continue
    if any(m['meaning'] == a['meaning'] for m in w['meanings']):
        continue
    w['meanings'].append({
        'pos': a.get('từ loại') or a.get('pos') or '',
        'meaning': a['meaning'],
        'example': None,
        'source': 'manual review',
        'context_hint': a.get('ngữ cảnh') or a.get('context'),
    })
    added += 1
print(f'manual meanings added: {added}, words not in tmp: {missing_words}')

# --- report words with no usable meaning ---
empty = [w['word'] for w in words if not w['meanings']]
print(f'words with 0 meanings: {len(empty)}')
for e in empty:
    print(f'  EMPTY: {e}')

# --- write output ---
OUT.write_text(
    json.dumps(words, ensure_ascii=False, indent=1),
    encoding='utf-8')
print(f'wrote {OUT} ({OUT.stat().st_size} bytes)')
