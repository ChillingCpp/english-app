import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open('batch_output\\batch_01.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
words = data.get('words', [])
w = words[0]
print(f'Word: {w["word"]}')
print(f'Senses: {len(w["senses"])}')
for i, s in enumerate(w['senses'][:3]):
    m = s['meaning_vi']
    print(f'Sense {i}: meaning={m}')
    exs = s.get('examples', [])
    print(f'  Examples: {len(exs)}')
    for j, ex in enumerate(exs):
        sent = ex.get('sentence', '')
        blank = ex.get('blank_sentence', '')
        ans = ex.get('answer', '')
        print(f'  Ex{j}: sent={sent[:40] if sent else "MISSING"}, blank={blank[:30] if blank else "MISSING"}, ans={ans}')