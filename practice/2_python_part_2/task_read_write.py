"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""


def read_files(path_to_files: str) -> list[int]:
    numbers: list[str] = []
    for i in range(1, 21):
        with open(f'{path_to_files}file_{i}.txt', 'r') as fh:
            numbers.append(fh.read())
    return numbers


def write_to_file(file_path: str, content: list[str]) -> None:
    with open(file_path, 'w') as fh:
        fh.write(', '.join(content))


def main():
    numbers: list[str] = read_files('practice/2_python_part_2/files/')
    write_to_file('practice/2_python_part_2/files/result.txt', numbers)


if __name__ == '__main__':
    main()
