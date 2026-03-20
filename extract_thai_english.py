"""Extract only sentences containing Thai + English characters (no numbers, no special chars)."""
import re
import sys

filepath = sys.argv[1] if len(sys.argv) > 1 else 'aoede.txt'
output = sys.argv[2] if len(sys.argv) > 2 else 'thai_english_only.txt'

# Only allow: Thai chars, English chars, spaces, and basic punctuation
allowed = re.compile(r'^[\u0E00-\u0E7Fa-zA-Z\s\.,!?\;\:\'\"\-\(\)\[\]]+$')

count = 0
total = 0

with open(filepath, 'r', encoding='utf-8') as fin, \
     open(output, 'w', encoding='utf-8') as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t', 1)
        if len(parts) != 2:
            continue
        idx, sentence = parts
        total += 1
        if allowed.match(sentence):
            fout.write(f"{idx}\t{sentence}\n")
            count += 1

print(f"Total: {total}")
print(f"Thai+English only: {count} ({count/total*100:.2f}%)")
print(f"Saved to: {output}")
