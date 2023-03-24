import socket


def create_socket(host, port, message):
    sock = socket.socket()
    sock.connect((host, port))
    send_message(sock, message)
    data = receive_answer(sock)
    sock.close()
    return data


def send_message(sock, message):
    encoded_message = message.encode() + b'\r\n'
    sock.send(encoded_message)


def receive_answer(sock):
    data = sock.recv(1000).decode()
    return data


def main():
    host = 'localhost'
    port = 8080
    message = 'Hello, world'
    server_answer = create_socket(host, port, message)
    print(server_answer)


if __name__ == '__main__':
    main()
