import glob
import os
from random import randint
from source.template import func1, func2, RESULT_FILE, OUTPUT_DIR


def test_all_numbers_are_in_results():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    func1(array=[randint(1000, 100000) for _ in range(1000)])
    func2(result_file=RESULT_FILE)

    txt_files = glob.glob('./output/*.txt')

    with open('./output/result.csv', 'r') as fh:
        lines_in_result = 0
        for _ in fh:
            lines_in_result += 1

    assert len(txt_files) == lines_in_result
