# -*- coding: utf-8 -*-
"""
Build wordlist.json by merging dictionary/oxford.md (Oxford 3000: word, POS, CEFR)
with dictionary/dict2.md (word, type, pronunciation, Vietnamese meaning).
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent / "dictionary"
OUT = Path(__file__).parent / "wordlist.json"

# ---------------------------------------------------------------- helpers
def norm_key(w: str) -> str:
    """normalize a word for cross-file matching"""
    w = unicodedata.normalize("NFKC", w)
    w = w.replace("\u2019", "'").replace("\u2018", "'")
    w = re.sub(r"\(.*?\)", "", w)          # "bank (money)" -> "bank"
    w = re.sub(r"\s+", " ", w).strip().lower()
    return w

def clean_ws(s: str) -> str:
    s = re.sub(r"\s+", " ", s.strip())
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    s = s.replace("<br>", "; ").replace("\u00a0", " ")
    return s.strip(" ;|")

# ---------------------------------------------------------------- parse oxford.md
ox_raw = (ROOT / "oxford.md").read_text(encoding="utf-8")
ox_raw = re.sub(r"\u00a9 Oxford University Press.*?\n?", " ", ox_raw)
ox_raw = re.sub(r"\d+ / 11", " ", ox_raw)
ox_raw = re.sub(r"\*\*.*?\*\*", " ", ox_raw)          # **The Oxford 3000...**
ox_raw = re.sub(r"<sup.*?</sup>", "", ox_raw, flags=re.S)  # can<sup>1</sup> -> can

POS_TOKENS = {
    "n", "v", "adj", "adv", "prep", "conj", "pron", "det", "exclam",
    "modal v", "auxiliary v", "number", "indefinite article", "definite article",
    "infinitive marker", "adj./adv", "exclam./n",
}

entry_re = re.compile(
    r"(?P<word>[A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*)?)\s+"
    r"(?P<pos>_[^_]+_)\s+"
    r"(?P<cefr>[AB][12])"
)

oxford = {}
for m in entry_re.finditer(ox_raw):
    word = m.group("word").strip()
    pos_raw = m.group("pos").strip("_").strip().rstrip(".")
    cefr = m.group("cefr")
    pos_raw_low = pos_raw.lower()
    pos_parts = [p.strip(" .,") for p in re.split(r"[,;]", pos_raw_low)]
    if not all(p in POS_TOKENS for p in pos_parts if p):
        continue
    if len(word) > 30 or "_" in word:
        continue
    key = norm_key(word)
    if not key or (len(key) == 1 and key not in {"a", "i"}):
        continue
    if key == "an":  # "a, an" share one entry line in the source
        oxford.setdefault("a", {"word": "a", "part_of_speech": [], "cefr": cefr})
    pos_list = [p.rstrip(".").strip() for p in re.split(r",\s*", pos_raw.strip()) if p]
    e = oxford.setdefault(key, {"word": word, "part_of_speech": [], "cefr": cefr})
    for p in pos_list:
        if p and p not in e["part_of_speech"]:
            e["part_of_speech"].append(p)

# ---------------------------------------------------------------- parse dict2.md
d2_raw = (ROOT / "dict2.md").read_text(encoding="utf-8")
d2 = {}
for line in d2_raw.splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 4:
        continue
    cleaned = [clean_ws(re.sub(r"\*", "", c)) for c in cells]
    word = None; typ = ""; pron = ""; meaning = ""
    bold_cells = [c for c in cells if "**" in c]
    if bold_cells:
        word = re.sub(r"\*", "", bold_cells[0]).strip()
        idx = cells.index(bold_cells[0])
        rest = [clean_ws(re.sub(r"\*", "", c)) for c in cells[idx + 1:]]
        if len(rest) >= 3:
            typ, pron, meaning = rest[0], rest[1], rest[2]
        elif len(rest) == 2:
            pron, meaning = rest
        elif len(rest) == 1:
            meaning = rest[0]
    elif len(cleaned) >= 4 and cleaned[1] and not cleaned[1].isdigit():
        word = cleaned[1]
        typ = cleaned[2]
        pron = cleaned[3] if len(cleaned) > 3 else ""
        meaning = cleaned[4] if len(cleaned) > 4 else ""
    if not word:
        continue
    word = re.sub(r"^\d+", "", word).strip().rstrip(", ").strip()
    if not word or len(word) > 40:
        continue
    key = norm_key(word)
    if not key or key in {"no", "tran", "g"} or "effortlessenglish" in key:
        continue
    entry = {"word": word, "type": typ.strip(),
             "pronunciation": clean_ws(pron).strip(" ;"),
             "meaning_vi": clean_ws(meaning).strip(" ;")}
    if key in d2 and d2[key]["meaning_vi"] and entry["meaning_vi"]:
        continue
    d2[key] = entry
    # alias support: "among, amongst" / "analyse, analyze" -> index each variant
    for part in re.split(r"[,/]", word):
        ak = norm_key(part)
        if ak and ak not in d2:
            d2[ak] = {**entry, "word": part.strip()}
    # index base form without trailing preposition: "consist of" -> "consist"
    m = re.match(r"(.+?)\s+(of|on|to|for|with|from)$", key)
    if m and m.group(1) not in d2:
        d2[m.group(1)] = {**entry, "word": m.group(1)}

# ---------------------------------------------------------------- merge
US_UK = {"center": ["centre"], "gray": ["grey"], "meter": ["metre"],
         "liter": ["litre"], "kilometer": ["kilometre"], "labor": ["labour"],
         "judgment": ["judgement"], "program": ["programme"], "jewelry": ["jewellery"]}

def lookup(key):
    cands = [key]
    # "consist of" / "depend on" style entries in dict2
    m = re.match(r"(.+?)\s+(of|on|to|for|with|from)$", key)
    if m:
        cands.append(m.group(1))
    cands += US_UK.get(key, [])
    for k in cands:
        e = d2.get(k)
        if e and (e["meaning_vi"] or e["pronunciation"]):
            return e
    return None

items = []
missing_meaning = []
for key, ox in oxford.items():
    d2e = lookup(key)
    pron = d2e["pronunciation"] if d2e else ""
    meaning = d2e["meaning_vi"] if d2e else ""
    status = "draft"
    if not meaning:
        status = "needs_meaning"
        missing_meaning.append(ox["word"])
    if pron and not pron.startswith("/"):
        pron = f"/{pron}/"
    items.append({
        "word": ox["word"],
        "part_of_speech": ox["part_of_speech"],
        "cefr": ox["cefr"],
        "pronunciation": pron,
        "meaning_vi": meaning,
        "source": {"word_source": "Oxford 3000",
                   "meaning_source": "dict2.md (needs verification)"},
        "status": status,
    })

extra = [
    {"word": e["word"], "type": e["type"], "pronunciation": e["pronunciation"],
     "meaning_vi": e["meaning_vi"], "source": {"word_source": "dict2.md only"}}
    for k, e in d2.items() if k not in oxford
]

OUT.write_text(json.dumps(
    {"meta": {"total_oxford_entries": len(items),
              "total_needs_meaning": len(missing_meaning),
              "total_dict2_only": len(extra)},
     "words": items, "dict2_only": extra},
    ensure_ascii=False, indent=1), encoding="utf-8")

print("oxford entries:", len(items))
print("needs_meaning :", len(missing_meaning))
print("dict2_only    :", len(extra))
print(json.dumps(items[:3] + items[600:601], ensure_ascii=False, indent=1))
print("missing sample:", missing_meaning[:50])

