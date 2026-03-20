import re
import sys

def analyze_sentences(filepath):
    """
    Analyze sentences from a tab-separated file (index\tsentence).
    Categories:
    1. Sentences containing special characters
    2. Sentences containing only Thai + English words (clean)
    3. Sentences containing numbers
    """

    # Thai character range
    thai_pattern = re.compile(r'[\u0E00-\u0E7F]')
    # English character range
    english_pattern = re.compile(r'[a-zA-Z]')
    # Number pattern
    number_pattern = re.compile(r'[0-9]')
    # Special characters: anything that is NOT Thai, English, numbers, or common punctuation/whitespace
    # Common punctuation: . , ! ? ; : ' " - () {} [] / \ @ # $ % & * + = ~ ` ^ | < > _
    # We define "special" as characters outside Thai, English, digits, basic whitespace, and standard punctuation
    special_char_pattern = re.compile(
        r'[^\u0E00-\u0E7Fa-zA-Z0-9\s'
        r'\.,!?\;\:\'\"\-\(\)\{\}\[\]\/\\@#\$%&\*\+\=\~\`\^\|<>_'
        r'ๆ็์ะิืูัำฺ่้๊๋'  # Thai marks already in Thai range
        r']'
    )
    # "Only Thai + English" means: contains Thai or English, no numbers, no special chars
    # Allowed: Thai chars, English chars, spaces, and basic Thai/English punctuation
    only_thai_english_pattern = re.compile(
        r'^[\u0E00-\u0E7Fa-zA-Z\s\.,!?\;\:\'\"\-\(\)\[\]]+$'
    )

    total = 0
    with_special = []
    only_thai_english = []
    with_numbers = []
    errors = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t', 1)
            if len(parts) != 2:
                errors.append((line_num, line))
                continue

            index, sentence = parts
            total += 1

            has_number = bool(number_pattern.search(sentence))
            has_special = False

            # Check for special characters (characters not in Thai, English, digits, whitespace, common punctuation)
            for char in sentence:
                if not (
                    '\u0E00' <= char <= '\u0E7F' or  # Thai
                    'a' <= char <= 'z' or 'A' <= char <= 'Z' or  # English
                    '0' <= char <= '9' or  # Digits
                    char in ' \t\n' or  # Whitespace
                    char in '.,!?;:\'"()-[]{}/@#$%&*+=~`^|<>_' or  # Common punctuation
                    char == 'ๆ'  # Thai repetition mark (already in Thai range)
                ):
                    has_special = True
                    break

            # Check if sentence contains only Thai + English (+ spaces + basic punctuation)
            # No numbers, no special characters
            is_only_thai_english = bool(only_thai_english_pattern.match(sentence))

            if has_special:
                with_special.append((index, sentence))
            if is_only_thai_english:
                only_thai_english.append((index, sentence))
            if has_number:
                with_numbers.append((index, sentence))

    # Print summary
    print("=" * 70)
    print(f"FILE: {filepath}")
    print(f"TOTAL SENTENCES: {total}")
    print("=" * 70)

    print(f"\n1. Sentences with SPECIAL CHARACTERS: {len(with_special)} ({len(with_special)/total*100:.2f}%)")
    print(f"2. Sentences with ONLY Thai + English (no numbers, no special): {len(only_thai_english)} ({len(only_thai_english)/total*100:.2f}%)")
    print(f"3. Sentences with NUMBERS: {len(with_numbers)} ({len(with_numbers)/total*100:.2f}%)")

    if errors:
        print(f"\n⚠ Lines with parsing errors: {len(errors)}")

    # Write filtered results to files
    write_results(with_special, 'filtered_special_chars.txt', 'Sentences with special characters')
    write_results(only_thai_english, 'filtered_thai_english_only.txt', 'Sentences with only Thai + English')
    write_results(with_numbers, 'filtered_with_numbers.txt', 'Sentences with numbers')

    # Print sample of each category
    print("\n" + "=" * 70)
    print("SAMPLE: Sentences with SPECIAL CHARACTERS (first 10)")
    print("=" * 70)
    for idx, sent in with_special[:10]:
        # Find and highlight the special characters
        specials = []
        for char in sent:
            if not (
                '\u0E00' <= char <= '\u0E7F' or
                'a' <= char <= 'z' or 'A' <= char <= 'Z' or
                '0' <= char <= '9' or
                char in ' \t\n' or
                char in '.,!?;:\'"()-[]{}/@#$%&*+=~`^|<>_'
            ):
                specials.append(f"'{char}' (U+{ord(char):04X})")
        print(f"  [{idx}] {sent[:80]}...")
        print(f"         Special chars: {', '.join(set(specials))}")

    print("\n" + "=" * 70)
    print("SAMPLE: Sentences with ONLY Thai + English (first 10)")
    print("=" * 70)
    for idx, sent in only_thai_english[:10]:
        print(f"  [{idx}] {sent[:100]}")

    print("\n" + "=" * 70)
    print("SAMPLE: Sentences with NUMBERS (first 10)")
    print("=" * 70)
    for idx, sent in with_numbers[:10]:
        nums = number_pattern.findall(sent)
        print(f"  [{idx}] {sent[:100]}")


def write_results(data, filename, description):
    """Write filtered results to a file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {description}\n")
        f.write(f"# Total: {len(data)}\n\n")
        for idx, sent in data:
            f.write(f"{idx}\t{sent}\n")
    print(f"   -> Saved to {filename}")


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'aoede.txt'
    analyze_sentences(filepath)
