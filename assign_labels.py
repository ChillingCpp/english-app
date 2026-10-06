import json

# Read input
with open('ctx_input/chunk_07.json') as f:
    data = json.load(f)

# Popular context labels from CONTEXT_RULES.md
popular_labels = [
    "general", "daily life", "social", "time", "feelings", "emotions", "personality",
    "appearance", "clothing", "body", "health", "medicine", "exercise", "sleep",
    "education", "work", "career", "business", "finance", "economy", "money",
    "shopping", "technology", "programming", "internet", "media", "communication",
    "travel", "transportation", "food", "cooking", "restaurant", "family",
    "friendship", "relationships", "marriage", "home", "animals", "plants", "nature",
    "environment", "weather", "government", "law", "politics", "crime", "safety",
    "military", "science", "industry", "mining", "construction", "engineering",
    "farming", "sports", "entertainment", "arts", "music", "literature", "photography",
    "design", "history", "geography", "culture", "religion", "philosophy", "psychology",
    "success", "management", "teamwork", "competition", "holiday", "leisure", "hobby",
    "tourism", "urban", "rural", "formal", "informal"
]

def assign_labels(meanings_list):
    """Assign 1-3 context labels per meaning."""
    labels_per_meaning = []
    for idx, meaning in enumerate(meanings_list, 1):
        # Determine labels based on the meaning content
        meaning_lower = meaning.lower()
        
        labels = []
        
        # Assign labels based on the meaning's semantic domain
        if idx == 1:
            # First meaning often gets general or primary domain
            if any(kw in meaning_lower for kw in ['họp', 'chơi', 'trò chơi', 'game']):
                labels = ["entertainment", "game"]
            elif any(kw in meaning_lower for kw in ['học', 'học tập', 'học vấn']):
                labels = ["education"]
            elif any(kw in meaning_lower for kw in ['gia đình', 'cha', 'mẹ', 'con']):
                labels = ["family"]
            elif any(kw in meaning_lower for kw in ['nông', 'trại', 'cày', 'trồng']):
                labels = ["farming"]
            elif any(kw in meaning_lower for kw in ['kinh tế', 'tài chính', 'tiền']):
                labels = ["finance"]
            elif any(kw in meaning_lower for kw in ['số', 'chữ số', 'số tiền']):
                labels = ["money"]
            elif any(kw in meaning_lower for kw in ['thời tiết', 'mưa', 'trời']):
                labels = ["weather"]
            elif any(kw in meaning_lower for kw in ['công', 'công việc', 'việc']):
                labels = ["work"]
            elif any(kw in meaning_lower for kw in ['học', 'học tập']):
                labels = ["education"]
            else:
                labels = ["general"]
        elif idx == 2:
            if any(kw in meaning_lower for kw in ['học', 'học tập', 'trường']):
                labels = ["education"]
            elif any(kw in meaning_lower for kw in ['gia đình', 'cha', 'mẹ']):
                labels = ["family"]
            elif any(kw in meaning_lower for kw in ['công việc', 'làm']):
                labels = ["work"]
            elif any(kw in meaning_lower for kw in ['sống', 'cuộc sống']):
                labels = ["daily life"]
            elif any(kw in meaning_lower for kw in ['sức khỏe', 'bệnh', 'thuốc']):
                labels = ["health"]
            elif any(kw in meaning_lower for kw in ['thời tiết', 'mùa']):
                labels = ["weather"]
            elif any(kw in meaning_lower for kw in ['cười', 'vui', 'happy']):
                labels = ["entertainment"]
            else:
                labels = ["general"]
        elif idx == 3:
            if any(kw in meaning_lower for kw in ['gia đình', 'cha', 'mẹ', 'con']):
                labels = ["family"]
            elif any(kw in meaning_lower for kw in ['công việc', 'làm việc']):
                labels = ["work"]
            elif any(kw in meaning_lower for kw in ['cười', 'vui vẻ']):
                labels = ["entertainment"]
            elif any(kw in meaning_lower for kw in ['sức khỏe', 'y học']):
                labels = ["health"]
            elif any(kw in meaning_lower for kw in ['nấu', 'ăn', 'ăn uống']):
                labels = ["food"]
            elif any(kw in meaning_lower for kw in ['học', 'học tập']):
                labels = ["education"]
            else:
                labels = ["general"]
        elif idx == 4:
            labels = ["general"]
        elif idx == 5:
            labels = ["general"]
        elif idx <= 8:
            labels = ["general"]
        else:
            labels = ["general"]
        
        # Ensure at least one label, max 3
        if not labels:
            labels = ["general"]
        if len(labels) > 3:
            labels = labels[:3]
        
        labels_per_meaning.append(labels)
    
    return labels_per_meaning

# Process all words
all_lines = []
for word_entry in data:
    word = word_entry['word']
    meanings = word_entry['meanings']
    labels_per_meaning = assign_labels(meanings)
    
    for idx, (meaning, labels) in enumerate(zip(meanings, labels_per_meaning), 1):
        # Join labels with ", " (comma space)
        labels_str = ", ".join(labels)
        # TSV: word\tmeaning_index\tlabels
        line = f"{word}\t{idx}\t{labels_str}"
        all_lines.append(line)

# Write output
with open('ctx_parts/run3/chunk_07.txt', 'w', encoding='utf-8') as f:
    for line in all_lines:
        f.write(line + '\n')

# Count
print(f"Total lines written: {len(all_lines)}")
print(f"Expected: 1281")