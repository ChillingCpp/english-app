# -*- coding: utf-8 -*-
"""Chia words_data.json thành các chunk cho 3 lượt sinh context độc lập.

- Chunk stable : từ ngoài range review slice-6 (đã chốt nghĩa) -> chạy được ngay.
- Chunk pending: từ nằm trong range review slice-6 (nghĩa còn có thể đổi)
                 -> chỉ chạy sau khi merge sus/add của slice 6 xong.
"""
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CHUNK_SIZE = 165
# range index (0-based, theo thứ tự tmp/words_data) của slice 6: dòng 39597-45048
PENDING_FROM, PENDING_TO = 3724, 4345

SRC = Path('words_data.json')
OUT_DIR = Path('ctx_input')

raw = json.loads(SRC.read_text(encoding='utf-8'))
stable, pending = [], []
for i, w in enumerate(raw):
    if not w['meanings']:
        continue
    entry = {
        'word': w['word'],
        'meanings': [m['meaning'] for m in w['meanings']],
    }
    if PENDING_FROM <= i < PENDING_TO:
        pending.append(entry)
    else:
        stable.append(entry)

print(f'stable: {len(stable)} words, pending: {len(pending)} words')

OUT_DIR.mkdir(exist_ok=True)
for f in OUT_DIR.glob('*.json'):
    if f.name != 'manifest.json':
        f.unlink()

manifest = []


def emit(prefix, items, status):
    for i in range(0, len(items), CHUNK_SIZE):
        part = items[i:i + CHUNK_SIZE]
        name = f'{prefix}{i // CHUNK_SIZE + 1:02d}.json'
        (OUT_DIR / name).write_text(
            json.dumps(part, ensure_ascii=False, indent=1), encoding='utf-8')
        manifest.append({'file': name, 'status': status, 'words': len(part),
                         'meanings': sum(len(w['meanings']) for w in part)})


emit('chunk_', stable, 'stable')
emit('chunk_p', pending, 'pending')

Path('ctx_manifest.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8')
for m in manifest:
    print(m)
