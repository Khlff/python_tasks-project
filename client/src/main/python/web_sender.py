import socket
import threading
import queue

MAX_BUFFER = 20


class WebSender:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.message_buffer = queue.Queue(maxsize=MAX_BUFFER)
        self.thread = threading.Thread(target=self._recv_thread)
        self.thread.setDaemon(True)
        self.thread.start()

    def __del__(self):
        self.sock.close()

    def _recv_thread(self):
        while True:
            data = self.sock.recv(1024)
            if data:
                self.message_buffer.put(data.decode())

    def send_message(self, message: str):
        encoded_message = message.encode()
        self.sock.sendall(encoded_message)

    def get_log(self) -> str:
        if not self.message_buffer.empty():
            return self.message_buffer.get()
        else:
            return ''
