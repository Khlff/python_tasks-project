import socket


class Client:
    HOST = 'localhost'
    PORT = 8080

    @staticmethod
    def get_parameters() -> None:
        """
        Gets parameters from the console from the use.
        """
        global mode, url, token, album_title
        mode = input("Режимы работы:\n1. image_downloader\n2. adblocker\n3. vk_downloader\nВыберите режим работы(число): ")

        if mode == '1':
            mode = "image_downloader"
            url = input("Введите url с которого будут скачаны изображения: ")
        elif mode == '2':
            mode = "adblocker"
            url = input("Введите url с которого нужно убрать рекламу: ")
        elif mode == '3':
            mode = "vk_downloader"
            token = input("Введите токен авторизации: ")
            album_title = input("Введите название альбома: ")

    def main(self) -> None:
        """
        Starts client.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((self.HOST, self.PORT))
            if mode == 'vk_downloader':
                message = f"{mode};{token};{album_title}"
            else:
                message = f"{mode};{url}"
            s.sendall(message.encode())
            if mode == 'adblocker':
                with open("file.html", 'w', encoding='utf-8') as f:
                    while True:
                        try:
                            data = s.recv(1024)
                            if not data:
                                raise socket.timeout()
                            f.write(data.decode('utf-8', errors='ignore'))
                        except socket.timeout:
                            s.close()
                            print("Файл без рекламы загружен.")
                            break
            else:
                while True:
                    try:
                        data = s.recv(1024)
                        if not data:
                            raise socket.timeout()
                        print(data)
                    except socket.timeout:
                        s.close()
                        break


if __name__ == '__main__':
    client = Client()
    Client.get_parameters()
    client.main()
