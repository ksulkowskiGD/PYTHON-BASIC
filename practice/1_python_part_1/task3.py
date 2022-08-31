"""
Write function which receives list of text lines
(which is space separated words) and word number.
It should enumerate unique words from each line
and then build string from all words of given number.
Restriction: word_number >= 0
Examples:
    >>> build_from_unique_words(
        'a b c',
        '1 1 1 2 3',
        'cat dog milk',
        word_number=1
        )
    'b 2 dog'
    >>> build_from_unique_words('a b c', '', 'cat dog milk', word_number=0)
    'a cat'
    >>> build_from_unique_words('1 2', '1 2 3', word_number=10)
    ''
    >>> build_from_unique_words(word_number=10)
    ''
"""
from typing import Iterable, List


def build_from_unique_words(*lines: Iterable[str], word_number: int) -> str:
    if word_number < 0:
        raise ValueError('Word number must not be less than zero!')
    words: List[str] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        unique_line: List[str] = list(dict.fromkeys(line.split(' ')))
        if len(unique_line) >= word_number:
            words.append(unique_line[word_number])
    return ' '.join(words)
