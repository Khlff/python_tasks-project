import socket

HOST = 'localhost'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(2)
    s.connect((HOST, PORT))
    message = "https://dvsemenov.ru/peredacha-fajla-cherez-soket-v-python-3/"
    s.sendall(message.encode())
    with open("file.html", 'w', encoding='utf-8') as f:
        while True:
            try:
                data = s.recv(1024)
                if not data:
                    raise socket.timeout()
                f.write(data.decode('utf-8', errors='ignore'))
            except socket.timeout:
                s.close()
                break

    print("Successful!")
