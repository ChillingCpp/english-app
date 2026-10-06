# -*- coding: utf-8 -*-
"""Tạo schema SQLite cho vocabulary database theo 'file hướng dẫn'."""
import sqlite3
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = 'dataset/vocabulary.sqlite'

if Path(DB_PATH).exists():
    Path(DB_PATH).unlink()

con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

cur.executescript("""
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL UNIQUE,
    pronunciation TEXT,
    cefr TEXT,
    part_of_speech TEXT,
    word_source TEXT,
    status TEXT DEFAULT 'ready',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE senses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    meaning_vi TEXT NOT NULL,
    pos TEXT,
    sense_order INTEGER DEFAULT 0,
    source_id INTEGER,
    status TEXT DEFAULT 'ready',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE TABLE contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sense_contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sense_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sense_id) REFERENCES senses(id) ON DELETE CASCADE,
    FOREIGN KEY (context_id) REFERENCES contexts(id) ON DELETE CASCADE,
    UNIQUE(sense_id, context_id)
);

CREATE TABLE examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sense_id INTEGER NOT NULL,
    sentence TEXT NOT NULL,
    blank_sentence TEXT NOT NULL,
    answer TEXT NOT NULL,
    source_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sense_id) REFERENCES senses(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE TABLE accepted_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    example_id INTEGER NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (example_id) REFERENCES examples(id) ON DELETE CASCADE
);

CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT,
    source_name TEXT,
    verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_words_word ON words(word);
CREATE INDEX idx_senses_word_id ON senses(word_id);
CREATE INDEX idx_examples_sense_id ON examples(sense_id);
CREATE INDEX idx_sense_contexts_sense_id ON sense_contexts(sense_id);
CREATE INDEX idx_sense_contexts_context_id ON sense_contexts(context_id);
CREATE INDEX idx_accepted_answers_example_id ON accepted_answers(example_id);
CREATE UNIQUE INDEX idx_accepted_answers_unique ON accepted_answers(example_id, answer);

INSERT INTO sources (source_type, source_name, verified) VALUES
    ('dictionary', 'Oxford 3000', 1),
    ('dictionary', 'Oxford 5000', 1),
    ('dictionary', 'dictionary.db', 1),
    ('AI', 'AI-generated', 0),
    ('manual', 'manual review', 0);
""")

# Seed contexts cơ bản (mở rộng động khi cần)
CONTEXTS = [
    'general', 'health', 'education', 'work', 'business', 'finance',
    'technology', 'programming', 'travel', 'transportation', 'food',
    'family', 'relationships', 'environment', 'government', 'law',
    'science', 'industry', 'economy', 'sports', 'entertainment', 'arts',
    'culture', 'history', 'geography', 'nature', 'home', 'shopping',
    'daily life', 'social', 'politics', 'media', 'internet',
    'communication', 'weather', 'time', 'feelings', 'emotions',
    'personality', 'appearance', 'clothing', 'body', 'animals', 'plants',
    'safety', 'military', 'religion', 'philosophy', 'psychology',
    'medicine', 'engineering', 'mathematics', 'physics', 'chemistry',
    'biology', 'literature', 'music', 'photography', 'design',
    'architecture', 'fashion', 'farming', 'construction', 'manufacturing',
    'trade', 'marketing', 'banking', 'insurance', 'crime', 'justice',
    'ethics', 'success', 'failure', 'management', 'leadership',
    'teamwork', 'negotiation', 'conflict', 'competition', 'innovation',
    'creativity', 'tradition', 'celebration', 'holiday', 'leisure',
    'hobby', 'gardening', 'cooking', 'restaurant', 'hotel', 'tourism',
    'adventure', 'urban', 'rural', 'digital', 'virtual', 'physical',
    'mental', 'financial', 'temporary', 'permanent', 'local', 'global',
    'public', 'private', 'personal', 'professional', 'formal', 'informal',
    'slang', 'grammar', 'vocabulary', 'translation', 'pronunciation',
    'writing', 'reading', 'feelings', 'behavior', 'belief', 'values',
    'decisions', 'options', 'opportunities', 'risks', 'problems',
    'solutions', 'results', 'changes', 'growth', 'progress', 'loss',
    'victory', 'defeat', 'training', 'exercise', 'sleep', 'stress',
    'habits', 'meetings', 'lessons', 'tasks', 'responsibilities',
    'promises', 'contracts', 'agreements', 'organizations', 'courts',
    'police', 'education', 'childhood', 'friendship', 'marriage',
]
cur.executemany("INSERT OR IGNORE INTO contexts (name) VALUES (?)",
                [(c,) for c in CONTEXTS])

con.commit()

# Thống kê
for t in ('words', 'senses', 'contexts', 'examples', 'sense_contexts',
          'sources'):
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    print(f"{t}: {cur.fetchone()[0]}")

con.close()
print(f"Created {DB_PATH}")
