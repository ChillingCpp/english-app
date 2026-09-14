# -*- coding: utf-8 -*-
"""
dictionary_query.py — Tra cứu dictionary.db (readonly, sqlite3 stdlib)

Schema (đã kiểm chứng):
  words(id, word, source_id, lang_code)  UNIQUE(word, lang_code)
  word_definitions(word_id, definition_id, example, source_id)
  definitions(id, definition, pos, sub_pos, definition_lang, links)
  pronunciations(word_id, ipa, region)
  translations(word_id, lang_code, translation)
  word_relations(word_id, related_word, relation_type)  # s=đồng nghĩa, a=trái nghĩa, d=phái sinh, r=liên quan
  sources(id, name)

CLI:
  python dictionary_query.py iron maintain          # tra nghĩa tiếng Việt của từ tiếng Anh
  python dictionary_query.py "duy trì" --lang vi    # tra từ tiếng Việt
  python dictionary_query.py maintain --relations   # kèm đồng nghĩa/trái nghĩa
"""
import sqlite3
import sys
import os
import re
import unicodedata

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "dictionary.db")

RELATION_LABELS = {
    "s": "đồng nghĩa",
    "a": "trái nghĩa",
    "d": "phái sinh",
    "r": "liên quan",
}

_POS_MAP = {  # mã POS trong DB -> tên đầy đủ
    "N": "noun", "V": "verb", "A": "adjective", "D": "adverb",
    "R": "adverb", "P": "pronoun", "C": "conjunction", "E": "preposition",
    "I": "interjection", "M": "determiner", "O": "exclamation", "X": "auxiliary", "Z": "suffix",
}


def connect(db_path=DB_PATH):
    """Mở DB ở chế độ read-only."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Không tìm thấy database: {db_path}")
    con = sqlite3.connect(f"file:{db_path.replace(os.sep, '/')}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def normalize_vi(text):
    """Chuẩn hóa tiếng Việt: NFC + y->i (sau h,k,l,m,s,t) + qui->quy (theo sql_query_example.ts)."""
    if not text:
        return ""
    result = text
    result = re.sub(r"(?<![uU])([hklmstHKLMSĐT])y(?=\s|$|[.,!?])", r"\1i", result)
    result = re.sub(r"(?<![uU])([hklmstHKLMSĐT])ỳ(?=\s|$|[.,!?])", r"\1ì", result)
    result = re.sub(r"(?<![uU])([hklmstHKLMSĐT])ý(?=\s|$|[.,!?])", r"\1í", result)
    result = re.sub(r"(?<![uU])([hklmstHKLMSĐT])ỷ(?=\s|$|[.,!?])", r"\1ỉ", result)
    result = re.sub(r"(?<![uU])([hklmstHKLMSĐT])ỹ(?=\s|$|[.,!?])", r"\1ĩ", result)
    result = re.sub(r"(?<![uU])([hklmstHKLMSĐT])ỵ(?=\s|$|[.,!?])", r"\1ị", result)
    if "qui" in result:
        result = (result.replace("qui", "quy").replace("quì", "quỳ")
                  .replace("quí", "quý").replace("quỉ", "quỷ")
                  .replace("quĩ", "quỹ").replace("quị", "quỵ"))
    if re.search(r"[ùúủũụòóỏõọ]", result):
        result = (result.replace("ùy", "uỳ").replace("úy", "uý").replace("ủy", "uỷ")
                  .replace("ũy", "uỹ").replace("ụy", "uỵ")
                  .replace("òa", "oà").replace("óa", "oá").replace("ỏa", "oả")
                  .replace("õa", "oã").replace("ọa", "oạ")
                  .replace("òe", "oè").replace("óe", "oé").replace("ỏe", "oẻ")
                  .replace("õe", "oẽ").replace("ọe", "oẹ"))
    return result


def pos_to_name(pos_code):
    """Chuyển mã POS của DB ('N','V','A'...) sang tên đầy đủ."""
    if not pos_code:
        return None
    return _POS_MAP.get(pos_code, pos_code)


def get_word_id(con, word, lang_code):
    """Tìm word_id. Thử bản normalized trước, rồi đến chuỗi gốc."""
    cur = con.cursor()
    norm = normalize_vi(unicodedata.normalize("NFC", word).lower())
    row = cur.execute(
        "SELECT id, word FROM words WHERE word = ? AND lang_code = ?", (norm, lang_code)
    ).fetchone()
    if not row and norm != word:
        row = cur.execute(
            "SELECT id, word FROM words WHERE word = ? AND lang_code = ?", (word, lang_code)
        ).fetchone()
    return (row["id"], row["word"]) if row else (None, None)

def lookup_en(word, db_path=DB_PATH):
    """Tra từ tiếng Anh -> nghĩa tiếng Việt + phiên âm + relations."""
    con = connect(db_path)
    try:
        wid, stored = get_word_id(con, word, "en")
        if not wid:
            return {"exists": False, "word": word, "pronunciations": [],
                    "meanings": [], "relations": []}
        cur = con.cursor()
        pron = [(r["ipa"], r["region"])
                for r in cur.execute("SELECT ipa, region FROM pronunciations WHERE word_id=?", (wid,))]
        meanings = [{
            "definition": r["definition"],
            "pos": pos_to_name(r["pos"]),
            "sub_pos": r["sub_pos"],
            "example": r["example"],
            "source": r["name"],
        } for r in cur.execute("""
            SELECT d.definition, d.pos, d.sub_pos, wd.example, s.name
            FROM word_definitions wd
            JOIN definitions d ON wd.definition_id = d.id
            LEFT JOIN sources s ON wd.source_id = s.id
            WHERE wd.word_id = ?
            ORDER BY d.pos, d.id
        """, (wid,))]
        relations = [{
            "related_word": r["related_word"],
            "relation_type": r["relation_type"],
            "relation_label": RELATION_LABELS.get(r["relation_type"], r["relation_type"]),
        } for r in cur.execute(
            "SELECT related_word, relation_type FROM word_relations WHERE word_id=?", (wid,))]
        return {"exists": True, "word": stored, "pronunciations": pron,
                "meanings": meanings, "relations": relations}
    finally:
        con.close()


def lookup_vi(word, db_path=DB_PATH):
    """Tra từ tiếng Việt -> định nghĩa trong DB (vi) + bản dịch en (nếu có)."""
    con = connect(db_path)
    try:
        wid, stored = get_word_id(con, word, "vi")
        if not wid:
            return {"exists": False, "word": word, "meanings": [], "en_translations": []}
        cur = con.cursor()
        meanings = [{
            "definition": r["definition"],
            "pos": pos_to_name(r["pos"]),
            "sub_pos": r["sub_pos"],
            "example": r["example"],
        } for r in cur.execute("""
            SELECT d.definition, d.pos, d.sub_pos, wd.example
            FROM word_definitions wd
            JOIN definitions d ON wd.definition_id = d.id
            WHERE wd.word_id = ?
            ORDER BY d.pos, d.id
        """, (wid,))]
        en_tr = [r["translation"] for r in cur.execute(
            "SELECT translation FROM translations WHERE word_id=? AND lang_code='en'", (wid,))]
        return {"exists": True, "word": stored, "meanings": meanings,
                "en_translations": en_tr}
    finally:
        con.close()


def format_result(res, show_relations=False):
    lines = []
    if not res["exists"]:
        return f"KHÔNG TÌM THẤY: {res['word']}"
    lines.append(f"== {res['word']} ==")
    if res.get("pronunciations"):
        lines.append("phiên âm: " + ", ".join(
            f"{ipa}{' (' + r + ')' if r else ''}" for ipa, r in res["pronunciations"]))
    for i, m in enumerate(res["meanings"], 1):
        pos = f" [{m['pos']}{'/' + m['sub_pos'] if m.get('sub_pos') else ''}]" if m.get("pos") else ""
        src = f" ({m['source']})" if m.get("source") else ""
        lines.append(f"{i}. {m['definition']}{pos}{src}")
        if m.get("example"):
            lines.append(f"   e.g. {m['example']}")
    if show_relations and res.get("relations"):
        lines.append("relations: " + "; ".join(
            f"{r['related_word']} ({r['relation_label']})" for r in res["relations"]))
    for t in res.get("en_translations", []):
        lines.append(f"en: {t}")
    return "\n".join(lines)


def main():
    argv = sys.argv[1:]
    show_relations = "--relations" in argv
    args = [a for a in argv if a != "--relations"]
    lang = "en"
    if "--lang" in args:
        i = args.index("--lang")
        lang = args[i + 1]
        del args[i:i + 2]
    if not args:
        print(__doc__)
        sys.exit(0)
    fn = lookup_en if lang == "en" else lookup_vi
    for w in args:
        print(format_result(fn(w), show_relations))
        print()


if __name__ == "__main__":
    main()
