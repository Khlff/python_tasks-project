import argparse
import os
import signal
import socket
import sys
from threading import Event

import chardet

exit_event = Event()
BUFFER_VALUE = 1024
SOCKET_TIMEOUT = 0.1


def signal_handler(_signal, _):
    """
    Устанавливает глобальную переменную Event в значение true
    """
    exit_event.set()


def receive_connection(connect: socket, client_address: socket):
    """
    Получает данные из установленного соединения и отправляет их обратно в Uppercase
    :param connect: сокет с установленным соединением
    :param client_address: адрес клиента
    """
    while True:
        try:
            data = connect.recv(BUFFER_VALUE)
            print(f'Connected: {client_address}')
            if data:
                print(f'Данные получены от: {client_address}')

                encoding = chardet.detect(data)['encoding']
                decoded_data = data.decode(encoding)

                data = decoded_data.encode('utf-8')
                connect.sendall(data)
            else:
                print(f'Нет данных от:{client_address}')
                break
        except socket.timeout:
            pass


def start_server(server_port: int):
    """
    Запускает сервер с переданным портом
    :param server_port: int(port)
    """

    signal.signal(signal.SIGINT, signal_handler)

    server_address = ('localhost', server_port)
    with socket.create_server(server_address) as sock:
        sock.settimeout(SOCKET_TIMEOUT)
        while not exit_event.is_set():
            try:
                connect, client_address = sock.accept()
                receive_connection(connect, client_address)
            except socket.timeout:
                pass
        else:
            print('Выход из программы...')
            sock.close()
            sys.exit(1)


def create_parser():
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} [--p] [-h]',
        description='It`s server that accepts the url to the site '
                    'in any encoding and saves all images from it.',
    )
    parser.add_argument('--p',
                        '--port', type=int, default=8080,
                        help='The port on which the server will start. '
                             '(8080 by default)',
                        )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    server_port = args.p
    start_server(server_port)


if __name__ == '__main__':
    main()
