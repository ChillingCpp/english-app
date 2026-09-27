import sqlite3, re
con = sqlite3.connect('dataset/vocabulary.sqlite')
cur = con.cursor()
print('contexts:')
for c, w, s in cur.execute("""
    SELECT c.name AS name, COUNT(DISTINCT w.id) AS word_count, COUNT(DISTINCT s.id) AS sense_count
    FROM contexts c
    JOIN sense_contexts sc ON sc.context_id=c.id
    JOIN senses s ON s.id=sc.sense_id
    JOIN words w ON w.id=s.word_id
    GROUP BY c.id ORDER BY word_count DESC""").fetchall():
    print(f'  {c:15} words={w:5} senses={s}')
def samples(ctx, n=6):
    return cur.execute("""
        SELECT DISTINCT w.word, s.meaning_vi FROM sense_contexts sc
        JOIN contexts c ON c.id=sc.context_id AND c.name=?
        JOIN senses s ON s.id=sc.sense_id JOIN words w ON w.id=s.word_id
        ORDER BY w.word LIMIT ?""", (ctx, n)).fetchall()
for ctx in ['family','food','travel','general']:
    print('===', ctx)
    for w, m in samples(ctx):
        print('   ', w, '::', (m or '')[:60])