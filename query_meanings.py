import sqlite3
import re
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = 'dataset/dictionary.db'
TMP_PATH = 'tmp'

# Read word lists
words1 = Path('words.txt').read_text(encoding='utf-8').splitlines()
words2 = Path('dictionary/words2.txt').read_text(encoding='utf-8').splitlines()

# Combine, preserving order, but track source
all_words = []
seen = set()
for w in words1 + words2:
    w = w.strip()
    if w and w not in seen:
        seen.add(w)
        all_words.append(w)

print(f"Total unique words to query: {len(all_words)}")

# Connect to DB
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# Cache for word lookups
word_cache = {}
# Track which base words we've already queried (strip trailing digits)
queried_bases = set()

def try_query(word):
    """Try to query a word from DB, return word_id or None"""
    # Exact match with lang_code='en'
    cur.execute("SELECT id, word, lang_code FROM words WHERE word = ? AND lang_code = 'en'", (word,))
    rows = cur.fetchall()
    if rows:
        return rows[0][0], rows[0][1], rows[0][2]
    
    # Case insensitive with lang_code='en'
    cur.execute("SELECT id, word, lang_code FROM words WHERE LOWER(word) = LOWER(?) AND lang_code = 'en'", (word,))
    rows = cur.fetchall()
    if rows:
        return rows[0][0], rows[0][1], rows[0][2]
    
    # Try any lang_code (for words that might be stored with wrong lang)
    cur.execute("SELECT id, word, lang_code FROM words WHERE word = ? LIMIT 5", (word,))
    rows = cur.fetchall()
    if rows:
        # Prefer 'vi' or 'en', then others
        for r in rows:
            if r[2] in ('vi', 'en'):
                return r[0], r[1], r[2]
        return rows[0][0], rows[0][1], rows[0][2]
    
    return None, None, None

def get_word_info(word_id):
    """Get definitions, pronunciations, translations for a word_id"""
    # Get definitions (Vietnamese meanings)
    cur.execute("""
        SELECT d.id, d.definition, d.pos, d.sub_pos, d.definition_lang, wd.example
        FROM word_definitions wd
        JOIN definitions d ON wd.definition_id = d.id
        WHERE wd.word_id = ?
    """, (word_id,))
    defs = cur.fetchall()
    
    # Get pronunciations
    cur.execute("SELECT ipa, region FROM pronunciations WHERE word_id = ?", (word_id,))
    prons = cur.fetchall()
    
    # Get translations
    cur.execute("SELECT lang_code, translation FROM translations WHERE word_id = ?", (word_id,))
    trans = cur.fetchall()
    
    return defs, prons, trans

def find_root_form(word):
    """Try to find root form by removing common suffixes"""
    suffixes = [
        'ly', 'ness', 'ity', 'tion', 'sion', 'ment', 'er', 'est', 's', 'es', 'ed', 'ing',
        'ies', 'ied', 'ying', 'able', 'ible', 'ful', 'less', 'ous', 'ive', 'ize', 'ise',
        'ally', 'ically', 'iness', 'ious', 'eous', 'uous', 'ant', 'ent', 'ance', 'ence',
        'ancy', 'ency', 'dom', 'ship', 'hood', 'th', 'ward', 'wards', 'wise', 'wide',
        'wards', 'ward', 'most', 'less', 'ful', 'ish', 'like', 'ly', 'y', 'al', 'ial',
        'ical', 'ic', 'ous', 'ious', 'eous', 'uous', 'ive', 'ative', 'itive', 'ize',
        'ise', 'ify', 'fy', 'en', 'ify', 'ate', 'ite', 'itude', 'itude', 'hood', 'ship',
        'dom', 'th', 'ward', 'wards', 'wise', 'wide', 'wards', 'ward', 'most', 'less',
        'ful', 'ish', 'like', 'ly', 'y', 'al', 'ial', 'ical', 'ic', 'ous', 'ious',
        'eous', 'uous', 'ive', 'ative', 'itive', 'ize', 'ise', 'ify', 'fy', 'en',
        'ify', 'ate', 'ite', 'itude', 'itude', 'hood', 'ship', 'dom', 'th', 'ward',
        'wards', 'wise', 'wide', 'wards', 'ward', 'most', 'less', 'ful', 'ish', 'like',
    ]
    
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            root = word[:-len(suffix)]
            # Try adding back common endings
            for ending in ['', 'e', 'y', 'i', 'a', 'o', 'u', 'er', 'or', 'ar']:
                candidate = root + ending
                wid, w, lang = try_query(candidate)
                if wid:
                    return wid, w, candidate
    
    return None, None, None

results = []
not_found = []

for i, word in enumerate(all_words):
    # Strip trailing digits for lookup
    base = re.sub(r'\d+$', '', word).strip()
    
    if base not in queried_bases:
        queried_bases.add(base)
        
        # Try direct query first
        wid, w, lang = try_query(base)
        
        if wid:
            defs, prons, trans = get_word_info(wid)
            word_cache[base] = {
                'word_id': wid,
                'word': w,
                'lang': lang,
                'definitions': defs,
                'pronunciations': prons,
                'translations': trans
            }
        else:
            # Try to find root form
            wid, w, root = find_root_form(base)
            if wid:
                defs, prons, trans = get_word_info(wid)
                word_cache[base] = {
                    'word_id': wid,
                    'word': w,
                    'lang': lang,
                    'definitions': defs,
                    'pronunciations': prons,
                    'translations': trans,
                    'root_form': root
                }
            else:
                word_cache[base] = None
    
    # Get cached result
    info = word_cache.get(base)
    if info is None:
        not_found.append(word)
        results.append({
            'word': word,
            'base': base,
            'found': False,
            'meanings': [],
            'pronunciations': [],
            'pos_list': []
        })
    else:
        # Format meanings
        meanings = []
        pos_set = set()
        for d in info['definitions']:
            meanings.append({
                'definition': d[1],
                'pos': d[2],
                'sub_pos': d[3],
                'example': d[5]
            })
            if d[2]:
                pos_set.add(d[2])
        
        prons = [{'ipa': p[0], 'region': p[1]} for p in info['pronunciations']]
        
        results.append({
            'word': word,
            'base': base,
            'found': True,
            'meanings': meanings,
            'pronunciations': prons,
            'pos_list': sorted(pos_set),
            'root_form': info.get('root_form'),
            'lang': info.get('lang')
        })
    
    if (i + 1) % 500 == 0:
        print(f"  Processed {i+1}/{len(all_words)}...")

con.close()

# Write tmp file
with open(TMP_PATH, 'w', encoding='utf-8') as f:
    for r in results:
        f.write(f"=== {r['word']} ===\n")
        if r['found']:
            if r.get('root_form'):
                f.write(f"(root: {r['root_form']})\n")
            if r.get('lang') and r['lang'] != 'en':
                f.write(f"(lang: {r['lang']})\n")
            f.write(f"POS: {', '.join(r['pos_list'])}\n")
            if r['pronunciations']:
                f.write(f"Pronunciation: {r['pronunciations'][0]['ipa']}\n")
            f.write(f"Meanings ({len(r['meanings'])}):\n")
            for j, m in enumerate(r['meanings'], 1):
                ex = f" | Ex: {m['example']}" if m['example'] else ""
                f.write(f"  {j}. [{m['pos']}] {m['definition']}{ex}\n")
        else:
            f.write("NOT FOUND in dictionary.db\n")
        f.write("\n")

print(f"\nResults written to {TMP_PATH}")
print(f"Found: {len(results) - len(not_found)}")
print(f"Not found: {len(not_found)}")
if not_found:
    print(f"Not found words ({len(not_found)}): {not_found[:100]}")
