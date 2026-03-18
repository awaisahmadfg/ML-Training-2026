from __future__ import annotations

import re
from collections import Counter
from typing import Dict, List, Tuple


def word_frequency(text: str) -> Dict[str, int]:
    # Extract only alphabetic sequences; this effectively ignores punctuation.
    words = re.findall(r"[A-Za-z]+", text.lower())
    return dict(Counter(words))


def top_n_words(text: str, n: int = 5) -> List[Tuple[str, int]]:
    freq = word_frequency(text)

    # sorted() with a key: sort by count descending, then word for stability.
    ranked = sorted(freq.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]


def main() -> None:
    paragraph = (
        "Hello world! This is a test. Hello again; world is big, "
        "and the world says hello."
    )

    freq = word_frequency(paragraph)
    print("Word frequency dict size:", len(freq))

    print("Top 5 most common words:")
    for i, (word, count) in enumerate(top_n_words(paragraph, 5), start=1):
        print(f"{i}. {word}: {count}")


if __name__ == "__main__":
    main()

