"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


def write_words(path_to_files: str, words: list[str]) -> None:
    with open(f'{path_to_files}file1.txt', 'w', encoding='utf8') as fh:
        fh.write('\n'.join(words))
    with open(f'{path_to_files}file2.txt', 'w', encoding='CP1252') as fh:
        fh.write(','.join(words[-1::-1]))


def main():
    write_words('practice/2_python_part_2/files/', generate_words(5))


if __name__ == '__main__':
    main()
