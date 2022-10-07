import os
from queue import Queue
import queue
from threading import Thread
import requests
import json

API_KEY = "xXv0Q4G8xmc6bI0ZVpge94HBcqL3BCyzKjOtmhza"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'
MAX_THREADS = 12


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    url: str = APOD_ENDPOINT + '?api_key=' + api_key + '&start_date=' +\
        start_date + '&end_date=' + end_date
    return json.loads(requests.get(url).content[:-1])


def download_apod_worker(tasks_queue: Queue) -> None:
    while True:
        try:
            task = tasks_queue.get(block=False)
        except queue.Empty:
            return
        image: bytes = requests.get(task['url']).content
        with open(OUTPUT_IMAGES + '/' + task['name'], 'wb') as fh:
            fh.write(image)
        tasks_queue.task_done()


def download_apod_images(metadata: list, download_hd: bool = False) -> None:
    tasks_queue: Queue = Queue()
    for day in metadata:
        if day['media_type'] == 'image':
            key: str = 'url'
            if download_hd:
                key = 'hdurl'
            image_url: str = day[key]
            image_name: str = image_url.split('/')[-1]
            tasks_queue.put({
                'url': image_url,
                'name': image_name
            })
    threads = [Thread(
        target=download_apod_worker,
        args=(tasks_queue,)
    ) for _ in range(MAX_THREADS)]
    for t in threads:
        t.start()
    tasks_queue.join()


def main() -> None:
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)

    metadata: list = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)


if __name__ == '__main__':
    main()
