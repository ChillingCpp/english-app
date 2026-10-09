import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
src = open('ctx_parts/run3/label_chunk_07.py', encoding='utf-8').read()
src = src.replace("sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')", "")
ns = {'__name__': 'dbg'}
exec(src.split('lines = []')[0], ns)
lab = ns['label_meaning']
blocks = re.findall(r"# --- (.*?) ---\n((?:    .*\n)+)", src)
tests = [
    ('game', 'Trò chơi (như bóng đá, quần vợt, bài lá... ).'),
    ('game', 'Trò cười; chuyện nực cười, trò đùa; sự trêu chọc, sự chế nhạo; trò láu cá, mánh khoé.'),
    ('gap', 'Khe hở, độ hở.'),
    ('general', '(từ cổ, nghĩa cổ) nhân dân quần chúng.'),
    ('garbage', 'Văn chương sọt rác ((cũng) literary garbage).'),
]
for w, m in tests:
    t = m.lower()
    hits = []
    for name, body in blocks:
        kws = re.findall(r"'([^']+)'", body.split('add(')[0])
        matched = [k for k in kws if (k.strip() in t) if (' ' in k.strip()) or
                   re.search(r'(?<![\wÀ-ỹ])' + re.escape(k) + r'(?![\wÀ-ỹ])', t)]
        if matched:
            hits.append((name, matched))
    print(w, '|', m)
    print('   labels:', lab(w, m))
    for name, mk in hits:
        print('   -', name, mk)
print('---chua---')
import json
d = json.load(open('ctx_input/chunk_07.json', encoding='utf-8'))
for e in d:
    for m in e['meanings']:
        if 'chữa' in m.lower():
            print('  ', e['word'], '|', m)
