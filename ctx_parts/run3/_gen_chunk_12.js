const fs = require('fs');
const path = require('path');

const input = JSON.parse(fs.readFileSync('E:/vibe_coding/english-app/ctx_input/chunk_12.json', 'utf8'));

// Labels per word, indexed by 1-based meaning index
const L = {
  "opponent": {
    1: "competition, conflict",
    2: "competition, conflict"
  },
  "opportunity": {
    1: "time, general",
    2: "career, general"
  },
  "oppose": {
    1: "competition, conflict",
    2: "politics, law",
    3: "conflict, general"
  },
  "opposed": {
    1: "education, grammar",
    2: "politics, conflict"
  },
  "opposite": {
    1: "general",
    2: "general",
    3: "general",
    4: "general"
  },
  "opposition": {
    1: "conflict, general",
    2: "general",
    3: "politics, conflict",
    4: "politics, government",
    5: "politics"
  },
  "option": {
    1: "general",
    2: "general",
    3: "finance, business"
  },
  "or": {
    1: "education, grammar",
    2: "general",
    3: "general",
    4: "time",
    5: "money",
    6: "money",
    7: "time"
  },
  "orange": {
    1: "food",
    2: "plants",
    3: "appearance",
    4: "appearance",
    5: "appearance"
  },
  "order": {
    1: "work, general",
    2: "general",
    3: "general",
    4: "law, government",
    5: "military, management",
    6: "medicine",
    7: "restaurant, shopping",
    8: "general",
    9: "work, general"
  },
  "ordinary": {
    1: "daily life, general",
    2: "daily life",
    3: "restaurant, food",
    4: "restaurant",
    5: "transportation",
    6: "religion",
    7: "religion",
    8: "religion, law"
  },
  "organ": {
    1: "music",
    2: "body, work",
    3: "media, government",
    4: "body, music"
  },
  "organization": {
    1: "management, work",
    2: "work, business"
  },
  "organize": {
    1: "management, work",
    2: "work",
    3: "management",
    4: "work"
  },
  "organized": {
    1: "education, grammar",
    2: "work, management",
    3: "work",
    4: "work"
  },
  "organizer": {
    1: "work, management",
    2: "work"
  },
  "origin": {
    1: "history, general",
    2: "family, history"
  },
  "original": {
    1: "history, general",
    2: "general",
    3: "personality",
    4: "general",
    5: "personality"
  },
  "originally": {
    1: "history, general",
    2: "general",
    3: "personality",
    4: "general",
    5: "personality"
  },
  "other": {
    1: "general",
    2: "general",
    3: "social, general",
    4: "general"
  },
  "otherwise": {
    1: "general",
    2: "general",
    3: "general"
  },
  "ought": {
    1: "general",
    2: "general",
    3: "general"
  },
  "our": {
    1: "general",
    2: "government, formal"
  },
  "ours": {
    1: "animals",
    2: "personality, social",
    3: "crime, law",
    4: "arts",
    5: "health",
    6: "animals",
    7: "general"
  },
  "ourselves": {
    1: "general"
  },
  "out": {
    1: "general",
    2: "general",
    3: "general",
    4: "politics",
    5: "work",
    6: "general",
    7: "clothing, culture",
    8: "communication",
    9: "health, body",
    10: "health",
    11: "general",
    12: "feelings",
    13: "media",
    14: "sports",
    15: "general",
    16: "general",
    17: "general",
    18: "general",
    19: "general",
    20: "general",
    21: "sports",
    22: "sports",
    23: "entertainment",
    24: "politics",
    25: "media",
    26: "work",
    27: "sports",
    28: "social",
    29: "social, communication"
  },
  "outcome": {
    1: "general",
    2: "education, philosophy"
  },
  "outdoor": {
    1: "nature"
  },
  "outdoors": {
    1: "nature",
    2: "general",
    3: "nature"
  },
  "outer": {
    1: "general",
    2: "sports",
    3: "sports"
  },
  "outline": {
    1: "arts, design",
    2: "appearance",
    3: "education, work",
    4: "general",
    5: "arts",
    6: "arts",
    7: "education, work"
  },
  "outside": {
    1: "general",
    2: "society, general",
    3: "transportation",
    4: "work",
    5: "travel, general",
    6: "general",
    7: "general",
    8: "general",
    9: "general",
    10: "general",
    11: "education"
  },
  "oven": {
    1: "cooking"
  },
  "over": {
    1: "general",
    2: "general",
    3: "general",
    4: "general",
    5: "general",
    6: "general",
    7: "general",
    8: "general",
    9: "general",
    10: "general",
    11: "general",
    12: "general",
    13: "time",
    14: "general",
    15: "military",
    16: "general",
    17: "general",
    18: "general",
    19: "time"
  },
  "overall": {
    1: "general",
    2: "clothing, work",
    3: "clothing, work",
    4: "military, clothing"
  },
  "overseas": {
    1: "travel, geography"
  },
  "owe": {
    1: "money, finance",
    2: "general"
  },
  "own": {
    1: "general",
    2: "general",
    3: "general",
    4: "crime, law"
  },
  "owner": {
    1: "business, general"
  },
  "pace": {
    1: "body, general",
    2: "sports, exercise",
    3: "animals",
    4: "animals",
    5: "work, general",
    6: "general",
    7: "animals",
    8: "general",
    9: "sports",
    10: "formal, communication"
  },
  "pack": {
    1: "travel, clothing",
    2: "animals",
    3: "general",
    4: "entertainment",
    5: "business",
    6: "sports",
    7: "nature, environment",
    8: "health, medicine",
    9: "health",
    10: "business",
    11: "animals",
    12: "general",
    13: "animals, transportation",
    14: "construction",
    15: "health",
    16: "law, politics",
    17: "crime",
    18: "travel",
    19: "business",
    20: "animals",
    21: "travel"
  },
  "package": {
    1: "business, shopping",
    2: "business",
    3: "media",
    4: "general",
    5: "business",
    6: "business, design",
    7: "general"
  },
  "page": {
    1: "literature, history",
    2: "media, education",
    3: "general",
    4: "work",
    5: "work",
    6: "work"
  },
  "pain": {
    1: "health, feelings",
    2: "health, medicine",
    3: "work",
    4: "law, crime",
    5: "feelings",
    6: "health"
  },
  "painful": {
    1: "health, feelings",
    2: "work"
  },
  "paint": {
    1: "construction, home",
    2: "arts",
    3: "appearance, health",
    4: "construction",
    5: "arts",
    6: "appearance",
    7: "arts",
    8: "appearance"
  },
  "painter": {
    1: "arts, work",
    2: "transportation"
  },
  "painting": {
    1: "education, grammar",
    2: "construction",
    3: "arts",
    4: "arts"
  },
  "pair": {
    1: "general",
    2: "marriage, animals",
    3: "general",
    4: "politics",
    5: "general",
    6: "relationships, marriage",
    7: "relationships",
    8: "relationships, animals"
  },
  "palace": {
    1: "history",
    2: "religion",
    3: "restaurant"
  },
  "pale": {
    1: "general",
    2: "appearance, health",
    3: "appearance, health",
    4: "general",
    5: "appearance",
    6: "appearance"
  },
  "pan": {
    1: "cooking",
    2: "cooking",
    3: "cooking",
    4: "cooking",
    5: "home",
    6: "mining",
    7: "geography",
    8: "media",
    9: "cooking",
    10: "food",
    11: "food",
    12: "home",
    13: "home",
    14: "body",
    15: "construction",
    16: "cooking",
    17: "military",
    18: "body",
    19: "construction",
    20: "home",
    21: "general",
    22: "military",
    23: "money",
    24: "general",
    25: "industry",
    26: "mining",
    27: "media",
    28: "success",
    29: "photography",
    30: "mining",
    31: "general",
    32: "photography",
    33: "music, technology",
    34: "social",
    35: "religion"
  },
  "panel": {
    1: "construction",
    2: "work, communication",
    3: "technology",
    4: "construction"
  },
  "pants": {
    1: "education, grammar",
    2: "clothing",
    3: "clothing"
  },
  "paper": {
    1: "general",
    2: "work, law",
    3: "media",
    4: "money, finance",
    5: "shopping",
    6: "entertainment",
    7: "education",
    8: "education",
    9: "home",
    10: "shopping",
    11: "work",
    12: "entertainment"
  },
  "paragraph": {
    1: "education, literature",
    2: "education",
    3: "media",
    4: "education",
    5: "media"
  },
  "parent": {
    1: "family",
    2: "family",
    3: "general",
    4: "family"
  },
  "park": {
    1: "nature, leisure",
    2: "nature",
    3: "transportation, military",
    4: "urban",
    5: "military",
    6: "transportation"
  },
  "parking": {
    1: "education, grammar",
    2: "transportation"
  },
  "part": {
    1: "general",
    2: "body",
    3: "work",
    4: "entertainment",
    5: "geography",
    6: "social",
    7: "social",
    8: "general",
    9: "general",
    10: "general",
    11: "general",
    12: "general",
    13: "relationships",
    14: "health",
    15: "general",
    16: "general"
  },
  "participant": {
    1: "work, general",
    2: "general"
  },
  "participate": {
    1: "teamwork, general",
    2: "general"
  },
  "particular": {
    1: "general",
    2: "general",
    3: "general",
    4: "personality",
    5: "general",
    6: "general",
    7: "general"
  },
  "particularly": {
    1: "general",
    2: "general",
    3: "general",
    4: "personality",
    5: "general",
    6: "general",
    7: "general"
  },
  "partly": {
    1: "general",
    2: "body",
    3: "work",
    4: "entertainment",
    5: "geography",
    6: "social",
    7: "social",
    8: "general",
    9: "general",
    10: "general",
    11: "general",
    12: "general",
    13: "relationships",
    14: "health",
    15: "general",
    16: "general"
  },
  "partner": {
    1: "business, work",
    2: "business, law",
    3: "entertainment",
    4: "entertainment",
    5: "marriage, family",
    6: "transportation",
    7: "business",
    8: "social",
    9: "business"
  },
  "party": {
    1: "general",
    2: "body",
    3: "work",
    4: "entertainment",
    5: "geography",
    6: "social",
    7: "social",
    8: "general",
    9: "general",
    10: "general",
    11: "general",
    12: "general",
    13: "relationships",
    14: "health",
    15: "general",
    16: "general",
    17: "holiday, social, politics"
  },
  "pass": {
    1: "travel, general",
    2: "time, general",
    3: "general",
    4: "general",
    5: "health",
    6: "time",
    7: "law, government",
    8: "education",
    9: "general",
    10: "general",
    11: "general",
    12: "games",
    13: "law",
    14: "law",
    15: "money",
    16: "sports",
    17: "health, body",
    18: "travel",
    19: "general",
    20: "law",
    21: "education",
    22: "general",
    23: "general",
    24: "sports",
    25: "money, crime",
    26: "law, communication",
    27: "general",
    28: "education",
    29: "general",
    30: "law, travel",
    31: "sports",
    32: "games, crime",
    33: "psychology",
    34: "geography",
    35: "geography, military",
    36: "geography, transportation",
    37: "animals",
    38: "technology, engineering"
  },
  "passage": {
    1: "travel, time",
    2: "travel",
    3: "home",
    4: "law, travel",
    5: "general",
    6: "travel",
    7: "literature",
    8: "law",
    9: "social, communication",
    10: "education",
    11: "health, body",
    12: "animals",
    13: "animals"
  },
  "passenger": {
    1: "transportation",
    2: "work, teamwork",
    3: "transportation"
  },
  "passion": {
    1: "feelings, emotions",
    2: "feelings, emotions",
    3: "relationships",
    4: "feelings, hobby",
    5: "religion",
    6: "religion, music",
    7: "feelings"
  },
  "passport": {
    1: "travel, law",
    2: "general"
  },
  "past": {
    1: "time, history",
    2: "time, history",
    3: "time, history",
    4: "time, history",
    5: "general",
    6: "general",
    7: "general"
  },
  "path": {
    1: "travel, nature",
    2: "general, career"
  },
  "patient": {
    1: "personality",
    2: "health, medicine",
    3: "general"
  },
  "pattern": {
    1: "general",
    2: "shopping, business",
    3: "design, general",
    4: "design, clothing",
    5: "transportation",
    6: "military",
    7: "general",
    8: "design, arts"
  },
  "pay": {
    1: "money, work",
    2: "money, work",
    3: "social",
    4: "money, finance",
    5: "money",
    6: "general",
    7: "money, business",
    8: "construction"
  },
  "payment": {
    1: "money, finance",
    2: "money, work"
  },
  "peace": {
    1: "politics",
    2: "politics, law",
    3: "safety, society",
    4: "feelings"
  },
  "peaceful": {
    1: "politics",
    2: "safety, feelings",
    3: "feelings"
  },
  "pen": {
    1: "education, writing",
    2: "education, writing",
    3: "literature",
    4: "literature",
    5: "animals, farming",
    6: "geography",
    7: "general",
    8: "animals",
    9: "education, writing",
    10: "crime",
    11: "animals, farming"
  },
  "pencil": {
    1: "education",
    2: "general",
    3: "education",
    4: "arts",
    5: "arts",
    6: "education",
    7: "gambling",
    8: "general"
  },
  "penny": {
    1: "money",
    2: "money",
    3: "money"
  },
  "people": {
    1: "society, politics",
    2: "general",
    3: "society, general",
    4: "family",
    5: "work, social",
    6: "geography, travel",
    7: "education, grammar"
  },
  "pepper": {
    1: "food, cooking",
    2: "food",
    3: "cooking",
    4: "general",
    5: "military, crime",
    6: "communication",
    7: "law, crime"
  },
  "per": {
    1: "general",
    2: "general",
    3: "general"
  },
  "percent": {
    1: "education, finance"
  },
  "percentage": {
    1: "education, finance",
    2: "general, education"
  },
  "perfect": {
    1: "general",
    2: "education",
    3: "education, grammar",
    4: "plants",
    5: "music",
    6: "education, grammar",
    7: "general",
    8: "education"
  },
  "perfectly": {
    1: "general",
    2: "education",
    3: "education, grammar",
    4: "plants",
    5: "music",
    6: "education, grammar",
    7: "general",
    8: "education"
  },
  "perform": {
    1: "work",
    2: "entertainment, arts",
    3: "entertainment",
    4: "entertainment"
  },
  "performance": {
    1: "work",
    2: "entertainment",
    3: "success",
    4: "success, work",
    5: "technology, work",
    6: "general",
    7: "transportation"
  },
  "perhaps": {
    1: "general"
  },
  "period": {
    1: "time, history",
    2: "time, history",
    3: "education",
    4: "health, body",
    5: "science",
    6: "education",
    7: "education",
    8: "literature",
    9: "history"
  },
  "permanent": {
    1: "time, general",
    2: "home"
  },
  "permission": {
    1: "law, general",
    2: "law"
  },
  "permit": {
    1: "law",
    2: "law",
    3: "law, general",
    4: "general"
  },
  "person": {
    1: "general",
    2: "informal, social",
    3: "general",
    4: "body, appearance",
    5: "literature, entertainment",
    6: "education, grammar",
    7: "law, business",
    8: "general"
  },
  "personal": {
    1: "general",
    2: "communication, social",
    3: "psychology",
    4: "general"
  },
  "personality": {
    1: "general",
    2: "communication",
    3: "psychology",
    4: "general",
    5: "personality, psychology"
  },
  "personally": {
    1: "general",
    2: "communication",
    3: "psychology",
    4: "general"
  },
  "perspective": {
    1: "general",
    2: "arts",
    3: "arts",
    4: "general",
    5: "arts",
    6: "general"
  },
  "persuade": {
    1: "communication, psychology"
  },
  "pet": {
    1: "feelings",
    2: "animals, home",
    3: "relationships, family",
    4: "feelings",
    5: "feelings"
  },
  "phase": {
    1: "science",
    2: "general",
    3: "general",
    4: "science",
    5: "work, management",
    6: "technology, engineering"
  },
  "phenomenon": {
    1: "science, general",
    2: "general"
  },
  "philosophy": {
    1: "philosophy, education",
    2: "philosophy",
    3: "education",
    4: "philosophy",
    5: "history",
    6: "philosophy",
    7: "philosophy",
    8: "philosophy"
  },
  "phone": {
    1: "technology, communication",
    2: "communication",
    3: "communication"
  },
  "photo": {
    1: "photography",
    2: "photography"
  },
  "photograph": {
    1: "photography",
    2: "photography",
    3: "photography"
  },
  "photographer": {
    1: "photography, work"
  },
  "photography": {
    1: "photography",
    2: "photography",
    3: "photography"
  },
  "phrase": {
    1: "communication",
    2: "education",
    3: "education",
    4: "communication",
    5: "communication",
    6: "music",
    7: "communication",
    8: "education"
  },
  "physical": {
    1: "science",
    2: "science",
    3: "science",
    4: "body, health"
  },
  "physics": {
    1: "science, education"
  },
  "piano": {
    1: "music",
    2: "music"
  },
  "pick": {
    1: "general",
    2: "general",
    3: "general",
    4: "work",
    5: "work",
    6: "work",
    7: "health, body",
    8: "farming, plants",
    9: "farming, food",
    10: "food, cooking",
    11: "animals, food",
    12: "food",
    13: "crime",
    14: "general",
    15: "music",
    16: "general",
    17: "crime, conflict",
    18: "food",
    19: "crime",
    20: "general"
  },
  "picture": {
    1: "arts, photography",
    2: "arts, photography",
    3: "general",
    4: "general",
    5: "general",
    6: "appearance, nature",
    7: "entertainment",
    8: "general",
    9: "general",
    10: "communication, literature",
    11: "psychology"
  },
  "piece": {
    1: "general",
    2: "general",
    3: "general, shopping",
    4: "arts, music, literature",
    5: "military",
    6: "games",
    7: "general",
    8: "money",
    9: "music",
    10: "informal, social",
    11: "construction",
    12: "clothing",
    13: "food"
  },
  "pig": {
    1: "animals, farming",
    2: "food",
    3: "personality, informal",
    4: "industry",
    5: "food",
    6: "crime",
    7: "animals",
    8: "animals",
    9: "home, informal"
  },
  "pile": {
    1: "construction",
    2: "construction",
    3: "construction",
    4: "general",
    5: "religion",
    6: "money, finance",
    7: "urban",
    8: "technology",
    9: "technology",
    10: "general",
    11: "military",
    12: "general",
    13: "transportation",
    14: "money, games",
    15: "clothing",
    16: "clothing",
    17: "construction",
    18: "health, medicine"
  },
  "pilot": {
    1: "transportation",
    2: "transportation",
    3: "travel",
    4: "transportation",
    5: "transportation",
    6: "general"
  },
  "pin": {
    1: "clothing",
    2: "clothing, general",
    3: "technology, engineering",
    4: "technology, engineering",
    5: "music",
    6: "body",
    7: "food",
    8: "clothing",
    9: "general",
    10: "general",
    11: "general",
    12: "construction"
  },
  "pink": {
    1: "appearance",
    2: "politics",
    3: "plants",
    4: "appearance",
    5: "general",
    6: "clothing",
    7: "medicine",
    8: "transportation",
    9: "sports",
    10: "clothing, design",
    11: "design, arts",
    12: "animals",
    13: "animals",
    14: "technology"
  },
  "pipe": {
    1: "construction, engineering",
    2: "music",
    3: "clothing",
    4: "health",
    5: "mining",
    6: "transportation",
    7: "music, animals",
    8: "animals",
    9: "food",
    10: "general",
    11: "construction",
    12: "music",
    13: "transportation, military",
    14: "transportation",
    15: "music",
    16: "clothing",
    17: "plants, farming",
    18: "general",
    19: "transportation",
    20: "music",
    21: "general"
  },
  "pitch": {
    1: "construction",
    2: "construction",
    3: "sports, general",
    4: "sports",
    5: "transportation",
    6: "animals",
    7: "music",
    8: "general",
    9: "construction",
    10: "business",
    11: "business",
    12: "engineering",
    13: "travel",
    14: "general",
    15: "business",
    16: "construction",
    17: "sports",
    18: "communication",
    19: "music",
    20: "communication",
    21: "travel",
    22: "transportation"
  },
  "place": {
    1: "geography, general",
    2: "home",
    3: "general, work",
    4: "work",
    5: "work",
    6: "society, work",
    7: "literature, education",
    8: "urban",
    9: "general",
    10: "education",
    11: "general",
    12: "general",
    13: "work",
    14: "finance, business",
    15: "general",
    16: "general",
    17: "business",
    18: "general",
    19: "general",
    20: "sports"
  },
  "plain": {
    1: "geography, nature",
    2: "general",
    3: "general",
    4: "communication, military",
    5: "general",
    6: "personality",
    7: "clothing, design",
    8: "appearance, informal",
    9: "general",
    10: "literature"
  },
  "plan": {
    1: "construction, design",
    2: "geography, travel",
    3: "arts",
    4: "education",
    5: "work, management",
    6: "general",
    7: "construction, design",
    8: "education",
    9: "work, management"
  },
  "plane": {
    1: "plants",
    2: "work",
    3: "work",
    4: "construction",
    5: "education",
    6: "transportation",
    7: "science",
    8: "general",
    9: "general",
    10: "travel",
    11: "transportation",
    12: "general",
    13: "general"
  },
  "planet": {
    1: "science"
  },
  "planning": {
    1: "education, grammar",
    2: "work, management",
    3: "urban"
  },
  "plant": {
    1: "plants",
    2: "industry",
    3: "farming",
    4: "farming"
  },
  "plastic": {
    1: "industry",
    2: "general",
    3: "arts, design",
    4: "personality, general"
  },
  "plate": {
    1: "industry",
    2: "general",
    3: "arts",
    4: "photography",
    5: "construction",
    6: "food, restaurant",
    7: "money",
    8: "religion",
    9: "sports",
    10: "health, medicine",
    11: "transportation",
    12: "media",
    13: "science",
    14: "industry",
    15: "industry",
    16: "media"
  },
  "platform": {
    1: "construction",
    2: "transportation",
    3: "transportation",
    4: "transportation",
    5: "education, communication",
    6: "communication",
    7: "politics",
    8: "media, technology",
    9: "general",
    10: "communication"
  },
  "play": {
    1: "leisure, entertainment",
    2: "sports",
    3: "general",
    4: "gambling, entertainment",
    5: "entertainment",
    6: "general",
    7: "work, general",
    8: "technology, engineering",
    9: "technology, engineering",
    10: "work",
    11: "leisure",
    12: "music",
    13: "sports",
    14: "gambling",
    15: "entertainment",
    16: "military, safety",
    17: "general",
    18: "general",
    19: "technology",
    20: "work",
    21: "sports",
    22: "music, sports",
    23: "sports, games",
    24: "sports",
    25: "sports",
    26: "entertainment",
    27: "general",
    28: "general",
    29: "military, safety",
    30: "animals"
  },
  "player": {
    1: "sports",
    2: "music",
    3: "entertainment",
    4: "sports",
    5: "gambling"
  },
  "pleasant": {
    1: "feelings, personality",
    2: "feelings",
    3: "personality, entertainment"
  },
  "please": {
    1: "social, communication",
    2: "general",
    3: "formal, communication",
    4: "communication"
  },
  "pleased": {
    1: "education, grammar",
    2: "feelings",
    3: "feelings"
  },
  "pleasure": {
    1: "feelings, leisure",
    2: "leisure, entertainment",
    3: "general",
    4: "social",
    5: "feelings"
  },
  "plenty": {
    1: "money, general",
    2: "general"
  },
  "plot": {
    1: "farming, geography",
    2: "literature, entertainment",
    3: "education, science",
    4: "crime, politics",
    5: "education, science",
    6: "general",
    7: "crime",
    8: "crime"
  },
  "plus1": {
    1: "education"
  },
  "pocket": {
    1: "clothing",
    2: "general",
    3: "money",
    4: "sports",
    5: "mining",
    6: "transportation",
    7: "military",
    8: "urban",
    9: "sports",
    10: "general",
    11: "crime",
    12: "general",
    13: "sports",
    14: "sports"
  },
  "poem": {
    1: "literature",
    2: "literature, arts"
  },
  "poet": {
    1: "literature"
  },
  "poetry": {
    1: "literature",
    2: "literature"
  },
  "point": {
    1: "general",
    2: "work",
    3: "geography",
    4: "military",
    5: "general",
    6: "clothing",
    7: "animals",
    8: "education",
    9: "education",
    10: "general",
    11: "general",
    12: "geography",
    13: "time",
    14: "general",
    15: "communication",
    16: "media",
    17: "transportation",
    18: "education",
    19: "animals",
    20: "education",
    21: "general",
    22: "communication",
    23: "general",
    24: "music, religion",
    25: "construction",
    26: "animals",
    27: "general",
    28: "general",
    29: "communication",
    30: "animals"
  },
  "pointed": {
    1: "education, grammar",
    2: "general",
    3: "communication",
    4: "general"
  },
  "poison": {
    1: "health, crime",
    2: "media, communication",
    3: "crime, health",
    4: "general",
    5: "crime"
  },
  "poisonous": {
    1: "health, animals"
  },
  "police": {
    1: "crime, law",
    2: "crime, law",
    3: "crime, military",
    4: "safety, crime",
    5: "crime"
  },
  "policeman": {
    1: "crime, law"
  },
  "policy": {
    1: "politics, government",
    2: "management, general",
    3: "personality",
    4: "home",
    5: "law, business"
  },
  "polite": {
    1: "social, communication",
    2: "literature"
  },
  "political": {
    1: "politics",
    2: "politics, government",
    3: "politics, government"
  },
  "politician": {
    1: "politics",
    2: "politics, informal"
  },
  "politics": {
    1: "politics",
    2: "politics",
    3: "politics"
  },
  "pollution": {
    1: "environment, religion",
    2: "environment",
    3: "general"
  },
  "pool": {
    1: "nature, geography",
    2: "sports, leisure",
    3: "nature, geography",
    4: "gambling, games",
    5: "gambling",
    6: "business, finance",
    7: "business, economy",
    8: "sports",
    9: "general",
    10: "business, finance"
  },
  "poor": {
    1: "money",
    2: "general",
    3: "personality, informal",
    4: "feelings",
    5: "general",
    6: "personality"
  },
  "pop": {
    1: "music, entertainment",
    2: "music, entertainment",
    3: "family, informal",
    4: "general",
    5: "animals, farming",
    6: "food",
    7: "general",
    8: "general",
    9: "crime, military",
    10: "general",
    11: "general",
    12: "general",
    13: "communication",
    14: "general",
    15: "food, cooking",
    16: "general",
    17: "general"
  },
  "popular": {
    1: "society, culture",
    2: "culture, society",
    3: "society, politics",
    4: "society, informal"
  }
};

// Validate coverage
let errors = [];
let totalMeanings = 0;
for (const w of input) {
  const labels = L[w.word];
  if (!labels) { errors.push(`MISSING word: ${w.word}`); continue; }
  for (let i = 1; i <= w.meanings.length; i++) {
    totalMeanings++;
    if (!labels[i]) { errors.push(`MISSING ${w.word} meaning ${i}`); }
  }
  // extra labels check
  for (const k of Object.keys(labels)) {
    if (parseInt(k) > w.meanings.length) errors.push(`EXTRA ${w.word} meaning ${k}`);
  }
}
if (errors.length) {
  console.error('ERRORS:\n' + errors.join('\n'));
  process.exit(1);
}

// Build lines
const lines = [];
for (const w of input) {
  for (let i = 1; i <= w.meanings.length; i++) {
    lines.push(`${w.word}\t${i}\t${L[w.word][i]}`);
  }
}

// Split into chunks of ~200 lines
const outDir = 'E:/vibe_coding/english-app/ctx_parts/run3';
fs.mkdirSync(outDir, { recursive: true });
const CHUNK = 200;
let idx = 0;
let fileNum = 0;
while (idx < lines.length) {
  const slice = lines.slice(idx, idx + CHUNK);
  const fname = fileNum === 0 ? 'chunk_12.txt' : `chunk_12${String.fromCharCode(98 + fileNum - 1)}.txt`;
  fs.writeFileSync(path.join(outDir, fname), slice.join('\n') + '\n', 'utf8');
  console.log(`${fname}: ${slice.length} lines`);
  idx += CHUNK;
  fileNum++;
}
console.log(`TOTAL lines=${lines.length} words=${input.length} meanings=${totalMeanings}`);
