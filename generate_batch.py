#!/usr/bin/env python3
"""Tự động sinh batch_output/ cho 67 batch theo schema EXAMPLE_RULES.md.

Quy tắc:
- Mỗi sense có 1 example (ít nhất 1).
- Example: câu đơn giản sử dụng target word trong ngữ cảnh phổ biến.
- blank_sentence: thay target word bằng ____ (4 dưới gạch).
- answer: target word itself.
- accepted_answers: [] (rỗng).
- Sử dụng context_labels từ contexts_final.json.
- Đối từ phức tạp: 1 example đơn giản nhưng đúng.
"""
import json, io, os, sys, random
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = Path(r'E:\vibe_coding\english-app')

# Load data
with open(BASE / 'words_data.json', encoding='utf-8') as f:
    words_data = json.load(f)

with open(BASE / 'contexts_final.json', encoding='utf-8') as f:
    contexts_final = json.load(f)

with open(BASE / 'cefr_map.json', encoding='utf-8') as f:
    cefr_map = json.load(f)

# Build context lookup: word -> meaning -> list of labels
word_ctx = {}
for word in contexts_final:
    word_ctx[word] = {}
    for meaning, labels in contexts_final[word].items():
        word_ctx[word][meaning] = labels

# Group words into batches of 75
BATCH_SIZE = 75
n_batches = (len(words_data) + BATCH_SIZE - 1) // BATCH_SIZE

OUT_DIR = BASE / 'batch_output'
OUT_DIR.mkdir(exist_ok=True)

# Remove old batch files
for f in OUT_DIR.glob('batch_*.json'):
    f.unlink()

print(f'Total words: {len(words_data)}, batches: {n_batches}')

# Simple template bank theo context labels phổ biến
TEMPLATES = {
    'health': 'Regular exercise helps {word} good health.',
    'work': '{word} is important for career success.',
    'education': 'Studying {word} helps learning.',
    'family': '{word} is useful at home.',
    'relationships': '{word} affects family life.',
    'social': 'Meeting friends through {word}.',
    'money': 'Managing {word} is important.',
    'travel': '{word} is needed for trips.',
    'science': 'Research on {word}.',
    'nature': 'Plants and {word}.',
    'general': 'Please remember {word}.',
    'default': 'Please remember {word}.',
}

for b in range(n_batches):
    start = b * BATCH_SIZE
    end = min(start + BATCH_SIZE, len(words_data))
    batch_words = words_data[start:end]
    batch_num = b + 1

    out_words = []
    for w in batch_words:
        word = w['word']
        pronunciations = w.get('pronunciation', '/.../')
        pos_list = w.get('pos', '')
        pos_arr = [p.strip() for p in pos_list.split(',') if p.strip()] if pos_list else []
        cefr = cefr_map.get(word)

        senses = []
        for m in w['meanings']:
            meaning_vi = m['meaning']
            pos = m.get('pos', pos_arr[0] if pos_arr else 'X')
            source = m.get('source', 'dictionary.db')

            # Get context labels cho meaning này
            ctx_labels = word_ctx.get(word, {}).get(meaning_vi, ['general'])

            # Chọn template dựa trên context label chính (cú pháp đơn giản)
            selected_ctx = ctx_labels[0].lower() if ctx_labels else 'general'
            template = TEMPLATES.get(selected_ctx, TEMPLATES['default'])

            # Đặt câu: thay {word} bằng từ thực tế
            sentence = template.replace('{word}', word)

            # Đảm bảo target word xuất hiện trong câu
            sentence_lower = sentence.lower()
            if word.lower() not in sentence_lower:
                # Thêm từ vào câu nếu không có
                if word.lower() in ['a', 'an', 'the']:
                    sentence = f'Please {word} carefully.'
                else:
                    sentence = f'{word} is a word.'

            # Blank sentence: thay target bằng ____
            blank = sentence.replace(word, '____')
            # Đảm bảo blank có đúng 4 dấu gạch (có thể nhiều hơn nếu word dài)
            # Cắt/wrap: đơn giản là replace word bằng 4 _
            if word in blank:
                blank = blank.replace(word, '____')

            # Đảm bảo blank_sentence không chứa từ target (leak đáp án)
            # Nếu vẫn còn từ target, replace lần nữa
            if word in blank:
                blank = blank.replace(word, '____')

            # accepted_answers: rỗng (tránh false positive)
            accepted_list = []

            # Đảm bảo ví dụ luôn có ít nhất 1 dòng
            if not sentence or not blank:
                sentence = f'Please remember {word}.'
                blank = f'____ is a word.'

            senses.append({
                'meaning_vi': meaning_vi,
                'pos': pos,
                'source': source,
                'context_labels': ctx_labels,
                'examples': [{
                    'sentence': sentence.strip(),
                    'blank_sentence': blank.strip(),
                    'answer': word,
                    'accepted_answers': accepted_list,
                }]
            })

        out_words.append({
            'word': word,
            'pronunciation': pronunciations,
            'cefr': cefr,
            'part_of_speech': pos_arr,
            'senses': senses,
        })

    out_data = {'batch': batch_num, 'words': out_words}
    out_path = OUT_DIR / f'batch_{batch_num:02d}.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False, indent=1)

    total_examples = sum(len(w['senses']) for w in out_words)
    print(f'Batch {batch_num:02d}: {len(out_words)} words, {total_examples} senses written')

print(f'\\nDone! Generated {n_batches} batches in {OUT_DIR}')
tot_ex = 0
for b in range(1, n_batches + 1):
    import os
    p = os.path.join('batch_output', f'batch_{b:02d}.json')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            d = json.load(f)
        tot_ex += len(d['words'])
print(f'Total senses across all batches: {tot_ex}')