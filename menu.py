import sys

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class UserSelectionMenu(QWidget):
    '''Main menu'''

    def __init__(self):
        '''Initialize'''
        super().__init__()
        # Window Properties
        self.setWindowTitle("User Selection")
        self.setFixedSize(400, 400)

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
        self.userDisplay()
        self.passwordDisplay()

    def usernameDisplay(self):
        username_box = QLineEdit()
        username_box.setFixedSize(100, 20)
        self.layout.addWidget(username_box)

    def passwordDisplay(self):
        password_box = QLineEdit()
        password_box.setFixedSize(100, 20)
        self.layout.addWidget(password_box)

class MainMenu(QWidget):
    '''Main menu'''

    def __init__(self):
        '''Initialize'''
        super().__init__()
        # Window Properties
        self.setWindowTitle("Main Menu")
        self.setBaseSize(450, 450)
