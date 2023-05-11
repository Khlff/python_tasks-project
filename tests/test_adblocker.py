import pytest
from re import Pattern
from server_directory.adblocker import EasyListRegex


def test_easylist_to_reg_normalize():
    easy_list_regex = EasyListRegex()
    assert isinstance(easy_list_regex._easylist_to_reg_normalize(), Pattern)


def test_process():
    easy_list_regex = EasyListRegex()
    result = easy_list_regex.process("https://www.example.com")
    assert isinstance(result, str)
    assert "ads" not in result