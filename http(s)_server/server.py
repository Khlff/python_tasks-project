import signal
import socket
import sys
from threading import Event

exit_event = Event()
BUFFER_VALUE = 1024


def signal_handler(signal, frame):
    print('Прерывание.')
    exit_event.set()


def receive_connection(connect, client_address):
    while True:
        try:
            data = connect.recv(BUFFER_VALUE)
            print(f'Подключён: {client_address}')
            if data:
                print(f'Данные получены от: {client_address}')
                temp_data = data.decode('utf-8').upper()
                data = temp_data.encode('utf-8')
                connect.sendall(data)
            else:
                print(f'Нет данных от:{client_address}')
                break
        except socket.timeout:
            pass


def start_server(server_address):
    signal.signal(signal.SIGINT, signal_handler)

    with socket.create_server(server_address) as sock:
        sock.settimeout(0.1)
        while not exit_event.is_set():
            try:
                connect, client_address = sock.accept()
                connect.settimeout(0.1)
                receive_connection(connect, client_address)
            except socket.timeout:
                pass
        else:
            print('Выход из программы...')
            sys.exit(1)


def main():
    server_address = ('localhost', 8081)
    start_server(server_address)


if __name__ == '__main__':
    main()
