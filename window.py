from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QTableWidget,
    QHeaderView,
    QPushButton
)

import filesystem

MODS_DIR = "/home/bogdan/Documents/Projects/mod-manager-py/test/mods_2"
GAME_DIR = "/home/bogdan/.local/share/Steam/steamapps/common/Skyrim Special Edition"
MOUNT_DIR = "test/mount"
PRIORITY_FILE = "profile/mods_priority.txt"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mod Manager Py")
        self.setGeometry(100, 100, 1600, 900)

        main_layout = QVBoxLayout()

        # NAV LAYOUT START
        nav_layout = QHBoxLayout()

        install_button = QPushButton("Install Mod")
        nav_layout.addWidget(install_button)

        mount_button = QPushButton("Mount")
        mount_button.clicked.connect(lambda: filesystem.mount_mods(MODS_DIR, GAME_DIR, MOUNT_DIR, PRIORITY_FILE))
        nav_layout.addWidget(mount_button)

        unmount_button = QPushButton("Unmount")
        unmount_button.clicked.connect(lambda: filesystem.unmount_mods(MOUNT_DIR))
        nav_layout.addWidget(unmount_button)

        start_button = QPushButton("Start Game")
        nav_layout.addWidget(start_button)

        main_layout.addLayout(nav_layout)
        # NAV LAYOUT END

        content_layout = QHBoxLayout()

        # LEFT CONTENT LAYOUT START
        left_layout = QVBoxLayout()

        mods_table = QTableWidget()
        mods_table.setEditTriggers(QTableWidget.NoEditTriggers)
        mods_table.setSelectionBehavior(QTableWidget.SelectRows)
        mods_table.setSelectionMode(QTableWidget.SingleSelection)
        mods_table.setColumnCount(3)
        mods_table_headers = ['Name', 'Version', 'Priority']
        mods_table.setHorizontalHeaderLabels(mods_table_headers)
        mods_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        mods_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        mods_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        left_layout.addWidget(mods_table)

        content_layout.addLayout(left_layout)
        # LEFT CONTENT LAYOUT END

        # RIGHT CONTENT LAYOUT START
        right_layout = QVBoxLayout()

        esp_table = QTableWidget()
        esp_table.setEditTriggers(QTableWidget.NoEditTriggers)
        esp_table.setSelectionBehavior(QTableWidget.SelectRows)
        esp_table.setSelectionMode(QTableWidget.SingleSelection)
        right_layout.addWidget(esp_table)

        content_layout.addLayout(right_layout)
        # RIGHT CONTENT LAYOUT END

        main_layout.addLayout(content_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

