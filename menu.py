import datetime
import sys
from functools import partial

import pyqtgraph as pg
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import database
import model
from settings import Settings
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
        # data for objects
        self.settings = Settings()
        self.sorted_weight_list = model.create_sorted_weight_history(self.user.weight_history)
        self.table_list = model.create_table_list(self.sorted_weight_list)
        self.weight_delta = model.weight_delta_calculator(self.sorted_weight_list)
        self.time_goal_data = model.time_to_goal(self.user.weight, self.user.goal, self.weight_delta)
        # Initializes widgets to display user metrics
        self.user_name = self.user_name_properties()
        self.user_weight = self.user_weight_properties()
        self.user_height = self.user_height_properties()
        self.user_bmi = self.user_bmi_properties()
        self.user_goal_weight = self.user_goal_weight_properties()
        self.user_box = self.user_box_properties()
        self.net_change = self.net_weight_change()
        self.weight_average = self.average_weight_change()
        self.time_goal = self.time_to_goal()
        self.end_date = self.end_date_properties()
        self.weight_box = self.weight_box_properties()
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
        self.lerp_7_days_button = self.lerp_7_days_btn()
        self.lerp_14_days_button = self.lerp_14_days_btn()
        self.lerp_28_days_button = self.lerp_28_days_btn()
        self.graph_box = self.graph_box_properties()
        # Sets the properties for all widgets and their layouts
        self.set_widget_properties()
        self.set_progress_metrics()
        self.user_history_table(self.table_list)
        self.generate_layout()
        self.update_graph()
        self.show()

    def user_name_properties(self):
        """
        Sets the default properties of the name QLineEdit object.
        :return: None
        """
        name = QLineEdit()
        name.setText(f'{self.user.name}')
        name.setReadOnly(True)
        return name

    def user_weight_properties(self):
        """
        Sets the default properties of the weight QLineEdit object.
        :return: None
        """
        weight = QLineEdit()
        weight.setText(f'{self.user.weight} lbs')
        weight.setToolTip('Your current weight.')
        weight.setReadOnly(True)
        return weight

    def user_weight_edit_button(self):
        pass

    def user_height_properties(self):
        """
        Sets the default properties of the height QLineEdit object.
        :return: None
        """
        height = QLineEdit()
        height.setText(f'{self.user.height} inches')
        height.setReadOnly(True)
        return height

    def user_bmi_properties(self):
        """
        Sets the default properties of the BMI object.
        :return: None
        """
        bmi = QLineEdit()
        bmi.setToolTip('BMI is a ')
        bmi.setText(f'{(self.user.weight / self.user.height ** 2 * 703):.1f}')
        bmi.setReadOnly(True)
        return bmi

    def user_goal_weight_properties(self):
        """
        Sets the default properties of the weight goal QLineEdit object.
        :return: None
        """
        goal_weight = QLineEdit()
        goal_weight.setToolTip('The goal weight you are trying to achieve.')
        goal_weight.setText(f'{self.user.goal} {self.settings.units}')
        goal_weight.setReadOnly(True)
        return goal_weight

    def set_name(self):
        self.user_name.setText(f'{self.user.name}')

    def set_weight(self):
        if len(self.sorted_weight_list) > 0:
            self.user_weight.setText(f'{self.sorted_weight_list[-1][2]} {self.settings.units}')
        else:
            self.user_weight.setText(f'Not available.')

    def set_goal(self):
        if self.user.goal is not None:
            self.user_goal_weight.setText(f'{self.user.goal} {self.self.settings.units}')
        else:
            self.user_goal_weight.setText(f'Please update your goal weight.')

    def set_bmi(self):
        if len(self.sorted_weight_list) > 0:
            self.user_bmi.setText(f'{(self.sorted_weight_list[-1][2] / self.user.height ** 2 * 703):.1f}')
        else:
            self.user_bmi.setText(f'Not available.')

    def set_height(self):
        self.user_height.setText(f'{self.user.height} {self.units}')

    def user_box_properties(self):
        box = QGroupBox('Personal information')
        box.setStyleSheet("""
        QGroupBox {
        font-size: 16px;
        font-weight: bold;
        }

        QLabel {
        font: bold 14px
        }
        """)
        layout = QGridLayout()
        name_label = QLabel('NAME')
        weight_label = QLabel('WEIGHT')
        goal_label = QLabel('GOAL WEIGHT')
        bmi_label = QLabel('BODY MASS INDEX')
        height_label = QLabel('HEIGHT')
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.user_name, 0, 1)
        layout.addWidget(weight_label, 1, 0)
        layout.addWidget(self.user_weight, 1, 1)
        layout.addWidget(goal_label, 2, 0)
        layout.addWidget(self.user_goal_weight, 2, 1)
        layout.addWidget(bmi_label, 3, 0)
        layout.addWidget(self.user_bmi, 3, 1)
        layout.addWidget(height_label, 4, 0)
        layout.addWidget(self.user_height, 4, 1)
        box.setLayout(layout)
        return box

    def net_weight_change(self):
        net = QLineEdit()
        net.setReadOnly(True)
        net.setToolTip('The total weight change you have experienced.')
        return net

    def average_weight_change(self):
        average = QLineEdit()
        average.setReadOnly(True)
        average.setToolTip('The average weight loss you have experienced per entry.')
        return average

    def time_to_goal(self):
        time = QLineEdit()
        time.setReadOnly(True)
        time.setToolTip(
            f'The amounts of days left until you reach your goal '
            f'should the trajectory of your weight progression '
            f'remain the same.'
        )
        return time

    def end_date_properties(self):
        end_date = QLineEdit()
        end_date.setReadOnly(True)
        end_date.setToolTip(
            f'The date upon which you will reach your end goal '
            f'should the trajectory of your weight progression'
            f'remain the same.'
        )
        return end_date

    def weight_box_properties(self):
        box = QGroupBox('Metrics for user weight progression')
        box.setStyleSheet("""
        QGroupBox {
        font-size: 16px;
        font-weight: bold;
        }
        
        QLabel {
        font: bold 14px
        }
        """)
        layout = QGridLayout()
        net_change_label = QLabel('NET CHANGE')
        average_label = QLabel('WEIGHT CHANGE')
        days_label = QLabel('DAYS UNTIL GOAL REACHED:')
        date_label = QLabel('END DATE')
        layout.addWidget(net_change_label, 0, 0)
        layout.addWidget(self.net_change, 0, 1)
        layout.addWidget(average_label, 1, 0)
        layout.addWidget(self.weight_average, 1, 1)
        layout.addWidget(days_label, 2, 0)
        layout.addWidget(self.time_goal, 2, 1)
        layout.addWidget(date_label, 3, 0)
        layout.addWidget(self.end_date, 3, 1)
        box.setLayout(layout)
        return box

    def set_progress_metrics(self):
        if len(self.sorted_weight_list) > 0:
            self.net_change.setText(
                f'{(self.sorted_weight_list[0][2] - self.sorted_weight_list[-1][2]):.2F}'
            )
        else:
            self.net_change.setText(f'Insufficient entries to calculate net change in weight')
        if self.weight_delta is not None:
            self.weight_average.setText(f'{self.weight_delta:.3f}')
            self.time_goal.setText(f'{self.time_goal_data[1]}')
            self.end_date.setText(f'{self.time_goal_data[0]}')
        else:
            self.weight_average.setText(f'Insufficient entries to calculate weight change delta.')
            self.time_goal.setText(f'Insufficient entries to calculate time until goal reached.')
            self.end_date.setText(f'Insufficient entries to calculate end date.')

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

    def user_history_table(self, table_list):
        """
        Sets the items of the user's weight history dynamically into the table.
        :return: None
        """
        self.user_history.setRowCount(len(self.sorted_weight_list))
        for row, items in enumerate(table_list):
            self.user_history.setItem(row, 0, items[0])
            self.user_history.setItem(row, 1, items[1])
            self.user_history.setItem(row, 2, items[2])
        self.user_history.itemSelectionChanged.connect(self.modify_entry_trigger)
        self.user_history.itemSelectionChanged.connect(self.delete_entry_trigger)

    def load_user_table(self):
        self.table_list = model.create_table_list(self.sorted_weight_list)
        self.user_history.clearContents()
        self.user_history_table(self.table_list)

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
        self.update_weight_history()
        self.load_user_table()
        self.weight_entry.clear()
        self.update_data()
        self.set_progress_metrics()
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
        self.update_weight_history()
        self.load_user_table()
        self.update_data()
        self.set_progress_metrics()
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
        self.update_weight_history()
        self.load_user_table()
        self.update_data()
        self.set_progress_metrics()
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
        return user_graph

    def update_graph(self, days=0):
        self.graph_x, self.graph_y = model.create_graph_list(self.user.weight_history, days)
        if len(self.graph_x) > 0:
            self.user_graph.setYRange((max(self.graph_y) + 20), (min(self.graph_y) - 20))
            self.user_graph.plot(self.graph_x, self.graph_y, symbol='o', clear=True)
            item = self.user_graph.listDataItems()[0]
        else:
            return

    def add_lerp_points(self, lerp_days):
        self.update_graph()
        lerp_x_list, lerp_y_list = model.lerp_weight_entry(
            lerp_days, self.graph_y, self.sorted_weight_list[-1][2],
            self.user.goal, self.weight_delta
        )
        self.user_graph.plot(lerp_x_list, lerp_y_list, symbol='h', symbolBrush='r')

    def graph_box_properties(self):
        box = QGroupBox('Press a button to change the graph displayed.')
        box.setStyleSheet("""
        QGroupBox {
        font-size: 16px;
        font-weight: bold;
        }

        QLabel {
        font: bold 14px
        }
        """)
        box_layout = QHBoxLayout()
        graph_layout = QVBoxLayout()
        lerp_layout = QVBoxLayout()
        graph_layout.addWidget(self.graph_14_days_button)
        graph_layout.addWidget(self.graph_28_days_button)
        graph_layout.addWidget(self.graph_3_months_button)
        lerp_layout.addWidget(self.lerp_7_days_button)
        lerp_layout.addWidget(self.lerp_14_days_button)
        lerp_layout.addWidget(self.lerp_28_days_button)
        box_layout.addLayout(graph_layout)
        box_layout.addLayout(lerp_layout)
        box.setLayout(box_layout)
        return box

    def graph_14_days_btn(self):
        button = QPushButton('Last 15 Entries')
        button.setToolTip('Display the last 15 entries of your weight history')
        button.clicked.connect(partial(self.update_graph, -14))
        return button

    def graph_28_days_btn(self):
        button = QPushButton('Last 30 Entries')
        button.setToolTip('Display the last 30 entries of your weight history')
        button.clicked.connect(partial(self.update_graph, -28))
        return button

    def graph_3_months_btn(self):
        button = QPushButton('Last 60 Entries')
        button.setToolTip('Display the last 60 entries of your weight history')
        button.clicked.connect(partial(self.update_graph, -84))
        return button

    def lerp_7_days_btn(self):
        button = QPushButton('Future 7 Days')
        button.setToolTip('See the next week of your weight progression based on your history')
        button.clicked.connect(partial(self.add_lerp_points, 7))
        return button

    def lerp_14_days_btn(self):
        button = QPushButton('Future 14 Days')
        button.setToolTip('See the next 2 weeks of your weight progression based on your history')
        button.clicked.connect(partial(self.add_lerp_points, 14))
        return button

    def lerp_28_days_btn(self):
        button = QPushButton('Future 28 Days')
        button.setToolTip('See the next 4 weeks of your weight progression based on your history')
        button.clicked.connect(partial(self.add_lerp_points, 28))
        return button

    def set_widget_properties(self):
        self.user_history_properties()
        self.weight_entry_edit()
        self.modify_entry_button()
        self.delete_entry_button()

    def generate_left_layout(self):
        self.layout_left.addWidget(self.user_box)
        self.layout_left.addWidget(self.weight_box)

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

    def update_weight_history(self):
        self.sorted_weight_list = model.create_sorted_weight_history(self.user.weight_history)

    def update_weight_delta(self):
        self.weight_delta = model.weight_delta_calculator(self.sorted_weight_list)

    def update_time_delta(self):
        self.time_goal_data = model.time_to_goal(self.user.weight, self.user.goal, self.weight_delta)

    def update_data(self):
        self.update_weight_history()
        self.update_weight_delta()
        self.update_time_delta()


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


class SettingsMenu(QWidget):

    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.settings = self.parent.settings
        # weight measurement radio buttons
        self.imperial_button = self.imperial_radio()
        self.metric_button = self.metric_radio()
        self.british_button = self.british_radio()
        # UI theme radio buttons
        self.light_button = self.light_radio()
        self.dark_button = self.dark_radio()
        # graph range radio buttons
        self.graph_7_button = self.graph_7_radio()
        self.graph_15_button = self.graph_15_radio()
        self.graph_30_button = self.graph_30_radio()
        self.graph_90_button = self.graph_90_radio()
        # graph future radio buttons
        self.graph_future_7 = self.future_7_radio()
        self.graph_future_14 = self.future_14_radio()
        self.graph_future_28 = self.future_28_radio()
        self.graph_future_none = self.future_none_radio()
        # containers for buttons
        self.measurement_system_group = self.weight_system_box()
        self.theme_group = self.theme_box()
        self.graph_group = self.graph_entry_box()
        self.graph_future_group = self.graph_future_box()
        # layouts
        self.v_layout_1 = self.create_vertical_layout_1()
        self.v_layout_2 = self.create_vertical_layout_2()
        self.master_layout = self.create_master_layout()


    def measurement_system_box(self):
        box = QGroupBox('Select a Measurement System')
        box.setStyleSheet("""
        QGroupBox {
        font-size: 14px;
        font-weight: bold;
        }
        """)
        layout = QVBoxLayout()
        layout.addWidget(self.imperial_button)
        layout.addWidget(self.metric_button)
        layout.addWidget(self.british_button)
        box.setLayout(layout)
        return box

    def imperial_radio(self):
        button = QRadioButton('Imperial')
        button.isChecked.connect(partial(self.select_measurement_system, 'Imperial'))
        return button

    def metric_radio(self):
        button = QRadioButton('Metric')
        button.isChecked.connect(partial(self.select_measurement_system, 'Metric'))
        return button

    def british_radio(self):
        button = QRadioButton('British Imperial')
        button.isChecked.connect(partial(self.select_measurement_system, 'British Imperial'))
        return button

    def select_measurement_system(self, system):
        self.settings.set_measurement_system(system)

    def theme_box(self):
        box = QGroupBox('Select a menu theme')
        box.setStyleSheet("""
        QGroupBox {
        font-size: 14px;
        font-weight: bold;
        }
        """)
        layout = QVBoxLayout()
        layout.addWidget(self.light_button)
        layout.addWidget(self.dark_button)
        box.setLayout(layout)
        return box

    def light_radio(self):
        button = QRadioButton('Light')
        button.isChecked.connect(partial(self.select_theme, "Light"))
        return button

    def dark_radio(self):
        button = QRadioButton('Dark')
        button.isChecked.connect(partial(self.select_theme, "Dark"))
        return button

    def select_theme(self, theme):
        self.settings.set_theme(theme)

    def graph_entry_box(self):
        box = QGroupBox('Select the default graphing range to display')
        box.setStyleSheet("""
        QGroupBox {
        font-size: 14px;
        font-weight: bold;
        }
        """)
        layout = QVBoxLayout()
        layout.addWidget(self.graph_7_button)
        layout.addWidget(self.graph_15_button)
        layout.addWidget(self.graph_30_button)
        layout.addWidget(self.graph_90_button)
        box.setLayout(layout)
        return box

    def graph_7_radio(self):
        button = QRadioButton('7 Entries')
        button.isChecked.connect(partial(self.set_graphing_range, '7'))
        return button

    def graph_15_radio(self):
        button = QRadioButton('15 Entries')
        button.isChecked.connect(partial(self.set_graphing_range, '15'))
        return button

    def graph_30_radio(self):
        button = QRadioButton('30 Entries')
        button.isChecked.connect(partial(self.set_graphing_range, '30'))
        return button

    def graph_90_radio(self):
        button = QRadioButton('90 Entries')
        button.isChecked.connect(partial(self.set_graphing_range, '90'))
        return button

    def set_graphing_range(self, entries):
        self.settings.set_graph_entry_default(entries)

    def graph_future_box(self):
        box = QGroupBox('Select the default behavior for graphing future entries')
        box.setStyleSheet("""
        QGroupBox {
        font-size: 14px;
        font-weight: bold;
        }
        """)
        layout = QVBoxLayout()
        layout.addWidget(self.graph_future_7)
        layout.addWidget(self.graph_future_14)
        layout.addWidget(self.graph_future_28)
        layout.addWidget(self.graph_future_none)
        box.setLayout(layout)
        return box

    def future_7_radio(self):
        button = QRadioButton('7 Entries')
        button.isChecked.connect(partial(self.set_future_graphing_range, '7'))
        return button

    def future_14_radio(self):
        button = QRadioButton('14 Entries')
        button.isChecked.connect(partial(self.set_future_graphing_range, '14'))
        return button

    def future_28_radio(self):
        button = QRadioButton('28 Entries')
        button.isChecked.connect(partial(self.set_future_graphing_range, '28'))
        return button

    def future_none_radio(self):
        button = QRadioButton('Off')
        button.isChecked.connect(partial(self.set_future_graphing_range, 'Off'))
        return button

    def set_future_graphing_range(self, entries):
        self.settings.set_graph_future_default(entries)

    def create_vertical_layout_1(self):
        layout = QVBoxLayout()
        layout.addWidget(self.measurement_system_group)
        layout.addWidget(self.theme_group)
        return layout

    def create_vertical_layout_2(self):
        layout = QVBoxLayout()
        layout.addWidget(self.graph_group)
        layout.addWidget(self.graph_future_group)
        return layout

    def create_master_layout(self):
        layout = QHBoxLayout()
        layout.addLayout(self.v_layout_1)
        layout.addLayout(self.v_layout_2)
        return layout


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
        """Creates a button that submits a user object to the database when it is clicked."""
        confirm = QPushButton('Confirm')
        confirm.setEnabled(False)
        confirm.clicked.connect(self.confirm_event)
        return confirm

    def cancel_button(self):
        """Creates a button that closes the application if it is clicked."""
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
