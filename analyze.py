import json

with open('batch_input\\batch_01.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

words = data['words']

# For each word, show word, pos, number of senses
for i, w in enumerate(words):
    pos_str = str(w['part_of_speech'])
    print(f'{i+1}. {w["word"]:15s} pos={pos_str:30s} senses={len(w["senses"])}')