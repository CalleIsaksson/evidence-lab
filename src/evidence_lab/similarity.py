import string
from math import sqrt


def word_frequencies(text: str) -> dict[str, int]:
    cleaned_text = text.lower().translate(
        str.maketrans("", "", string.punctuation)
    )

    words = cleaned_text.split()
    frequencies: dict[str, int] = {}

    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1

    return frequencies


def cosine_similarity(
    first: dict[str, int],
    second: dict[str, int],
) -> float:
    all_words = set(first) | set(second)

    dot_product = 0
    first_squared_sum = 0
    second_squared_sum = 0

    for word in all_words:
        first_value = first.get(word, 0)
        second_value = second.get(word, 0)
        dot_product += first_value * second_value

        first_squared_sum += first_value**2
        second_squared_sum += second_value**2

    first_length = sqrt(first_squared_sum)
    second_length = sqrt(second_squared_sum)

    if first_length == 0 or second_length == 0:
        return 0.0

    return dot_product / (first_length * second_length)
