import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

con = sqlite3.connect('dataset/dictionary.db')
cur = con.cursor()

# Check some "not found" words
test_words = ['ability', 'absolutely', 'acquire', 'activity', 'actually', 'app', 'apply', 'approximately', 'arms', 'army', 'authority', 'automatically', 'badly', 'basically', 'best', 'born', 'capacity', 'carefully', 'CD', 'celebrity', 'certainly', 'charity', 'city', 'clearly', 'closely', 'colored', 'commonly', 'community', 'completely', 'constantly', 'correctly', 'county', 'curly', 'currently', 'daily', 'deeply', 'definitely', 'deliberately', 'differently', 'difficulty', 'directly', 'dirty', 'district', 'early', 'easily', 'easy', 'economy', 'effectively', 'eighty']

for w in test_words:
    cur.execute("SELECT id, word, lang_code FROM words WHERE LOWER(word) = LOWER(?)", (w,))
    rows = cur.fetchall()
    if rows:
        print(f"  '{w}': FOUND as '{rows[0][1]}' (lang={rows[0][2]}, id={rows[0][0]})")
    else:
        # Try LIKE
        cur.execute("SELECT id, word, lang_code FROM words WHERE LOWER(word) LIKE LOWER(?) AND lang_code='en' LIMIT 3", (f'%{w}%',))
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': NOT EXACT, but similar: {[(r[1], r[2]) for r in rows]}")
        else:
            print(f"  '{w}': NOT FOUND AT ALL")

con.close()
