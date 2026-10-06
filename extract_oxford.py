import re
from pathlib import Path

src = Path("dictionary/oxford.md")
dst = Path("words.txt")

text = src.read_text(encoding="utf-8")

# Remove headers/footers/boilerplate
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

# Split by CEFR levels (A1/A2/B1/B2). Each marker ends an entry.
tokens = re.split(r" (A1|A2|B1|B2)(?= )", body)
entries = []
for i in range(0, len(tokens) - 1, 2):
    chunk = tokens[i]
    lvl = tokens[i + 1]
    entries.append((chunk, lvl))

print(f"Total level markers: {len(entries)}")

words = []          # final list, keeps every meaning (>=3000 lines)
raw_entries = []    # explicit headwords (3000)
continued = []      # continuation entries reusing previous headword (306)
last_word = None

def clean_hw(hw_raw, pos_raw):
    hw = hw_raw
    # Special case from PDF conversion: "according _to prep._" should be "according to"
    if hw == "according" and pos_raw == "to prep.":
        return "according to"
    # Keep sense numbers: can<sup>1</sup> -> can1, do1 stays do1
    hw = re.sub(r"<sup>(.*?)</sup>", r"\1", hw)
    # Remove parenthetical sense labels: "kind (type)" -> "kind", "bear (animal)" -> "bear"
    hw = re.sub(r"\s*\(.*?\)", "", hw).strip()
    # Normalize curly apostrophe to ASCII: o’clock -> o'clock
    hw = hw.replace("\u2019", "'").replace("\u2018", "'")
    hw = hw.strip()
    hw = re.sub(r"\s+", " ", hw)
    return hw

for chunk, lvl in entries:
    c = chunk.strip()
    c = re.sub(r"^\d+ / \d+\s+", "", c)  # leading page number e.g. "5 / 11 initial"
    m = re.match(r"^(.*)\s+_(.*?)_$", c)
    if not m:
        # Continuation like "_, v._": same word, different POS/meaning -> repeat previous word
        assert last_word is not None, f"Continuation without previous word: {c!r}"
        words.append(last_word)
        continued.append((c, lvl, last_word))
        continue
    hw_raw = m.group(1).strip()
    pos_raw = m.group(2).strip()
    raw_entries.append((hw_raw, pos_raw, lvl, c))

    # ---- cleaning ----
    # Special: "a, an" -> keep both forms as separate lines (don't drop "an")
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

# Verify: never drop below 3000; duplicates and continuations are all kept
assert len(raw_entries) == 3000, f"Expected 3000 headword entries, got {len(raw_entries)}"
assert len(words) >= 3000, f"Must not drop below 3000, got {len(words)}"
assert all(s and not s.startswith("_,") for s in words), "Continuation leaked"

# Check duplicates (homographs without numbers share spelling; last1/second1 share same number)
from collections import Counter
cnt = Counter(words)
dups = {k: v for k, v in cnt.items() if v > 1}
print(f"Unique spellings: {len(cnt)} (dup groups: {len(dups)})")
if dups:
    print("Duplicates (same spelling, different senses - both kept to preserve 3000 lines):")
    for k in sorted(dups):
        print(f"  {k!r}: {dups[k]}x")

# Write words.txt, one word per line, original order (a -> zone, as in oxford.md)
dst.write_text("\n".join(words) + "\n", encoding="utf-8")
print(f"Wrote {dst.resolve()} with {len(words)} lines")

# Quick sanity: first 10, last 10
print("First 10:", words[:10])
print("Last 10:", words[-10:])
