# -*- coding: utf-8 -*-
"""
build_oxford_dataset.py — Tạo dataset từ vựng mới (SQLite) từ dictionary/oxford.md

Nguồn nghĩa tiếng Việt / phiên âm / ví dụ: dataset/dictionary.db (tra cứu theo
cấu trúc của sql_query_example.ts + dictionary_query.py).

Output:
  dataset/vocabulary.sqlite   (words, senses, contexts, sense_contexts,
                               examples, accepted_answers, sources)
  dataset/vocabulary_import_report.json
"""
import json
import os
import re
import sqlite3
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DB = os.path.join(ROOT, "dataset", "dictionary.db")
OUT_DB = os.path.join(ROOT, "dataset", "vocabulary.sqlite")
OXFORD_MD = os.path.join(ROOT, "dictionary", "oxford.md")
REPORT = os.path.join(ROOT, "dataset", "vocabulary_import_report.json")

# ---------------------------------------------------------------- parse oxford
POS_TOKEN_MAP = {
    "n": "noun", "v": "verb", "adj": "adjective", "adv": "adverb",
    "prep": "preposition", "pron": "pronoun", "conj": "conjunction",
    "det": "determiner", "exclam": "exclamation", "modal v": "modal verb",
    "auxiliary v": "auxiliary verb", "number": "number", "article": "article",
    "indefinite article": "article", "definite article": "article",
    "infinitive marker": "infinitive marker",
}

def map_pos(pos_text):
    """'prep., adv.' -> ['preposition','adverb']; 'modal v.' -> ['modal verb']."""
    t = pos_text.strip().strip('.,').replace('\u2019', "'")
    t = re.sub(r"\([^)]*\)", "", t)             # bỏ qualifier '(money)', '(river)'
    out = []
    if "modal v" in t:
        out.append("modal verb")
        t = t.replace("modal v", "")
    if "auxiliary v" in t:
        out.append("auxiliary verb")
        t = t.replace("auxiliary v", "")
    if "infinitive marker" in t:
        out.append("infinitive marker")
        t = t.replace("infinitive marker", "")
    for tok in re.split(r"[,/]+", t):
        tok = tok.strip().strip('.').lower()
        if tok and tok in POS_TOKEN_MAP:
            out.append(POS_TOKEN_MAP[tok])
    return out or ["unknown"]

def clean_word(w):
    w = w.replace("<sup>", "").replace("</sup>", "").strip()
    w = re.sub(r"\d+$", "", w).strip()          # can1 -> can
    w = w.replace("’", "'")
    return w

def parse_oxford(path):
    text = open(path, encoding="utf-8").read()
    text = text.replace("**The Oxford 3000™ (American English)**", "")
    text = text.replace("© Oxford University Press", "")
    text = re.sub(r"\b\d+ / 11\b", "", text)
    entries, seen = [], set()
    for m in re.finditer(r"([A-Za-z][A-Za-z'’\-,() ]*?)\s*_([^_]+?)_\s*(A1|A2|B1|B2)\b", text):
        raw_word, pos_text, cefr = m.group(1), m.group(2), m.group(3)
        raw_word = re.sub(r"\s+", " ", raw_word).strip(" ,")
        if not raw_word:
            continue
        poss = map_pos(pos_text)
        for w in raw_word.split(","):
            w = re.sub(r"\([^)]*\)", "", w)      # 'light (from the sun...)' -> 'light'
            w = clean_word(w)
            if not w or not re.fullmatch(r"[A-Za-z][A-Za-z'\- ]*", w):
                continue
            key = (w.lower(), cefr)
            if key in seen:
                continue
            seen.add(key)
            entries.append({"word": w, "pos": poss, "cefr": cefr})
    # merge trùng word (khác cefr): giữ CEFR thấp nhất
    byword = {}
    for e in entries:
        k = e["word"].lower()
        if k in byword:
            for p in e["pos"]:
                if p not in byword[k]["pos"]:
                    byword[k]["pos"].append(p)
        else:
            byword[k] = e
    out = sorted(byword.values(), key=lambda e: e["word"].lower())
    return out

# ---------------------------------------------------------------- source db
def connect_src():
    con = sqlite3.connect(f"file:{SRC_DB.replace(os.sep, '/')}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con

REGION_MAP = {"US": "US", "General-American": "US",
              "UK": "UK", "Received-Pronunciation": "UK"}

def get_pronunciations(cur, word_id):
    us, uk = [], []
    for r in cur.execute(
            "SELECT ipa, region FROM pronunciations WHERE word_id=?", (word_id,)):
        key = REGION_MAP.get(r["region"])
        if key == "US" and r["ipa"] not in us:
            us.append(r["ipa"])
        elif key == "UK" and r["ipa"] not in uk:
            uk.append(r["ipa"])
    if not us and not uk:
        # IPA generic của Wiktionary (không gán region) — chỉ dùng khi thiếu US/UK
        gen = [r["ipa"] for r in cur.execute(
            "SELECT ipa FROM pronunciations WHERE word_id=? AND region IS NULL"
            " LIMIT 2", (word_id,))]
        if gen:
            return {"us": gen, "uk": gen}
    return {"us": us[:2], "uk": uk[:2]}

def lookup_word(cur, word):
    """Chọn dòng words('en') có nhiều định nghĩa vi nhất cho `word`."""
    w = word.lower()
    rows = cur.execute(
        "SELECT id FROM words WHERE lower(word)=? AND lang_code='en'", (w,)).fetchall()
    best, best_n = None, -1
    for r in rows:
        n = cur.execute("""
            SELECT COUNT(*) FROM word_definitions wd
            JOIN definitions d ON d.id = wd.definition_id
            WHERE wd.word_id=? AND d.definition_lang='vi'
        """, (r["id"],)).fetchone()[0]
        if n > best_n:
            best, best_n = r["id"], n
    return best

def y_i_variants(word):
    """Sinh biến thể y<->i tại từng vị trí.

    dictionary.db lưu một số từ tiếng Anh sai chính tả:
      'city' -> 'citi', 'finally' -> 'finalli', 'usually' -> 'usualli',
      và ngược chiều: 'acquire' -> 'acquyre', 'quit' -> 'quyt',
      'equipment' -> 'equypment', 'inquiry' -> 'inquyry'.
    """
    w = word.lower()
    out = set()
    for i, ch in enumerate(w):
        if ch == "y":
            out.add(w[:i] + "i" + w[i + 1:])
        elif ch == "i":
            out.add(w[:i] + "y" + w[i + 1:])
    out.discard(w)
    return sorted(out)

def lookup_word_variant(cur, word):
    """Tra cứu từ khi DB lưu sai chính tả y<->i. Trả về (word_id, stored_word).

    Chỉ nhận dòng có >= 1 định nghĩa vi để tránh khớp nhầm từ khác nghĩa.
    """
    for f in y_i_variants(word):
        rows = cur.execute(
            "SELECT id, word FROM words WHERE lower(word)=? AND lang_code='en'",
            (f,)).fetchall()
        best, best_n = None, -1
        for r in rows:
            n = cur.execute("""
                SELECT COUNT(*) FROM word_definitions wd
                JOIN definitions d ON d.id = wd.definition_id
                WHERE wd.word_id=? AND d.definition_lang='vi'
            """, (r["id"],)).fetchone()[0]
            if n > best_n:
                best, best_n = (r["id"], r["word"]), n
        if best is not None and best_n > 0:
            return best
    return None

def lookup_via_translation(cur, word):
    """Fallback: tìm từ tiếng Việt mà bản dịch en trùng `word` (exact, CI)."""
    w = word.lower()
    rows = cur.execute("""
        SELECT t.word_id, w.word FROM translations t
        JOIN words w ON w.id = t.word_id
        WHERE t.lang_code='en' AND lower(t.translation)=?
        ORDER BY LENGTH(w.word)
    """, (w,)).fetchall()
    seen, out = set(), []
    for r in rows:
        key = unicodedata.normalize("NFC", r["word"]).lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(r["word"])
    return out[:8]

POS_CODE_MAP = {"N": "noun", "V": "verb", "A": "adjective", "D": "adverb",
                "R": "adverb", "P": "pronoun", "C": "conjunction", "E": "preposition",
                "I": "interjection", "M": "determiner", "O": "exclamation",
                "X": "auxiliary verb", "S": "unknown", "Z": "unknown"}

def get_senses(cur, word_id, poss):
    """Nghĩa VI khớp POS Oxford; ghép định nghĩa EN để suy context + example."""
    rows = cur.execute("""
        SELECT d.definition, d.pos, d.definition_lang, wd.example
        FROM word_definitions wd
        JOIN definitions d ON wd.definition_id = d.id
        WHERE wd.word_id = ?
        ORDER BY d.id
    """, (word_id,)).fetchall()
    pos_set = set(poss) | {"unknown"}
    vi_defs, en_defs = [], []
    for r in rows:
        d = (r["definition"] or "").strip()
        if not d or len(d) > 200:
            continue
        if r["definition_lang"] == "vi":
            if not d.lower().startswith(("xem ", "=", "—")):
                vi_defs.append({"definition": d, "pos": r["pos"],
                                "example": (r["example"] or "").strip() or None})
        elif r["definition_lang"] == "en":
            en_defs.append({"definition": d, "example": r["example"]})
    matched = [x for x in vi_defs if POS_CODE_MAP.get(x["pos"], "unknown") in pos_set]
    vi_filtered = matched if matched else vi_defs
    senses, seen = [], set()
    en_iter = iter(en_defs)
    for item in vi_filtered:
        norm = unicodedata.normalize("NFC", item["definition"]).lower()
        if norm in seen:
            continue
        seen.add(norm)
        try:
            e = next(en_iter)
            en_def = e["definition"]
        except StopIteration:
            en_def = None
        code_pos = POS_CODE_MAP.get(item["pos"], "unknown")
        sense_pos = code_pos if code_pos in poss else (poss[0] if poss else "unknown")
        senses.append({"pos": sense_pos, "meaning_vi": item["definition"],
                       "en_definition": en_def, "example": item["example"]})
    return senses[:12]

# ---------------------------------------------------------------- context
CONTEXT_KEYWORDS = {
    "business": r"company|business|market|trade|commercial|customer|sales|firm",
    "finance": r"money|bank|payment|loan|debt|invest|tax|price|cost|salary|currency",
    "law": r"law|legal|court|crime|police|contract|trial|judge|guilty|prison",
    "health": r"medical|disease|doctor|patient|medicine|hospital|health|illness|body",
    "education": r"school|student|learn|teach|study|exam|university|class|lesson",
    "technology": r"computer|software|internet|device|digital|electronic|machine|data",
    "programming": r"program|code|software|algorithm",
    "food": r"food|cook|eat|meal|dish|kitchen|recipe|fruit|vegetable|meat",
    "travel": r"travel|trip|journey|flight|tourist|hotel|destination|passport",
    "transportation": r"car|vehicle|drive|road|traffic|train|bus|transport|ship",
    "family": r"family|parent|child|mother|father|brother|sister|relative|home",
    "relationships": r"friend|relationship|love|marry|partner|social",
    "environment": r"environment|climate|pollution|wildlife|ecolog",
    "science": r"science|research|experiment|theory|chemistry|physics|biology",
    "work": r"job|work|employee|office|career|profession|employ|manager",
    "government": r"government|state|policy|election|political|president|public",
    "economy": r"economy|economic|growth|inflation|gross domestic",
    "industry": r"factory|industry|manufactur|production|steel|construction|mining",
    "sports": r"sport|game|team|match|ball|race|score|fitness",
    "emotions": r"feel|emotion|happy|sad|angry|afraid|fear|excited|proud",
    "weather": r"weather|rain|snow|wind|storm|sun|hot|cold|temperature|cloud",
    "time": r"time|day|year|month|hour|minute|date|period|schedule",
    "communication": r"speak|talk|say|message|communicate|conversation|write|phone",
    "art": r"art|music|paint|film|movie|design|artist|gallery|theater",
    "nature": r"animal|plant|tree|flower|bird|sea|river|mountain|land|earth",
}

CONTEXT_KEYWORDS_VI = {
    # Suy ngữ cảnh từ nghĩa tiếng Việt (meaning_vi) — nguồn chính vì
    # dictionary.db hầu như không có định nghĩa tiếng Anh.
    "business": r"doanh nghiệp|kinh doanh|công ty|thương mại|khách hàng|bán hàng|buôn bán",
    "finance": r"tiền|ngân hàng|khoản|nợ|vay|lãi suất|giá|thuế|đầu tư|ngân sách|chi tiêu|tiết kiệm|lương|thanh toán|tiền tệ|tài chính|cổ phần|vốn|thu nhập|poverty|nghèo đói",
    "law": r"pháp luật|luật|tòa án|tội phạm|cảnh sát|hợp đồng|phiên tòa|thẩm phán|có tội|nhà tù|án tù|đấu vật|mua chuộc|hối lộ",
    "health": r"bệnh|sức khỏe|bác sĩ|thuốc|cơ thể|đau|bệnh viện|nhiễm|cấn|thương|vết|nhiễm trùng|tiêm|kê đơn",
    "education": r"trường|học|sinh viên|giáo viên|bài học|kỳ thi|đại học|lớp học|sách|bảng chữ|bài tập",
    "technology": r"máy tính|phần mềm|internet|điện thoại|kỹ thuật số|công nghệ|thiết bị điện tử|robot|pin|ắc quy",
    "programming": r"chương trình máy tính|mã nguồn|thuật toán|lập trình",
    "food": r"món ăn|món|nấu|bữa|trái cây|quả|rau|thịt|bánh|thức uống|nhà hàng|cà phê|ăn|uống|gia vị|phô mai|cá|tôm",
    "travel": r"du lịch|chuyến đi|hành trình|chuyến bay|khách du lịch|khách sạn|điểm destina|điểm",
    "transportation": r"xe hơi|ô tô|lái xe|xe buýt|tàu hoả|máy bay|giao thông|đường|tàu|xe|thuyền|du thuyền|hàng không",
    "family": r"gia đình|bố|mẹ|cha|con|anh|chị|em|ông|bà|cậu|dì|chú|bác|cháu|cháu gái|con trai|con gái|người yêu|hôn nhân|vợ|chồng|bố mẹ",
    "relationships": r"bạn bè|mối quan hệ|tình yêu|kết hôn|đối tác|cặp đôi|hẹn hò|duyên|tình bạn",
    "environment": r"môi trường|khí hậu|ô nhiễm|đa dạng sinh học|sinh thái",
    "science": r"khoa học|nghiên cứu|thí nghiệm|lý thuyết|hóa học|vật lý|sinh học|vi khuẩn",
    "work": r"công việc|nghề nghiệp|nhân viên|văn phòng|sự nghiệp|thuê|người sử dụng lao động|quản lý|làm việc|hợp đồng lao động",
    "government": r"chính phủ|nhà nước|chính sách|bầu cử|chính trị|tổng thống|quốc hội|dân chúng|công dân|thành phố|toà thị chính",
    "economy": r"kinh tế|tăng trưởng|lạm phát|suy thoái|sản lượng",
    "industry": r"nhà máy|công nghiệp|sản xuất|dây chuyền|thép|xây dựng|mỏ|hầm mỏ|khai thác",
    "sports": r"thể thao|trò chơi|đội|trận đấu|bóng|cuộc đua|ghi điểm|sức khỏe thể chất|thể dục",
    "emotions": r"cảm xúc|vui|buồn|giận|sợ|hạnh phúc|tự hào|xúc động|lo lắng|nỗi sợ|hạnh phúc|ngạc nhiên|thích thú",
    "weather": r"thời tiết|mưa|tuyết|gió|bão|nắng|nóng|lạnh|nhiệt độ|mây|sương mù|dự báo",
    "time": r"thời gian|ngày|năm|tháng|giờ|tuần|lịch|khoảng thời gian|lịch trình|lịch phát sóng|đúng giờ",
    "communication": r"nói|trò chuyện|lời nói|tin nhắn|giao tiếp|cuộc trò chuyện|viết|điện thoại|thư điện tử",
    "art": r"nghệ thuật|âm nhạc|vẽ|bức tranh|phim|thiết kế|hoạ sĩ|phòng trưng bày|nhà hát|điêu khắc",
    "nature": r"động vật|thực vật|cây|hoa|chim|biển|sông|núi|đất|trái đất|côn trùng|loài vật|hoang dã",
    "music": r"âm nhạc|bài hát|nhạc cụ|ban nhạc|ca sĩ|buổi hoà nhạc",
}

def _boundary_patterns(patterns):
    """Transformă liste de cuvînțe in-regex într-ul un regex cu word-boundaries.

    Necesitel dĕ căûtă tinđranțe substring-uri scurte:
      - 'ăn' gàsește în 'khănăng', 'còn' în 'công', 'em' în 'thêm',
      - 'bà' în 'bàn', 'an' în 'nhạ đàn'.
    Cu \b...\b cojí din a și pot été literal whălt stă independent.
    """
    alts = []
    for p in patterns:
        for tok in p.split("|"):
            tok = tok.strip()
            if not tok:
                continue
            esc = re.escape(tok)
            if " " in tok:
                alts.append(r"(?:\b)" + esc + r"(?:\b)")
            else:
                alts.append(r"\b" + esc + r"\b")
    return r"(?:" + "|".join(alts) + r")"

CONTEXT_KEYWORDS_VI_PAT = {
    name: re.compile(_boundary_patterns(pat))
    for name, pat in CONTEXT_KEYWORDS_VI.items()
}

CONTEXT_KEYWORDS_EN_PAT = {
    name: re.compile(_boundary_patterns(pat))
    for name, pat in CONTEXT_KEYWORDS.items()
}


# ---------------------------------------------------------------- curated contexts
# Gán context label theo TỪ (curated-per-word) cho các từ RÕ RÀNG thuộc 1-2 lĩnh vực.
# KHÔNG tự suy từ nghĩa tiếng Việt vì Tiếng Việt đa nghĩa (vd 'ô' trong 'ô tô/ô danh',
# 'ế' trong 'ế ẩm', 'e' trong 'e rằng') -> sai nghĩa nghiêm trọng (spec §7/§17/§21/§23).
# Từ không có mapping (trừu tượng, đa nghĩa, hàm từ) -> general.
CONTEXT_BY_WORD = {}

def add_ctx(context, words):
    for w in words:
        CONTEXT_BY_WORD.setdefault(w.strip().lower(), []).append(context)

add_ctx("food",
    "apple banana bean beef bread breakfast cake candy carrot cereal cheese cheese "
    "chicken chocolate coffee cookie corn cream dessert diet dinner dish drink "
    "egg fish flour fruit garlic grain honey ice-cream jam juice kitchen lemon lunch "
    "meal meat menu milk mushroom nut oil onion orange pepper pie pizza potato "
    "recipe restaurant rice salad salt sandwich sauce snack soup spice steak sugar "
    "tea tomato vegetable water wine cook bake boil fry eat drink dinner lunch breakfast"
add_ctx("family",
    "aunt baby brother child cousin dad family father grandfather grandmother "
    "grandparent husband kid mother parent sister son uncle wife married marry marriage wedding"
add_ctx("relationships",
    "friend friendship date boyfriend girlfriend marriage married marry love "
    "couple partner relationship romance wedding divorce"
add_ctx("work",
    "ambition boss career colleague company employee employer job manager "
    "meeting office profession retire salary staff worker colleague profession recruit"
add_ctx("education",
    "class classroom college education exam graduate homework lecture library "
    "lesson learn professor school student study teach teacher test tutor "
    "university degree subject campus assignment"
add_ctx("health",
    "body bone brain blood breathe chest disease doctor fever health hospital "
    "ill illness infection knee medicine medical muscle nurse pain patient "
    "sick surgery symptom therapy tooth treatment virus"
add_ctx("finance",
    "account bank budget cash coin cost credit debt dollar economy expense "
    "fee finance income insurance invest investment loan money pay payment "
    "price profit salary save saving share tax wage wealthy wealth currency"
add_ctx("business",
    "advertise advertisement advertising brand business company competition "
    "competitor customer deal employ employee employer hire manager market "
    "marketing profit product sale sell share trade"
add_ctx("government",
    "congress election government minister policy political politician "
    "president senator state vote mayor nation national citizen campaign"
add_ctx("law",
    "arrest attorney crime criminal court judge jury law legal "
    "lawyer police prison illegal guilty innocent witness evidence suspect punishment"
add_ctx("transportation",
    "airport bicycle bike boat bus car driver elevator flight fly highway "
    "fuel journey plane railroad road ship station subway ticket "
    "traffic train transport transportation travel trip truck van vehicle passenger"
add_ctx("sports",
    "athlete ball baseball basketball exercise fitness football golf hockey "
    "match player race run runner soccer sport swimming team tennis"
add_ctx("time",
    "century century date day decade evening hour minute month morning night "
    "o'clock schedule second week weekend year today tomorrow yesterday time "
    "December January February March April May June July August September "
    "October November Monday Tuesday Wednesday Thursday Friday Saturday Sunday agent agreement date"
add_ctx("weather",
    "climate cloud flood fog freeze frost hurricane ice rain snow storm "
    "sun sunshine temperature thunder tornado weather wind cold hot warm lightning"
add_ctx("nature",
    "animal beach bird coast earth field flower forest grass hill island lake "
    "land landscape mountain ocean plant river rock sand sea sky soil star sun "
    "tree valley wave wood stone wildlife leaf river lake"
add_ctx("emotions",
    "angry annoyed anxious ashamed bored excited fear frightened frightened "
    "frightening happy hate hope joy love nervous proud sad lonely mad "
    "disappointed emotional mood pleasure relaxed shock surprised tear"
add_ctx("communication",
    "communicate conversation discuss email information interview language "
    "letter message phone read response say speak speech talk tell text "
    "translate write headline internet communicate discuss"
add_ctx("technology",
    "app battery computer digital email keyboard laptop machine online "
    "screen software video website data computer technology"
add_ctx("programming",
    "algorithm code data database software program function"
add_ctx("art",
    "art artist artistic concert dance design drama film gallery magazine "
    "literature music instrument novel painting performance poem poet poetry "
    "portrait sculpture song theater"
add_ctx("music",
    "album band concert guitar musician piano singer song"
add_ctx("travel",
    "accommodation adventure destination hotel journey passport reception "
    "resort tour tourism tourist travel trip vacation"
add_ctx("environment",
    "climate carbon energy pollution recycle environment renewable solar"
add_ctx("industry",
    "factory manufacture production steel construction mining engineer "
    "engineering industrial"
add_ctx("economy",
    "economy economic employment inflation interest rate stock tax invest "
    "market trade export import industry"
add_ctx("science",
    "analysis biology chemical experiment genetic laboratory medicine "
    "physics research science scientist species theory"
add_ctx("mining",
    "coal mine mineral mining iron gold silver metal"

def derive_contexts(word):
    """Trả context theo mapping curated-per-word; từ không rõ -> general."""
    return CONTEXT_BY_WORD.get(word.lower(), ["general"])

CURATED_WORDS = {
    # 28 từ KHÔNG tồn tại trong dictionary.db (cả chính tả gốc, biến thể y<->i,
    # lẫn bảng translations). Tự định nghĩa theo POS/CEFR của oxford.md.
    # Người dùng chủ động cho phép tự định nghĩa các từ này.
    "CD": [("noun", "đĩa CD (Compact Disc)")],
    "cafe": [("noun", "quán cà phê")],
    "increasingly": [("adverb", "ngày càng, ngày một (tăng dần)")],
    "app": [("noun", "ứng dụng (phần mềm trên điện thoại/máy tính)")],
    "arms": [("noun", "vũ khí")],
    "born": [("verb", "sinh ra, được sinh ra (be born)")],
    "colored": [("adjective", "có màu, được nhuộm màu")],
    "found": [("verb", "thành lập, xây dựng (tổ chức, thành phố)")],
    "fur": [("noun", "lông thú, bộ lông (của động vật)")],
    "grandparent": [("noun", "ông bà (nội/ngoại)")],
    "hers": [("pronoun", "của cô ấy, của bà ấy")],
    "herself": [("pronoun", "chính cô ấy, tự cô ấy")],
    "himself": [("pronoun", "chính anh ấy, tự anh ấy")],
    "his": [("determiner", "của anh ấy"), ("pronoun", "cái của anh ấy")],
    "invitation": [("noun", "lời mời, thư mời")],
    "lifestyle": [("noun", "lối sống, cách sống")],
    "o'clock": [("adverb", "giờ (dùng khi nói giờ: it is five o'clock)")],
    "off": [("adverb", "rời khỏi, tách ra; tắt (thiết bị)"),
            ("preposition", "rời khỏi, cách ra")],
    "ours": [("pronoun", "của chúng tôi, của chúng ta")],
    "ourselves": [("pronoun", "chính chúng tôi, tự chúng tôi")],
    "quietly": [("adverb", "một cách yên lặng, nhẹ nhàng")],
    "spending": [("noun", "việc chi tiêu, khoản chi tiêu")],
    "stove": [("noun", "bếp lò, bếp nấu")],
    "strongly": [("adverb", "một cách mạnh mẽ, quyết liệt")],
    "teenage": [("adjective", "thuộc tuổi vị thành niên (13-19)")],
    "theirs": [("pronoun", "của họ, của chúng nó")],
    "used to": [("modal verb", "đã từng (thói quen trong quá khứ)")],
    "whose": [("determiner", "của ai (chỉ sự sở hữu)"),
              ("pronoun", "của ai")],
    "worldwide": [("adjective", "trên toàn thế giới"),
                  ("adverb", "khắp thế giới")],
    "written": [("adjective", "viết, bằng văn bản")],
}


# ---------------------------------------------------------------- blank
SUFFIXES = ["", "s", "es", "ed", "d", "ing", "er", "ers", "ies", "y"]

def blank_sentence(sentence, word):
    if not sentence:
        return None
    w = word.lower()
    forms = {w} | {w + s for s in SUFFIXES}
    if w.endswith("e"):
        forms.add(w[:-1] + "ing")
    if w.endswith("y"):
        forms.add(w[:-1] + "ies")
        forms.add(w[:-1] + "ied")
    if w.endswith("s") and not w.endswith("ss"):
        forms.add(w[:-1])                      # "class" -> avoid, but e.g. "buses"
    alts = sorted((re.escape(f) for f in forms), key=len, reverse=True)
    pat = re.compile(r"\b(" + "|".join(alts) + r")\b", re.IGNORECASE)
    if not pat.search(sentence):
        return None
    return pat.sub("_____", sentence, count=1)

# ---------------------------------------------------------------- output db
SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE sources (
    id INTEGER PRIMARY KEY,
    source_type TEXT NOT NULL,
    source_name TEXT NOT NULL,
    verified INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE words (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL UNIQUE,
    pronunciation TEXT,
    cefr TEXT,
    part_of_speech TEXT NOT NULL,
    word_source TEXT NOT NULL
);
CREATE TABLE senses (
    id INTEGER PRIMARY KEY,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    pos TEXT,
    meaning_vi TEXT NOT NULL
);
CREATE TABLE contexts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE sense_contexts (
    sense_id INTEGER NOT NULL REFERENCES senses(id) ON DELETE CASCADE,
    context_id INTEGER NOT NULL REFERENCES contexts(id) ON DELETE CASCADE,
    PRIMARY KEY (sense_id, context_id)
);
CREATE TABLE examples (
    id INTEGER PRIMARY KEY,
    sense_id INTEGER NOT NULL REFERENCES senses(id) ON DELETE CASCADE,
    sentence TEXT NOT NULL,
    blank_sentence TEXT,
    answer TEXT NOT NULL
);
CREATE TABLE accepted_answers (
    id INTEGER PRIMARY KEY,
    example_id INTEGER NOT NULL REFERENCES examples(id) ON DELETE CASCADE,
    answer TEXT NOT NULL,
    UNIQUE (example_id, answer)
);
CREATE INDEX idx_words_word ON words(word);
CREATE INDEX idx_senses_word_id ON senses(word_id);
CREATE INDEX idx_examples_sense_id ON examples(sense_id);
CREATE INDEX idx_sc_sense ON sense_contexts(sense_id);
CREATE INDEX idx_sc_context ON sense_contexts(context_id);
CREATE INDEX idx_aa_example ON accepted_answers(example_id);
"""

def build():
    entries = parse_oxford(OXFORD_MD)
    print(f"Parsed {len(entries)} Oxford entries")

    if os.path.exists(OUT_DB):
        os.remove(OUT_DB)
    con = sqlite3.connect(OUT_DB)
    con.executescript(SCHEMA)
    cur = con.cursor()
    for stype, sname, verified in [
            ("word_source", "Oxford 3000", 1),
            ("dictionary", "dictionary.db (Wiktionary vi/en)", 0),
            ("example_source", "dictionary.db examples", 0),
            ("curated_definition", "manual curation", 0)]:
        cur.execute("INSERT INTO sources(source_type, source_name, verified)"
                    " VALUES (?,?,?)", (stype, sname, verified))

    src_con = connect_src()
    scur = src_con.cursor()

    context_ids = {}
    def get_context_id(name):
        if name not in context_ids:
            cur.execute("INSERT INTO contexts(name) VALUES (?)", (name,))
            context_ids[name] = cur.lastrowid
        return context_ids[name]

    report = {"total_entries": len(entries), "words_built": 0, "senses": 0,
              "examples": 0, "blanks": 0, "missing_words": [], "missing_senses": [],
              "fallback_translation_words": [], "variant_matched_words": [],
              "curated_defined_words": []}

    for entry in entries:
        word = entry["word"]
        source_label = "Oxford 3000"
        pron = {"us": [], "uk": []}
        senses = None

        # Tầng 1: tra chính xác trong words('en')
        wid = lookup_word(scur, word)
        if wid is not None:
            senses = get_senses(scur, wid, entry["pos"])
            if senses:
                pron = get_pronunciations(scur, wid)

        # Tầng 2: tra biến thể y<->i (dictionary.db lưu 'city'->'citi', ...)
        if not senses:
            var = lookup_word_variant(scur, word)
            if var is not None:
                senses = get_senses(scur, var[0], entry["pos"])
                if senses:
                    pron = get_pronunciations(scur, var[0])
                    report["variant_matched_words"].append(word)

        # Tầng 3: fallback qua bảng translations (từ VI có bản dịch EN)
        if not senses:
            vi_words = lookup_via_translation(scur, word)
            if vi_words:
                senses = [{"pos": entry["pos"][0] if entry["pos"] else "unknown",
                           "meaning_vi": v, "en_definition": None, "example": None}
                          for v in vi_words]
                report["fallback_translation_words"].append(word)

        # Tầng 4: tự định nghĩa (từ không có trong dictionary.db)
        if not senses and word in CURATED_WORDS:
            senses = [{"pos": p, "meaning_vi": v, "en_definition": None,
                       "example": None} for p, v in CURATED_WORDS[word]]
            source_label = "Oxford 3000 (curated)"
            report["curated_defined_words"].append(word)

        if not senses:
            report["missing_words"].append(word)
            continue
        cur.execute(
            "INSERT INTO words(word, pronunciation, cefr, part_of_speech, word_source)"
            " VALUES (?,?,?,?,?)",
            (word, json.dumps(pron, ensure_ascii=False), entry["cefr"],
             ", ".join(entry["pos"]), source_label))
        new_wid = cur.lastrowid
        report["words_built"] += 1
        for s in senses:
            cur.execute("INSERT INTO senses(word_id, pos, meaning_vi) VALUES (?,?,?)",
                        (new_wid, s["pos"], s["meaning_vi"]))
            sense_id = cur.lastrowid
            report["senses"] += 1
            for cname in derive_contexts(word):
                cur.execute(
                    "INSERT OR IGNORE INTO sense_contexts(sense_id, context_id)"
                    " VALUES (?,?)", (sense_id, get_context_id(cname)))
            ex = (s["example"] or "").strip()
            if ex:
                blank = blank_sentence(ex, word)
                cur.execute(
                    "INSERT INTO examples(sense_id, sentence, blank_sentence, answer)"
                    " VALUES (?,?,?,?)", (sense_id, ex, blank, word))
                report["examples"] += 1
                if blank:
                    report["blanks"] += 1

    con.commit()
    report["missing_words"] = sorted(set(report["missing_words"]))
    report["missing_senses"] = sorted(set(report["missing_senses"]))
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"words_built={report['words_built']} senses={report['senses']} "
          f"examples={report['examples']} blanks={report['blanks']} "
          f"missing_words={len(report['missing_words'])} "
          f"missing_senses={len(report['missing_senses'])}")
    con.close()
    src_con.close()

if __name__ == "__main__":
    build()



