import datetime
import sqlite3
from pathlib import Path

from user import User

BASE_DIR = Path().resolve()
DATABASE = 'user.db'
DATABASE_PATH = BASE_DIR / DATABASE
DATE_TODAY = str(datetime.date.today())


def create_user_tables():
    """
    Constructs two SQLite tables: USER and WEIGHT_HISTORY. USER stores user personal metrics.
    WEIGHT_HISTORY foreign keys USER by ID and stores the USER's weight entry history.
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute('''
    CREATE TABLE USER
        (USER_ID INTEGER PRIMARY KEY NOT NULL,
        NAME            TEXT NOT NULL,
        WEIGHT          REAL NOT NULL,
        GOAL            REAL NOT NULL,
        HEIGHT          INT NOT NULL);'''
                )

    cur.execute('''
    CREATE TABLE WEIGHT_HISTORY
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATE                TEXT NOT NULL,
        WEIGHT              REAL NOT NULL,
        PERSON_ID           INT NOT NULL,
        FOREIGN KEY(PERSON_ID) REFERENCES USER(USER_ID));'''
                )
    db.commit()
    db.close()


def retrieve_user(user_id):
    """
    Loads the supplied ID from the USER table and WEIGHT_HISTORY. If ID is not found, none is returned instead.
    :param user_id: the user ID to query the database
    :return: None or USER Object
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    if cur.execute("SELECT USER_ID from USER where USER_ID = ?", (user_id,)) == "":
        return None
    else:
        user_data = cur.execute("SELECT NAME, WEIGHT, GOAL, HEIGHT from USER where USER_ID = ?", (user_id,))
        row = user_data.fetchone()
        user_history = cur.execute("SELECT ID, DATE, WEIGHT from WEIGHT_HISTORY where PERSON_ID = ?", (user_id,))
        row_history = user_history.fetchall()
        user = User(name=row[0], weight=row[1], goal=row[2], height=row[3], weight_history=row_history)
        return user


def insert_user(user):
    """
    Inserts the user object into the database with the object's attributes as parameters
    :param user: a user object
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    INSERT INTO USER (NAME,WEIGHT,GOAL,HEIGHT) 
        VALUES (?,?,?,?)''', (user.name, user.weight, user.goal, user.height))
    cur.execute('''
    INSERT INTO WEIGHT_HISTORY (DATE, WEIGHT, PERSON_ID)
        VALUES (?,?,?)''', (DATE_TODAY, user.weight, user.user_id))
    db.commit()
    db.close()


def load_user_history(user):
    """
    Loads the user's weight history as an attribute of the user instance.
    :param user: a user object
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    user_history = cur.execute("SELECT ID, DATE, WEIGHT from WEIGHT_HISTORY where PERSON_ID = ?", (user.user_id,))
    row_history = user_history.fetchall()
    user.set_weight_history(row_history)


def update_user_name(name, user_id):
    """
    Updates the user's name in the USER table.
    :param name: The personal name of the user
    :param user_id: The user's ID in the database
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET NAME = ? WHERE USER_ID = ?''', (name, user_id))
    db.commit()
    db.close()


def update_user_weight(weight, user_id):
    """
    Updates the user's weight in the USER table.
    :param weight: the weight of the user
    :param user_id: the user's ID in the database
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET WEIGHT = ? WHERE USER_ID = ?''', (weight, user_id))
    db.commit()
    db.close()


def update_user_goal(goal, user_id):
    """
    Updates the user's goal weight in the USER table.
    :param goal: the user's goal weight in the USER table.
    :param user_id: the user's ID in the database
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET GOAL = ? WHERE USER_ID = ?''', (goal, user_id))
    db.commit()
    db.close()


def update_user_height(height, user_id):
    """
    Updates the user's height in the USER table.
    :param height: the user's height in the USER table.
    :param user_id: the user's ID in the database
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET HEIGHT = ? WHERE USER_ID = ?''', (height, user_id))
    db.commit()
    db.close()


def insert_weight_entry(date, weight, person_id):
    """
    Inserts a new entry into the WEIGHT_HISTORY table.
    :param date: the date in which the weight was recorded.
    :param weight: the user's weight.
    :param person_id: the ID of the user in the WEIGHT_HISTORY table.
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    INSERT INTO WEIGHT_HISTORY (DATE, WEIGHT, PERSON_ID) 
        VALUES (?,?,?)''', (date, weight, person_id))
    db.commit()
    db.close()


def update_weight_entry(entry_id, weight, date):
    """

    :param entry_id: the ID of the entry.
    :param weight: the weight of the user
    :param date: the date in which the weight was recorded.
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    UPDATE WEIGHT_HISTORY SET WEIGHT = ?, SET DATE = ? WHERE ID = ?''', (weight, date, entry_id))
    db.commit()
    db.close()


def delete_weight_entry(entry_id):
    """
    Deletes the entry in the WEIGHT_HISTORY table that matches the ID parameter.
    :param entry_id: the ID of the entry.
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''DELETE from WEIGHT_HISTORY where ID = ?''', (entry_id,))
    db.commit()
    db.close()
