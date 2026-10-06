import json
import os

os.makedirs('ctx_parts\\run3', exist_ok=True)

with open('ctx_input\\chunk_11.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Popular context labels from CONTEXT_RULES.md
# These are the labels we should prefer
POPULAR_LABELS_SET = {
    "general", "daily life", "social", "time", "feelings", "emotions", "personality",
    "appearance", "clothing", "body", "health", "medicine", "exercise", "sleep",
    "education", "work", "career", "business", "finance", "economy", "money", "shopping",
    "technology", "programming", "internet", "media", "communication", "travel",
    "transportation", "food", "cooking", "restaurant", "family", "friendship", "relationships",
    "marriage", "home", "animals", "plants", "nature", "environment", "weather",
    "government", "law", "politics", "crime", "safety", "military", "science",
    "industry", "mining", "construction", "engineering", "farming", "sports",
    "entertainment", "arts", "music", "literature", "photography", "design",
    "history", "geography", "culture", "religion", "philosophy", "psychology",
    "success", "management", "teamwork", "competition", "holiday", "leisure", "hobby",
    "tourism", "urban", "rural", "formal", "informal"
}

# For each word and meaning, assign labels based on the meaning content
# The label should describe the SITUATION where that sense is used

output_lines = []

# Mapping from Vietnamese meaning keywords to context labels
# This is based on careful analysis of when each sense is used

def assign_labels(meaning_text):
    """Assign 1-4 context labels describing the situation where this sense is used."""
    labels = []
    meaning_lower = meaning_text.lower()
    
    # Skip very short meaningless labels
    # Analyze the meaning and determine the situational context
    
    # === Mining / Extraction ===
    if any(kw in meaning_lower for kw in ['mỏ', 'đào', 'khoáng', 'quặng', 'thủy lôi', 'địa lôi', 'mìn', 'bóng mìn']):
        # Mining, mineral extraction, landmines
        if any(kw in meaning_lower for kw in ['mìn', 'địa lôi', 'thủy lôi', 'bóng mìn', 'phá hoại']):
            # Landmine/underwater mine - military context
            if 'military' not in labels:
                labels.append('military')
            if 'defense' not in labels:
                labels.append('defense')
        else:
            # Actual mining operation
            if 'mining' not in labels:
                labels.append('mining')
            if 'industry' not in labels:
                labels.append('industry')
        if 'economy' not in labels:
            labels.append('economy')
    
    # === Mineral / Chemical ===
    elif any(kw in meaning_lower for kw in ['khoáng', 'vô cơ', 'khoáng vật', 'nước khoáng']):
        if 'industry' not in labels:
            labels.append('industry')
        if 'science' not in labels:
            labels.append('science')
    
    # === Mathematical / Quantitative ===
    elif any(kw in meaning_lower for kw in ['tối thiểu', 'số lượng', 'mức tối thiểu', 'lớn nhất', 'hơn hơn']):
        if 'mathematics' not in labels:
            labels.append('mathematics')
        if 'quantification' not in labels:
            labels.append('quantification')
    
    # === Government / Political ===
    elif any(kw in meaning_lower for kw in ['bộ tướng', 'chính phủ', 'quốc gia', 'quốc dân', 'chính trị']):
        if 'government' not in labels:
            labels.append('government')
        if 'politics' not in labels:
            labels.append('politics')
    
    # === Military / Defense ===
    elif any(kw in meaning_lower for kw in ['quân sự', 'công binh', 'pháo', 'tài']):
        if 'military' not in labels:
            labels.append('military')
        if 'defense' not in labels:
            labels.append('defense')
    
    # === Family / Household ===
    elif any(kw in meaning_lower for kw in ['mẹ', 'cha', 'con', 'gia đình', 'phụ', 'mẫu', 'nuôi']):
        if 'family' not in labels:
            labels.append('family')
    
    # === Work / Employment ===
    elif any(kw in meaning_lower for kw in ['công việc', 'làm', 'việc', 'cơ', 'động cơ', 'làm việc', 'nghề']):
        if 'work' not in labels:
            labels.append('work')
    
    # === Education ===
    elif any(kw in meaning_lower for kw in ['học', 'trường', 'giáo viên', 'học tập', 'bài học', 'khóa học']):
        if 'education' not in labels:
            labels.append('education')
    
    # === Money / Finance ===
    elif any(kw in meaning_lower for kw in ['tiền', 'tiền tệ', 'tài sản', 'thanh toán', 'tiết kiệm', 'tiiền']):
        if 'money' not in labels:
            labels.append('money')
        if 'finance' not in labels:
            labels.append('finance')
    
    # === Time / Temporal ===
    elif any(kw in meaning_lower for kw in ['giờ', 'ngày', 'tháng', 'năm', 'buổi', 'lúc', 'thời gian']):
        if 'time' not in labels:
            labels.append('time')
    
    # === Nature / Environment ===
    elif any(kw in meaning_lower for kw in ['mặt trăng', 'trăng', 'bùn', 'thiên nhiên', 'cây cối']):
        if 'nature' not in labels:
            labels.append('nature')
    
    # === Animals ===
    elif any(kw in meaning_lower for kw in ['con khỉ', 'con chó', 'con mèo', 'thú vật', 'con cuốn']):
        if 'animals' not in labels:
            labels.append('animals')
    
    # === Appearance / Physical ===
    elif any(kw in meaning_lower for kw in ['xinh', 'đẹp', 'rõ', 'sạch', 'néat', 'trang', 'dáng']):
        if 'appearance' not in labels:
            labels.append('appearance')
    
    # === Health / Medicine ===
    elif any(kw in meaning_lower for kw in ['y tá', 'bệnh', 'cơ địa', 'sức khỏe', 'thuốc', 'chữa']):
        if 'health' not in labels:
            labels.append('health')
        if 'medicine' not in labels:
            labels.append('medicine')
    
    # === Transportation / Travel ===
    elif any(kw in meaning_lower for kw in ['xe', 'đạp', 'công đường', 'máy bay', ' tàu', 'lãn đón']):
        if 'transportation' not in labels:
            labels.append('transportation')
    
    # === Food / Cooking ===
    elif any(kw in meaning_lower for kw in ['ăn', 'nấu', 'thực đơn', 'nguyên liệu', 'cơm', 'món ăn']):
        if 'food' not in labels:
            labels.append('food')
        if 'cooking' not in labels:
            labels.append('cooking')
    
    # === Shopping / Commerce ===
    elif any(kw in meaning_lower for kw in ['mua', 'bán', 'cửa hàng', 'giá', 'số lượng mua']):
        if 'shopping' not in labels:
            labels.append('shopping')
    
    # === Media / Entertainment ===
    elif any(kw in meaning_lower for kw in ['phim', 'ca nhạc', 'diễn', 'bài hát', 'nghe nhạc']):
        if 'entertainment' not in labels:
            labels.append('entertainment')
    
    # === Religion / Spiritual ===
    elif any(kw in meaning_lower for kw in ['thờ', 'kiến', 'tôn giáo', 'thánh', 'kiến đồ', 'phép']):
        if 'religion' not in labels:
            labels.append('religion')
    
    # === Science / Technology ===
    elif any(kw in meaning_lower for kw in ['hóa', 'vật lý', 'khoa học', 'thí nghiệm', 'công thức', 'điện']):
        if 'science' not in labels:
            labels.append('science')
    
    # === Art / Literature ===
    elif any(kw in meaning_lower for kw in ['tiểu thuyết', 'thơ', 'văn học', 'bức tranh', 'phong ca']):
        if 'arts' not in labels:
            labels.append('arts')
    
    # === Social / Daily Life ===
    elif any(kw in meaning_lower for kw in ['xóm', 'hàng xóm', 'bộ đôi', 'cưới hỏi', 'cấp hô']):
        if 'social' not in labels:
            labels.append('social')
    
    # === General fallback ===
    else:
        if 'general' not in labels:
            labels.append('general')
    
    # Limit to max 4 labels
    labels = labels[:4]
    
    # If we only have 1 label and it's not general, that's fine
    # But we need at least 1 label
    if not labels:
        labels = ['general']
    
    return labels


for entry in data:
    word = entry['word']
    meanings = entry['meanings']
    
    for idx, meaning in enumerate(meanings, 1):  # 1-based index
        labels = assign_labels(meaning)
        label_str = ", ".join(labels)
        output_lines.append(f"{word}\t{idx}\t{label_str}")

# Write output
with open('ctx_parts\\run3\\chunk_11.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Wrote {len(output_lines)} lines")