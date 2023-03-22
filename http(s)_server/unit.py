import socket
import unittest
import server


class MyTestCase(unittest.TestCase):
    def test_correct(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 8081))
        message = "Hello world!"
        s.send(bytes(message, 'utf-8') + b'\r\n')
        msg = s.recv(server.BUFFER_VALUE).decode()
        s.close()
        self.assertEqual(msg, message.upper() + '\r\n',
                         "Некорректная работа сервера!")


if __name__ == '__main__':
    unittest.main()
