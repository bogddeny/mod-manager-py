from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit
)

import pyfomod
import logger


def get_page(installer):
    try:
        page = installer.next()
        if page is None:
            logger.log.debug("Installer Finished")
        return page

    except pyfomod.FailedCondition as e:
        logger.log.debug(f"Failed Condition: {e}")


def get_groups(page):
    groups = []

    try:
        for group in page:
            groups.append(group)
        return groups

    except pyfomod.FailedCondition as e:
        logger.log.debug(f"Failed Condition: {e}")


def get_options(group):
    options = []

    try:
        for option in group:
            options.append(option)
        return options

    except pyfomod.FailedCondition as e:
        logger.log.debug(f"Failed Condition: {e}")


class FomodDialog(QDialog):
    def __init__(self, path: str):
        super().__init__()
        self.setGeometry(0, 0, 800, 450)
        main_layout = QVBoxLayout()

        top_bar_layout = QHBoxLayout()
        main_layout.addLayout(top_bar_layout)
        name_label = QLabel("Mod Name")
        name_line_edit = QLineEdit()
        top_bar_layout.addWidget(name_label)
        top_bar_layout.addWidget(name_line_edit)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        content_left_layout = QVBoxLayout()
        content_layout.addLayout(content_left_layout)
        left_label = QLabel("left")
        content_left_layout.addWidget(left_label)

        content_right_layout = QVBoxLayout()
        content_layout.addLayout(content_right_layout)
        right_label = QLabel("right")
        content_right_layout.addWidget(right_label)

        controls_layout = QHBoxLayout()
        main_layout.addLayout(controls_layout)
        previous_button = QPushButton("Previous")
        next_button = QPushButton("Next")
        cancel_button = QPushButton("Cancel")
        controls_layout.addWidget(previous_button)
        controls_layout.addWidget(next_button)
        controls_layout.addWidget(cancel_button)

        self.setLayout(main_layout)

        root = pyfomod.parse(path)
        installer = pyfomod.Installer(root, path)
        page = get_page(installer)
        groups = get_groups(page)
        for group in groups:
            options = get_options(group)
            for option in options:
                print("Option:", option.name)
                print("Description:", option.description)
