from functools import partial
import sys

from user import User

import database

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import pyqtgraph as pg


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
        self.check_user_status()

    def check_user_status(self):
        if self.user == None:
            self.new_user_layout()
        else:
            self.existing_user_layout()

    def new_user_layout(self):
        new_user_layout = NewUserLayout(self)
        # self.change_layout(new_user_layout)

    def existing_user_layout(self):
        existing_user_layout = UserLayout(self, self.user)
        self.change_layout(existing_user_layout)

    def change_layout(self, layout):
        self.setLayout(layout)


class UserLayout(QLayout):

    def __init__(self, parent_window, user):
        super().__init__()
        self.parent = parent_window
        self.user = user
        # Initializes the layouts with a master layout
        self.layout = QHBoxLayout(self.parent)
        self.layout_left = QVBoxLayout()
        self.layout_center = QVBoxLayout()
        self.center_layout_left = QVBoxLayout()
        self.center_layout_right = QVBoxLayout()
        self.layout_right = QVBoxLayout()
        # Initializes widgets to display user metrics
        self.user_name = QLineEdit()
        self.user_weight = QLineEdit()
        self.user_height = QLineEdit()
        self.user_bmi = QLineEdit()
        self.user_goal_weight = QLineEdit()
        # Initializes a tree for displaying all user's weight history and buttons for editing DB
        self.user_history = QTableWidget()
        self.add_entry = QPushButton()
        self.modify_entry = QPushButton()
        self.delete_entry = QPushButton()
        self.weight_entry = QLineEdit()
        self.calendar = QCalendarWidget()
        # Initializes the graph for visualizing weight history with buttons for modifying display
        self.graph_label = QLabel()
        self.user_history_graph = pg.plot()
        # Sets the properties for all widgets and their layouts
        self.set_widget_properties()
        self.generate_layout()

    def user_name_properties(self):
        self.user_name.setText(f'Name: {self.user.name}')
        self.user_name.setReadOnly(True)

    def user_weight_properties(self):
        self.user_weight.setText(f'Weight: {self.user.weight} lbs')
        self.user_weight.setReadOnly(True)

    def user_height_properties(self):
        self.user_height.setText(f'Height: {self.user.height} inches')
        self.user_height.setReadOnly(True)

    def user_bmi_properties(self):
        self.user_bmi.setText(f'Body Mass Index: {(self.user.weight / self.user.height**2 * 703):.1f}')
        self.user_bmi.setReadOnly(True)

    def user_goal_weight_properties(self):
        self.user_goal_weight.setText(f'Goal Weight: {self.user.goal} lbs')
        self.user_goal_weight.setReadOnly(True)

    def user_history_properties(self):
        hlabel_list = ['Date', 'Weight']
        self.user_history.setColumnCount(2)
        self.user_history.setRowCount(len(self.user.weight_history))
        self.user_history.setHorizontalHeaderLabels(hlabel_list)
        # populates the table with entries by date
        for row, items in enumerate(self.user.weight_history_table):
            self.user_history.setItem(row, 0, items[0])
            self.user_history.setItem(row, 1, items[1])

    def add_entry_button(self):
        self.add_entry.setText('Add Entry')
        self.add_entry.setEnabled(False)
        self.add_entry.clicked.connect(self.add_entry_database)

    def add_entry_trigger(self):
        if self.weight_entry.hasAcceptableInput() is True:
            self.add_entry.setEnabled(True)
        else:
            self.add_entry.setEnabled(False)

    def add_entry_database(self):
        date, weight = self.calendar.selectedDate(), float(self.weight_entry.text())
        date = date.toString('yyyy-MM-dd')
        database.insert_weight_entry(date, weight, self.user.user_id)

    def modify_entry_button(self):
        self.modify_entry.setText('Modify Entry')
        self.modify_entry.setEnabled(False)

    def delete_entry_button(self):
        self.delete_entry.setText('Delete Entry')
        self.delete_entry.setEnabled(False)

    def weight_entry_edit(self):
        self.weight_entry.setPlaceholderText('Type a valid weight into here')
        validator = QDoubleValidator(0, 1000, 2, self.weight_entry)
        self.weight_entry.setValidator(validator)
        self.weight_entry.setAlignment(Qt.Alignment.AlignCenter)
        self.weight_entry.textEdited.connect(self.add_entry_trigger)

    def calendar_widget(self):
        pass
        #self.calendar.selectionChanged.connect()

    def graph_label_properties(self):
        self.graph_label.setText('Weight Visualizer')
        self.graph_label.setStyleSheet(
            'font: bold 18px;'
            'color: steel grey;'

        )
        self.graph_label.setAlignment(Qt.Alignment.AlignCenter)

    def user_graph_properties(self):
        axis_label_style = {'color': '#FFF', 'font-size': '14pt', 'font-weight': 'bold'}
        axis_left = pg.AxisItem(
            orientation='left',
            text='Weight',
            **axis_label_style
        )
        axis_left.showLabel(show=True)
        axis_bottom = pg.AxisItem(
            orientation='bottom',
            text='Date',
            **axis_label_style
        )
        axis_bottom.showLabel(show=True)
        title_label_style = {'color': 'FFF', 'size': '22pt', 'font-weight': 'bold'}
        # self.user_history_graph.setTitle(title='Weight Visualizer', **title_label_style)
        self.user_history_graph.setAxisItems(axisItems={'left': axis_left, 'bottom': axis_bottom})

    def set_widget_properties(self):
        self.user_name_properties()
        self.user_weight_properties()
        self.user_height_properties()
        self.user_bmi_properties()
        self.user_goal_weight_properties()
        self.graph_label_properties()
        self.user_graph_properties()
        self.add_entry_button()
        self.modify_entry_button()
        self.delete_entry_button()
        self.weight_entry_edit()
        self.calendar_widget()
        self.user_history_properties()

    def generate_left_layout(self):
        self.layout_left.addWidget(self.user_name)
        self.layout_left.addWidget(self.user_weight)
        self.layout_left.addWidget(self.user_height)
        self.layout_left.addWidget(self.user_bmi)
        self.layout_left.addWidget(self.user_goal_weight)

    def generate_center_layout(self):
        self.layout_center.addWidget(self.user_history)
        self.center_layout_left.addWidget(self.add_entry)
        self.center_layout_left.addWidget(self.modify_entry)
        self.center_layout_left.addWidget(self.delete_entry)
        self.center_layout_right.addWidget(self.weight_entry)
        self.center_layout_right.addWidget(self.calendar)
        self.layout_center.addLayout(self.center_layout_left)
        self.layout_center.addLayout(self.center_layout_right)

    def generate_right_layout(self):
        self.layout_right.addWidget(self.graph_label)
        self.layout_right.addWidget(self.user_history_graph)

    def generate_master_layout(self):
        self.layout.addLayout(self.layout_left, 1)
        self.layout.addLayout(self.layout_center, 1)
        self.layout.addLayout(self.layout_right, 1)

    def generate_layout(self):
        self.generate_left_layout()
        self.generate_center_layout()
        self.generate_right_layout()
        self.generate_master_layout()


class NewUserLayout(QLayout):

    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.user = User()
        self.layout = QGridLayout(self.parent)
        self.person_name = QLineEdit()
        self.weight = QLineEdit()
        self.goal = QLineEdit()
        self.height = QLineEdit()
        self.confirm = QPushButton('Confirm')
        self.cancel = QPushButton('Cancel')
        self.set_widget_properties()
        self.generate_layout()

    def name_properties(self):
        self.person_name.setPlaceholderText('Type your name here')
        self.person_name.textEdited.connect(partial(self.user.set_name, self.person_name))
        self.person_name.textEdited.connect(self.enable_confirm_btn)

    def weight_properties(self):
        self.weight.setPlaceholderText('Type your current weight here')
        validator = QDoubleValidator(0, 2000, 2, self.weight)
        self.weight.setValidator(validator)
        self.weight.textEdited.connect(partial(self.user.set_weight, self.weight))
        self.weight.textEdited.connect(self.enable_confirm_btn)

    def goal_properties(self):
        self.goal.setPlaceholderText('Type your goal weight here')
        validator = QDoubleValidator(0, 2000, 2, self.goal)
        self.goal.setValidator(validator)
        self.goal.textEdited.connect(partial(self.user.set_goal_weight, self.goal))
        self.goal.textEdited.connect(self.enable_confirm_btn)

    def height_properties(self):
        self.height.setPlaceholderText('Type your height here')
        validator = QDoubleValidator(0, 110, 2, self.height)
        self.height.setValidator(validator)
        self.height.textEdited.connect(partial(self.user.set_height, self.height))
        self.height.textEdited.connect(self.enable_confirm_btn)

    def validation_color(self, obj):
        pass

    def confirm_properties(self):
        self.confirm.setFixedHeight(35)
        self.confirm.setEnabled(False)
        self.confirm.clicked.connect(partial(self.confirm_transition, self.user))

    def cancel_properties(self):
        self.cancel.setFixedHeight(35)
        self.cancel.clicked.connect(self.cancel_transition)

    def enable_confirm_btn(self):
        if (self.person_name.hasAcceptableInput() == True and self.weight.hasAcceptableInput() == True and
                self.goal.hasAcceptableInput() == True and self.height.hasAcceptableInput() == True):
            self.confirm.setEnabled(True)
        else:
            self.confirm.setEnabled(False)

    def confirm_transition(self, user):
        database.insert_user(user)
        self.parent.existing_user_layout()
        self.layout.setEnabled(False)

    def cancel_transition(self):
        sys.exit()

    def set_widget_properties(self):
        self.name_properties()
        self.weight_properties()
        self.goal_properties()
        self.height_properties()
        self.confirm_properties()
        self.cancel_properties()

    def generate_layout(self):
        self.layout.addWidget(self.person_name, 1, 0)
        self.layout.addWidget(self.weight, 2, 0)
        self.layout.addWidget(self.goal, 3, 0)
        self.layout.addWidget(self.height, 4, 0)
        self.layout.addWidget(self.confirm, 5, 0, Qt.Alignment.AlignRight)
        self.layout.addWidget(self.cancel, 5, 1, Qt.Alignment.AlignRight)