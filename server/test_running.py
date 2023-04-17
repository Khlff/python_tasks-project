import os

from http_server.server.images_downloader import ImageDownloader, _is_valid


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


def test_download():
    url = "https://www.example.com/images/example.jpg"
    downloader = ImageDownloader(url, "downloads")
    downloader._download(url)
    assert os.path.isfile("downloads/example.jpg")


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
        assert _is_valid(url) == False
    for url in valid_urls:
        assert _is_valid(url) == True
