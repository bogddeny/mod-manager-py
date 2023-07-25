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


def get_page(installer, options=None):
    try:
        if options is not None:
            page = installer.next(options)
        else:
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


def print_selected_options(options):
    for option in options:
        print(option.name)


class FomodDialog(QDialog):
    def __init__(self, path: str):
        super().__init__()
        self.setGeometry(0, 0, 800, 450)
        main_layout = QVBoxLayout()
        self.selected_options = []

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
        next_button.clicked.connect(lambda: self.get_next_page_layout(self.installer, True))
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: print_selected_options(self.selected_options))
        controls_layout.addWidget(previous_button)
        controls_layout.addWidget(next_button)
        controls_layout.addWidget(cancel_button)

        self.setLayout(main_layout)

        self.installer = None

        self.initialize_installer(path)

        self.get_next_page_layout(self.installer)

    def initialize_installer(self, path):
        root = pyfomod.parse(path)
        self.installer = pyfomod.Installer(root, path)

    def get_next_page_layout(self, installer, reset=False):
        if reset:
            while self.content_right_layout.count():
                item = self.content_right_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    self.content_right_layout.removeWidget(widget)
                    widget.deleteLater()
        page = get_page(installer, options=self.selected_options)
        groups = get_groups(page)

        scroll_area = QScrollArea()
        page_widget = QWidget(scroll_area)
        scroll_area.setWidget(page_widget)
        scroll_area.setWidgetResizable(True)
        content_layout = QVBoxLayout(page_widget)
        self.content_right_layout.addWidget(scroll_area)

        self.group_selected = []

        for group in groups:
            options = get_options(group)
            group_label = QLabel("----- " + group.name + " -----" + str(group.type))
            content_layout.addWidget(group_label)

            if group.type is pyfomod.GroupType.ALL:
                layout = self.create_all_button_layout(options)
                content_layout.addLayout(layout)

            elif group.type is pyfomod.GroupType.ANY:
                layout = self.create_any_least_button_layout(options)
                content_layout.addLayout(layout)

            elif group.type is pyfomod.GroupType.ATLEASTONE:
                layout = self.create_any_least_button_layout(options)
                content_layout.addLayout(layout)

            elif group.type is pyfomod.GroupType.ATMOSTONE:
                layout = self.create_most_button_layout(options)
                content_layout.addLayout(layout)

            elif group.type is pyfomod.GroupType.EXACTLYONE:
                layout = self.create_exact_button_layout(options)
                content_layout.addLayout(layout)

            else:
                logger.log.error("Invalid fomod GroupType")
        return scroll_area

    def create_all_button_layout(self, options):
        layout = QVBoxLayout()
        button_group = QButtonGroup(layout)
        button_group.setExclusive(False)

        for option in options:
            button = QCheckBox(option.name)
            button.setToolTip(option.description)
            button.setChecked(True)
            button.setEnabled(False)
            button_group.addButton(button)
            layout.addWidget(button)
            self.add_selected_option(option)
        return layout

    def create_any_least_button_layout(self, options):
        layout = QVBoxLayout()
        button_group = QButtonGroup(layout)
        button_group.setExclusive(False)

        for option in options:
            button = QCheckBox(option.name)
            button.setToolTip(option.description)
            button.clicked.connect(lambda check=False, opt=option: self.toggle_selected_option(opt))
            button_group.addButton(button)
            layout.addWidget(button)
        return layout

    def create_most_button_layout(self, options):
        layout = QVBoxLayout()
        button_group = QButtonGroup(layout)

        for option in options:
            button = QRadioButton(option.name)
            button.setToolTip(option.description)
            button.clicked.connect(lambda checked=False, grp_opt=self.group_selected, opt=option: self.handle_selection(grp_opt, opt))
            button_group.addButton(button)
            layout.addWidget(button)
        button_none = QRadioButton("None")
        button_none.toggle()
        button_none.clicked.connect(lambda checked=False, grp_opt=self.group_selected: self.clear_selection(grp_opt))
        button_group.addButton(button_none)
        layout.addWidget(button_none)
        return layout

    def create_exact_button_layout(self, options):
        layout = QVBoxLayout()
        button_group = QButtonGroup(layout)
        id = 0
        for option in options:
            button = QRadioButton(option.name)
            button.setToolTip(option.description)
            button.toggled.connect(lambda checked=False, grp_opt=self.group_selected, opt=option: self.handle_selection(grp_opt, opt))
            button_group.addButton(button)
            if id == 0:
                button.toggle()
            id += 1
            layout.addWidget(button)
        return layout

    def handle_selection(self, group_options, option):
        if len(group_options) == 0:
            group_options.append(option)
            self.selected_options.append(option)
        else:
            self.selected_options.remove(group_options[0])
            group_options.clear()
            group_options.append(option)
            self.selected_options.append(option)

    def clear_selection(self, grp_opt):
        self.selected_options.remove(grp_opt[0])
        grp_opt.clear()

    def add_selected_option(self, option):
        if option not in self.selected_options:
            self.selected_options.append(option)

    def toggle_selected_option(self, option):
        if option in self.selected_options:
            self.selected_options.remove(option)
        else:
            self.selected_options.append(option)







































