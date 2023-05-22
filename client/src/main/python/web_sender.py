import socket
import threading
import queue
from typing import Optional

from PyQt5.QtCore import QThread

MAX_BUFFER = 20


class WebSender(QThread):
    def __init__(self, ip: str, port: int, log_updated: threading.Event):
        """
        Initialize a WebSender object.

        Args:
            ip (str): The IP address of the server.
            port (int): The port number of the server.
        """
        QThread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.message_buffer = queue.Queue(maxsize=MAX_BUFFER)
        self.thread = threading.Thread(target=self._recv_thread, daemon=True)
        self.thread.start()
        self.log_updated = log_updated
        self.buffer_log = threading.Lock()

    def __del__(self):
        """
        Close the socket when the WebSender object is deleted.
        """
        self.sock.close()

    def _recv_thread(self):
        """
        Internal thread function to receive data from the server and put it into the message buffer.
        """
        while True:
            data = self.sock.recv(1024)
            if data:
                with self.buffer_log:
                    self.message_buffer.put(data.decode())
                self.log_updated.set()

    def send_message(self, message: str):
        """
        Send a message to the server.

        Args:
            message (str): The message to be sent.
        """
        encoded_message = message.encode()
        self.sock.sendall(encoded_message)

    def get_log(self) -> Optional[str]:
        """
        Get the log message from the message buffer.

        Returns:
            str: The log message. Returns None if the message buffer is empty.
        """
        with self.buffer_log:
            if not self.message_buffer.empty():
                return self.message_buffer.get()
