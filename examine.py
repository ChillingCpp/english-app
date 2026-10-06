import json

with open('ctx_input\\chunk_11.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Let me examine a few specific words and meanings
for entry in data[:5]:
    word = entry['word']
    meanings = entry['meanings']
    print(f"\n=== {word} ===")
    for i, m in enumerate(meanings, 1):
        print(f"  {i}: {m}")