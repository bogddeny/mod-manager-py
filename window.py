from PySide6.QtWidgets import QMainWindow, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mod Manager Py")
        self.setGeometry(100, 100, 1600, 900)

        label = QLabel("Hello PySide6!")

        self.setCentralWidget(label)
