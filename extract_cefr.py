# -*- coding: utf-8 -*-
"""Trích CEFR level từ 2 nguồn Oxford -> cefr_map.json (sidecar, KHÔNG đụng words.txt).

- dictionary/oxford.md  -> A1/A2/B1/B2 (nguồn words.txt)
- dictionary/2000.md    -> B1/B2/C1    (nguồn dictionary/words2.txt)

Quy tắc:
- Ưu tiên level từ oxford.md (Oxford 3000).
- Từ xuất hiện nhiều lần với nhiều level: giữ level dễ nhất (A1 < A2 < B1 < B2 < C1).
- Không suy diễn level khi nguồn không ghi -> null (không bịa CEFR).
"""
import re
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RANK = {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5}


def clean_lines_of(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("# The Oxford"):
            continue
        if s.startswith("_The Oxford"):
            continue
        if "Oxford University Press" in s:
            continue
        if re.match(r"^\d+ / \d+$", s):
            continue
        if s.startswith("**The Oxford"):
            continue
        if "©" in s:
            continue
        out.append(s)
    return out


def clean_hw(hw_raw):
    hw = hw_raw
    hw = re.sub(r"<sup>(.*?)</sup>", r"\1", hw)
    hw = re.sub(r"\s*\(.*?\)", "", hw).strip()
    hw = hw.replace("\u2019", "'").replace("\u2018", "'")
    hw = re.sub(r"\s+", " ", hw).strip()
    return hw


def parse(src_path, levels):
    text = Path(src_path).read_text(encoding="utf-8")
    body = " ".join(clean_lines_of(text))
    body = re.sub(r"\s+", " ", body)
    # fix malformed POS containing level: "specialize _v. B1_" -> "specialize _v._ B1"
    body = re.sub(r"_([a-z\.\/, ]*?) (B1|B2|C1)_", r"_\1_ \2", body)
    tokens = re.split(r" (" + "|".join(levels) + r")(?= )", body)
    entries = []
    for i in range(0, len(tokens) - 1, 2):
        entries.append((tokens[i], tokens[i + 1]))

    result = []   # (word, level)
    last_word = None
    for chunk, lvl in entries:
        c = chunk.strip()
        c = re.sub(r"^\d+ / \d+\s+", "", c)
        m = re.match(r"^(.*)\s+_(.*?)_$", c)
        if not m:
            if last_word is None:
                continue
            # continuation: cùng headword, level khác -> vẫn ghi nhận
            result.append((last_word, lvl))
            continue
        hw_raw = m.group(1).strip()
        if hw_raw == "a, an":
            result.append(("a", lvl))
            result.append(("an", lvl))
            last_word = "a"
            continue
        hw = clean_hw(hw_raw)
        if not hw or hw.startswith("_,"):
            continue
        result.append((hw, lvl))
        last_word = hw
    return result


def merge(pairs_list):
    merged = {}
    for pairs in pairs_list:
        for w, lvl in pairs:
            cur = merged.get(w)
            if cur is None or RANK.get(lvl, 99) < RANK.get(cur, 99):
                merged[w] = lvl
    return merged


oxford = parse("dictionary/oxford.md", ['A1', 'A2', 'B1', 'B2'])
two_k = parse("dictionary/2000.md", ['B1', 'B2', 'C1'])
print(f"oxford.md pairs: {len(oxford)}, 2000.md pairs: {len(two_k)}")

merged = merge([oxford, two_k])
print(f"unique words with CEFR: {len(merged)}")

# đối chiếu với danh sách từ thực tế
words1 = Path("words.txt").read_text(encoding="utf-8").splitlines()
words2 = Path("dictionary/words2.txt").read_text(encoding="utf-8").splitlines()
allw = set(w.strip() for w in words1 + words2 if w.strip())
covered = sum(1 for w in allw if w in merged)
print(f"word list unique: {len(allw)}, CEFR covered: {covered} "
      f"({100.0 * covered / len(allw):.1f}%)")

Path("cefr_map.json").write_text(
    json.dumps(merged, ensure_ascii=False, indent=0, sort_keys=True),
    encoding="utf-8")
print("wrote cefr_map.json")
