"""Tokenize Thai sentences to words using PyThaiNLP with attacut engine."""
from pythainlp.tokenize import word_tokenize
import sys
import time

input_file = sys.argv[1] if len(sys.argv) > 1 else 'aoede_thai_en.txt'
output_file = sys.argv[2] if len(sys.argv) > 2 else 'aoede_tokenized.txt'

with open(input_file, 'r', encoding='utf-8') as fin:
    lines = fin.readlines()

total_lines = len(lines)
print(f"Total lines to tokenize: {total_lines}")

count = 0
start = time.time()

with open(output_file, 'w', encoding='utf-8') as fout:
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t', 1)
        if len(parts) != 2:
            continue

        idx, sentence = parts
        tokens = word_tokenize(sentence, engine="attacut")
        tokenized = ' '.join(tokens)
        fout.write(f"{idx}\t{tokenized}\n")
        count += 1

        if count % 1000 == 0:
            elapsed = time.time() - start
            rate = count / elapsed
            remaining = (total_lines - count) / rate
            print(f"  [{count}/{total_lines}] {elapsed:.1f}s elapsed, ~{remaining:.0f}s remaining")

elapsed = time.time() - start
print(f"\nDone! Tokenized {count} sentences in {elapsed:.1f}s")
print(f"Saved to: {output_file}")
