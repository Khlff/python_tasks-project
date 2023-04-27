import socket
import threading
import queue

MAX_BUFFER = 20


class WebSender:
    def __init__(self, ip: str, port: int):
        """
        Initialize a WebSender object.

        Args:
            ip (str): The IP address of the server.
            port (int): The port number of the server.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.message_buffer = queue.Queue(maxsize=MAX_BUFFER)
        self.thread = threading.Thread(target=self._recv_thread, daemon=True)
        self.thread.start()

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
                self.message_buffer.put(data.decode())

    def send_message(self, message: str):
        """
        Send a message to the server.

        Args:
            message (str): The message to be sent.
        """
        encoded_message = message.encode()
        self.sock.sendall(encoded_message)

    def get_log(self) -> str:
        """
        Get the log message from the message buffer.

        Returns:
            str: The log message. Returns an empty string if the message buffer is empty.
        """
        if not self.message_buffer.empty():
            return self.message_buffer.get()
        else:
            return ''
