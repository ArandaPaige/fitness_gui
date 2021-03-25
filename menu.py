import sys

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class UserSelectionMenu(QWidget):
    '''Main menu'''

    def __init__(self):
        '''Initialize'''
        super().__init__()
        # Window properties
        self.setWindowTitle("Boog's Fitness Cruncher")
        self.setFixedSize(400, 400)
        # Sets the layout
        self.layout = QHBoxLayout(self)
        self.menu()

    def menu(self):
        self.new_user_button = QPushButton('New User', self)
        self.new_user_button.setFixedHeight(35)
        self.layout.addWidget(self.new_user_button)

        self.existing_user_button = QPushButton('Existing User', self)
        self.existing_user_button.setFixedHeight(35)
        self.layout.addWidget(self.existing_user_button)


class CreateUserMenu(QWidget):
    '''Create new user'''

    def __init__(self):
        '''Initialize'''
        super().__init__()
        # Window properties
        self.setWindowTitle("Boog's Fitness Cruncher: New User")
        self.setFixedSize(400, 400)
        # Sets the layout
        self.layout = QVBoxLayout(self)
        self.menu()

    def menu(self):
        username = QLineEdit('Username', self)
        names = QLineEdit('Name', self)
        starting_weight = QLineEdit('Starting Weight', self)
        current_weight = QLineEdit('Current Weight', self)
        height = QLineEdit('Height', self)
        # arranges the widgets in the layout
        self.layout.addWidget(username)
        self.layout.addWidget(names)
        self.layout.addWidget(starting_weight)
        self.layout.addWidget(current_weight)
        self.layout.addWidget(height)


class LoginMenu(QWidget):
    '''Main menu'''

    def __init__(self):
        '''Initialize'''
        super().__init__()
        # Window Properties
        self.setWindowTitle("Login")
        self.setFixedSize(400, 200)
        self.layout = QVBoxLayout()
        # Login display
        self.username_display()

    def username_display(self):
        username_box = QLineEdit()
        username_box.setFixedSize(100, 20)
        self.layout.addWidget(username_box)


class MainMenu(QWidget):
    '''Main menu'''

    def __init__(self):
        '''Initialize'''
        super().__init__()
        # Window Properties
        self.setWindowTitle("Main Menu")
        self.setBaseSize(450, 450)
