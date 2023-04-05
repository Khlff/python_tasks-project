import os

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse, urljoin


def is_valid(url):
    """
    Проверяет, является ли url допустимым URL
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_urls_images(url):
    """
    Возвращает все URL‑адреса изображений по одному `url`
    """
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    urls = []
    for img in tqdm(soup.find_all("img"), "Ворую картинки с сайта"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue

        img_url = urljoin(url, img_url)

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass

        if is_valid(img_url):
            urls.append(img_url)
    return urls


def download(url, pathname):
    """
    Загружает файл по URL‑адресу и помещает его в папку `pathname`
    """

    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    response = requests.get(url, stream=True)

    file_size = int(response.headers.get("Content-Length", 0))

    filename = os.path.join(pathname, url.split("/")[-1])

    progress = tqdm(response.iter_content(1024), f"Downloading {filename}",
                    total=file_size, unit="B", unit_scale=True,
                    unit_divisor=1024)

    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))
