from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
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
        self.setWindowTitle("Mod Manager Linux")
        self.setGeometry(100, 100, 1600, 900)

        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        install_button = QPushButton("Install Mod")
        install_button.clicked.connect(self.start_mod_installation)
        button_layout.addWidget(install_button)

        start_button = QPushButton("Start Game")
        button_layout.addWidget(start_button)

        mount_button = QPushButton("Mount")
        mount_button.clicked.connect(lambda: filesystem.mount_mods(MODS_DIR, GAME_DIR, MOUNT_DIR, PRIORITY_FILE))
        button_layout.addWidget(mount_button)

        unmount_button = QPushButton("Unmount")
        unmount_button.clicked.connect(lambda: filesystem.unmount_mods(MOUNT_DIR))
        button_layout.addWidget(unmount_button)

        main_layout.addLayout(button_layout)

        tables_layout = QHBoxLayout()

        mods_table = QTableWidget()
        mods_table.setEditTriggers(QTableWidget.NoEditTriggers)
        mods_table.setSelectionBehavior(QTableWidget.SelectRows)
        mods_table.setSelectionMode(QTableWidget.SingleSelection)
        mods_table.setColumnCount(2)
        mods_table_headers = ['Name', 'Priority']
        mods_table.setHorizontalHeaderLabels(mods_table_headers)
        mods_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        mods_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        tables_layout.addWidget(mods_table)

        plugin_table = QTableWidget()
        plugin_table.setEditTriggers(QTableWidget.NoEditTriggers)
        plugin_table.setSelectionBehavior(QTableWidget.SelectRows)
        plugin_table.setSelectionMode(QTableWidget.SingleSelection)

        tables_layout.addWidget(plugin_table)

        main_layout.addLayout(tables_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def start_mod_installation(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Mod File", "", "All Files (*)", options=options)
        extract_to = "/home/bogdan/Documents/Projects/mod-manager-py/.temp"

        if file_path:
            print("Selected File: ", file_path)
            filesystem.extract(file_path, extract_to)

