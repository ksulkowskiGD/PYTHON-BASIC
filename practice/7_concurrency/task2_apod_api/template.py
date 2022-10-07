import requests

API_KEY = "xXv0Q4G8xmc6bI0ZVpge94HBcqL3BCyzKjOtmhza"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    url: str = APOD_ENDPOINT + '?api_key=' + api_key + '&start_date=' +\
         start_date + '&end_date=' + end_date


def download_apod_images(metadata: list):
    pass


def main():
    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)


if __name__ == '__main__':
    main()
