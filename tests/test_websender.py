import pytest
from unittest.mock import Mock, patch
from client.src.main.python.web_sender import WebSender


def test_send_message():
    with patch('socket.socket') as mock_socket:
        mock_conn = mock_socket.return_value
        sender = WebSender('localhost', 1234, Mock())
        message = 'Hello, server!'
        sender.send_message(message)
        mock_conn.sendall.assert_called_once_with(message.encode())


def test_get_log():
    with patch('socket.socket') as mock_socket:
        sender = WebSender('localhost', 1234, Mock())
        sender.message_buffer.put('Log message')
        assert sender.get_log() == 'Log message'


def test_get_empty_log():
    with patch('socket.socket') as mock_socket:
        sender = WebSender('localhost', 1234, Mock())
        assert sender.get_log() == ''
