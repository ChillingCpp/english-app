import json
with open('batch_output\\batch_01.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
words = data.get('words', [])
w = words[0]
print(f'Word: {w["word"]}')
print(f'Senses: {len(w["senses"])}')
for i, s in enumerate(w['senses'][:3]):
    print(f'Sense {i}: meaning={s["meaning_vi"]}')
    exs = s.get('examples', [])
    print(f'  Examples: {len(exs)}')
    for j, ex in enumerate(exs):
        print(f'  Ex{j}: sent={ex.get("sentence")[:50] if ex.get("sentence") else "MISSING"}, blank={ex.get("blank_sentence")[:30] if ex.get("blank_sentence") else "MISSING"}, ans={ex.get("answer")}')