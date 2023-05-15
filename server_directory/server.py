import signal
import socket
import string
from threading import Event

import chardet

from args_parser import create_parser
from images_downloader import ImageDownloader
from constants import SOCKET_TIMEOUT, BUFFER_VALUE
from adblocker import EasyListRegex

exit_event = Event()


def signal_handler(_signal: signal, _) -> None:
    """
    Set global variable Event into True
    """
    exit_event.set()


class ServerHTTP:
    def __init__(self, server_address: tuple, path_to_download: string, operation_mode: string):
        """
        :param server_address: (ip, port) address on which the server will be started
        :param path_to_download: the path where the images will be downloaded
        """

        signal.signal(signal.SIGINT, signal_handler)
        self.server_address = server_address
        self.path_to_download = path_to_download
        self.operation_mode = operation_mode

    def start_server(self):
        """
        Starts the server
        """

        with socket.create_server(self.server_address) as sock:
            sock.settimeout(SOCKET_TIMEOUT)
            while not exit_event.is_set():
                try:
                    connect, client_address = sock.accept()
                    self._receive_connection(connect, client_address)
                except socket.timeout as ex:
                    pass
            else:
                print('Exit from program...')

    def _receive_connection(self, sock: socket,
                            client_address: socket) -> None:
        """
        Gets the url from the established connection and downloads all the images from it
        :param sock: socket with an established connection
        :param client_address: client address
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
                decoded_url = data.decode(encoding)
                if self.operation_mode == 'download':
                    image_downloader = ImageDownloader(
                        decoded_url,
                        self.path_to_download
                    )

                    image_downloader.download_images(sock)

                    sock.sendall(
                        f'\nDownloaded {image_downloader.total_downloaded}'
                        f' pictures from {decoded_url}'.encode()
                    )
                elif self.operation_mode == 'adblocker':
                    easy_list_regex = EasyListRegex()
                    html_without_ads = easy_list_regex.process(decoded_url)
                    sock.sendall(html_without_ads.encode())

            except ConnectionResetError as ex:
                print(ex)
                break
            except ConnectionAbortedError as ex:
                print(ex)
                break


def main():
    parser = create_parser()
    args = parser.parse_args()

    server_address = ('localhost', args.port)
    server = ServerHTTP(server_address, args.path, args.mode)
    server.start_server()


if __name__ == '__main__':
    main()
