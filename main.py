import sys
import pathlib
import sqlite3

from PyQt6.QtWidgets import QApplication

from menu import GUIManager


QTAPP = QApplication(sys.argv)


def main():
    appgui = GUIManager(QTAPP)

if __name__ == '__main__':
    main()
