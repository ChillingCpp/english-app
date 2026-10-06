import json
with open('batch_output\\batch_01.json', encoding='utf-8') as f:
    data = json.load(f)
w = data['words'][0]
print('Word:', w['word'])
print('Pronunciation:', w['pronunciation'])
print('CEFR:', w['cefr'])
print('POS:', w['part_of_speech'])
s = w['senses'][0]
print('Sense meaning:', s['meaning_vi'])
print('POS sense:', s['pos'])
print('Context labels:', s['context_labels'])
ex = s['examples'][0]
print('Example sentence:', ex['sentence'])
print('Blank sentence:', ex['blank_sentence'])
print('Answer:', ex['answer'])
print('Accepted answers:', ex['accepted_answers'])
print('Senses count in word:', len(w['senses']))