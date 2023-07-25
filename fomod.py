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
    QButtonGroup
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

        self.content_left_layout = QVBoxLayout()
        content_layout.addLayout(self.content_left_layout)

        self.content_right_layout = QVBoxLayout()
        content_layout.addLayout(self.content_right_layout)

        controls_layout = QHBoxLayout()
        main_layout.addLayout(controls_layout)
        previous_button = QPushButton("Previous")
        next_button = QPushButton("Next")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: print(self.selected_options))
        controls_layout.addWidget(previous_button)
        controls_layout.addWidget(next_button)
        controls_layout.addWidget(cancel_button)

        self.setLayout(main_layout)

        self.installer = None
        self.selected_options = []

        self.initialize_installer(path)

        self.get_next_page_layout(self.installer)

    def initialize_installer(self, path):
        root = pyfomod.parse(path)
        self.installer = pyfomod.Installer(root, path)

    def get_next_page_layout(self, installer):
        page = get_page(installer)
        groups = get_groups(page)

        scroll_area = QScrollArea()
        page_widget = QWidget(scroll_area)
        scroll_area.setWidget(page_widget)
        scroll_area.setWidgetResizable(True)
        content_layout = QVBoxLayout(page_widget)
        self.content_right_layout.addWidget(scroll_area)

        for group in groups:
            label = QLabel("----- " + group.name + " -----")
            content_layout.addWidget(label)
            local_layout = QVBoxLayout()
            group_atmostone_selected = []
            button_group_most = QButtonGroup()

            options = get_options(group)
            for option in options:
                if group.type is pyfomod.GroupType.ALL:
                    button = QCheckBox(option.name + " all")
                    button.setToolTip(option.description)
                    button.setChecked(True)
                    button.setEnabled(False)
                    local_layout.addWidget(button)
                    self.add_selected_option(option)

                if group.type is pyfomod.GroupType.ANY:
                    button = QCheckBox(option.name + " any")
                    button.setToolTip(option.description)
                    local_layout.addWidget(button)
                    button.clicked.connect(lambda checked=False, opt=option: self.toggle_selected_option(opt))

                if group.type is pyfomod.GroupType.ATLEASTONE:
                    button = QCheckBox(option.name + " at least one")
                    button.setToolTip(option.description)
                    local_layout.addWidget(button)
                    button.clicked.connect(lambda checked=False, opt=option: self.toggle_selected_option(opt))

                if group.type is pyfomod.GroupType.ATMOSTONE:
                    button = QRadioButton(option.name + " at most one")
                    button.setToolTip(option.description)
                    button_group_most.addButton(button)
                    local_layout.addWidget(button)
                    button.clicked.connect(lambda checked=False, opt=option: self.handle_atmostone_selection(group_atmostone_selected, opt))

                if group.type is pyfomod.GroupType.EXACTLYONE:
                    button_group = QButtonGroup()
                    button = QRadioButton(option.name + " exactly one")
                    button.setToolTip(option.description)
                    button_group.addButton(button)
                    local_layout.addWidget(button)

            if group.type is pyfomod.GroupType.ATMOSTONE:
                button_none = QRadioButton("None")
                button_group_most.addButton(button_none)
                local_layout.addWidget(button_none)
                button_none.clicked.connect(lambda: self.clear_selection(group_atmostone_selected))

            content_layout.addLayout(local_layout)

    def handle_atmostone_selection(self, group_selected_options, option):
        if not group_selected_options:
            self.selected_options.append(option)
            group_selected_options.append(option)
        else:
            self.selected_options.remove(group_selected_options[0])
            group_selected_options.clear()
            self.selected_options.append(option)
            group_selected_options.append(option)

    def clear_selection(self, group_selected_options):
        self.selected_options.remove(group_selected_options[0])
        group_selected_options.clear()

    def add_selected_option(self, option):
        if option not in self.selected_options:
            self.selected_options.append(option)

    def toggle_selected_option(self, option):
        if option in self.selected_options:
            self.selected_options.remove(option)
        else:
            self.selected_options.append(option)







































