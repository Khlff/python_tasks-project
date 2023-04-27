import sys

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox, QTextEdit,
)

from web_sender import WebSender


class ServerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Images Downloader Client')
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.url_label = QLabel('Site URL:')
        self.grid.addWidget(self.url_label, 0, 0)
        self.url_input = QLineEdit()
        self.grid.addWidget(self.url_input, 0, 1)

        self.address_label = QLabel('Server IP:')
        self.grid.addWidget(self.address_label, 1, 0)
        self.address_input = QLineEdit('127.0.0.1')
        self.grid.addWidget(self.address_input, 1, 1)

        self.port_label = QLabel('Server Port:')
        self.grid.addWidget(self.port_label, 2, 0)
        self.port_input = QLineEdit('8080')
        self.grid.addWidget(self.port_input, 2, 1)

        self.start_button = QPushButton('Download')
        self.grid.addWidget(self.start_button, 3, 0, 1, 2)
        self.start_button.clicked.connect(self.start_client)

        self.response_label = QLabel('Log:')
        self.grid.addWidget(self.response_label, 4, 0)
        self.response_field = QTextEdit()
        self.response_field.setReadOnly(True)
        self.grid.addWidget(self.response_field, 5, 0, 1, 3)

        self.show()

        self.sender = None

    def check_input(self) -> bool:
        """
        Checks whether the gui fields are filled in
        @return: True if the gui fields are filled correctly
        """
        if not self.url_input.text():
            self._print_error('Site URL cannot be empty.')
            return False

        if not int(self.port_input.text()):
            self._print_error('Port cannot be empty.')
            return False

        if not self.address_input.text():
            self._print_error('IP cannot be empty.')
            return False

        return True

    def _print_log(self, text: str):
        """
        Outputs a string in the log field
        @param: string to print
        """
        cursor = self.response_field.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text + '\n')
        self.response_field.setTextCursor(cursor)
        self.response_field.ensureCursorVisible()

    def _print_error(self, message: str):
        """
         Outputs a error box
         @param: error message
         """
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Warning)
        error_box.setWindowTitle('Error')
        error_box.setText(message)
        error_box.exec_()

    def _print_status(self, message: str):
        """
         Outputs a status box
         @param: status message
         """
        error_box = QMessageBox()
        error_box.setWindowTitle('')
        error_box.setText(message)
        error_box.exec_()

    def start_client(self):
        """
        The function that starts after pressing the Start button
        """
        if not self.check_input():
            return

        self.sender = WebSender(
            self.address_input.text(),
            int(self.port_input.text())
        )
        self._print_status('Download started')
        self.sender.send_message(self.url_input.text())
        answer = self.sender.get_log()
        while not answer:
            answer = self.sender.get_log()
        self._print_log(answer)
        self._print_status('Successful download')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ServerGUI()
    sys.exit(app.exec_())
