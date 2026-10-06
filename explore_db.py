import sqlite3

con = sqlite3.connect('dataset/dictionary.db')
cur = con.cursor()

# List tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("TABLES:", tables)
print()

# For each table, show schema and row count
for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    cnt = cur.fetchone()[0]
    cur.execute(f"PRAGMA table_info({t})")
    cols = cur.fetchall()
    print(f"=== {t} ({cnt} rows) ===")
    for c in cols:
        print(f"  {c[1]} ({c[2]})")
    print()

con.close()
