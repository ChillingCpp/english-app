# -*- coding: utf-8 -*-
"""Gộp context_tmp(1..3) -> contexts_final.json + ctx_conflicts.json.

Quy tắc gộp (theo chỉ dẫn của user):
- kết hợp cả 3 lượt
- ưu tiên context GENERAL (phổ quát hơn) khi các lượt mâu thuẫn
- lượt mâu thuẫn cùng meaning -> đưa vào ctx_conflicts.json để assistant xử lý tay
"""
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# mức độ general: số nhỏ = general hơn
GENERAL_RANK = [
    'general', 'daily life', 'social', 'time', 'feelings', 'education',
    'work', 'health', 'family', 'relationships', 'communication', 'money',
    'home', 'shopping', 'food', 'travel', 'technology', 'science',
    'government', 'law', 'economy', 'business', 'sports', 'entertainment',
    'arts', 'culture', 'nature', 'environment', 'media', 'internet',
    'personality', 'appearance', 'body', 'animals', 'plants', 'weather',
    'geography', 'history', 'politics', 'medicine', 'literature', 'music',
    'safety', 'crime', 'religion',
]
RANK = {name: i for i, name in enumerate(GENERAL_RANK)}


def rank_of(label):
    return RANK.get(label, len(GENERAL_RANK) + 1)


# đọc 3 lượt
runs = {}
for n in (1, 2, 3):
    p = Path(f'context_tmp({n})')
    d = {}
    if p.exists():
        for line in p.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            word, meaning, labels = line.split('\t')
            d[(word, meaning)] = [l.strip() for l in labels.split(',') if l.strip()]
    runs[n] = d
    print(f'run{n}: {len(d)} meanings')

all_keys = set()
for d in runs.values():
    all_keys |= set(d)
print(f'union meanings: {len(all_keys)}')

final = {}
conflicts = []
missing = []

for key in all_keys:
    word, meaning = key
    present = {n: runs[n].get(key) for n in (1, 2, 3)}
    lists = [v for v in present.values() if v]
    if not lists:
        missing.append({'word': word, 'meaning': meaning, 'reason': 'no run covered'})
        continue

    # đếm số lượt có label này
    freq = {}
    for lst in lists:
        for lab in set(lst):
            freq[lab] = freq.get(lab, 0) + 1

    # xếp: số lượt giảm dần -> rank general tăng dần
    ordered = sorted(freq, key=lambda l: (-freq[l], rank_of(l), -len(l)))
    top = ordered[:4]

    union = set(freq)
    agreed = [l for l in ordered if freq[l] >= 2]
    is_conflict = (len(lists) >= 2 and not agreed) or len(union) > 6

    if is_conflict:
        conflicts.append({
            'word': word, 'meaning': meaning,
            'run1': present[1], 'run2': present[2], 'run3': present[3],
            'picked': top,
        })

    final.setdefault(word, {})[meaning] = top

# điền word còn thiếu meaning? (so với words_data)
words = json.loads(Path('words_data.json').read_text(encoding='utf-8'))
miss_words = []
for w in words:
    for m in w['meanings']:
        if m['meaning'] not in final.get(w['word'], {}):
            missing.append({'word': w['word'], 'meaning': m['meaning'],
                            'reason': 'not in any run'})

Path('contexts_final.json').write_text(
    json.dumps(final, ensure_ascii=False, indent=1), encoding='utf-8')
Path('ctx_conflicts.json').write_text(
    json.dumps(conflicts, ensure_ascii=False, indent=1), encoding='utf-8')
Path('ctx_missing.json').write_text(
    json.dumps(missing, ensure_ascii=False, indent=1), encoding='utf-8')

print(f'contexts_final: {sum(len(v) for v in final.values())} meanings in {len(final)} words')
print(f'conflicts for manual review: {len(conflicts)}')
print(f'missing: {len(missing)}')
