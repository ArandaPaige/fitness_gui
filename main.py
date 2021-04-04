import sys
from pathlib import Path
import database

from PyQt6.QtWidgets import QApplication

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

    appgui = GUIManager(QTAPP, user)
    sys.exit(appgui.exec())


if __name__ == '__main__':
    main()
