import tempfile
from unittest import mock

import pytest
from server_directory import ImageDownloader


@pytest.fixture
def test_image_downloader():
    return ImageDownloader('https://www.example.com', tempfile.mkdtemp())


@pytest.fixture
def mock_response():
    response = mock.Mock()
    response.headers = {
        'Content-Length': 1000,
    }
    response.iter_content.return_value = b'fake_data'
    yield response


@pytest.fixture
def mock_requests_get(mock_response):
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        yield mock_get
