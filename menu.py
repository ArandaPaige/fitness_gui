import datetime
import sqlite3
from functools import partial

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

DATETODAY = datetime.date.today()

class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, username, name, startingweight, currentweight, height, weight_history=None):
        self.username = username
        self.user_dict = self.user_dict_create(name, startingweight, currentweight, height, weight_history)

    def __repr__(self):
        return f'{self.user_dict}'

    def set_weight(self, weight=None):
        if weight == None:
            while True:
                weight = input("What is the user's current weight in lbs: ")
                try:
                    weight = float(weight)
                    break
                except ValueError as error:
                    print(error)
                    print("Please type a valid number.")
                    continue
        self.current_weight = weight
        self.user_dict['current weight'] = weight

    def set_startweight(self, weight=None):
        '''
        Sets the user's starting weight to a new figure.
        :param weight: the new starting weight entry
        '''
        if weight == None:
            while True:
                weight = input("What is the user's starting weight in lbs: ")
                try:
                    weight = float(weight)
                    break
                except ValueError as error:
                    print(error)
                    print("Please type a valid number.")
                    continue
        self.starting_weight = weight
        self.user_dict['starting weight'] = weight

    def user_dict_create(self, name, startingweight, currentweight, height, weight_history=None):
        '''
        Creates a dictionary with all of the user's personal statistics to be serialized as JSON.
        :param name: User's full name
        :param startingweight: The user's starting weight.
        :param currentweight: The user's current weight.
        :param height: The user's height.
        :param weight_history: User's weight history is mapped by date.
        :return Dictionary: a dictionary containing the user's personal statistics.
        '''
        if weight_history == None:
            return {
                'name': name,
                'starting weight': startingweight,
                'current weight': currentweight,
                'height': height,
                'weight history': {
                    str(DATETODAY): currentweight
                }
            }
        else:
            return {
                'name': name,
                'starting weight': startingweight,
                'current weight': currentweight,
                'height': height,
                'weight history': weight_history
            }

    def weight_entry(self, date, weight):
        '''Assign a new weight entry to the dictionary with the date as the key'''
        try:
            self.user_dict['weight history'][date] = weight
        except KeyError as error:
            print(error)


    def display_weight_history(self):
        '''Average all of the dictionary's entries and compares to starting weight and current weight'''
        for key, value in sorted(self.user_dict['weight history'].items()):
            print(f"Date: {key} | Weight: {value}")

    def display_weight_change(self):
        '''Average all of the dictionary's entries and compares to starting weight and current weight'''
        comparison_value = None
        count = 0
        for key, value in sorted(self.user_dict['weight history'].items()):
            if comparison_value == None:
                comparison_value = value

            count += 1


class GUIManager(QWidget):
    '''Main GUI'''

    def __init__(self, database):
        '''Initialize'''
        super().__init__()
        self.database = database
        self.user_selection_menu = UserSelectionMenu(self)
        self.new_user_menu = CreateUserMenu(self)
        self.login_menu = LoginMenu(self)
        self.main_menu = MainMenu(self)
        self.active_window = self.user_selection_menu
        self.active_window.show()

    def set_active_window(self, window):
        self.active_window.hide()
        self.active_window = window
        self.active_window.show()

    def hide_window(self, window):
        window.hide()

    def close_window(self, window):
        window.close()


class UserSelectionMenu(QWidget):
    '''Main menu'''

    def __init__(self, master):
        '''Initialize'''
        super().__init__()
        self.master = master
        # Window properties
        self.setWindowTitle("Boog's Fitness Cruncher: User Selection")
        self.setFixedSize(400, 400)
        # Sets the layout
        self.layout = QHBoxLayout(self)
        self.menu()

    def new_user_display(self):
        new_user_button = QPushButton('New User', self)
        new_user_button.setFixedHeight(35)
        new_user_button.clicked.connect(self.new_user_transition)
        return new_user_button

    def existing_user_display(self):
        existing_user_button = QPushButton('Existing User', self)
        existing_user_button.setFixedHeight(35)
        existing_user_button.clicked.connect(self.existing_user_transition)
        return existing_user_button

    def menu(self):
        new_user_button = self.new_user_display()
        existing_user_button = self.existing_user_display()
        self.layout.addWidget(new_user_button)
        self.layout.addWidget(existing_user_button)

    def new_user_transition(self):
        self.master.set_active_window(self.master.new_user_menu)

    def existing_user_transition(self):
        self.master.set_active_window(self.master.login_menu)


class CreateUserMenu(QWidget):
    '''Create new user'''

    def __init__(self, master):
        '''Initialize'''
        super().__init__()
        self.master = master
        # Window properties
        self.setWindowTitle("Boog's Fitness Cruncher: New User")
        self.setFixedSize(400, 400)
        # Sets the layout
        self.layout = QGridLayout(self)
        self.menu()

    def username_edit(self):
        username = QLineEdit(self)
        username.setPlaceholderText('Username')
        return username

    def name_edit(self):
        name = QLineEdit(self)
        name.setPlaceholderText('Name')
        return name

    def starting_weight_edit(self):
        starting_weight = QLineEdit(self)
        starting_weight.setPlaceholderText('Starting Weight')
        validator = QDoubleValidator(50, 999, 2, starting_weight)
        starting_weight.setValidator(validator)
        starting_weight.editingFinished.connect()
        return starting_weight

    def current_weight_edit(self):
        current_weight = QLineEdit(self)
        current_weight.setPlaceholderText('Current Weight')
        validator = QDoubleValidator(50, 99, 2, current_weight)
        current_weight.setValidator(validator)
        return current_weight

    def height_edit(self):
        height = QLineEdit(self)
        height.setPlaceholderText('Height')
        validator = QDoubleValidator(2, 9, 2, height)
        height.setValidator(validator)
        return height

    def confirm_button(self):
        confirm = QPushButton('Confirm', self)
        confirm.setFixedHeight(35)
        confirm.clicked.connect(partial(self.confirm_transition))
        return confirm

    def cancel_button(self):
        cancel = QPushButton('Cancel', self)
        cancel.setFixedHeight(35)
        cancel.clicked.connect(self.cancel_transition)
        return cancel

    def confirm_transition(self, username, name, starting_weight, current_weight, height):
        pass

    def cancel_transition(self):
        self.master.set_active_window(self.master.user_selection_menu)

    def menu(self):
        username = self.username_edit()
        name = self.name_edit()
        starting_weight = self.starting_weight_edit()
        current_weight = self.current_weight_edit()
        height = self.height_edit()
        confirm = self.confirm_button()
        cancel = self.cancel_button()
        # arranges the widgets in the menu layout
        self.layout.addWidget(username, 1, 0)
        self.layout.addWidget(name, 2, 0)
        self.layout.addWidget(starting_weight, 3, 0)
        self.layout.addWidget(current_weight, 4, 0)
        self.layout.addWidget(height, 5, 0)
        self.layout.addWidget(confirm, 6, 0, Qt.Alignment.AlignRight)
        self.layout.addWidget(cancel, 6, 1, Qt.Alignment.AlignRight)



class LoginMenu(QWidget):
    '''Main menu'''

    def __init__(self, master):
        '''Initialize'''
        super().__init__()
        self.master = master
        # Window Properties
        self.setWindowTitle("Boog's Fitness Cruncher: Login")
        self.setFixedSize(400, 400)
        self.layout = QGridLayout(self)
        # Login display
        self.menu()

    def username_display(self):
        username = QLineEdit(self)
        username.setFixedSize(400, 40)
        username.setPlaceholderText('Enter a valid username')
        return username

    def confirm_button(self):
        confirm = QPushButton('Confirm', self)
        confirm.setFixedHeight(35)
        confirm.clicked.connect(partial(self.confirm_transition))
        return confirm

    def cancel_button(self):
        cancel = QPushButton('Cancel', self)
        cancel.setFixedHeight(35)
        cancel.clicked.connect(self.cancel_transition)
        return cancel

    def confirm_transition(self, username):
        pass

    def cancel_transition(self):
        self.master.set_active_window(self.master.user_selection_menu)

    def menu(self):
        username = self.username_display()
        confirm = self.confirm_button()
        cancel = self.cancel_button()
        self.layout.addWidget(username, 0, 0, Qt.Alignment.AlignLeft)
        self.layout.addWidget(confirm, 1, 1, Qt.Alignment.AlignRight)
        self.layout.addWidget(cancel, 1, 2, Qt.Alignment.AlignRight)


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


class UsernameValidator(QValidator):
    '''Docstring'''

    def __init__(self):
        super().__init__()

    def validate(self, str, pos):
        pass
