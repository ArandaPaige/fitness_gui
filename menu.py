from functools import partial
import sys

from user import User

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class GUIManager(QWidget):
    '''Main GUI'''

    def __init__(self, app):
        '''Initialize'''
        super().__init__()
        self.main_menu = MainMenu(self)
        self.app = app
        self.active_window = self.main_menu
        self.active_window.show()
        sys.exit(self.app.exec())


class MainMenu(QWidget):
    '''Main menu'''

    def __init__(self, master, user=None):
        '''Initialize'''
        super().__init__()
        self.master = master
        self.user = user
        # Window Properties
        self.setWindowTitle("Main Menu")
        self.setBaseSize(450, 450)
        self.user_layout = UserLayout(self)
        self.setLayout(self.user_layout)
        self.show()

    def new_user_layout(self):
        pass

    def existing_user_layout(self):
        pass

    def change_layout(self, layout):
        self.setLayout(layout)


class UserLayout(QLayout):

    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.layout = QVBoxLayout(self.parent)
        self.user_name = QLineEdit(self.parent)
        self.user_weight = QLineEdit(self.parent)
        self.user_height = QLineEdit(self.parent)
        self.generate_layout()

    def user_name_properties(self):
        self.user_name.setReadOnly(True)

    def user_weight_properties(self):
        self.user_weight.setReadOnly(True)

    def user_height_properties(self):
        self.user_height.setReadOnly(True)

    def user_graph_properties(self):
        pass

    def generate_layout(self):
        self.layout.addWidget(self.user_name)
        self.layout.addWidget(self.user_weight)
        self.layout.addWidget(self.user_height)


class NewUserLayout(QLayout):

    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.layout = QVBoxLayout
        self.menu()

    def name_edit(self):
        name = QLineEdit(self.parent)
        name.setPlaceholderText('Name')
        name.editingFinished.connect(partial(self.user_setup, name=name))
        return name

    def starting_weight_edit(self):
        starting_weight = QLineEdit(self.parent)
        starting_weight.setPlaceholderText('Starting Weight')
        validator = QDoubleValidator(50, 999, 2, starting_weight)
        starting_weight.setValidator(validator)
        starting_weight.editingFinished.connect(partial(self.user_setup, starting_weight=starting_weight))
        return starting_weight

    def current_weight_edit(self):
        current_weight = QLineEdit(self.parent)
        current_weight.setPlaceholderText('Current Weight')
        validator = QDoubleValidator(50, 99, 2, current_weight)
        current_weight.setValidator(validator)
        current_weight.editingFinished.connect(partial(self.user_setup, current_weight=current_weight))
        return current_weight

    def height_edit(self):
        height = QLineEdit(self.parent)
        height.setPlaceholderText('Height')
        validator = QDoubleValidator(2, 9, 2, height)
        height.setValidator(validator)
        height.editingFinished.connect(partial(self.user_setup, height=height))
        return height

    def confirm_button(self):
        confirm = QPushButton('Confirm', self.parent)
        confirm.setFixedHeight(35)
        confirm.clicked.connect(partial(self.confirm_transition))
        return confirm

    def cancel_button(self):
        cancel = QPushButton('Cancel', self.parent)
        cancel.setFixedHeight(35)
        cancel.clicked.connect(self.cancel_transition)
        return cancel

    def confirm_transition(self):
        self.master.set_active_window(self.master.main_menu)

    def cancel_transition(self):
        self.master.set_active_window(self.master.user_selection_menu)

    def menu(self):
        name = self.name_edit()
        starting_weight = self.starting_weight_edit()
        current_weight = self.current_weight_edit()
        height = self.height_edit()
        confirm = self.confirm_button()
        cancel = self.cancel_button()
        # arranges the widgets in the menu layout
        self.layout.addWidget(name, 1, 0)
        self.layout.addWidget(starting_weight, 2, 0)
        self.layout.addWidget(current_weight, 3, 0)
        self.layout.addWidget(height, 4, 0)
        self.layout.addWidget(confirm, 5, 0, Qt.Alignment.AlignRight)
        self.layout.addWidget(cancel, 5, 1, Qt.Alignment.AlignRight)
