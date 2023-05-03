import os
import re
import urllib
from socket import socket
from urllib.parse import urlparse

import requests
from tqdm import tqdm

LOG_SIZE = 20


def _is_valid(url: str) -> bool:
    """
    Checks if the url is a valid URL
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


class ImageDownloader:
    def __init__(self, url: str, path: str):
        self.SITE_URL = url
        self.PATH_TO_DOWNLOAD = path
        self.TQDM_CHUNK_SIZE = 1024
        self.TQDM_UNIT_DIVISOR_SIZE = 1024
        self.total_downloaded = 0

    def get_image_urls(self) -> list:
        """
        Returns a list of links to site images
        """
        response = requests.get(self.SITE_URL)
        html = response.text

        image_urls = re.findall(
            r'<img.*?src=["\']?(.*?\.(?:jpg|jpeg|png))["\']?.*?>', html)

        image_urls = [
            urllib.parse.urljoin(self.SITE_URL, url)
            for url in image_urls
            if _is_valid(urllib.parse.urljoin(self.SITE_URL, url))
        ]
        return image_urls

    def _download(self, url: str, sock: socket) -> None:
        """
        Downloads the file by URL and places it in the `pathname` folder
        """

        if not os.path.isdir(self.PATH_TO_DOWNLOAD):
            os.makedirs(self.PATH_TO_DOWNLOAD)
        try:
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
            sock.sendall(f'Downloaded picture {url.split("/")[-1]}'.encode())
            self.total_downloaded += 1
        except requests.exceptions.ConnectionError as ex:
            pass

    def download_images(self, sock) -> None:
        """
        Downloads all images from the site
        :param sock: socket with an established connection
        """
        url_list = self.get_image_urls()
        for url in url_list:
            self._download(url, sock)
