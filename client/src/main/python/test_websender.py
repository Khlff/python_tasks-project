import pytest
import socket
from client.src.main.python.web_sender import WebSender


@pytest.fixture
def web_sender(mocker):
    mocker.patch.object(socket, 'socket')
    mock_socket = socket.socket.return_value
    mock_socket.recv.return_value = b"Received Message"
    return WebSender("localhost", 8080)


def test_send_message(web_sender, mocker):
    mock_socket = mocker.patch.object(web_sender.sock, 'sendall')
    web_sender.send_message("Test Message")
    mock_socket.assert_called_once_with(b"Test Message")


def test_get_log_empty(web_sender, mocker):
    mock_socket = mocker.patch.object(web_sender.message_buffer, 'empty',
                                      return_value=True)
    assert web_sender.get_log() == ""


def test_get_log_nonempty(web_sender, mocker):
    mock_socket = mocker.patch.object(web_sender.message_buffer, 'empty',
                                      return_value=False)
    assert web_sender.get_log() == "Received Message"


def test_get_log_multiple_messages(web_sender, mocker):
    mock_get = mocker.patch.object(web_sender.message_buffer, 'get',
                                   side_effect=["Message 1", "Message 2",
                                                "Message 3", ""])
    assert web_sender.get_log() == "Message 1"
    assert web_sender.get_log() == "Message 2"
    assert web_sender.get_log() == "Message 3"
    assert web_sender.get_log() == ""


if __name__ == "__main__":
    pytest.main()
