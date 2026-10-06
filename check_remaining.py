import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

con = sqlite3.connect('dataset/dictionary.db')
cur = con.cursor()

# Check remaining not found words
not_found = ['acquire', 'app', 'best', 'born', 'CD', 'district', 'equipment', 'fly', 'found', 'fur', 'grandparent', 'herself', 'himself', 'his', 'inquiry', 'invitation', 'lifestyle', 'liquid', 'my', 'no one', "o'clock", 'off', 'OK', 'ourselves', 'problem', 'quick', 'quickly', 'quiet', 'quietly', 'quit', 'quite', 'require', 'requirement', 'shy', 'single', 'sky', 'stove', 'teenage', 'used to', 'which', 'whose', 'why', 'written', 'yourself', 'acquisition', 'bound', 'catalog', 'coordination', 'councilor', 'decision-making', 'equip', 'equivalent', 'filmmaker', 'freshman', 'high-profile', 'harbor', 'healthcare', 'inquire', 'large-scale', 'lineup', 'longtime', 'makeup', 'mosquito', 'opera', 'résumé', 'rose', 'teen', 'temporarily', 'texture', 'thought-provoking', 'turnout', 'utility', 'visa', 'workplace']

for w in not_found:
    # Exact match
    cur.execute("SELECT id, word, lang_code FROM words WHERE word = ?", (w,))
    rows = cur.fetchall()
    if rows:
        print(f"  '{w}': FOUND EXACT -> {[(r[1], r[2]) for r in rows]}")
        continue
    
    # Case insensitive
    cur.execute("SELECT id, word, lang_code FROM words WHERE LOWER(word) = LOWER(?)", (w,))
    rows = cur.fetchall()
    if rows:
        print(f"  '{w}': FOUND CI -> {[(r[1], r[2]) for r in rows]}")
        continue
    
    # Try with different forms
    if w == 'best':
        cur.execute("SELECT id, word FROM words WHERE word IN ('good', 'well') AND lang_code = 'en'")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': root forms: {rows}")
    elif w == 'born':
        cur.execute("SELECT id, word FROM words WHERE word IN ('bear', 'birth') AND lang_code = 'en'")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': root forms: {rows}")
    elif w == 'fly':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%fly%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'found':
        cur.execute("SELECT id, word FROM words WHERE word IN ('find', 'foundation') AND lang_code = 'en'")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': root forms: {rows}")
    elif w == 'fur':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%fur%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'liquid':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%liquid%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'problem':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%problem%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'quick':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%quick%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'quiet':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%quiet%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'quit':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%quit%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'quite':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%quite%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'shy':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%shy%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'single':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%single%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'sky':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%sky%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'stove':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%stove%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'teenage':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%teen%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'used to':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%used%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'which':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%which%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'whose':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%whose%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'why':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%why%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'written':
        cur.execute("SELECT id, word FROM words WHERE word IN ('write', 'wrote') AND lang_code = 'en'")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': root forms: {rows}")
    elif w == 'yourself':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%yourself%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'acquire':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%acqui%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'equipment':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%equip%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'require':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%requir%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'requirement':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%requirement%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'inquiry':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%inquir%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'invitation':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%invit%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'lifestyle':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%life%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'grandparent':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%grand%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'herself':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%herself%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'himself':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%himself%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'his':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%his%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'my':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%my%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'no one':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%no one%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == "o'clock":
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%clock%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'off':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%off%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'OK':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%ok%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'ourselves':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%ourselves%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'app':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%app%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'CD':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%cd%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'district':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%district%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'acquisition':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%acquisition%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'bound':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%bound%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'catalog':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%catalog%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'coordination':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%coordinat%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'councilor':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%council%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'decision-making':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%decision%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'equip':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%equip%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'equivalent':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%equivalent%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'filmmaker':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%film%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'freshman':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%fresh%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'high-profile':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%profile%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'harbor':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%harbor%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'healthcare':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%health%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'inquire':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%inquir%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'large-scale':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%scale%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'lineup':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%line%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'longtime':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%long%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'makeup':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%make%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'mosquito':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%mosquito%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'opera':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%opera%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'résumé':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%resume%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'rose':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%rose%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'teen':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%teen%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'temporarily':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%temporary%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'texture':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%texture%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'thought-provoking':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%thought%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'turnout':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%turn%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'utility':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%utility%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'visa':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%visa%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    elif w == 'workplace':
        cur.execute("SELECT id, word FROM words WHERE word LIKE '%work%' AND lang_code = 'en' LIMIT 5")
        rows = cur.fetchall()
        if rows:
            print(f"  '{w}': similar: {rows}")
    else:
        print(f"  '{w}': NOT FOUND AT ALL")

con.close()
