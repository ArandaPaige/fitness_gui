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
        self.existing_user_button.clicked.connect(self.existing_user_transition)
        self.layout.addWidget(self.existing_user_button)

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
        self.layout = QVBoxLayout(self)
        self.menu()

    def username_edit(self):
        username_label = QLabel(self)
        username_label.setText('Username')
        username = QLineEdit(self)
        username.setPlaceholderText('Username')
        return username_label, username

    def names_edit(self):
        name = QLineEdit(self)
        name.setPlaceholderText('Name')
        return name

    def starting_weight_edit(self):
        starting_weight = QLineEdit(self)
        starting_weight.setPlaceholderText('Starting Weight')
        validator = QDoubleValidator(75, 999, 3, starting_weight)
        validator.Notation(0)
        starting_weight.setValidator(validator)
        return starting_weight

    def current_weight_edit(self):
        current_weight = QLineEdit(self)
        current_weight.setPlaceholderText('Current Weight')
        return current_weight

    def height_edit(self):
        height = QLineEdit(self)
        height.setPlaceholderText('Height')
        return height

    def menu(self):
        username_label, username = self.username_edit()
        name = self.names_edit()
        starting_weight = self.starting_weight_edit()
        current_weight = self.current_weight_edit()
        height = self.height_edit()
        # arranges the widgets in the menu layout
        self.layout.addWidget(username_label)
        self.layout.addWidget(username)
        self.layout.addWidget(name)
        self.layout.addWidget(starting_weight)
        self.layout.addWidget(current_weight)
        self.layout.addWidget(height)


class LoginMenu(QWidget):
    '''Main menu'''

    def __init__(self, master):
        '''Initialize'''
        super().__init__()
        self.master = master
        # Window Properties
        self.setWindowTitle("Boog's Fitness Cruncher: Login")
        self.setFixedSize(400, 400)
        self.layout = QVBoxLayout()
        # Login display
        self.username_display()

    def username_display(self):
        self.username_box = QLineEdit(self)
        self.username_box.setFixedSize(400, 40)
        self.username_box.setPlaceholderText('Enter a valid username')
        self.layout.addWidget(self.username_box)


class MainMenu(QWidget):
    '''Main menu'''

    def __init__(self, master):
        '''Initialize'''
        super().__init__()
        self.master = master
        # Window Properties
        self.setWindowTitle("Main Menu")
        self.setBaseSize(450, 450)
