import os
import queue
from queue import Queue
from random import randint
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from threading import Thread
import glob

OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'
MAX_WORKERS = 12


def fib(n: int) -> tuple[int, int]:
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    return n, f1


def save_to_file_func1(n: int, result_number: int) -> None:
    output_path: str = f'{OUTPUT_DIR}/{n}.txt'
    with open(output_path, 'w') as fh:
        fh.write(str(result_number))


def worker_func1(numbers_queue: mp.JoinableQueue) -> None:
    while True:
        try:
            task = numbers_queue.get(block=False)
        except queue.Empty:
            return
        save_to_file_func1(*task)
        numbers_queue.task_done()


def func1(array: list) -> None:
    with ProcessPoolExecutor(MAX_WORKERS) as ex1:
        results = ex1.map(fib, array)

    results_queue: mp.JoinableQueue = mp.JoinableQueue()
    for x in list(results):
        results_queue.put(x)

    threads: list[Thread] = [Thread(
        target=worker_func1,
        args=(results_queue,)
        ) for _ in range(MAX_WORKERS)]

    for t in threads:
        t.start()
    results_queue.join()


def read_write_func2(results_file: str, input_file: str) -> None:
    with open(input_file, 'r') as fh:
        result = input_file.split('/')[2].split('.')[0], fh.read()
    with open(results_file, 'a') as fh:
        fh.write(f'{result[0]},{result[1]}\n')


def worker_func2(task_queue: Queue, results_file: str) -> None:
    while True:
        try:
            task = task_queue.get(block=False)
        except queue.Empty:
            return
        read_write_func2(results_file, task)
        task_queue.task_done()


def func2(result_file: str) -> None:
    files: list[str] = glob.glob(OUTPUT_DIR + '/*')
    task_queue: Queue = Queue()
    for file_name in files:
        task_queue.put(file_name)

    threads: list[Thread] = [Thread(
        target=worker_func2,
        args=(task_queue, result_file)
        ) for _ in range(MAX_WORKERS)]

    for t in threads:
        t.start()
    task_queue.join()


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    func1(array=[randint(1000, 100000) for _ in range(1000)])
    func2(result_file=RESULT_FILE)
