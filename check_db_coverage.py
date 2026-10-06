import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

con = sqlite3.connect('dataset/dictionary.db')
cur = con.cursor()

# Count English words
cur.execute("SELECT COUNT(*) FROM words WHERE lang_code = 'en'")
print(f"Total English words: {cur.fetchone()[0]}")

# Check if common words exist
common_words = ['able', 'absolute', 'acquire', 'activity', 'act', 'add', 'agree', 'bad', 'basic', 'good', 'great', 'happy', 'sad', 'big', 'small', 'fast', 'slow', 'hot', 'cold', 'new', 'old', 'young', 'love', 'hate', 'like', 'want', 'need', 'have', 'do', 'make', 'take', 'get', 'go', 'come', 'see', 'look', 'watch', 'hear', 'listen', 'speak', 'talk', 'say', 'tell', 'ask', 'answer', 'think', 'know', 'understand', 'learn', 'teach', 'study', 'read', 'write', 'work', 'play', 'run', 'walk', 'eat', 'drink', 'sleep', 'wake', 'sit', 'stand', 'open', 'close', 'start', 'stop', 'end', 'begin', 'finish', 'help', 'give', 'find', 'use', 'try', 'feel', 'become', 'leave', 'put', 'mean', 'keep', 'let', 'seem', 'turn', 'hand', 'part', 'place', 'case', 'week', 'company', 'system', 'program', 'question', 'number', 'night', 'point', 'home', 'water', 'room', 'mother', 'area', 'money', 'story', 'fact', 'month', 'lot', 'right', 'study', 'book', 'eye', 'job', 'word', 'business', 'issue', 'side', 'kind', 'head', 'house', 'service', 'friend', 'father', 'power', 'hour', 'game', 'line', 'end', 'member', 'law', 'car', 'city', 'community', 'name', 'team', 'minute', 'idea', 'kid', 'body', 'information', 'back', 'parent', 'face', 'others', 'level', 'office', 'door', 'health', 'person', 'art', 'war', 'history', 'party', 'result', 'change', 'morning', 'reason', 'research', 'girl', 'guy', 'moment', 'air', 'teacher', 'force', 'education']

found = 0
not_found = []
for w in common_words:
    cur.execute("SELECT id FROM words WHERE word = ? AND lang_code = 'en'", (w,))
    if cur.fetchone():
        found += 1
    else:
        not_found.append(w)

print(f"Common words found: {found}/{len(common_words)}")
print(f"Not found: {not_found}")

# Check total words with definitions
cur.execute("""
    SELECT COUNT(DISTINCT w.id) 
    FROM words w
    JOIN word_definitions wd ON wd.word_id = w.id
    WHERE w.lang_code = 'en'
""")
print(f"English words with definitions: {cur.fetchone()[0]}")

# Sample some English words
cur.execute("SELECT word FROM words WHERE lang_code = 'en' ORDER BY RANDOM() LIMIT 20")
print("Sample English words:", [r[0] for r in cur.fetchall()])

con.close()
