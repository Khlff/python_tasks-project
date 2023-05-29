import logging
import signal
import socket
import string
from threading import Event

import chardet

from server_package import EasyListRegex
from server_package import ImageDownloader
from server_package.args_parser import create_parser
from server_package.constants import SOCKET_TIMEOUT, BUFFER_VALUE
from server_package.vk_photo_worker import VKPhotoWorker, VKException

exit_event = Event()


def signal_handler(_signal: signal, _) -> None:
    """
    Set global variable Event into True
    :param _signal: The signal that was received.
    :param _: Additional information about the signal (not used).
    """
    exit_event.set()


class ServerHTTP:
    """
    Class for starting an HTTP server at a specified address and port.
    """

    def __init__(self, server_address: tuple, path_to_download: string):
        """
        :param server_address: (ip, port) address on which the server will be started
        :param path_to_download: the path where the images will be downloaded
        """
        signal.signal(signal.SIGINT, signal_handler)
        self.server_address = server_address
        self.path_to_download = path_to_download

    def start_server(self):
        """
        Starts the HTTP server and begins listening for incoming connections.
        """
        with socket.create_server(self.server_address) as sock:
            sock.settimeout(SOCKET_TIMEOUT)
            while not exit_event.is_set():
                try:
                    connect, client_address = sock.accept()
                    self._receive_connection(connect, client_address)
                except socket.timeout:
                    pass
            else:
                print('Exit from program...')

    def _receive_connection(self, sock: socket,
                            client_address: socket) -> None:
        """
        Gets the URL from the established connection.
        :param sock: the socket with an established connection
        :param client_address: the client address
        """

        while True:
            try:
                data = sock.recv(BUFFER_VALUE)
                print(f'Connected: {client_address}')

                if not data:
                    print(f'No data from:{client_address}')
                    break

                print(f'Data received from: {client_address}')
                encoding = chardet.detect(data)['encoding']
                decoded_data = data.decode(encoding).split(';')

                if decoded_data[0] == 'image_downloader':
                    self._image_downloader_process(decoded_data[1], sock)
                elif decoded_data[0] == 'adblocker':
                    self._adblocker_process(decoded_data[1], sock)
                elif decoded_data[0] == 'vk_downloader':
                    self._vk_downloader_process(
                        decoded_data[1],
                        decoded_data[2],
                        sock
                    )

            except ConnectionResetError as ex:
                logging.warning(ex)
                break
            except ConnectionAbortedError as ex:
                logging.warning(ex)
                break
            except Exception as ex:
                logging.warning(ex)

    def _image_downloader_process(self, data, sock):
        """
        Processes a URL containing links to images and downloads those images.
        :param data: The URL with the images.
        :param sock: The socket with the established connection.
        """
        image_downloader = ImageDownloader(data, self.path_to_download)
        image_downloader.download_images(sock)
        sock.sendall(
            f'\nDownloaded {image_downloader.total_downloaded}'
            f' pictures from {data}'.encode()
        )

    @staticmethod
    def _adblocker_process(data, sock):
        """
        Removes ads from HTML code located at the specified URL.
        :param data: The URL with HTML code containing ads.
        :param sock: The socket with the established connection.
        """
        easy_list_regex = EasyListRegex()
        html_without_ads = easy_list_regex.process(data)
        sock.sendall(html_without_ads.encode())

    def _vk_downloader_process(self, token, album_title, sock):
        """
        Processes a URL containing a VKontakte token and album name and downloads images from the album.
        :param token: VKontakte token.
        :param album_title: VKontakte album name.
        :param sock: The socket with the established connection.
        """
        try:
            vk_worker = VKPhotoWorker(token)
            dict_titles = vk_worker.request_albums_list()
            photo_urls = None

            for title in dict_titles:
                if title == album_title:
                    photo_urls = vk_worker.request_photos_from_album(
                        dict_titles[title])
                    break
            image_downloader = ImageDownloader("", self.path_to_download)

            if photo_urls:
                for url in photo_urls:
                    image_downloader.download(url, sock)
        except VKException as ex:
            sock.sendall(ex.message.encode())
            logging.warning(ex)


def main():
    """
    The main function for starting the HTTP server.
    """
    parser = create_parser()
    args = parser.parse_args()
    server_address = ('localhost', args.port)
    server = ServerHTTP(server_address, args.path)
    server.start_server()


if __name__ == '__main__':
    main()
