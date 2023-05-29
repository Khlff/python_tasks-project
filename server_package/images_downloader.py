import logging
import os
import re
import urllib
from socket import socket
from urllib.parse import urlparse

import requests
from tqdm import tqdm

import server_package


# from server_package import TQDM_CHUNK_SIZE, TQDM_UNIT_DIVISOR_SIZE


def is_valid(url: str) -> bool:
    """
    Checks if the given URL is a valid URL.
    :param url: The URL to check.
    :return: True if the URL is valid, False otherwise.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


class ImageDownloader:
    """
    Provides methods for downloading images from a website.
    """
    def __init__(self, url: str, path: str):
        """
        Initializes a new instance of the ImageDownloader class.
        :param url: The URL of the website to download images from.
        :param path: The directory to save the downloaded images to.
        """
        self.SITE_URL = url
        self.path_to_download = path
        self.total_downloaded = 0

    def get_image_urls(self) -> list:
        """
        Retrieves a list of image URLs from the website.
        :return: A list of image URLs.
        :raises: Any exception raised during the request process.
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

    def download(self, url: str, sock: socket) -> None:
        """
        Downloads a single file specified by the URLand saves it to the specified directory.
        :param url: The URL of the file to download.
        :param sock: The socket with an established connection.
        :raises: Any exception raised during the download process.
        """

        if not os.path.isdir(self.path_to_download):
            os.makedirs(self.path_to_download)
        try:
            response = requests.get(url, stream=True)
            file_size = int(response.headers.get("Content-Length", 0))
            url_ = url.split("/")[-1]
            filename = os.path.join(self.path_to_download, url_.split("?")[0])
            progress = tqdm(
                response.iter_content(server_package.TQDM_CHUNK_SIZE),
                f"Скачиваю {filename}",
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=server_package.TQDM_UNIT_DIVISOR_SIZE
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
            self.download(url, sock)
