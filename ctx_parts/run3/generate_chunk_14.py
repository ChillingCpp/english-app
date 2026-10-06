import json

# Read input
with open('E:/vibe_coding/english-app/ctx_input/chunk_14.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Count words and meanings
total_meanings = 0
for item in data:
    total_meanings += len(item['meanings'])

print(f"Words: {len(data)}")
print(f"Total meanings: {total_meanings}")

# Print word counts for verification
for item in data:
    print(f"{item['word']}: {len(item['meanings'])}")
