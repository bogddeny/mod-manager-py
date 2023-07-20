import sys
import time

from PySide6.QtWidgets import QApplication

import filesystem
import window

LOG_DEBUG = True
MODS_DIR = "test/mods"
GAME_DIR = "test/game"
MOUNT_DIR = "test/mount"
PRIORITY_FILE = "profile/mods_priority.txt"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window.MainWindow()
    win.show()
    app.aboutToQuit.connect(print("handle about to quit later"));
    sys.exit(app.exec())
    #filesystem.mount_mods(MODS_DIR, GAME_DIR, MOUNT_DIR, PRIORITY_FILE)
    #time.sleep(30)
    #filesystem.unmount_mods(MOUNT_DIR)
