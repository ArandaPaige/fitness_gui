import sys
from pathlib import Path
import logging.config

from PyQt6.QtWidgets import QApplication

import database
from menu import GUIManager

BASE_DIR = Path().resolve()
DATABASE = 'user.db'
DATABASE_PATH = BASE_DIR / DATABASE

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'detailed':    {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'basic':    {
            'format': '%(name)s %(message)s'
        }
    },
    'handlers': {
        'file_logger': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'tracker.log',
            'mode': 'a',
            'encoding': 'utf-8',
        },
        'console_logger': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'basic',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file_logger', 'console_logger'],
            'level': 'WARNING',
            'propagate': False
        },
        '__main__': {
            'handlers': ['file_logger', 'console_logger'],
            'level': 'WARNING',
            'propagate': False
        },
        'menu.py': {
            'handlers': ['file_logger', 'console_logger'],
            'level': 'WARNING',
            'propagate': False
        },
        'model.py': {
            'handlers': ['file_logger'],
            'level': 'ERROR',
            'propagate': False
        },
        'database.py': {
            'handlers': ['file_logger'],
            'level': 'ERROR',
            'propagate': False
        },
        'settings.py': {
            'handlers': ['file_logger'],
            'level': 'ERROR',
            'propagate': False
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)

QTAPP = QApplication(sys.argv)


def main():
    if DATABASE_PATH.exists() is False:
        database.create_user_tables()
        user = None
    else:
        user = database.retrieve_user(user_id=1)

    appgui = GUIManager(user)
    sys.exit(QTAPP.exec())


if __name__ == '__main__':
    main()
