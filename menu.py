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
        self.user_display()
        self.password_display()

    def user_display(self):
        self.layout.addWidget(QLineEdit)

    def password_display(self):
        self.layout.addWidget(QLineEdit)

class MainMenu(QWidget):
    '''Main menu'''

    def __init__(self):
        '''Initialize'''
        super().__init__()
        # Window Properties
        self.setWindowTitle("Main Menu")
        self.setBaseSize(450, 450)
