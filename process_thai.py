"""
Filter Thai+English sentences and tokenize using PyThaiNLP attacut.
Output: index\tword1 word2 word3 ...  (sorted by index)

Usage: python process_thai.py input.txt output.txt
"""
import re
import sys
import time
from pythainlp.tokenize import word_tokenize

input_file = sys.argv[1] if len(sys.argv) > 1 else 'aoede.txt'
output_file = sys.argv[2] if len(sys.argv) > 2 else 'aoede_tokenized.txt'

# Only allow: Thai chars, English chars, spaces, and basic punctuation
allowed = re.compile(r'^[\u0E00-\u0E7Fa-zA-Z\s\.,!?\;\:\'\"\-\(\)\[\]]+$')

# Step 1: Filter Thai+English only
print(f"[1/2] Filtering Thai+English sentences from {input_file}...")
filtered = []
total = 0

with open(input_file, 'r', encoding='utf-8') as fin:
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
            filtered.append((idx, sentence))

print(f"  Total: {total}, Thai+English only: {len(filtered)} ({len(filtered)/total*100:.2f}%)")

# Sort filtered by index
filtered.sort(key=lambda x: x[0])

# Save filtered (non-tokenized) file sorted by index
filtered_file = output_file.replace('.txt', '_filtered.txt')
with open(filtered_file, 'w', encoding='utf-8') as fout:
    for idx, sentence in filtered:
        fout.write(f"{idx}\t{sentence}\n")
print(f"  Saved filtered to: {filtered_file}")

# Step 2: Tokenize with attacut
print(f"[2/2] Tokenizing {len(filtered)} sentences with attacut...")
start = time.time()
results = []

for i, (idx, sentence) in enumerate(filtered):
    tokens = word_tokenize(sentence, engine="attacut")
    # Join with single space, filter empty tokens
    tokenized = ' '.join(t for t in tokens if t.strip())
    results.append((idx, tokenized))

    if (i + 1) % 2000 == 0:
        elapsed = time.time() - start
        rate = (i + 1) / elapsed
        remaining = (len(filtered) - i - 1) / rate
        print(f"  [{i+1}/{len(filtered)}] {elapsed:.1f}s elapsed, ~{remaining:.0f}s remaining")

# Write output (already sorted since filtered was sorted)
with open(output_file, 'w', encoding='utf-8') as fout:
    for idx, tokenized in results:
        fout.write(f"{idx}\t{tokenized}\n")

elapsed = time.time() - start
print(f"\nDone! {len(results)} sentences in {elapsed:.1f}s")
print(f"Saved to: {output_file}")
