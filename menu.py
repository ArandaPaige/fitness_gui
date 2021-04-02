from functools import partial
import sys
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from user import User

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class GUIManager(QWidget):
    '''Main GUI'''

    def __init__(self, app, user=None):
        '''Initialize'''
        super().__init__()
        self.user = user
        self.main_menu = MainMenu(self, self.user)
        self.app = app
        self.active_window = self.main_menu
        self.active_window.show()
        sys.exit(self.app.exec())


class MainMenu(QWidget):
    '''Main menu'''

    def __init__(self, master, user):
        '''Initialize'''
        super().__init__()
        self.master = master
        self.user = user
        # Window Properties
        self.setWindowTitle("Main Menu")
        self.setBaseSize(450, 450)
        self.user_layout = UserLayout(self)
        self.show()

    def check_user_status(self):
        if self.user == None:
            self.new_user_layout()
        else:
            self.existing_user_layout()

    def new_user_layout(self):
        new_user_layout = NewUserLayout(self)
        self.change_layout(new_user_layout)

    def existing_user_layout(self):
        existing_user_layout = UserLayout(self)
        self.change_layout(existing_user_layout)

    def change_layout(self, layout):
        self.setLayout(layout)


class UserLayout(QLayout):

    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.layout = QHBoxLayout(self.parent)
        self.layout_left = QVBoxLayout()
        self.layout_center = QVBoxLayout()
        self.layout_right = QVBoxLayout()
        self.user_name = QLineEdit(self.parent)
        self.user_weight = QLineEdit(self.parent)
        self.user_height = QLineEdit(self.parent)
        self.user_history = QTreeWidget(self.parent)
        self.set_widget_properties()
        self.generate_layout()

    def user_name_properties(self):
        self.user_name.setReadOnly(True)

    def user_weight_properties(self):
        self.user_weight.setReadOnly(True)

    def user_height_properties(self):
        self.user_height.setReadOnly(True)

    def user_history_properties(self):
        label_list = ['Date', 'Weight']
        self.user_history.setHeaderLabels(label_list)

    def user_graph_properties(self):
        pass

    def set_widget_properties(self):
        self.user_name_properties()
        self.user_weight_properties()
        self.user_height_properties()
        self.user_graph_properties()
        self.user_history_properties()

    def left_layout_properties(self):
        self.layout_left.addWidget(self.user_name)
        self.layout_left.addWidget(self.user_weight)
        self.layout_left.addWidget(self.user_height)

    def center_layout_properties(self):
        self.layout_center.addWidget(self.user_history)

    def right_layout_properties(self):
        pass

    def main_layout_properties(self):
        self.layout.addLayout(self.layout_left, 1)
        self.layout.addLayout(self.layout_center, 1)
        self.layout.addLayout(self.layout_right, 1)

    def generate_layout(self):
        self.left_layout_properties()
        self.center_layout_properties()
        self.main_layout_properties()

class NewUserLayout(QLayout):

    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.user = User()
        self.layout = QGridLayout(self.parent)
        self.name = QLineEdit(self.parent)
        self.weight = QLineEdit(self.parent)
        self.height = QLineEdit(self.parent)
        self.confirm = QPushButton('Confirm', self.parent)
        self.cancel = QPushButton('Cancel', self.parent)
        self.set_widget_properties()
        self.generate_layout()

    def name_properties(self):
        self.name.setPlaceholderText('Name')
        self.name.editingFinished.connect(partial(self.user_setup, name=self.name))

    def weight_properties(self):
        self.weight.setPlaceholderText('Current Weight')
        validator = QDoubleValidator(0, 2000, 2, self.weight)
        self.weight.setValidator(validator)
        self.weight.editingFinished.connect(partial(self.user_setup, weight=self.weight))

    def height_properties(self):
        self.height.setPlaceholderText('Height')
        validator = QDoubleValidator(0, 110, 2, self.height)
        self.height.setValidator(validator)
        self.height.editingFinished.connect(partial(self.user_setup, height=self.height))

    def confirm_properties(self):
        self.confirm.setFixedHeight(35)
        self.confirm.clicked.connect(partial(self.confirm_transition))

    def cancel_properties(self):
        self.cancel.setFixedHeight(35)
        self.cancel.clicked.connect(self.cancel_transition)

    def confirm_transition(self):
        self.master.set_active_window(self.master.main_menu)

    def cancel_transition(self):
        self.master.set_active_window(self.master.user_selection_menu)

    def set_widget_properties(self):
        self.name_properties()
        self.weight_properties()
        self.height_properties()
        self.confirm_properties()
        self.cancel_properties()

    def generate_layout(self):
        self.layout.addWidget(self.name, 1, 0)
        self.layout.addWidget(self.weight, 2, 0)
        self.layout.addWidget(self.height, 3, 0)
        self.layout.addWidget(self.confirm, 4, 0, Qt.Alignment.AlignRight)
        self.layout.addWidget(self.cancel, 4, 1, Qt.Alignment.AlignRight)
