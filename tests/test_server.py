import socket
import threading
import time
from unittest.mock import MagicMock, patch

import pytest

from server_directory.server import ServerHTTP, exit_event


class TestServerHTTP:
    @pytest.fixture()
    def server(self):
        return ServerHTTP(('localhost', 8000), './images', 'downloader')

    def test_init(self, server):
        assert server.server_address == ('localhost', 8000)
        assert server.path_to_download == './images'

    def test_receive_connection(self, server):
        sock = MagicMock()
        client_address = ('127.0.0.1', 1234)
        data = b'http://test.com\n'
        sock.recv.side_effect = [data, b'']

        with patch('server_directory.server.ImageDownloader') as mock_downloader:
            mock_downloader.return_value.download_images.return_value = None
            mock_downloader.return_value.total_downloaded = 0
            server._receive_connection(sock, client_address)

            mock_downloader.assert_called_once_with('http://test.com\n',
                                                    './images')
            mock_downloader.return_value.download_images.assert_called_once_with(
                sock)
            sock.sendall.assert_called_once_with(
                b'\nDownloaded 0 pictures from http://test.com\n'
            )

    def test_start_server(self, server):
        sock_mock = MagicMock()
        sock_mock.accept.side_effect = socket.timeout
        with patch('socket.create_server') as mock_create_server:
            mock_create_server.return_value.__enter__.return_value = sock_mock

            thread = threading.Thread(target=server.start_server)
            thread.start()
            time.sleep(1)
            exit_event.set()

            thread.join()
            mock_create_server.assert_called_once_with(('localhost', 8000))
            sock_mock.settimeout.assert_called_once_with(0.1)
            sock_mock.accept.assert_called()
