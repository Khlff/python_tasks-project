import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
)
from server_directory import server
from PyQt5.QtCore import pyqtSignal, QObject



class ServerGUI(QWidget):
    download_requested = pyqtSignal(str, str, object)
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.setWindowTitle('Images Downloader Server')
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # Create URL input
        self.url_label = QLabel('Site URL:')
        self.grid.addWidget(self.url_label, 0, 0)
        self.url_input = QLineEdit()
        self.grid.addWidget(self.url_input, 0, 1)

        # Create Path input
        self.path_label = QLabel('Path to save images:')
        self.grid.addWidget(self.path_label, 1, 0)
        self.path_input = QLineEdit()
        self.grid.addWidget(self.path_input, 1, 1)

        # Create Port input
        self.port_label = QLabel('Server Port:')
        self.grid.addWidget(self.port_label, 2, 0)
        self.port_input = QLineEdit('8080')
        self.grid.addWidget(self.port_input, 2, 1)

        # Create Start and Stop buttons
        self.start_button = QPushButton('Start Server')
        self.grid.addWidget(self.start_button, 3, 0)
        self.start_button.clicked.connect(self.start_server)

        self.stop_button = QPushButton('Stop Server')
        self.grid.addWidget(self.stop_button, 3, 1)
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setDisabled(True)

        # Show the window
        self.show()

    def start_server(self):
        url = self.url_input.text()
        path = self.path_input.text()
        port = int(self.port_input.text())

        if not url:
            self.show_error_message('Site URL cannot be empty.')
            return

        if not path:
            self.show_error_message('Path to save images cannot be empty.')
            return

        self.server_process = server.start_server(port, path)
        self.start_button.setDisabled(True)
        self.stop_button.setEnabled(True)

    def stop_server(self):
        self.server_process.terminate()
        self.start_button.setEnabled(True)
        self.stop_button.setDisabled(True)

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Warning)
        error_box.setWindowTitle('Error')
        error_box.setText(message)
        error_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ServerGUI()
    sys.exit(app.exec_())
