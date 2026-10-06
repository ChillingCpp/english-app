import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

con = sqlite3.connect('dataset/dictionary.db')
cur = con.cursor()

# Sample: query "iron" in English
print("=== Query 'iron' (en) ===")
cur.execute("""
    SELECT w.id, w.word, w.lang_code
    FROM words w
    WHERE w.word = 'iron' AND w.lang_code = 'en'
""")
rows = cur.fetchall()
print("word rows:", rows)

if rows:
    wid = rows[0][0]
    # Get definitions
    cur.execute("""
        SELECT d.id, d.definition, d.pos, d.sub_pos, d.definition_lang, wd.example
        FROM word_definitions wd
        JOIN definitions d ON wd.definition_id = d.id
        WHERE wd.word_id = ?
    """, (wid,))
    defs = cur.fetchall()
    print(f"definitions ({len(defs)}):")
    for d in defs[:10]:
        print(f"  id={d[0]} pos={d[2]} sub={d[3]} lang={d[4]} def={d[1][:80]}... ex={d[5][:50] if d[5] else None}")

    # Get pronunciations
    cur.execute("SELECT ipa, region FROM pronunciations WHERE word_id = ?", (wid,))
    prons = cur.fetchall()
    print("pronunciations:", prons)

    # Get translations
    cur.execute("SELECT lang_code, translation FROM translations WHERE word_id = ?", (wid,))
    trans = cur.fetchall()
    print("translations:", trans)

print()
print("=== Query 'duy trì' (vi) ===")
cur.execute("""
    SELECT w.id, w.word, w.lang_code
    FROM words w
    WHERE w.word = 'duy trì' AND w.lang_code = 'vi'
""")
rows = cur.fetchall()
print("word rows:", rows)

if rows:
    wid = rows[0][0]
    cur.execute("""
        SELECT d.id, d.definition, d.pos, d.sub_pos, d.definition_lang
        FROM word_definitions wd
        JOIN definitions d ON wd.definition_id = d.id
        WHERE wd.word_id = ?
    """, (wid,))
    defs = cur.fetchall()
    print(f"definitions ({len(defs)}):")
    for d in defs[:10]:
        print(f"  id={d[0]} pos={d[2]} def={d[1][:80]}")

print()
print("=== Sources ===")
cur.execute("SELECT * FROM sources")
for r in cur.fetchall():
    print(r)

print()
print("=== Sample words with lang_code ===")
cur.execute("SELECT lang_code, COUNT(*) FROM words GROUP BY lang_code")
for r in cur.fetchall():
    print(r)

con.close()
