import socket

HOST = 'localhost'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)
    s.connect((HOST, PORT))
    message = "vk1.a.DvFHjnmnOld1eXXS1xU4NF74q1_uZbQCZKJ_xYgkHAaMCGPN_YKSOTd9ovu2pcM_2AXEe85aCH9ES_00ybXdXstcbW2HxBXCfiEvxBCX-anndoy0hwY-y-CUPVcejAz7Ys-HWGyZ21OReI7d-902miHKJFNbCnqORdzKRdyW5x690-BWT8mPWO5RGDEuBJPszGUsWimT2oovbgOP-fHmPg;Kolya Fura"
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
