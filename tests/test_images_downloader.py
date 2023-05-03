import os
import socket
from unittest.mock import MagicMock, patch

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


def test_download_images(tmpdir):
    download_dir = tmpdir.mkdir("test_images")
    url = "https://example.com"
    downloader = ImageDownloader(url, download_dir)

    mock_socket = MagicMock()

    with patch("requests.get") as mock_get:
        mock_get.return_value.text = """
            <html>
                <body>
                    <img src="https://example.com/image1.jpg">
                    <img src="https://example.com/image2.jpg">
                    <img src="https://example.com/image3.png">
                </body>
            </html>
        """
        downloader.download_images(mock_socket)

    expected_files = ["image1.jpg", "image2.jpg", "image3.png"]
    expected_count = len(expected_files)
    assert downloader.total_downloaded == expected_count
    for file in expected_files:
        assert os.path.isfile(os.path.join(download_dir, file))


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
