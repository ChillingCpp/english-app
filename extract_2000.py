import re
from pathlib import Path

src = Path("dictionary/2000.md")
dst = Path("dictionary/words2.txt")

text = src.read_text(encoding="utf-8")

clean_lines = []
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
    clean_lines.append(line)

body = " ".join(clean_lines)
body = re.sub(r"\s+", " ", body)

# Fix malformed POS containing level, e.g. "specialize _v. B1_" -> "specialize _v._ B1"
body = re.sub(r"_([a-z\.\/, ]*?) (B1|B2|C1)_", r"_\1_ \2", body)

tokens = re.split(r" (B1|B2|C1)(?= )", body)
entries = []
for i in range(0, len(tokens) - 1, 2):
    entries.append((tokens[i], tokens[i + 1]))

print(f"Total level markers: {len(entries)}")

words = []
raw_entries = []
continued = []
last_word = None

def clean_hw(hw_raw, pos_raw):
    hw = hw_raw
    if hw == "according" and pos_raw == "to prep.":
        return "according to"
    # Keep sense numbers: bow<sup>1</sup> -> bow1
    hw = re.sub(r"<sup>(.*?)</sup>", r"\1", hw)
    # Remove parenthetical sense labels: "counter (long flat surface)" -> "counter"
    hw = re.sub(r"\s*\(.*?\)", "", hw).strip()
    hw = hw.replace("\u2019", "'").replace("\u2018", "'")
    hw = hw.strip()
    hw = re.sub(r"\s+", " ", hw)
    return hw

for chunk, lvl in entries:
    c = chunk.strip()
    c = re.sub(r"^\d+ / \d+\s+", "", c)
    m = re.match(r"^(.*)\s+_(.*?)_$", c)
    if not m:
        assert last_word is not None, f"Continuation without previous word: {c!r}"
        words.append(last_word)
        continued.append((c, lvl, last_word))
        continue
    hw_raw = m.group(1).strip()
    pos_raw = m.group(2).strip()
    raw_entries.append((hw_raw, pos_raw, lvl, c))
    if hw_raw == "a, an":
        words.append("a")
        words.append("an")
        last_word = "a"
        continue
    hw = clean_hw(hw_raw, pos_raw)
    words.append(hw)
    last_word = hw

print(f"Parsed headword entries: {len(raw_entries)}")
print(f"Continued meanings (same word, other POS): {len(continued)}")
print(f"Final words: {len(words)}")

assert len(raw_entries) >= 2000, f"Must not drop below 2000, got {len(raw_entries)}"
assert len(words) >= 2000, f"Must not drop below 2000, got {len(words)}"
assert all(s and not s.startswith("_,") for s in words)

from collections import Counter
cnt = Counter(words)
dups = {k: v for k, v in cnt.items() if v > 1}
print(f"Unique spellings: {len(cnt)} (dup groups: {len(dups)})")

dst.write_text("\n".join(words) + "\n", encoding="utf-8")
print(f"Wrote {dst.resolve()} with {len(words)} lines")
print("First 10:", words[:10])
print("Last 10:", words[-10:])
