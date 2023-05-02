import os
import socket

from server_directory.images_downloader import ImageDownloader, _is_valid
from test_fixtures import test_image_downloader, mock_requests_get, mock_response


def test_is_valid_url():
    assert not _is_valid('invalid_url')
    assert _is_valid('http://validurl.com')


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


def test_download_images():
    url = "https://www.example.com"
    downloader = ImageDownloader(url, "../server_directory/downloads")
    server_address = ('localhost', 8080)
    with socket.create_server(server_address) as sock:
        downloader.download_images(sock)
    assert len(os.listdir("../server_directory/downloads")) > 0


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
        assert _is_valid(url) == False
    for url in valid_urls:
        assert _is_valid(url) == True
