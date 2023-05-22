import requests
from server_directory.vk_photo_worker import VKPhotoWorker, VKException
import pytest
from unittest.mock import patch


@patch('requests.get')
def test_request_user_id(mock_get):
    mock_get.return_value.json.return_value = {
        "response": [{"id": 123}]
    }
    vk = VKPhotoWorker("access_token")
    user_id = vk.request_user_id()
    assert user_id == 123


@patch('requests.get')
def test_request_albums_list_success(mock_get):
    mock_get.return_value.json.return_value = {
        "response":
            [{
                "title": "Some album",
                "id": 123
            }]
    }
    vk = VKPhotoWorker("access_token")
    mock_get.return_value.json.return_value = {
        "response":
            {'items': [{
                "title": "Some album",
                "id": 123
            }]
            }
    }
    albums = vk.request_albums_list()
    assert len(albums) == 1
    assert albums["Some album"] == 123


@patch('requests.get')
def test_request_photos_from_album(mock_get):
    mock_get.return_value.json.return_value = {
        "response":
            [{
                "title": "Some album",
                "id": 123
            }]
    }

    vk = VKPhotoWorker("access_token")
    mock_get.return_value.json.return_value = {
        "response": {
            "items": [
                {"sizes": [{"url": "some_url"}]}
            ]
        }
    }

    photo_urls = vk.request_photos_from_album(1)
    assert isinstance(photo_urls, list)
    assert len(photo_urls) == 1


def test_init_invalid_token():
    with pytest.raises(VKException):
        VKPhotoWorker("invalid_token")

