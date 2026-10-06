import json
try:
    with open('batch_output\\batch_01.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    words = data.get('words', [])
    print('JSON parsed OK')
    print(f'Words: {len(words)}')
    if words:
        w = words[0]
        print(f'Word: {w.get("word")}')
        senses = w.get('senses', [])
        print(f'Senses: {len(senses)}')
        if senses:
            s = senses[0]
            print(f'Sense0: meaning={s.get("meaning_vi")}, pos={s.get("pos")}')
            exs = s.get('examples', [])
            print(f'Examples: {len(exs)}')
            for i, ex in enumerate(exs[:2]):
                print(f'Ex{i}: sent={ex.get("sentence")}, blank={ex.get("blank_sentence")}, ans={ex.get("answer")}')
except Exception as e:
    print(f'Error: {e}')