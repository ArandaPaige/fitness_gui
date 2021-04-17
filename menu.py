import datetime
import sys
from functools import partial

import pyqtgraph as pg
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import database
import model
from user import User

DATETODAY = datetime.date.today()


class GUIManager(QWidget):
    """Overall manager for all GUI objects and app UI functions."""

    def __init__(self, user=None):
        """
        Initializes with an instance of the main menu and a user. It controls the state of the user interface.
        :param user: an instance of a user object.
        """
        super().__init__()
        self.user = user
        self.active_window = self.user_check()

    def user_check(self):
        if self.user is None:
            window = NewUserDialog(self)
            return window
        else:
            window = MainMenu(self, self.user)
            return window

    def create_main_menu(self, user):
        self.active_window = MainMenu(self, user)


class MainMenu(QWidget):
    """The main menu is the main window of the application. It manages the layouts that constitute the GUI."""

    def __init__(self, master, user):
        """
        Initializes the main menu's main GUI properties and checks user instance to direct the creation of the
        appropriate layout.
        :param master: the master object that controls the main menu's state.
        :param user: the user object.
        """
        super().__init__()
        self.master = master
        self.user = user
        self.setWindowTitle('Main Menu')
        # Initializes the layouts with a master layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout_left = QVBoxLayout()
        self.layout_center = QVBoxLayout()
        self.center_layout_left = QVBoxLayout()
        self.center_layout_right = QVBoxLayout()
        self.layout_right = QVBoxLayout()
        self.layout_right_graph_buttons = QHBoxLayout()
        self.layout_right_lerp_buttons = QHBoxLayout()
        # Initializes widgets to display user metrics
        self.user_name = self.user_name_properties()
        self.user_weight = self.user_weight_properties()
        self.user_height = self.user_height_properties()
        self.user_bmi = self.user_bmi_properties()
        self.user_goal_weight = self.user_goal_weight_properties()
        # Initializes a tree for displaying all user's weight history and buttons for editing DB
        self.user_history = QTableWidget()
        self.add_entry = self.add_entry_button()
        self.modify_entry = QPushButton()
        self.delete_entry = QPushButton()
        self.weight_entry = QLineEdit()
        self.calendar = self.calendar_widget()
        # Initializes the graph for visualizing weight history with buttons for modifying display
        self.graph_x, self.graph_y = model.create_graph_list(self.user.weight_history)
        self.user_graph = self.user_graph_properties()
        self.graph_14_days_button = self.graph_14_days_btn()
        self.graph_28_days_button = self.graph_28_days_btn()
        self.graph_3_months_button = self.graph_3_months_btn()
        self.lerp_14_days_button = self.lerp_14_days_btn()
        self.lerp_28_days_button = self.lerp_28_days_btn()
        self.graph_box = self.graph_box_properties()
        # Sets the properties for all widgets and their layouts
        self.set_widget_properties()
        self.user_history_table()
        self.generate_layout()
        self.update_graph()
        self.show()

    def user_name_properties(self):
        """
        Sets the default properties of the name QLineEdit object.
        :return: None
        """
        name = QLineEdit()
        name.setText(f'Name: {self.user.name}')
        name.setReadOnly(True)
        return name

    def user_weight_properties(self):
        """
        Sets the default properties of the weight QLineEdit object.
        :return: None
        """
        weight = QLineEdit()
        weight.setText(f'Weight: {self.user.weight} lbs')
        weight.setReadOnly(True)
        return weight

    def user_height_properties(self):
        """
        Sets the default properties of the height QLineEdit object.
        :return: None
        """
        height = QLineEdit()
        height.setText(f'Height: {self.user.height} inches')
        height.setReadOnly(True)
        return height

    def user_bmi_properties(self):
        """
        Sets the default properties of the BMI object.
        :return: None
        """
        bmi = QLineEdit()
        bmi.setText(f'Body Mass Index: {(self.user.weight / self.user.height ** 2 * 703):.1f}')
        bmi.setReadOnly(True)
        return bmi

    def user_goal_weight_properties(self):
        """
        Sets the default properties of the weight goal QLineEdit object.
        :return: None
        """
        goal_weight = QLineEdit()
        goal_weight.setText(f'Goal Weight: {self.user.goal} lbs')
        goal_weight.setReadOnly(True)
        return goal_weight

    def user_history_properties(self):
        """
        Sets the default properties of the user history table.
        :return: None
        """
        hlabel_list = ['ID', 'DATE', 'WEIGHT']
        self.user_history.setColumnCount(3)
        self.user_history.setColumnHidden(0, True)
        self.user_history.setHorizontalHeaderLabels(hlabel_list)
        self.user_history.setAlternatingRowColors(True)
        self.user_history.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.user_history.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.user_history.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.user_history.verticalHeader().setVisible(False)
        style_sheet = '''
            QHeaderView::section {
                border-radius:20px;
                font-size:20px;
                font-weight:bold;
            }
            QTableCornerButton::section {
                border-radius:14px;
                font-size:10px;
                font-weight:bold;
            }
            QTableWidget::item {
                border-radius:12px;
                font-size:16px;
            }
        '''
        self.user_history.setStyleSheet(style_sheet)

    def user_history_table(self):
        """
        Sets the items of the user's weight history dynamically into the table.
        :return: None
        """
        self.user_history.setRowCount(len(self.user.weight_history))
        weight_history_items = model.create_table_list(self.user.weight_history)
        for row, items in enumerate(weight_history_items):
            self.user_history.setItem(row, 0, items[0])
            self.user_history.setItem(row, 1, items[1])
            self.user_history.setItem(row, 2, items[2])
        self.user_history.itemSelectionChanged.connect(self.modify_entry_trigger)
        self.user_history.itemSelectionChanged.connect(self.delete_entry_trigger)

    def add_entry_button(self):
        """
        Sets the default properties of the 'Add Entry' button. Clicking the button adds an entry to the database.
        :return: None
        """
        add_entry = QPushButton()
        add_entry.setText('Add Entry')
        add_entry.setEnabled(False)
        add_entry.clicked.connect(self.add_entry_database)
        return add_entry

    def add_entry_trigger(self):
        if self.weight_entry.hasAcceptableInput() is True:
            self.add_entry.setEnabled(True)
        else:
            self.add_entry.setEnabled(False)

    def add_entry_database(self):
        date, weight = self.calendar.selectedDate(), float(self.weight_entry.text())
        date = date.toString('yyyy-MM-dd')
        database.insert_weight_entry(date, weight, self.user.user_id)
        database.load_user_history(self.user)
        self.user_history.clearContents()
        self.user_history_table()
        self.weight_entry.clear()
        self.update_graph()

    def modify_entry_button(self):
        """
        Sets the default properties of the 'Modify Entry' button. It is enabled when a valid selection on the table
        is made. Clicking the button modifies the entry in the database.
        :return: None
        """
        self.modify_entry.setText('Modify Entry')
        self.modify_entry.setEnabled(False)
        self.modify_entry.clicked.connect(self.modify_entry_database)

    def modify_entry_trigger(self):
        """
        Checks whether items have been selected on the weight history and enables/disables the modify QPushButton.
        :return:
        """
        if self.weight_entry.hasAcceptableInput() is True and len(self.user_history.selectedItems()) == 1:
            self.modify_entry.setEnabled(True)
        else:
            self.modify_entry.setEnabled(False)
        return

    def modify_entry_database(self):
        """
        Updates the selected item in the table with the new value for weight and/or date.
        :return: None
        """
        entry = self.user_history.selectedItems()[0]
        item_id = self.user_history.item(entry.row(), 0)
        date, weight = self.calendar.selectedDate(), float(self.weight_entry.text())
        date = date.toString('yyyy-MM-dd')
        database.update_weight_entry(item_id.data(0), weight, date)
        database.load_user_history(self.user)
        self.user_history.clearContents()
        self.user_history_table()
        self.update_graph()

    def delete_entry_button(self):
        """
        Sets the default properties of the 'Delete Entry' button. It is enabled when a valid selection on the table
        is made. Clicking the button deletes the entries in the database.
        :return: None
        """
        self.delete_entry.setText('Delete Entry')
        self.delete_entry.setEnabled(False)
        self.delete_entry.clicked.connect(self.delete_entry_dialog)

    def delete_entry_dialog(self):
        self.dialog = DeleteDialog(self, self.user_history.selectedItems())

    def delete_entry_trigger(self):
        """
        Checks whether items have been selected on the weight history and enables/disables the delete QPushButton.
        :return: None
        """
        if len(self.user_history.selectedItems()) >= 1:
            self.delete_entry.setEnabled(True)
        else:
            self.delete_entry.setEnabled(False)

    def delete_entry_database(self, entry):
        """
        Deletes the set of entries from the database.
        :return: None
        """
        entries = set()
        for item in entry:
            item_id = self.user_history.item(item.row(), 0)
            entries.add(item_id.data(0))
        for entry in entries:
            database.delete_weight_entry(entry)
        database.load_user_history(self.user)
        self.user_history.clearContents()
        self.user_history_table()
        self.update_graph()

    def weight_entry_edit(self):
        """
        Sets the default properties of the weight entry QLineEdit object.
        :return: None
        """
        self.weight_entry.setPlaceholderText('Type a valid weight into here')
        validator = QDoubleValidator(0, 1000, 2, self.weight_entry)
        self.weight_entry.setValidator(validator)
        self.weight_entry.setAlignment(Qt.Alignment.AlignCenter)
        self.weight_entry.textEdited.connect(self.add_entry_trigger)
        self.weight_entry.textEdited.connect(self.modify_entry_trigger)

    def calendar_widget(self):
        calendar = QCalendarWidget()
        calendar.setMaximumDate(DATETODAY)
        return calendar

    def user_graph_properties(self):
        """
        Sets the default properties of the graph.
        :return: None
        """
        axis_label_style = {
            'color': '#FFF',
            'font-size': '14pt',
            'font-weight': 'bold'
        }
        axis_title = pg.AxisItem(
            orientation='top',
            text='Weight Visualizer',
            **axis_label_style
        )
        axis_title.showLabel(show=True)
        axis_left = pg.AxisItem(
            orientation='left',
            text='Weight',
            **axis_label_style
        )
        axis_left.showLabel(show=True)
        axis_bottom = pg.AxisItem(
            orientation='bottom',
            text='Entries',
            **axis_label_style
        )
        axis_bottom.showLabel(show=True)
        viewbox = pg.ViewBox()
        user_graph = pg.PlotWidget(
            viewbox=viewbox,
            axisItems={
                'top': axis_title,
                'left': axis_left,
                'bottom': axis_bottom
            }
        )
        if len(self.graph_x) > 0:
            user_graph.setYRange((max(self.graph_y) + 20), (min(self.graph_y) - 20))
        else:
            return user_graph
        return user_graph

    def update_graph(self):
        self.graph_x, self.graph_y = model.create_graph_list(self.user.weight_history)
        if len(self.graph_x) > 0:
            self.user_graph.getPlotItem().plot(self.graph_x, self.graph_y, symbol='o', clear=True)
        else:
            return

    def add_lerp_points(self, start_entry, end_entry, future_date):
        weight_delta = model.weight_delta_calculator(start_entry, end_entry)
        lerp_x_list, lerp_y_list = model.lerp_weight(future_date, end_entry[1], self.user.goal, weight_delta)
        self.user_graph.getPlotItem().addPoints(lerp_x_list, lerp_y_list, symbol='h')

    def graph_box_properties(self):
        box = QGroupBox(title='Press a button to change the graph displayed.')
        box_layout = QHBoxLayout()
        graph_layout = QVBoxLayout()
        lerp_layout = QVBoxLayout()
        graph_layout.addWidget(self.graph_14_days_button)
        graph_layout.addWidget(self.graph_28_days_button)
        graph_layout.addWidget(self.graph_3_months_button)
        lerp_layout.addWidget(self.lerp_14_days_button)
        lerp_layout.addWidget(self.lerp_28_days_button)
        box_layout.addLayout(graph_layout)
        box_layout.addLayout(lerp_layout)
        box.setLayout(box_layout)
        return box

    def graph_14_days_btn(self):
        button = QPushButton('14 Days')
        return button

    def graph_28_days_btn(self):
        button = QPushButton('28 Days')
        return button

    def graph_3_months_btn(self):
        button = QPushButton('3 Months')
        return button

    def lerp_14_days_btn(self):
        button = QPushButton('Lerp 14 Days')
        button.setToolTip('See future weight progression based on past performance')
        return button

    def lerp_28_days_btn(self):
        button = QPushButton('Lerp 28 Days')
        button.setToolTip('See future weight progression based on past performance')
        return button

    def set_widget_properties(self):
        self.user_history_properties()
        self.weight_entry_edit()
        self.modify_entry_button()
        self.delete_entry_button()

    def generate_left_layout(self):
        self.layout_left.addWidget(self.user_name)
        self.layout_left.addWidget(self.user_weight)
        self.layout_left.addWidget(self.user_goal_weight)
        self.layout_left.addWidget(self.user_height)
        self.layout_left.addWidget(self.user_bmi)

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
        """
        :return: None
        """
        self.layout_right.addWidget(self.user_graph)
        self.layout_right.addWidget(self.graph_box)

    def generate_master_layout(self):
        """
        Adds all the child layouts to the master layout.
        :return: None
        """
        self.layout.addLayout(self.layout_left, 1)
        self.layout.addLayout(self.layout_center, 1)
        self.layout.addLayout(self.layout_right, 1)

    def generate_layout(self):
        """
        Calls all layout property setting functions and generates the layout.
        :return: None
        """
        self.generate_left_layout()
        self.generate_center_layout()
        self.generate_right_layout()
        self.generate_master_layout()


class DeleteDialog(QDialog):

    def __init__(self, parent_window, entry):
        super().__init__()
        self.parent = parent_window
        self.entry = entry
        self.layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()
        self.label = self.deletion_label()
        self.confirm = self.confirm_button()
        self.cancel = self.cancel_button()
        self.btn_layout()
        self.main_layout()
        self.open()

    def deletion_label(self):
        label = QLabel()
        label.setText('Are you sure you want to delete these entries?\n')
        return label

    def confirm_button(self):
        confirm = QPushButton('Confirm')
        confirm.setFixedSize(75, 35)
        confirm.clicked.connect(self.confirm_event)
        return confirm

    def cancel_button(self):
        cancel = QPushButton('Cancel')
        cancel.setFixedSize(75, 35)
        cancel.clicked.connect(self.cancel_event)
        return cancel

    def confirm_event(self):
        self.parent.delete_entry_database(self.entry)
        self.close()

    def cancel_event(self):
        self.close()

    def btn_layout(self):
        self.button_layout.addWidget(self.confirm)
        self.button_layout.addWidget(self.cancel)

    def main_layout(self):
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.button_layout)


class NewUserDialog(QDialog):

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.user = User()
        self.dialog = self.create_dialog()
        self.layout = QVBoxLayout(self.dialog)
        self.button_layout = QHBoxLayout()
        self.label = self.label_properties()
        self.name = self.name_properties()
        self.weight = self.weight_properties()
        self.goal = self.goal_properties()
        self.height = self.height_properties()
        self.confirm = self.confirm_button()
        self.cancel = self.cancel_button()
        self.open_dialog()
        self.btn_layout()
        self.main_layout()
        self.dialog.resize(200, 200)

    def create_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle('New User Creation')
        return dialog

    def label_properties(self):
        label = QLabel()
        label.setText(
            'Welcome to the Weight Tracker and Visualization tool!\n'
            'Please input your personal details in the boxes below\n'
            'These details will become the base of your history.\n'
        )
        return label

    def name_properties(self):
        """
        Sets the default properties of the name QLineEdit object.
        :return: None
        """
        name = QLineEdit()
        name.setPlaceholderText('Type your name here')
        name.textEdited.connect(partial(self.user.set_name, name))
        name.textEdited.connect(self.enable_confirm_btn)
        return name

    def weight_properties(self):
        """
        Sets the default properties of the weight QLineEdit object.
        :return: None
        """
        weight = QLineEdit()
        weight.setPlaceholderText('Type your current weight here')
        validator = QDoubleValidator(0, 2000, 2, weight)
        weight.setValidator(validator)
        weight.textEdited.connect(partial(self.user.set_weight, weight))
        weight.textEdited.connect(self.enable_confirm_btn)
        return weight

    def goal_properties(self):
        """
        Sets the default properties of the goal weight QLineEdit object.
        :return: None
        """
        goal = QLineEdit()
        goal.setPlaceholderText('Type your goal weight here')
        validator = QDoubleValidator(0, 2000, 2, goal)
        goal.setValidator(validator)
        goal.textEdited.connect(partial(self.user.set_goal_weight, goal))
        goal.textEdited.connect(self.enable_confirm_btn)
        return goal

    def height_properties(self):
        """
        Sets the default properties of the height QLineEdit object.
        :return: None
        """
        height = QLineEdit()
        height.setPlaceholderText('Type your height here')
        validator = QDoubleValidator(0, 110, 2, height)
        height.setValidator(validator)
        height.textEdited.connect(partial(self.user.set_height, height))
        height.textEdited.connect(self.enable_confirm_btn)
        return height

    def confirm_button(self):
        confirm = QPushButton('Confirm')
        confirm.setEnabled(False)
        confirm.clicked.connect(self.confirm_event)
        return confirm

    def cancel_button(self):
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.cancel_event)
        return cancel

    def enable_confirm_btn(self):
        if (self.name.hasAcceptableInput() is True and
                self.weight.hasAcceptableInput() is True and
                self.goal.hasAcceptableInput() is True and
                self.height.hasAcceptableInput() is True):
            self.confirm.setEnabled(True)
        else:
            self.confirm.setEnabled(False)

    def confirm_event(self):
        """
        Instantiates a user object and adds it to the database and then instantiates the main menu with the user
        :return: None
        """
        user = User(str(self.name.text()), float(self.weight.text()), float(self.goal.text()), int(self.height.text()))
        database.insert_user(user)
        user = database.retrieve_user(user_id=1)
        self.master.create_main_menu(user)
        self.close_dialog()

    def cancel_event(self):
        sys.exit()

    def open_dialog(self):
        self.dialog.open()

    def close_dialog(self):
        self.dialog.close()

    def btn_layout(self):
        self.button_layout.addWidget(self.confirm)
        self.button_layout.addWidget(self.cancel)

    def main_layout(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.weight)
        self.layout.addWidget(self.goal)
        self.layout.addWidget(self.height)
        self.layout.addLayout(self.button_layout)
