import sys
import pathlib
import sqlite3

from PyQt6.QtWidgets import QApplication

from menu import GUIManager


QTAPP = QApplication(sys.argv)
DATABASE = sqlite3.connect('user.db')


def main():
    appgui = GUIManager(DATABASE)
    sys.exit(QTAPP.exec())


if __name__ == '__main__':
    main()
