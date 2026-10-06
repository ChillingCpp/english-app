import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

con = sqlite3.connect('dataset/dictionary.db')
cur = con.cursor()

# Check specific words with exact match
test_words = ['ability', 'absolutely', 'acquire', 'activity', 'actually', 'apply', 'approximately', 'authority', 'automatically', 'badly', 'basically', 'best', 'capacity', 'carefully', 'certainly', 'charity', 'city', 'clearly', 'closely', 'colored', 'commonly', 'community', 'completely', 'constantly', 'correctly', 'county', 'curly', 'currently', 'daily', 'deeply', 'definitely', 'deliberately', 'differently', 'difficulty', 'directly', 'dirty', 'district', 'early', 'easily', 'easy', 'economy', 'effectively', 'eighty']

for w in test_words:
    # Exact match
    cur.execute("SELECT id, word, lang_code FROM words WHERE word = ?", (w,))
    rows = cur.fetchall()
    if rows:
        print(f"  '{w}': FOUND EXACT -> {rows}")
        continue
    
    # Case insensitive
    cur.execute("SELECT id, word, lang_code FROM words WHERE LOWER(word) = LOWER(?)", (w,))
    rows = cur.fetchall()
    if rows:
        print(f"  '{w}': FOUND CI -> {rows}")
        continue
    
    # Check if word exists in any form
    cur.execute("SELECT id, word, lang_code FROM words WHERE word LIKE ? AND lang_code = 'en' LIMIT 5", (f'{w}%',))
    rows = cur.fetchall()
    if rows:
        print(f"  '{w}': NOT FOUND, but starts with: {[(r[1], r[2]) for r in rows]}")
    else:
        # Check if it's a plural/derived form
        cur.execute("SELECT id, word, lang_code FROM words WHERE word LIKE ? AND lang_code = 'en' LIMIT 5", (f'%{w}%',))
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': NOT FOUND, but contains: {[(r[1], r[2]) for r in rows]}")
        else:
            print(f"  '{w}': NOT FOUND AT ALL")

# Check if 'able' exists (for ability)
print("\n=== Checking root forms ===")
for root in ['able', 'absolute', 'acquire', 'act', 'actual', 'apply', 'approximate', 'authority', 'automatic', 'bad', 'basic', 'good', 'careful', 'certain', 'charity', 'city', 'clear', 'close', 'color', 'common', 'community', 'complete', 'constant', 'correct', 'count', 'curl', 'current', 'day', 'deep', 'definite', 'deliberate', 'different', 'difficult', 'direct', 'dirt', 'district', 'early', 'easy', 'economy', 'effective', 'eight']:
    cur.execute("SELECT id, word FROM words WHERE word = ? AND lang_code = 'en'", (root,))
    row = cur.fetchone()
    if row:
        print(f"  '{root}': id={row[0]}")
    else:
        print(f"  '{root}': NOT FOUND")

con.close()
