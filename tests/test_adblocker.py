from unittest.mock import Mock

import pytest
from re import Pattern
from server_directory.adblocker import EasyListRegex


def test_easylist_to_reg_normalize():
    easy_list_regex = EasyListRegex()
    assert isinstance(easy_list_regex._easylist_to_reg_normalize(), Pattern)


def test_process(monkeypatch):
    easy_list_regex = EasyListRegex()
    mock_response = Mock()

    with open("test_html.html", "r", encoding="utf-8") as f:
        html = f.read()

    mock_response.content.decode.return_value = html
    monkeypatch.setattr("requests.get", lambda url: mock_response)

    result = easy_list_regex.process("https://www.example.com")
    assert isinstance(result, str)

    with open("test_html_result.html", "r", encoding="utf-8") as f:
        html_result = f.read()

    assert result == html_result
