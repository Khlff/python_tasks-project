import os
import re
import urllib

import requests
from tqdm import tqdm
from urllib.parse import urlparse, urljoin


def _is_valid(url: str) -> bool:
    """
    Проверяет, является ли url допустимым URL
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


class ImageDownloader:
    def __init__(self, url: str, path: str, connection):
        self.SITE_URL = url
        self.PATH_TO_DOWNLOAD = path
        self.connection = connection
        self.TQDM_CHUNK_SIZE = 1024
        self.TQDM_UNIT_DIVISOR_SIZE = 1024

    def get_image_urls(self) -> list:
        """
        Возвращает список ссылок на картинки сайта
        """
        response = requests.get(self.SITE_URL)
        html = response.text

        image_urls = re.findall(r'<img.*?src="(.*?)".*?>', html)

        image_urls = [
            urllib.parse.urljoin(self.SITE_URL, url)
            for url in image_urls
            if _is_valid(urllib.parse.urljoin(self.SITE_URL, url))
        ]

        return image_urls

    def _download(self, url: str) -> None:
        """
        Загружает файл по URL‑адресу и помещает его в папку `pathname`
        """

        if not os.path.isdir(self.PATH_TO_DOWNLOAD):
            os.makedirs(self.PATH_TO_DOWNLOAD)

        response = requests.get(url, stream=True)
        file_size = int(response.headers.get("Content-Length", 0))
        filename = os.path.join(self.PATH_TO_DOWNLOAD, url.split("/")[-1])
        progress = tqdm(
            response.iter_content(self.TQDM_CHUNK_SIZE),
            f"Скачиваю {filename}",
            total=file_size,
            unit="B",
            unit_scale=True,
            unit_divisor=self.TQDM_UNIT_DIVISOR_SIZE
        )

        with open(filename, "wb") as f:
            for data in progress.iterable:
                f.write(data)
                progress.update(len(data))

    def download_images(self) -> None:
        url_list = self.get_image_urls()
        for url in url_list:
            self._download(url)
