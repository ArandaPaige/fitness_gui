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

    def confirm_button(self):
        confirm = QPushButton(self)
        return confirm

    def cancel_button(self):
        cancel = QPushButton(self)
        return cancel

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
        self.menu()

    def username_display(self):
        username = QLineEdit(self)
        username.setFixedSize(400, 40)
        username.setPlaceholderText('Enter a valid username')
        return username

    def confirm_button(self):
        confirm = QPushButton(self)
        return confirm

    def cancel_button(self):
        cancel = QPushButton(self)
        return cancel

    def menu(self):
        username = self.username_display()
        self.layout.addWidget(username)


class MainMenu(QWidget):
    '''Main menu'''

    def __init__(self, master):
        '''Initialize'''
        super().__init__()
        self.master = master
        # Window Properties
        self.setWindowTitle("Main Menu")
        self.setBaseSize(450, 450)
