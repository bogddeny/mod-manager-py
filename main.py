import sys

from PySide6.QtWidgets import QApplication

import window

LOG_DEBUG = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window.MainWindow()
    win.show()
    app.aboutToQuit.connect(lambda: print("handle about to quit later"))
    sys.exit(app.exec())
