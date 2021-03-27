from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class GUIManager(QWidget):
    '''Main GUI'''

    def __init__(self):
        '''Initialize'''
        super().__init__()
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
        self.new_user_display()
        self.existing_user_display()

    def new_user_display(self):
        self.new_user_button = QPushButton('New User', self)
        self.new_user_button.setFixedHeight(35)
        self.new_user_button.clicked.connect(self.new_user_transition)
        self.layout.addWidget(self.new_user_button)

    def existing_user_display(self):
        self.existing_user_button = QPushButton('Existing User', self)
        self.existing_user_button.setFixedHeight(35)
        self.layout.addWidget(self.existing_user_button)

    def new_user_transition(self):
        self.master.set_active_window(self.master.new_user_menu)

    def existing_user_transition(self):
        pass



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
        self.layout = QVBoxLayout(self)
        self.menu()

    def menu(self):
        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        self.name = QLineEdit(self)
        self.name.setPlaceholderText('Name')
        self.starting_weight = QLineEdit(self)
        self.starting_weight.setPlaceholderText('Starting Weight')
        self.current_weight = QLineEdit(self)
        self.current_weight.setPlaceholderText('Current Weight')
        self.height = QLineEdit(self)
        self.height.setPlaceholderText('Height')
        # arranges the widgets in the layout
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.starting_weight)
        self.layout.addWidget(self.current_weight)
        self.layout.addWidget(self.height)


class LoginMenu(QWidget):
    '''Main menu'''

    def __init__(self, master):
        '''Initialize'''
        super().__init__()
        self.master = master
        # Window Properties
        self.setWindowTitle("Boog's Fitness Cruncher: Login")
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

    def __init__(self, master):
        '''Initialize'''
        super().__init__()
        self.master = master
        # Window Properties
        self.setWindowTitle("Main Menu")
        self.setBaseSize(450, 450)

