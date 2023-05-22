import logging
import os
import re
import urllib
from socket import socket
from urllib.parse import urlparse

import requests
from tqdm import tqdm

import server_directory


# from server_directory import TQDM_CHUNK_SIZE, TQDM_UNIT_DIVISOR_SIZE


def is_valid(url: str) -> bool:
    """
    Checks if the url is a valid URL
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


class ImageDownloader:
    def __init__(self, url: str, path: str):
        self.SITE_URL = url
        self.path_to_download = path
        self.total_downloaded = 0

    def get_image_urls(self) -> list:
        """
        Returns a list of links to site images
        """
        response = requests.get(self.SITE_URL)
        html = response.text

        re_pattern = re.compile(
            r'<img.*?src=["\']?(.*?\.(?:jpg|jpeg|png))["\']?.*?>'
        )
        image_urls = re_pattern.findall(html)

        image_urls = [
            urllib.parse.urljoin(self.SITE_URL, url)
            for url in image_urls
            if is_valid(urllib.parse.urljoin(self.SITE_URL, url))
        ]
        return image_urls

    def _download(self, url: str, sock: socket) -> None:
        """
        Downloads the file by URL and places it in the `pathname` folder
        """

        if not os.path.isdir(self.path_to_download):
            os.makedirs(self.path_to_download)
        try:
            response = requests.get(url, stream=True)
            file_size = int(response.headers.get("Content-Length", 0))
            filename = os.path.join(self.path_to_download, url.split("/")[-1])
            progress = tqdm(
                response.iter_content(server_directory.TQDM_CHUNK_SIZE),
                f"Скачиваю {filename}",
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=server_directory.TQDM_UNIT_DIVISOR_SIZE
            )

            with open(filename, "wb") as f:
                for data in progress.iterable:
                    f.write(data)
                    progress.update(len(data))
            sock.sendall(f'Downloaded picture {url.split("/")[-1]}'.encode())
            self.total_downloaded += 1
        except requests.exceptions.ConnectionError as ex:
            logging.warning(ex)

    def download_images(self, sock) -> None:
        """
        Downloads all images from the site
        :param sock: socket with an established connection
        """
        url_list = self.get_image_urls()
        for url in url_list:
            self._download(url, sock)
