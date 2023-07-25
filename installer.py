from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QWidget,
    QRadioButton,
    QCheckBox,
    QButtonGroup,
    QFrame
)

from PySide6.QtCore import Qt

import pyfomod
import logger


def initialize_installer(path):
    root = pyfomod.parse(path)
    installer = pyfomod.Installer(root, path)
    return installer


def get_page(installer, options, previous=False):
    try:
        if previous:
            page = installer.previous()
        else:
            print_selected_options(options)
            page = installer.next(options)
        if page is None:
            logger.log.debug("Installer Finished")
        else:
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


def print_selected_options(options):
    for option in options:
        print(option.name)


class InstallerDialog(QDialog):
    def __init__(self, path: str):
        super().__init__()
        self.setGeometry(0, 0, 1000, 600)
        self.selected_options = []

        main_layout = QVBoxLayout()

        installer = initialize_installer(path)

        # Top Bar Layout
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)
        name_label = QLabel("Mod Name")
        name_line_edit = QLineEdit()
        top_layout.addWidget(name_label)
        top_layout.addWidget(name_line_edit)

        # Main Content Layout
        center_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)

        self.center_left_layout = QVBoxLayout()
        center_layout.addLayout(self.center_left_layout)
        label = QLabel("Label")
        self.center_left_layout.addWidget(label)

        self.center_right_layout = QVBoxLayout()
        center_layout.addLayout(self.center_right_layout)

        # Bottom Bar Layout
        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)
        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(lambda: print_selected_options(self.selected_options))
        bottom_layout.addWidget(button_cancel)
        button_previous = QPushButton("Previous")
        button_previous.clicked.connect(lambda: print(installer.files()))
        bottom_layout.addWidget(button_previous)
        button_next = QPushButton("Next")
        button_next.clicked.connect(lambda: self.next_page_layout(installer, self.selected_options))
        bottom_layout.addWidget(button_next)

        self.setLayout(main_layout)

        self.next_page_layout(installer, self.selected_options)

    def next_page_layout(self, installer, options):
        self.selected_options = []
        if options is not None:
            while self.center_right_layout.count():
                item = self.center_right_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    self.center_right_layout.removeWidget(widget)
                    widget.deleteLater()

        page = get_page(installer, options)

        print(options)

        scroll_area = QScrollArea()
        page_widget = QWidget(scroll_area)
        scroll_area.setWidget(page_widget)
        scroll_area.setWidgetResizable(True)
        page_layout = QVBoxLayout(page_widget)
        page_layout.setAlignment(Qt.AlignVCenter)
        self.center_right_layout.addWidget(scroll_area)

        if page is None:
            print(installer.files())
            finished_label = QLabel("Finished!")
            page_layout.addWidget(finished_label)
            return

        groups = get_groups(page)

        for group in groups:
            group_layout = QVBoxLayout()
            group_layout.setAlignment(Qt.AlignTop)
            group_frame = QFrame()
            group_frame.setLayout(group_layout)
            group_frame.setFrameShape(QFrame.StyledPanel)
            group_frame.setFrameShadow(QFrame.Plain)

            group_label = QLabel(group.name)
            group_layout.addWidget(group_label)

            button_group = QButtonGroup()
            button_group.setExclusive(False)
            if group.type is pyfomod.GroupType.ATMOSTONE or group.type is pyfomod.GroupType.EXACTLYONE:
                button_group.setExclusive(True)

            options = get_options(group)

            group_selected = []

            id = 0

            for option in options:
                if group.type is pyfomod.GroupType.ALL:
                    button = QCheckBox(option.name)
                    button.setToolTip(option.description)
                    button.setChecked(True)
                    button.setEnabled(False)
                    button_group.addButton(button)
                    group_layout.addWidget(button)
                    self.add_option(option)
                elif group.type is pyfomod.GroupType.ANY:
                    button = QCheckBox(option.name)
                    button.setToolTip(option.description)
                    button.clicked.connect(lambda check=False, opt=option: self.toggle_option(opt))
                    button_group.addButton(button)
                    group_layout.addWidget(button)
                elif group.type is pyfomod.GroupType.ATLEASTONE:
                    button = QCheckBox(option.name)
                    button.setToolTip(option.description)
                    button.clicked.connect(lambda check=False, opt=option: self.toggle_option(opt))
                    button_group.addButton(button)
                    group_layout.addWidget(button)
                elif group.type is pyfomod.GroupType.ATMOSTONE:
                    button = QRadioButton(option.name)
                    button.setToolTip(option.description)
                    button.toggled.connect(lambda checked=False, grp_opt=group_selected, opt=option: self.exclusive_option(grp_opt, opt))
                    button_group.addButton(button)
                    group_layout.addWidget(button)
                elif group.type is pyfomod.GroupType.EXACTLYONE:
                    button = QRadioButton(option.name)
                    button.setToolTip(option.description)
                    button.toggled.connect(lambda checked=False, grp_opt=group_selected, opt=option: self.exclusive_option(grp_opt, opt))
                    button_group.addButton(button)
                    if id == 0:
                        button.toggle()
                    id += 1
                    group_layout.addWidget(button)
                else:
                    logger.log.error("Invalid fomod GroupType")

            if group.type is pyfomod.GroupType.ATMOSTONE:
                button_none = QRadioButton("None")
                button_none.toggle()
                button_none.clicked.connect(lambda checked=False, grp_opt=group_selected: self.clear_group_selected(grp_opt))
                button_group.addButton(button_none)
                group_layout.addWidget(button_none)

            page_layout.addWidget(group_frame)

    def clear_group_selected(self, group_selected):
        if len(group_selected) > 0:
            self.remove_option(group_selected[0])
            group_selected.clear()

    def add_option(self, option):
        if option not in self.selected_options:
            self.selected_options.append(option)
        else:
            logger.log.error(f"Option {option.name} already exists in selected options table")

    def remove_option(self, option):
        if option in self.selected_options:
            self.selected_options.remove(option)
        else:
            logger.log.error(f"Option {option.name} does not exist in selected options table")

    def toggle_option(self, option):
        if option in self.selected_options:
            self.selected_options.remove(option)
        else:
            self.selected_options.append(option)

    def exclusive_option(self, group_selected, option):
        if len(group_selected) == 0:
            group_selected.append(option)
            self.add_option(option)
        else:
            self.remove_option(group_selected[0])
            group_selected.clear()
            self.add_option(option)
            group_selected.append(option)
