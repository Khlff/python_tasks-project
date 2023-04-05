import os
import socket
import subprocess
import tempfile
import time
from unittest import mock
from unittest.mock import patch, Mock, MagicMock

import pytest
import requests
import server
from test_fixtures import test_image_downloader
from test_fixtures import mock_response
from test_fixtures import mock_requests_get

from images_downloader import ImageDownloader


def test_is_valid_url(test_image_downloader):
    test_image_downloader.SITE_URL = 'invalid_url'
    assert not test_image_downloader._is_valid()

    test_image_downloader.SITE_URL = 'http://validurl.com'
    assert test_image_downloader._is_valid()


def test_get_image_urls(test_image_downloader, mock_requests_get):
    mock_requests_get.return_value.text = """
        <html>
            <img src="http://example.com/img1.jpg">
            <img src="http://example.com/img2.jpg">
        </html>
    """
    assert test_image_downloader.get_image_urls() == [
        'http://example.com/img1.jpg',
        'http://example.com/img2.jpg'
    ]


def test_download():
    url = "https://www.example.com/images/example.jpg"
    downloader = ImageDownloader(url, "downloads")
    downloader._download(url)
    assert os.path.isfile("downloads/example.jpg") == True

def test_download_images():
    url = "https://www.example.com"
    downloader = ImageDownloader(url, "downloads")
    downloader.download_images()
    assert len(os.listdir("downloads")) > 0


def test_is_valid():
    invalid_urls = [
        'http://',
        'vbfhsb',
        'http:/jnvjf.dd'
    ]
    valid_urls = [
        'http://example.com',
        'https://example.com',
        'http://www.example.com'
    ]
    for url in invalid_urls:
        downloader = ImageDownloader(url, 'path/to/download')
        assert downloader._is_valid() == False
    for url in valid_urls:
        downloader = ImageDownloader(url, 'path/to/download')
        assert downloader._is_valid() == True
