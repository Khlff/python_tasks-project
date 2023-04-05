import socket
import subprocess
import time

import pytest

HOST = '127.0.0.1'
PORT = 8080
BUFFER_VALUE = 16


@pytest.fixture(scope="session")
def awg_server():
    print("loading server")
    p = subprocess.Popen(["python3", "server.py"])
    time.sleep(1)
    yield p
    p.terminate()


@pytest.fixture
def client_socket():
    print("entering client part")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_sock:
        my_sock.connect((HOST, PORT))
        yield my_sock
        my_sock.close()
