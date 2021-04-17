import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

import database
from menu import GUIManager

BASE_DIR = Path().resolve()
DATABASE = 'user.db'
DATABASE_PATH = BASE_DIR / DATABASE

QTAPP = QApplication(sys.argv)


def main():
    if DATABASE_PATH.exists() == False:
        database.create_user_tables()
        user = None
    else:
        user = database.retrieve_user(user_id=1)

    appgui = GUIManager(user)
    sys.exit(QTAPP.exec())


if __name__ == '__main__':
    main()