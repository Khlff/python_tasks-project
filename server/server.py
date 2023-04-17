import argparse
import os
import signal
import socket
import string
import sys
from threading import Event

import chardet

from http_server.server.images_downloader import ImageDownloader

exit_event = Event()
BUFFER_VALUE = 1024
SOCKET_TIMEOUT = 0.1


def signal_handler(_signal: signal, _) -> None:
    """
    Set global variable Event into True
    """
    exit_event.set()


def receive_connection(connect: socket,
                       client_address: socket,
                       path_to_download: string) -> None:
    """
    Gets the url from the established connection and downloads all the images from it
    :param connect: socket with an established connection
    :param client_address: client address
    :param path_to_download: the path where the images will be downloaded
    """
    while True:
        try:
            data = connect.recv(BUFFER_VALUE)
            print(f'Connected: {client_address}')

            if not data:
                print(f'No data from:{client_address}')
                break

            print(f'Data received from: {client_address}')
            encoding = chardet.detect(data)['encoding']
            decoded_url = data.decode(encoding)
            image_downloader = ImageDownloader(
                decoded_url, path_to_download, connect
            )
            image_downloader.download_images()

            connect.sendall('Successful download'.encode())
        except socket.timeout:
            pass


def start_server(server_port: int, path_to_download: string):
    """
    Starts the server
    :param server_port: port on which the server will be started
    :param path_to_download: the path where the images will be downloaded
    """

    signal.signal(signal.SIGINT, signal_handler)

    server_address = ('localhost', server_port)
    with socket.create_server(server_address) as sock:
        sock.settimeout(SOCKET_TIMEOUT)
        while not exit_event.is_set():
            try:
                connect, client_address = sock.accept()
                receive_connection(connect, client_address, path_to_download)
            except socket.timeout:
                pass
        else:
            print('Exit from program...')


def create_parser() -> argparse.ArgumentParser:
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} PATH [--port] [-h]',
        description='It`s server that accepts the url to the site '
                    'in any encoding and saves all images from it.',
    )

    parser.add_argument(
        '--port',
        '--port',
        type=int,
        default=8080,
        help='The port on which the server will start. '
             '(8080 by default)',
    )
    parser.add_argument('-path',
                        '-PATH',
                        type=str,
                        help='The path where the images will be saved',
                        )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    start_server(args.port, args.path)


if __name__ == '__main__':
    main()
