import socket

HOST = 'localhost'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = "https://habr.com/ru/articles/734486/"
    s.sendall(message.encode())
    with open("file.html", 'w', encoding='utf-8') as f:
        while True:
            data = s.recv(1024)
            if not data:
                s.close()
                break
            print(data)
            f.write(data.decode('utf-8', errors='ignore'))
