import chardet
import pytest

import server

HOST = '127.0.0.1'
PORT = 8080
BUFFER_VALUE = 16


@pytest.mark.run_this
def test_short_message(awg_server, client_socket):
    client_socket.send(b"Hello World!")
    assert client_socket.recv(BUFFER_VALUE) == b"Hello World!"


@pytest.mark.run_this
def test_long_message(awg_server, client_socket):
    message = b"Four score and seven years ago our fathers did stuff"
    client_socket.send(message)
    received_message = b''
    size_expected = len(message)
    size_received = 0
    while True:
        tmp_received_message = client_socket.recv(BUFFER_VALUE)
        received_message += tmp_received_message
        size_received += len(tmp_received_message)
        if size_received >= size_expected:
            break

    assert received_message == message


@pytest.mark.run_this
def test_message_not_utf8(awg_server, client_socket):
    message = 'Привет'
    client_socket.sendall(message.encode('cp866'))
    received_message = client_socket.recv(BUFFER_VALUE)
    encoding = chardet.detect(received_message)
    assert encoding["encoding"] == 'utf-8'


@pytest.mark.run_this
def test_shutdown(awg_server, client_socket):
    server.exit_event.set()
    if server.exit_event.is_set():
        assert True
